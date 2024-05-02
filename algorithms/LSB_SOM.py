from PIL import Image
import numpy as np
import math

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class LSB_SOM(steganographyAlgorythm):
    def __init__(self, k=1):
        self.stego_img_path = ""
        self.destination_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.k = k
        self.error_msg = ""
        if k > 8:
            self.k = 7
            self.error_msg += "The value of parameter k has been changed to 7."

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

    def reset_params(self):
        self.is_success = False
        self.error_msg = ""

    def encode(self, img_path, msg_path):
        img = Image.open(img_path, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        
        msg_file = open(msg_path,'r')
        message = msg_file.read()
        msg_file.close()

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n
        b_message = ''.join([format(ord(i), "08b") for i in message])
        
        SOM_bit_len = math.ceil(math.log2(total_pixels * 3 * self.k))
        SOM_bit_value = len(b_message)
        SOM = bin(SOM_bit_value)[2:]
        padding_length = SOM_bit_len - len(SOM)
        SOM = '0'*padding_length + SOM

        b_message = SOM + b_message
        req_bits = len(b_message)

        if req_bits > total_pixels * 3 * self.k:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return
        else:
            array = self.__hide_text__(total_pixels, req_bits, array, b_message)

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)

        self.stego_img_path = util.get_encode_path(self)
        enc_img.save(self.stego_img_path)

        self.is_success = True

    def decode(self):
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
        msg_size_b, SOM_bit_len = self.__calculate_SOM__(total_pixels, array)
        used_bits = int(msg_size_b, 2)

        hidden_bits = self.__get_hidded_bits__(total_pixels, used_bits + SOM_bit_len, array)
        hidden_bits = hidden_bits[SOM_bit_len:]
        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            message += chr(int(hidden_bits[i], 2))

        self.destination_path = util.get_decode_path(self)
        destination_file = open(self.destination_path, "w")
        destination_file.write(message)
        destination_file.close()

        self.is_success = True

    def __hide_text__(self, total_pixels, req_bits, array, b_message):
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                AND_value = 255
                BIT_value = 1
                new_value = 0
                for bit in range(self.k):
                    if index < req_bits:
                        AND_value -= BIT_value
                        new_value += int(b_message[index]) * BIT_value
                        BIT_value *= 2
                        index += 1
                    else:
                        array[p][q] = (array[p][q] & AND_value) + new_value
                        return array
                    
                array[p][q] = (array[p][q] & AND_value) + new_value

    def __calculate_SOM__(self, total_pixels, array):
        SOM_bit_len = math.ceil(math.log2(total_pixels * 3 * self.k))
        loop_counter = SOM_bit_len
        msg_size_b = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                for bit in range(self.k):
                    msg_size_b += str(self.get_bit_value(array[p][q], bit))
                    loop_counter -= 1
                    if loop_counter == 0:
                        return msg_size_b, SOM_bit_len

    def __get_hidded_bits__(self, total_pixels, loop_counter, array):
        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                for bit in range(self.k):
                    hidden_bits += str(self.get_bit_value(array[p][q], bit))
                    loop_counter -= 1
                    if loop_counter == 0:
                        return hidden_bits

    def get_bit_value(self, number, n):
        # Create a mask with a 1 at the nth position
        mask = 1 << n

        # Perform bitwise AND operation with the number and mask
        # If the result is non-zero, the bit at position n is 1, otherwise, it's 0
        return (number & mask) >> n