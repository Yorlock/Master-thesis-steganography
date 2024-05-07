from PIL import Image
import numpy as np
import math

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class BF(steganographyAlgorythm):
    def __init__(self, type=1, color=""):
        self.stego_img_path = ""
        self.destination_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.location_map = []
        if type != 1 or type != 2:
            self.type = 1
        else:
            self.type = type

        self.colors = ['R', 'G', 'B']
        if color in self.colors:
            self.color = color
        else:
            self.color = ""

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
        color_number = 1
        if self.color == "":
            color_number = 3

        type_number = 2
        if self.type == 2:
            type_number = 3

        available_blocks = (total_pixels * color_number) // type_number
        SOM_bit_len = math.ceil(math.log2(available_blocks))
        SOM_bit_value = len(b_message)
        SOM = bin(SOM_bit_value)[2:]
        SOM = '0' * (SOM_bit_len - len(SOM)) + SOM

        b_message = SOM + b_message
        req_blocks = len(b_message) // 3
        if req_blocks > available_blocks:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return
        
        if self.type == 1:
            self.__calculate_location_map_type_1__(total_pixels, array)
            array = self.__hide_text_type_1__(array, b_message)
        else:
            self.__calculate_location_map_type_2__(total_pixels, array)
            array = self.__hide_text_type_2__(array, b_message)

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

        if self.type == 1:
            hidden_bits = self.__get_hidded_bits_type_1__(total_pixels, array)
        else:
            hidden_bits = self.__get_hidded_bits_type_2__(total_pixels, array)

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
        if len(hidden_bits[-1]) != 8:
            hidden_bits = hidden_bits[:-1]

        message = ""
        for i in range(len(hidden_bits)):
            message += chr(int(hidden_bits[i], 2))

        self.destination_path = util.get_decode_path(self)
        destination_file = open(self.destination_path, "w")
        destination_file.write(message)
        destination_file.close()

        self.is_success = True

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1

    def __reverse_bit__(self, value):
        if value == '0':
            return '1'
        return '0'

    def __calculate_location_map_type_1__(self, total_pixels, array):
        location_map = []
        color_init, color_end = self.__get_color_range__()
        for p in range(total_pixels):
            for color in range(color_init, color_end):
                value = array[p][color]
                value_bit = bin(value)[2:]
                value_bit = '0' * (8 - len(value_bit)) + value_bit
                location_map.append(value_bit[-2:])
        
        self.location_map = location_map

    def __hide_text_type_1__(self, array, b_message):
        b_message_block = [b_message[i:i+3] for i in range(0, len(b_message), 3)]
        if len(b_message_block[-1]) != 3:
            b_message_block[-1] = b_message_block[-1] + '0' * (3 - len(b_message_block[-1]))

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
                index, color_value, value_1 = self.__get_value_type_1__(array, index, color_value)
                value_2_index = index
                value_2_color = color_value
                index, color_value, value_2 = self.__get_value_type_1__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin

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

            array[value_1_index][value_1_color] = int(value_1_bin, 2)
            array[value_2_index][value_2_color] = int(value_2_bin, 2)
        return array

    def __get_value_type_1__(self, array, index, color_value):
        if color_value == 2:
            value = array[index][color_value]
            color_value = 0
            index += 1
        else:
            value = array[index][color_value]
            color_value += 1

        return index, color_value, value

    def __calculate_location_map_type_2__(self, total_pixels, array):
        pass

    def __hide_text_type_2__(self, array, b_message):
        pass

    def __get_value_type_2__(self, array, index, color_value):
        pass

    def __get_hidded_bits_type_1__(self, total_pixels, array):
        count = 0
        hidden_bits = ""
        color_number = 1
        if self.color == "":
            color_number = 3

        type_number = 2
        if self.type == 2:
            type_number = 3

        msg_len = 0
        index = 0
        map_index = 0
        SOM_bit_len = math.ceil(math.log2((total_pixels * color_number) // type_number))
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
                index, color_value, value_1 = self.__get_value_type_1__(array, index, color_value)
                index, color_value, value_2 = self.__get_value_type_1__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_1_chunk = value_1_bin[-2:]
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin
            value_2_chunk = value_2_bin[-2:]
            hidden_bits += self.__calculate_hidden_bits_type_1__(self.location_map[map_index], self.location_map[map_index+1], value_1_chunk, value_2_chunk)
            map_index += 2
            count += 3
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
                index, color_value, value_1 = self.__get_value_type_1__(array, index, color_value)
                index, color_value, value_2 = self.__get_value_type_1__(array, index, color_value)

            value_1_bin = bin(value_1)[2:]
            value_1_bin = '0' * (8 - len(value_1_bin)) + value_1_bin
            value_1_chunk = value_1_bin[-2:]
            value_2_bin = bin(value_2)[2:]
            value_2_bin = '0' * (8 - len(value_2_bin)) + value_2_bin
            value_2_chunk = value_2_bin[-2:]
            hidden_bits += self.__calculate_hidden_bits_type_1__(self.location_map[map_index], self.location_map[map_index+1], value_1_chunk, value_2_chunk)
            map_index += 2
            msg_len -= 3
        
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

    def __get_hidded_bits_type_2__(self, total_pixels):
        pass