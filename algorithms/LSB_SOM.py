from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class LSB_SOM(steganographyAlgorithm):
    def __init__(self, k=1):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.k = k
        self.error_msg = ""
        if k > 8:
            self.k = 7
            self.error_msg += "The value of parameter k has been changed to 7."
        
        self.timeout = 10
        self.json_content = {"algorithm":"LSB_SOM", "settings": {"k":self.k}}

    @property
    def is_success(self):
        return self._is_success
    
    @is_success.setter
    def is_success(self, value):
        self._is_success = value

    @property
    def error_msg(self):
        return self._error_msg
    
    @error_msg.setter
    def error_msg(self, value):
        self._error_msg = value

    @property
    def msg_extension(self):
        return self._msg_extension
    
    @msg_extension.setter
    def msg_extension(self, value):
        self._msg_extension = value

    @property
    def stego_extension(self):
        return self._stego_extension
    
    @stego_extension.setter
    def stego_extension(self, value):
        self._stego_extension = value

    @property
    def stego_img_path(self):
        return self._stego_img_path
    
    @stego_img_path.setter
    def stego_img_path(self, value):
        self._stego_img_path = value
    
    @property
    def destination_path(self):
        return self._destination_path
    
    @destination_path.setter
    def destination_path(self, value):
        self._destination_path = value

    @property
    def algorithm_path_dir(self):
        return self._algorithm_path_dir
    
    @algorithm_path_dir.setter
    def algorithm_path_dir(self, value):
        self._algorithm_path_dir = value

    @property
    def metadata_path(self):
        return self._metadata_path
    
    @metadata_path.setter
    def metadata_path(self, value):
        self._metadata_path = value

    @property
    def json_content(self):
        return self._json_content
    
    @json_content.setter
    def json_content(self, value):
        self._json_content = value

    def reset_params(self):
        self.is_success = False
        self.error_msg = ""

    def encode(self, img_path, msg_path):
        self.algorithm_path_dir = util.get_algorithm_path_dir(self)
        self.stego_img_path = util.get_encode_path(self)
        self.destination_path = util.get_decode_path(self)
        self.metadata_path = util.get_metadata_path(self)
        
        img = Image.open(img_path, 'r')
        width, height = img.size
        all_pixels = width * height * 3 * 8
        array = np.array(list(img.getdata()))
        
        msg_file = open(msg_path,'r')
        message = msg_file.read()
        msg_file.close()

        start_time = time()

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n
        b_message = ''.join([format(ord(i), "08b") for i in message])
        
        available_bits = total_pixels * 3 * self.k
        SOM_bit_len = math.ceil(math.log2(available_bits))
        SOM_bit_value = len(b_message)
        SOM = bin(SOM_bit_value)[2:]
        SOM = '0' * (SOM_bit_len - len(SOM)) + SOM

        b_message = SOM + b_message
        req_bits = len(b_message)

        if req_bits > available_bits:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return

        self.json_content["estimated_capacity"] =  available_bits / all_pixels
        array = self.__hide_text__(total_pixels, req_bits, array, b_message)
        
        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_encode"] =  milli_sec_elapsed

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(self.stego_img_path)
        self.is_success = True

    def decode(self, pipe=None, save_to_txt=True):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return

        self.reset_params()
        img = Image.open(self.stego_img_path, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n

        start_time = time()

        msg_size_b, SOM_bit_len = self.__calculate_SOM__(total_pixels, array)
        used_bits = int(msg_size_b, 2)

        hidden_bits = self.__get_hidded_bits__(total_pixels, used_bits + SOM_bit_len, array)
        hidden_bits = hidden_bits[SOM_bit_len:]
        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            message += chr(int(hidden_bits[i], 2))

        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_decode"] = milli_sec_elapsed

        with open(self.metadata_path, "w") as f:
            json.dump(self.json_content, f)

        if save_to_txt:
            destination_file = open(self.destination_path, "w")
            destination_file.write(message)
            destination_file.close()

        if pipe is not None:
            pipe.put(message)
            pipe.close()
            
        self.is_success = True
        return message

    def __hide_text__(self, total_pixels, req_bits, array, b_message):
        index = 0
        for p in range(total_pixels):
            for color in range(0, 3):
                if index >= req_bits:
                    return array

                value_old = array[p][color]
                value_old_bin = bin(value_old)[2:]
                value_old_bin = '0' * (8 - len(value_old_bin)) + value_old_bin
                b_message_bit = b_message[index:index+self.k]
                b_message_bit = '0' * (self.k - len(b_message_bit)) + b_message_bit
                value_new_int = value_old_bin[:8-self.k] + b_message_bit
                value_new = int(value_new_int, 2)
                index += self.k
                array[p][color] = value_new

        return array

    def __calculate_SOM__(self, total_pixels, array):
        SOM_bit_len = math.ceil(math.log2(total_pixels * 3 * self.k))
        loop_counter = SOM_bit_len
        msg_size_b = ""
        for p in range(total_pixels):
            for color in range(0, 3):
                value_bit = bin(array[p][color])[2:]
                value_bit = '0' * (8 - len(value_bit)) + value_bit
                msg_size_b += value_bit[-self.k:]
                loop_counter -= self.k
                if loop_counter <= 0:
                    return msg_size_b[:SOM_bit_len], SOM_bit_len

    def __get_hidded_bits__(self, total_pixels, loop_counter, array):
        hidden_bits = ""
        for p in range(total_pixels):
            for color in range(0, 3):
                value_bit = bin(array[p][color])[2:]
                value_bit = '0' * (8 - len(value_bit)) + value_bit
                k = self.k
                if loop_counter < self.k:
                    k = loop_counter

                hidden_bits += value_bit[-k:]
                loop_counter -= k
                if loop_counter <= 0:
                    return hidden_bits

    def get_bit_value(self, number, n):
        # Create a mask with a 1 at the nth position
        mask = 1 << n

        # Perform bitwise AND operation with the number and mask
        # If the result is non-zero, the bit at position n is 1, otherwise, it's 0
        return (number & mask) >> n