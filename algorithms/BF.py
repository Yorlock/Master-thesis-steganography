from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class BF(steganographyAlgorithm):
    def __init__(self, type=1, color=""):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.location_map = []
        if type != 1 and type != 2:
            self.type = 1
        else:
            self.type = type

        self.colors = ['R', 'G', 'B']
        if color in self.colors:
            self.color = color
        else:
            self.color = ""
        
        self.timeout = 15
        json_color = self.color
        if json_color == "":
            json_color = "RGB"

        self.json_content = {"algorithm":"BF", "settings": {"type":self.type, "color":json_color}}

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
        color_number = 1
        if self.color == "":
            color_number = 3

        block_number = 3
        if self.type == 2:
            block_number = 4

        available_bits = (total_pixels * color_number) * 2
        available_blocks = (total_pixels * color_number) // 2
        SOM_bit_len = math.ceil(math.log2(available_bits))
        SOM_bit_value = len(b_message)
        SOM = bin(SOM_bit_value)[2:]
        SOM = '0' * (SOM_bit_len - len(SOM)) + SOM

        b_message = SOM + b_message
        req_blocks = len(b_message) // block_number
        if req_blocks > available_blocks:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return

        self.json_content["estimated_capacity"] =  available_blocks * block_number / all_pixels
        self.__calculate_location_map__(total_pixels, array)
        array = self.__hide_text__(array, b_message)
        
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

        hidden_bits = self.__get_hidded_bits__(total_pixels, array)
        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
        if len(hidden_bits[-1]) != 8:
            hidden_bits = hidden_bits[:-1]

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

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1

    def __reverse_bit__(self, value):
        if value == '0':
            return '1'
        return '0'

    def __calculate_location_map__(self, total_pixels, array):
        location_map = []
        color_init, color_end = self.__get_color_range__()
        for p in range(total_pixels):
            for color in range(color_init, color_end):
                value = array[p][color]
                value_bit = bin(value)[2:]
                value_bit = '0' * (8 - len(value_bit)) + value_bit
                location_map.append(value_bit[-2:])
        
        self.location_map = location_map

    def __get_value__(self, array, index, color_value):
        if color_value == 2:
            value = array[index][color_value]
            color_value = 0
            index += 1
        else:
            value = array[index][color_value]
            color_value += 1

        return index, color_value, value

    def __hide_text__(self, array, b_message):
        if self.type == 1:
            block_size = 3
            calculate_hide_text = self.__calculate_hide_text_type_1__
        else:
            block_size = 4
            calculate_hide_text = self.__calculate_hide_text_type_2__
        
        b_message_block = [b_message[i:i+block_size] for i in range(0, len(b_message), block_size)]
        if len(b_message_block[-1]) != block_size:
            b_message_block[-1] = b_message_block[-1] + '0' * (block_size - len(b_message_block[-1]))

        index = 0
        color_init, color_end = self.__get_color_range__()
        one_color = False
        color_value = color_init
        if color_init + 1 == color_end:
            one_color = True

        for block in b_message_block:
            value_1_index = index
            value_1_color = color_value
            if one_color:
                value_1 = array[index][color_value]
                value_2_index = index+1
                value_2_color = color_value
                value_2 = array[index+1][color_value]
                index += 2
            else:
                index, color_value, value_1 = self.__get_value__(array, index, color_value)
                value_2_index = index
                value_2_color = color_value
                index, color_value, value_2 = self.__get_value__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin
            value_1_bin, value_2_bin = calculate_hide_text(block, value_1_bin, value_2_bin)
            array[value_1_index][value_1_color] = int(value_1_bin, 2)
            array[value_2_index][value_2_color] = int(value_2_bin, 2)
        return array

    def __calculate_hide_text_type_1__(self, block, value_1_bin, value_2_bin):
        if block == '001':
            value_1_bin = value_1_bin[:7] + self.__reverse_bit__(value_1_bin[-1])
        elif block == '010':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + value_1_bin[-1]
        elif block == '011':
            value_2_bin = value_2_bin[:7] + self.__reverse_bit__(value_2_bin[-1])
        elif block == '100':
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + value_2_bin[-1]
        elif block == '101':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
        elif block == '110':
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
        elif block == '111':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
    
        return value_1_bin, value_2_bin

    def __calculate_hide_text_type_2__(self, block, value_1_bin, value_2_bin):
        if block == '0001':
            value_2_bin = value_2_bin[:7] + self.__reverse_bit__(value_2_bin[-1])
        elif block == '0010':
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + value_2_bin[-1]
        elif block == '0011':
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
        elif block == '0100':
            value_1_bin = value_1_bin[:7] + self.__reverse_bit__(value_1_bin[-1])
        elif block == '0101':
            value_1_bin = value_1_bin[:7] + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:7] + self.__reverse_bit__(value_2_bin[-1])
        elif block == '0110':
            value_1_bin = value_1_bin[:7] + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + value_2_bin[-1]
        elif block == '0111':
            value_1_bin = value_1_bin[:7] + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
        elif block == '1000':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + value_1_bin[-1]
        elif block == '1001':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + value_1_bin[-1]
            value_2_bin = value_2_bin[:7] + self.__reverse_bit__(value_2_bin[-1])
        elif block == '1010':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + value_1_bin[-1]
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + value_2_bin[-1]
        elif block == '1011':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + value_1_bin[-1]
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
        elif block == '1100':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
        elif block == '1101':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:7] + self.__reverse_bit__(value_2_bin[-1])
        elif block == '1110':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + value_2_bin[-1]
        elif block == '1111':
            value_1_bin = value_1_bin[:6] + self.__reverse_bit__(value_1_bin[-2]) + self.__reverse_bit__(value_1_bin[-1])
            value_2_bin = value_2_bin[:6] + self.__reverse_bit__(value_2_bin[-2]) + self.__reverse_bit__(value_2_bin[-1])
        
        return value_1_bin, value_2_bin

    def __get_hidded_bits__(self, total_pixels, array):
        count = 0
        hidden_bits = ""
        color_number = 1
        if self.color == "":
            color_number = 3

        if self.type == 1:
            count_inc = 3
            calculate_hidden_bit = self.__calculate_hidden_bits_type_1__
        else:
            count_inc = 4
            calculate_hidden_bit = self.__calculate_hidden_bits_type_2__

        msg_len = 0
        index = 0
        map_index = 0
        SOM_bit_len = math.ceil(math.log2((total_pixels * color_number) * 2))
        color_init, color_end = self.__get_color_range__()
        one_color = False
        color_value = color_init
        if color_init + 1 == color_end:
            one_color = True

        while (msg_len == 0):
            if one_color:
                value_1 = array[index][color_value]
                value_2 = array[index+1][color_value]
                index += 2
            else:
                index, color_value, value_1 = self.__get_value__(array, index, color_value)
                index, color_value, value_2 = self.__get_value__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_1_chunk = value_1_bin[-2:]
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin
            value_2_chunk = value_2_bin[-2:]
            hidden_bits += calculate_hidden_bit(self.location_map[map_index], self.location_map[map_index+1], value_1_chunk, value_2_chunk)
            map_index += 2
            count += count_inc
            if count < SOM_bit_len:
                continue
        
            msg_len = int(hidden_bits[:SOM_bit_len], 2)
            hidden_bits = hidden_bits[SOM_bit_len:]
            break

        while (msg_len > 0):
            if one_color:
                value_1 = array[index][color_value]
                value_2 = array[index+1][color_value]
                index += 2
            else:
                index, color_value, value_1 = self.__get_value__(array, index, color_value)
                index, color_value, value_2 = self.__get_value__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_1_chunk = value_1_bin[-2:]
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin
            value_2_chunk = value_2_bin[-2:]
            hidden_bits += calculate_hidden_bit(self.location_map[map_index], self.location_map[map_index+1], value_1_chunk, value_2_chunk)
            map_index += 2
            msg_len -= count_inc
        
        return hidden_bits

    def __calculate_hidden_bits_type_1__(self, map, map_2, value_1_chunk, value_2_chunk):
        if map == value_1_chunk and map_2 == value_2_chunk:
            return '000'
        elif map[0] == value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '001'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '010'
        elif map[0] == value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '011'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '100'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '101'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '110'
        elif map[0] != value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '111'
        
        return '000'

    def __calculate_hidden_bits_type_2__(self, map, map_2, value_1_chunk, value_2_chunk):
        if map == value_1_chunk and map_2 == value_2_chunk:
            return '0000'
        elif map[0] == value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '0001'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '0010'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '0011'
        elif map[0] == value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '0100'
        elif map[0] == value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '0101'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '0110'
        elif map[0] == value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '0111'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '1000'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '1001'
        elif map[0] != value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '1010'
        elif map[0] != value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] == value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '1011'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '1100'
        elif map[0] != value_1_chunk[0] and map_2[0] == value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '1101'
        elif map[0] != value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] == value_2_chunk[1]:
            return '1110'
        elif map[0] != value_1_chunk[0] and map_2[0] != value_2_chunk[0] and map[1] != value_1_chunk[1] and map_2[1] != value_2_chunk[1]:
            return '1111'
        
        return '0000'