from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

# the type parameter allows you to change the capacity of the hidden bits when QVD is used
# k parameter allows you to specify how many bits should be hidden in one byte when LSB is used
class QVD_8D(steganographyAlgorithm):
    def __init__(self, end_msg="$t3g0", color="", type=3, k=4, estimation=False):
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

        if k < 1 or k > 7:
            self.k = 4
        else:
            self.k = k

        self.estimation = estimation
        self.type_range = np.array([[0,7],[8,15],[16,31],[32,63]])
        if type == 0:
            self.type = 0
            self.type_capacity = np.array([1, 1, 1, 1])
        elif type == 1:
            self.type = 1
            self.type_capacity = np.array([2, 2, 3, 4])
        elif type == 2:
            self.type = 2
            self.type_capacity = np.array([1, 1, 2, 3])
        else:
            self.type = 3
            self.type_capacity = np.array([3, 3, 4, 5])
        
        json_color = self.color
        if json_color == "":
            json_color = "RGB"

        self.timeout = 10
        self.json_content = {"algorithm":"QVD_8D", "settings": {"type":self.type ,"end_msg":self.end_msg, "color":json_color, "k":self.k}}

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

        quotient_block_list, reminder_block_list = self.__calculate_support_block_bits__(block_list)
        enc_block_list = self.__hide_text__(req_bits, block_list, quotient_block_list, reminder_block_list, b_message, n)
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
        
        if 1 + 2 * 8 + 8 * self.type_capacity[0] * color_number > (self.k - 1 + self.k * 8) * color_number:
            min_bits = (self.k - 1 + self.k * 8) * color_number
        else:
            min_bits = 1 + 2 * 8 + 8 * self.type_capacity[0] * color_number

        for i in range(num_blocks_row):
            for j in range(num_blocks_col):
                start_row = i * 3
                start_col = j * 3
                block = matrix[start_row:start_row+3, start_col:start_col+3]
                block = np.array(block, dtype='int')
                available_bits += min_bits
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

    def __calculate_capacity__(self, value):
        for index in range(len(self.type_range)):
            if value >= self.type_range[index][0] and value <= self.type_range[index][1]:
                return int(self.type_capacity[index]), int(self.type_range[index][0])
        return 0, 0

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1

    def __calculate_support_block_bits__(self, block_list):
        quotient_block_list = []
        reminder_block_list = []
        color_init, color_end = self.__get_color_range__()
        for block in block_list:
            block_quotient = block.copy()
            block_reminder = block.copy()
            for color in range(color_init, color_end):
                for x in range(3):
                    for y in range(3):
                        block_quotient[x][y][color] = block_quotient[x][y][color] // 4
                        block_reminder[x][y][color] = np.mod(block_reminder[x][y][color], 4)

            quotient_block_list.append(block_quotient)
            reminder_block_list.append(block_reminder)

        return quotient_block_list, reminder_block_list

    def __hide_text__(self, req_bits, block_list, quotient_block_list, reminder_block_list, b_message, n_image):
        used_bits = 0
        used_block = -1
        data_bits_len = 1 + 2*8 + 5*8 #always assume the worst case scenario
        left_bits = data_bits_len
        color_init, color_end = self.__get_color_range__()
        while used_bits < req_bits:
            used_block += 1
            current_array = block_list[used_block].flatten()
            quotient_array = quotient_block_list[used_block].flatten()
            reminder_array = reminder_block_list[used_block].flatten()     
            for color in range(color_init, color_end):
                if used_bits >= req_bits:
                    return block_list

                is_end_of_message = False
                if used_bits+data_bits_len > req_bits:
                    is_end_of_message = True
                    left_bits = req_bits - used_bits
                    current_b_message = b_message[used_bits:used_bits+left_bits]
                    current_b_message = current_b_message + '0'*(data_bits_len - left_bits)
                    used_bits += left_bits
                else:
                    current_b_message = b_message[used_bits:used_bits+data_bits_len]
                    used_bits += data_bits_len

                current_b_message_FOBP = current_b_message #In case of FOBP - Fall of boundary problem
                middle_value = block_list[used_block][1][1][color]
                color_array = current_array[color::n_image]
                color_array = np.delete(color_array, 4)

                quotient_middle_value = quotient_block_list[used_block][1][1][color]
                color_quotient_array = quotient_array[color::n_image]
                color_quotient_array = np.delete(color_quotient_array, 4)

                color_reminder_array = reminder_array[color::n_image]
                color_reminder_array = np.delete(color_reminder_array, 4)

                color_reminder_2_array = []
                middle_value_bit = bin(middle_value)[2:]
                middle_value_bit = '0' * (8 - len(middle_value_bit)) + middle_value_bit
                middle_value_LSB_bit = current_b_message[0] + '1'
                middle_value_LSB_int = int(middle_value_LSB_bit, 2)
                current_b_message = current_b_message[1:]
                for i in range(8):
                    value_LSB = int(current_b_message[:2], 2)
                    current_b_message = current_b_message[2:]
                    color_reminder_2_array.append(value_LSB)
                
                color_quotient_q_array = []
                quotient_avg = 0
                fall_of_boundary = False
                for q_value in color_quotient_array:
                    value_d = q_value - quotient_middle_value
                    n, L = self.__calculate_capacity__(np.abs(value_d))
                    value_LSB = int(current_b_message[:n], 2)
                    current_b_message = current_b_message[n:]
                    if value_d >= 0:
                        value_d_2 = L + value_LSB
                    else:
                        value_d_2 = -L - value_LSB
                    
                    m = value_d_2 - value_d
                    if value_d%2 == 0:
                        q_middle_value_2 = int(quotient_middle_value -  np.floor(m/2))
                        q_value_2 = int(q_value + np.ceil(m/2))
                    else:
                        q_middle_value_2 = int(quotient_middle_value -  np.ceil(m/2))
                        q_value_2 = int(q_value + np.floor(m/2))
                    
                    if (q_value_2 < 0 or q_value_2 > 63) or (q_middle_value_2 < 0 or q_middle_value_2 > 63): #LSB
                            fall_of_boundary = True
                            break

                    quotient_avg += q_middle_value_2
                    color_quotient_q_array.append([q_middle_value_2, q_value_2])
                
                if not fall_of_boundary: #QVD
                    color_array_new = np.empty((0,), int)
                    q_middle_value_avg = int(np.ceil(quotient_avg / 8))
                    middle_value_new = q_middle_value_avg * 4 + middle_value_LSB_int
                    for i in range(8):
                        Q_i = color_quotient_q_array[i][1] + (q_middle_value_avg - color_quotient_q_array[i][0])
                        if Q_i < 0 or Q_i > 63: #LSB
                            fall_of_boundary = True
                            break

                        value_new = Q_i * 4 + color_reminder_2_array[i]
                        color_array_new = np.append(color_array_new, value_new)

                if not fall_of_boundary:
                    color_array_new = np.insert(color_array_new, 4, middle_value_new)
                else:
                    current_b_message, color_array_new = self.__hide_text_fall_of_boundary__(middle_value, current_b_message_FOBP, color_array)

                if not is_end_of_message:
                    used_bits -= len(current_b_message)
                elif data_bits_len - left_bits < len(current_b_message):
                    used_bits -= len(current_b_message) - (data_bits_len - left_bits)

                self.__write_new_value_to_block__(color_array_new, block_list[used_block], color)

        return block_list
    
    def __hide_text_fall_of_boundary__(self, middle_value, current_b_message, color_array):
        color_array_new = np.empty((0,), int)
        middle_value_bit = bin(middle_value)[2:]
        middle_value_bit = '0' * (8 - len(middle_value_bit)) + middle_value_bit
        dec_old = int(middle_value_bit[-self.k:], 2)
        middle_value_bit_LSB = current_b_message[:self.k-1] + '0'
        current_b_message = current_b_message[self.k-1:]
        dec_new = int(middle_value_bit_LSB, 2)
        middle_value_new = int(middle_value_bit[:self.k] + middle_value_bit_LSB, 2)
        dev = dec_old - dec_new
        if dev > 16 and 0 <= middle_value_new + 32 <= 255:
            middle_value_new += 32
        elif dev < -16 and 0 <= middle_value_new - 32 <= 255:
            middle_value_new -= 32

        for value in color_array:
            value_bit = bin(value)[2:]
            value_bit = '0' * (8 - len(value_bit)) + value_bit
            deci_old = int(value_bit[-self.k:], 2)
            value_bit_LSB = current_b_message[:self.k]
            current_b_message = current_b_message[self.k:]
            deci_new = int(value_bit_LSB, 2)
            value_new = int(value_bit[:self.k] + value_bit_LSB, 2)
            devi = deci_old - deci_new
            if devi > 16 and 0 <= value_new + 32 <= 255:
                value_new += 32
            elif devi < -16 and 0 <= value_new - 32 <= 255:
                value_new -= 32
            
            color_array_new = np.append(color_array_new, value_new)
            
        color_array_new = np.insert(color_array_new, 4, middle_value_new)
        return current_b_message, color_array_new

    def __write_new_value_to_block__(self, array, block, color):
        x = 0
        y = 0
        for value in array:
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
    
    def __get_hidden_text_from_block__(self, block, n_image):
        hidden_bits = ""
        array = block.flatten()
        color_init, color_end = self.__get_color_range__()
        for color in range(color_init, color_end):
            middle_value = int(block[1][1][color])
            middle_value_bit = bin(middle_value)[2:]
            middle_value_bit = '0' * (8 - len(middle_value_bit)) + middle_value_bit
            color_array = array[color::n_image]
            color_array = np.delete(color_array, 4)

            LSB = middle_value_bit[-1]
            if LSB == '0': #LSB
                hidden_bits += middle_value_bit[-self.k:-1]
                for value in color_array:
                    value_bit = bin(value)[2:]
                    value_bit = '0' * (8 - len(value_bit)) + value_bit
                    hidden_bits += value_bit[-self.k:]
            else: #QVD
                hidden_bits += middle_value_bit[-2]
                for value in color_array:
                    R = np.mod(value, 4)
                    R_bit = bin(R)[2:]
                    R_bit = '0' * (2 - len(R_bit)) + R_bit
                    hidden_bits += R_bit
                
                Qc = middle_value // 4
                for value in color_array:
                    Q = value // 4
                    d = np.abs(Qc - Q)
                    n, L  = self.__calculate_capacity__(d)
                    b_value = int(np.abs(d - L))
                    b_bit = bin(b_value)[2:]
                    b_bit = '0' * (8 - len(b_bit)) + b_bit
                    hidden_bits += b_bit[-n:]

        return hidden_bits