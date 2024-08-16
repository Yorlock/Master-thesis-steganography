from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util


class n_RMBR(steganographyAlgorithm):
    def __init__(self, end_msg="$t3g0", color="", n=4):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.end_msg = end_msg
        self.colors = ['R', 'G', 'B']
        if color in self.colors:
            self.color = color
        else:
            self.color = ""

        if n < 1 or n > 4:
            self.n = 4
        else:
            self.n = n
        
        json_color = self.color
        if json_color == "":
            json_color = "RGB"

        self.timeout = 15
        self.json_content = {"algorithm":"n_RMBR", "settings": {"n":self.n, "color":json_color ,"end_msg":self.end_msg}}

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

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n

        start_time = time()

        message += self.end_msg
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_bits = len(b_message)

        color_number = 1
        if self.color == "":
            color_number = 3

        available_bits = total_pixels * color_number * self.n
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

        hidden_bits = ""
        block_bits = ""
        message = ""
        color_init, color_end = self.__get_color_range__()
        is_end = False
        left_bits = ''
        for p in range(total_pixels):
            if is_end:
                break

            block_bits = left_bits
            for color in range(color_init, color_end):
                value_bit = bin(array[p][color])[2:]
                value_bit = '0' * (8 - len(value_bit)) + value_bit
                block_bits += value_bit[-self.n:]

            hidden_bits = [block_bits[i:i+8] for i in range(0, len(block_bits), 8)]
            if hidden_bits[len(hidden_bits) - 1] != 8:
                left_bits = hidden_bits[-1]
                hidden_bits = hidden_bits[:-1]
            else:
                left_bits = ''
            
            for i in range(len(hidden_bits)):
                if message[-len(self.end_msg):] == self.end_msg:
                    is_end = True
                    break
                else:
                    message += chr(int(hidden_bits[i], 2))   

        if self.end_msg not in message:
            self.is_success = False
            self.error_msg = "No Hidden Message Found\n"
            return

        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_decode"] = milli_sec_elapsed

        with open(self.metadata_path, "w") as f:
            json.dump(self.json_content, f)

        message = message[:-len(self.end_msg)]

        if save_to_txt:
            destination_file = open(self.destination_path, "w")
            destination_file.write(message)
            destination_file.close()

        if pipe is not None:
            pipe.put(message)
            pipe.close()
            
        self.is_success = True
        return message

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1

    def __hide_text__(self, total_pixels, req_bits, array, b_message):
        color_init, color_end = self.__get_color_range__()
        index = 0
        for p in range(total_pixels):
            for color in range(color_init, color_end):
                if index >= req_bits:
                    return array

                value_old = array[p][color]
                value_old_int = bin(value_old)[2:]
                value_old_int = '0' * (8 - len(value_old_int)) + value_old_int
                dec_1 = int(value_old_int[-self.n:], 2)
                dec_2 = int(b_message[index:index+self.n], 2)
                index += self.n
                d = dec_1 - dec_2
                P_1 = value_old - d
                P_2 = value_old - np.power(2, self.n)
                P_3 = value_old + np.power(2, self.n)
                d_1 = np.abs(value_old - P_1)
                d_2 = np.abs(value_old - P_2)
                d_3 = np.abs(value_old - P_3)
                value_new = P_1
                if d_1 <= d_2 and d_1 <= d_3 and 0 <= P_1 <= 255:
                    value_new = P_1
                elif d_2 <= d_1 and d_2 <= d_3 and 0 <= P_2 <= 255:
                    value_new = P_2
                elif d_3 <= d_1 and d_3 <= d_2 and 0 <= P_2 <= 255:
                    value_new = P_3
                elif P_2 <= P_1 and 0 <= P_2 <= 255:
                    value_new = P_2
                
                array[p][color] = value_new

        return array