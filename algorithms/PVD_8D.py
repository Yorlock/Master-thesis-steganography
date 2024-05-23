from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

#Type 1 possesses higher PSNR and type 2 possesses higher hiding capacity
class PVD_8D(steganographyAlgorithm):
    def __init__(self, end_msg="$t3g0", color="", type=1, estimation = False):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.end_msg = end_msg
        self.estimation = estimation
        self.colors = ['R', 'G', 'B']
        if color in self.colors:
            self.color = color
        else:
            self.color = ""

        if not isinstance(type, int):
            self.type = 1
            self.error_msg += "Parameter type was set to 1."
        elif type != 0 and type != 1 and type != 2:
            self.type = 1
            self.error_msg += "Parameter type was set to 1."
        else:
            self.type = type

        self.type_range = np.array([[0,7],[8,15],[16,31],[32,63],[64,127],[128,255]])
        if self.type == 1:
            self.t = 3
            self.type_capacity = np.array([3, 3, 3, 3, 4, 4])
        elif self.type == 2:
            self.t = 4
            self.type_capacity = np.array([3, 3, 4, 5, 6, 6])
        else:
            self.t = 1
            self.type_capacity = np.array([1, 1, 1, 1, 1, 1])
        
        json_color = self.color
        if json_color == "":
            json_color = "RGB"

        self.timeout = 10
        self.json_content = {"algorithm":"PVD_8D", "settings": {"type":self.type, "color":json_color, "end_msg":self.end_msg}}

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
        matrix = np.array(img)

        msg_file = open(msg_path,'r')
        message = msg_file.read()
        msg_file.close()

        start_time = time()

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        message += self.end_msg
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_bits = len(b_message)
        available_bits, block_list = self.__calculate_available_bits__(req_bits, matrix, width, height)

        if self.estimation and req_bits > available_bits:
            self.is_success = False
            self.error_msg = "ERROR: An estimate of the available bits shows that a larger file size is needed. Turn off estimation, but this may cause an application error."
            return

        enc_block_list = self.__hide_text__(req_bits, block_list, b_message, n)
        enc_matrix = self.__update_matrix__(matrix, enc_block_list, width, height)

        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_encode"] =  milli_sec_elapsed

        enc_img = Image.fromarray(enc_matrix.astype('uint8'), img.mode)
        enc_img.save(self.stego_img_path)
        self.is_success = True

    def decode(self, pipe=None, save_to_txt=True):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return

        self.reset_params()
        img = Image.open(self.stego_img_path, 'r')
        width, height = img.size
        matrix = np.array(img)

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        start_time = time()

        block_list = self.__get_block_list__(matrix, width, height)
        block_bits = ""
        message = ""

        is_end = False
        left_bits = ''
        for block in block_list:
            if is_end:
                break

            block_bits = left_bits + self.__get_hidden_text_from_block__(block, n)
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
            pipe.send(message)
            pipe.close()
        
        self.is_success = True
        return message

    def __calculate_available_bits__(self, req_bits, matrix, cols, rows):
        available_bits = 0
        blocks = []
        num_blocks_row = rows // 3
        num_blocks_col = cols // 3
        color_number = 1
        if self.color == "":
            color_number = 3

        for i in range(num_blocks_row):
            for j in range(num_blocks_col):
                start_row = i * 3
                start_col = j * 3
                block = matrix[start_row:start_row+3, start_col:start_col+3]
                block = np.array(block, dtype='int')
                available_bits += self.t * color_number + self.type_capacity[0] * 8 * color_number
                blocks.append(block)
                if self.estimation and req_bits <= available_bits:
                    return available_bits, blocks

        return available_bits, blocks

    def __get_pixel_value__(self, pixel, num_bits):
        bits = ''
        for i in range(num_bits-1,-1,-1):
            bits += str(self.get_bit_value(pixel, i))
        
        return bits

    def get_bit_value(self, number, n):
        # Create a mask with a 1 at the nth position
        mask = 1 << n

        # Perform bitwise AND operation with the number and mask
        # If the result is non-zero, the bit at position n is 1, otherwise, it's 0
        return (number & mask) >> n

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1


    def __calculate_capacity__(self, value):
        for index in range(len(self.type_range)):
            if value >= self.type_range[index][0] and value <= self.type_range[index][1]:
                return int(self.type_capacity[index]), int(self.type_range[index][0])
        return 0, 0
    
    def __hide_text__(self, req_bits, block_list, b_message, n):
        used_bits = 0
        used_block = -1
        color_init, color_end = self.__get_color_range__()
        while used_bits < req_bits:
            used_block += 1
            current_array = block_list[used_block].flatten()
            for color in range(color_init, color_end):
                if used_bits >= req_bits:
                    return block_list

                if used_bits+self.t > req_bits:
                    left_bits = req_bits - used_bits
                    message_value_bit = b_message[used_bits:used_bits+left_bits]
                    message_value_bit = message_value_bit + '0' * (self.t - left_bits)
                    used_bits += left_bits
                else:
                    message_value_bit = b_message[used_bits:used_bits+self.t]
                    used_bits += self.t

                color_array = current_array[color::n]
                color_array = np.delete(color_array, 4)
                middle_value_int_old = block_list[used_block][1][1][color]
                middle_value_bit_old = bin(middle_value_int_old)[2:]
                middle_value_bit_old = '0' * (8 - len(middle_value_bit_old)) + middle_value_bit_old
                middle_value_bit_new = middle_value_bit_old[:8-self.t] + message_value_bit
                P_1 = int(middle_value_bit_new, 2)

                dec_old = int(middle_value_bit_old[-self.t:],2)
                dec_new = int(message_value_bit,2)
                dev = dec_old - dec_new
                value = np.power(2, self.t)
                if dev > np.power(2, self.t-1) and 0 <= P_1 + value <= 255:
                    P_1 = P_1 + value
                elif dev < -np.power(2, self.t-1) and 0 <= P_1 - value <= 255:
                    P_1 = P_1 - value

                block_list[used_block][1][1][color] = P_1
                if used_bits >= req_bits:
                    return block_list

                new_color_array = np.empty((0,), int)
                for P in color_array:
                    P = int(P)
                    d = np.abs(P_1 - P) 
                    t, L = self.__calculate_capacity__(d)
                    if used_bits+t > req_bits:
                        left_bits = req_bits - used_bits
                        message_value_bit = b_message[used_bits:used_bits+left_bits]
                        message_value_bit = message_value_bit + '0' * (self.t - left_bits)
                        S = int(message_value_bit,2)
                        used_bits += left_bits
                    else:
                        S = int(b_message[used_bits:used_bits+t],2)
                        used_bits += t

                    d_1 = L + S
                    P_2 = P_1 - d_1
                    P_3 = P_1 + d_1
                    if np.abs(P - P_2) < np.abs(P - P_3) and 0 <= P_2 <= 255:
                        new_P_1 = P_2
                    else:
                        new_P_1 = P_3

                    new_color_array = np.append(new_color_array, new_P_1)
                    if used_bits >= req_bits:
                        self.__write_new_value_to_block__(new_color_array, block_list[used_block], color)
                        return block_list
            
                self.__write_new_value_to_block__(new_color_array, block_list[used_block], color)

        return block_list
    
    def __write_new_value_to_block__(self, array, block, color):
        x = 0
        y = 0
        for value in array:
            if x == 1 and y == 1:
                y += 1

            block[x][y][color] = value
            y += 1
            if y == 3:
                y = 0
                x += 1
    
    def __update_matrix__(self, matrix, block_list, cols, rows):
        num_blocks_row = rows // 3
        num_blocks_col = cols // 3
        block_index = 0
        for i in range(num_blocks_row):
            for j in range(num_blocks_col):
                if block_index == len(block_list):
                    return matrix

                start_row = i * 3
                start_col = j * 3
                matrix[start_row:start_row+3, start_col:start_col+3] = block_list[block_index]
                block_index += 1

        return matrix

    def __get_block_list__(self, matrix, cols, rows):
        blocks = []
        num_blocks_row = rows // 3
        num_blocks_col = cols // 3
        for i in range(num_blocks_row):
            for j in range(num_blocks_col):
                start_row = i * 3
                start_col = j * 3
                block = matrix[start_row:start_row+3, start_col:start_col+3]
                blocks.append(block)

        return blocks
    
    def __get_hidden_text_from_block__(self, block, n):
        hidden_bits = ""
        array = block.flatten()
        color_init, color_end = self.__get_color_range__()
        for color in range(color_init, color_end):
            P_1 = int(block[1][1][color])
            hidden_bits += self.__get_pixel_value__(P_1, self.t)
            color_array = array[color::n]
            color_array = np.delete(color_array, 4)
            for P in color_array:
                P = int(P)
                d = np.abs(P_1 - P)
                t, L = self.__calculate_capacity__(d)
                S = d - L
                S_bits = bin(S)[2:]
                if len(S_bits) > t:
                    upper_value = np.power(2, len(S_bits))
                    new_value = upper_value - S
                    new_value_bits = bin(new_value)[2:]
                    new_value_bits = '0' * (8 - len(new_value_bits)) + new_value_bits
                    S_bits = new_value_bits[-self.t:]
                elif len(S_bits) < t:
                    S_bits = '0' * (t - len(S_bits)) + S_bits

                hidden_bits += S_bits
        return hidden_bits