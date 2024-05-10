from PIL import Image
import numpy as np
import math
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class PVDMF(steganographyAlgorithm):
    def __init__(self, end_msg="$t3g0", type=1, color="", estimation=True, calculate_metrics=False):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.algorithm_path_dir = util.get_algorithm_path_dir(self)
        self.stego_img_path = util.get_encode_path(self)
        self.destination_path = util.get_decode_path(self)
        self.metrics_path = util.get_metrics_path(self)
        self.is_success = False
        self.error_msg = ""
        self.estimation = estimation
        self.end_msg = end_msg
        if type == 1:
            self.type = 1
            self.type_range = np.array([[0,15],[16,31],[32,255]])
            self.type_capacity = np.array([2, 3, 4])
        else:
            self.type = 2
            self.type_range = np.array([[0,15],[16,255]])
            self.type_capacity = np.array([3, 4])

        self.colors = ['R', 'G', 'B']
        if color in self.colors:
            self.color = color
        else:
            self.color = ""
        
        self.calculate_metrics = calculate_metrics
        self.json_content = {"algorythm":"PVDMF", "settings": {"type":self.type ,"end_msg":self.end_msg, "color":self.color}}

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
    def metrics_path(self):
        return self._metrics_path
    
    @metrics_path.setter
    def metrics_path(self, value):
        self._metrics_path = value

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

        message += self.end_msg
        b_message = ''.join([format(ord(i), "08b") for i in message])
        min_type_capacity = self.type_capacity[0]
        color_number = 1
        if self.color == "":
            color_number = 3

        req_bits = len(b_message)
        available_bits = total_pixels // 2 * color_number * min_type_capacity
        if self.estimation and req_bits > available_bits:
            self.is_success = False
            self.error_msg = "ERROR: An estimate of the available bits shows that a larger file size is needed. Turn off estimation, but this may cause an application error."
            return
        
        array = self.__hide_text__(array, b_message)
        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
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

        color_number = 1
        if self.color == "":
            color_number = 3

        total_bits = array.size//n * color_number
        index = 0
        color_init, color_end = self.__get_color_range__()
        one_color = False
        color_value = color_init
        if color_init + 1 == color_end:
            one_color = True

        if self.type == 1:
            get_hidded_bits = self.__get_hidded_bits_type_1__
        else:
            get_hidded_bits = self.__get_hidded_bits_type_2__

        hidden_bits = ""
        block_bits = ""
        message = ""
        is_end = False
        left_bits = ''
        for p in range(0, total_bits, 2):
            if is_end:
                break

            if one_color:
                value_1 = array[index][color_value]
                value_2 = array[index+1][color_value]
                index += 2
            else:
                index, color_value, value_1 = self.__get_value__(array, index, color_value)
                index, color_value, value_2 = self.__get_value__(array, index, color_value)

            block_bits = left_bits + get_hidded_bits(value_1, value_2)
            hidden_bits = [block_bits[i:i+8] for i in range(0, len(block_bits), 8)]
            if len(hidden_bits[-1]) != 8:
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

        with open(self.metrics_path, "w") as f:
            json.dump(self.json_content, f)

        destination_file = open(self.destination_path, "w")
        destination_file.write(message[:-len(self.end_msg)])
        destination_file.close()
        self.is_success = True

    def __get_color_range__(self):
        if self.color == "":
            return 0, 3

        color = self.colors.index(self.color)
        return color, color + 1

    def __get_value__(self, array, index, color_value):
        if color_value == 2:
            value = array[index][color_value]
            color_value = 0
            index += 1
        else:
            value = array[index][color_value]
            color_value += 1

        return index, color_value, value

    def __calculate_capacity__(self, value):
        for index in range(len(self.type_range)):
            if value >= self.type_range[index][0] and value <= self.type_range[index][1]:
                return int(self.type_capacity[index]), index+1
        return 0, 0

    def __hide_text__(self, array, b_message):
        if self.type == 1:
            calculate_new_values = self.__calculate_new_values_type_1__
        else:
            calculate_new_values = self.__calculate_new_values_type_2__

        index = 0
        color_init, color_end = self.__get_color_range__()
        one_color = False
        color_value = color_init
        b_message_len = len(b_message)
        b_message_index = 0
        if color_init + 1 == color_end:
            one_color = True

        while b_message_len > b_message_index:
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

            value_1, value_2, b_message_index = calculate_new_values(b_message, b_message_index, value_1, value_2)
            array[value_1_index][value_1_color] = value_1
            array[value_2_index][value_2_color] = value_2
        return array

    def __calculate_new_values_type_1__(self, b_message, index, P_1, P_2):
        d = np.abs(P_1 - P_2)
        n, R = self.__calculate_capacity__(d)
        hidden_msg_1 = b_message[index:index+n]
        if len(hidden_msg_1) < n:
            hidden_msg_1 = hidden_msg_1 + '0' * (n - len(hidden_msg_1))

        index += n
        hidden_msg_2 = b_message[index:index+n]
        if len(hidden_msg_2) < n:
            hidden_msg_2 = hidden_msg_2 + '0' * (n - len(hidden_msg_2))

        index += n
        dec_1 = int(hidden_msg_1, 2)
        dec_2 = int(hidden_msg_2, 2)
        if R == 1:
            rem_1 = np.mod(P_1, 4)
            rem_2 = np.mod(P_2, 4)
        elif R == 2:
            rem_1 = np.mod(P_1, 8)
            rem_2 = np.mod(P_2, 8)
        else:
            rem_1 = np.mod(P_1, 16)
            rem_2 = np.mod(P_2, 16)

        x_1 = rem_1 - dec_1
        x_2 = dec_1 - rem_1
        y_1 = rem_2 - dec_2
        y_2 = dec_2 - rem_2
        P_1_new = P_1
        if rem_1 < dec_1 and np.abs(x_1) < np.power(2, n-1):
            P_1_new = P_1 - x_1
        elif rem_1 > dec_1 and np.abs(x_2) < np.power(2, n-1):
            P_1_new = P_1 + x_2
        elif rem_1 < dec_1 and np.abs(x_1) >= np.power(2, n-1):
            z = np.power(2, n) + x_1
            P_1_new = P_1 - z
        elif rem_1 > dec_1 and np.abs(x_2) >= np.power(2, n-1):
            z = np.power(2, n) + x_2
            P_1_new = P_1 + z
        
        P_2_new = P_2
        if rem_2 < dec_2 and np.abs(y_1) < np.power(2, n-1):
            P_2_new = P_2 - y_1
        elif rem_2 > dec_2 and np.abs(y_2) < np.power(2, n-1):
            P_2_new = P_2 + y_2
        elif rem_2 < dec_2 and np.abs(y_1) >= np.power(2, n-1):
            zz = np.power(2, n) + y_1
            P_2_new = P_2 - zz
        elif rem_2 > dec_2 and np.abs(y_2) >= np.power(2, n-1):
            zz = np.power(2, n) + y_2
            P_2_new = P_2 + zz

        d_new = np.abs(P_1_new - P_2_new)
        _, R_new = self.__calculate_capacity__(d_new)
        P_1_stego = P_1_new
        P_2_stego = P_2_new
        if R == 1:
            if R_new == 2 and P_1_new >= P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)
            elif R_new == 2 and P_1_new < P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
        elif R == 2:
            if R_new == 1 and P_1_new >= P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
            elif R_new == 1 and P_1_new < P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)
            elif R_new == 3 and P_1_new >= P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)
            elif R_new == 3 and P_1_new < P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
        elif R == 3:
            if R_new == 1 and P_1_new >= P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
            elif R_new == 1 and P_1_new < P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)
            elif R_new == 2 and P_1_new >= P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
            elif R_new == 2 and P_1_new < P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)

        if P_1_stego < 0 or P_2_stego < 0:
            P_1_stego = P_1_stego + np.power(2, n)
            P_2_stego = P_2_stego + np.power(2, n)
        elif P_1_stego > 255 or P_2_stego > 255:
            P_1_stego = P_1_stego - np.power(2, n)
            P_2_stego = P_2_stego - np.power(2, n)

        return P_1_stego, P_2_stego, index

    def __calculate_new_values_type_2__(self, b_message, index, P_1, P_2):
        d = np.abs(P_1 - P_2)
        n, R = self.__calculate_capacity__(d)
        hidden_msg_1 = b_message[index:index+n]
        if len(hidden_msg_1) < n:
            hidden_msg_1 = hidden_msg_1 + '0' * (n - len(hidden_msg_1))

        index += n
        hidden_msg_2 = b_message[index:index+n]
        if len(hidden_msg_2) < n:
            hidden_msg_2 = hidden_msg_2 + '0' * (n - len(hidden_msg_2))

        index += n
        dec_1 = int(hidden_msg_1, 2)
        dec_2 = int(hidden_msg_2, 2)
        if R == 1:
            rem_1 = np.mod(P_1, 8)
            rem_2 = np.mod(P_2, 8)
        else:
            rem_1 = np.mod(P_1, 16)
            rem_2 = np.mod(P_2, 16)

        x_1 = rem_1 - dec_1
        x_2 = dec_1 - rem_1
        y_1 = rem_2 - dec_2
        y_2 = dec_2 - rem_2
        P_1_new = P_1
        if rem_1 < dec_1 and np.abs(x_1) < np.power(2, n-1):
            P_1_new = P_1 - x_1
        elif rem_1 > dec_1 and np.abs(x_2) < np.power(2, n-1):
            P_1_new = P_1 + x_2
        elif rem_1 < dec_1 and np.abs(x_1) >= np.power(2, n-1):
            z = np.power(2, n) + x_1
            P_1_new = P_1 - z
        elif rem_1 > dec_1 and np.abs(x_2) >= np.power(2, n-1):
            z = np.power(2, n) + x_2
            P_1_new = P_1 + z
        
        P_2_new = P_2
        if rem_2 < dec_2 and np.abs(y_1) < np.power(2, n-1):
            P_2_new = P_2 - y_1
        elif rem_2 > dec_2 and np.abs(y_2) < np.power(2, n-1):
            P_2_new = P_2 + y_2
        elif rem_2 < dec_2 and np.abs(y_1) >= np.power(2, n-1):
            zz = np.power(2, n) + y_1
            P_2_new = P_2 - zz
        elif rem_2 > dec_2 and np.abs(y_2) >= np.power(2, n-1):
            zz = np.power(2, n) + y_2
            P_2_new = P_2 + zz

        d_new = np.abs(P_1_new - P_2_new)
        _, R_new = self.__calculate_capacity__(d_new)
        P_1_stego = P_1_new
        P_2_stego = P_2_new
        if R == 1:
            if R_new == 2 and P_1_new >= P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)
            elif R_new == 2 and P_1_new < P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
        elif R == 2:
            if R_new == 1 and P_1_new >= P_2_new:
                P_1_stego = P_1_new + np.power(2, n)
                P_2_stego = P_2_new - np.power(2, n)
            elif R_new == 1 and P_1_new < P_2_new:
                P_1_stego = P_1_new - np.power(2, n)
                P_2_stego = P_2_new + np.power(2, n)

        if P_1_stego < 0 or P_2_stego < 0:
            P_1_stego = P_1_stego + np.power(2, n)
            P_2_stego = P_2_stego + np.power(2, n)
        elif P_1_stego > 255 or P_2_stego > 255:
            P_1_stego = P_1_stego - np.power(2, n)
            P_2_stego = P_2_stego - np.power(2, n)

        return P_1_stego, P_2_stego, index

    def __get_hidded_bits_type_1__(self, P_1, P_2):
        d = np.abs(P_1 - P_2)
        n, R = self.__calculate_capacity__(d)
        if R == 1:
            rem_1 = np.mod(P_1, 4)
            rem_2 = np.mod(P_2, 4)
        elif R == 2:
            rem_1 = np.mod(P_1, 8)
            rem_2 = np.mod(P_2, 8)
        else:
            rem_1 = np.mod(P_1, 16)
            rem_2 = np.mod(P_2, 16)
        
        rem_1_bit = bin(rem_1)[2:]
        rem_1_bit = '0' * (8 - len(rem_1_bit)) + rem_1_bit
        rem_2_bit = bin(rem_2)[2:]
        rem_2_bit = '0' * (8 - len(rem_2_bit)) + rem_2_bit

        return rem_1_bit[-n:] + rem_2_bit[-n:]

    def __get_hidded_bits_type_2__(self, P_1, P_2):
        d = np.abs(P_1 - P_2)
        n, R = self.__calculate_capacity__(d)
        if R == 1:
            rem_1 = np.mod(P_1, 8)
            rem_2 = np.mod(P_2, 8)
        else:
            rem_1 = np.mod(P_1, 16)
            rem_2 = np.mod(P_2, 16)
        
        rem_1_bit = bin(rem_1)[2:]
        rem_1_bit = '0' * (8 - len(rem_1_bit)) + rem_1_bit
        rem_2_bit = bin(rem_2)[2:]
        rem_2_bit = '0' * (8 - len(rem_2_bit)) + rem_2_bit

        return rem_1_bit[-n:] + rem_2_bit[-n:]