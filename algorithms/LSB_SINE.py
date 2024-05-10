from PIL import Image
import numpy as np
import math
import os
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class LSB_SINE(steganographyAlgorithm):
    def __init__(self, end_msg="$t3g0", round_accuracy=2, sine_phase=1.0, calculate_metrics=False):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.algorithm_path_dir = util.get_algorithm_path_dir(self)
        self.stego_img_path = util.get_encode_path(self)
        self.destination_path = util.get_decode_path(self)
        self.metrics_path = util.get_metrics_path(self)
        self.is_success = False
        self.error_msg = ""
        self.end_msg = end_msg
        if not isinstance(round_accuracy, int):
            self.round_accuracy = 2
            self.error_msg += "Parameter round_accuracy was set to 2."
        elif round_accuracy < 1 or round_accuracy > 10:
            self.round_accuracy = 2
            self.error_msg += "Parameter round_accuracy was set to 2."
        else:
            self.round_accuracy = round_accuracy
        
        if not isinstance(sine_phase, float):
            self.sine_phase = 1.0
            self.error_msg += "Parameter sine_phase was set to 1.0."
        elif sine_phase > 1.0 or sine_phase < -1.0:
            self.sine_phase = 1.0
            self.error_msg += "Parameter sine_phase was set to 1.0."
        else:
            self.sine_phase = sine_phase
        
        self.calculate_metrics = calculate_metrics
        self.json_content = {"algorythm":"LSB_SINE", "settings": {"round_accuracy":self.round_accuracy, "sine_phase":self.sine_phase ,"end_msg":self.end_msg}}

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
        w, h = img.size
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
        req_bits = len(b_message)
        available_bits, available_pixels_list = self.__calculate_available_bits__(total_pixels, req_bits, w, h)
        if req_bits > available_bits:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return

        bit_embedded = 0
        pixel_index = 0
        for pixel_index in available_pixels_list:
            for color in range(3):
                if req_bits <= bit_embedded:
                    break

                color_MSB_3 = self.__get_MSB_3__(array[pixel_index][color])
                bit_position = 0
                if color_MSB_3 == '000':
                    bit_position = 1

                bit_value = b_message[bit_embedded]
                bits_array = bin(array[pixel_index][color])[2:]
                bits_array = '0' * (8 - len(bits_array)) + bits_array
                bit_set_position = len(bits_array) - bit_position - 1
                bits_array = bits_array[:bit_set_position] + bit_value + bits_array[bit_set_position + 1:]
                array[pixel_index][color] = int(bits_array, 2)
                bit_embedded += 1

        array=array.reshape(h, w, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(self.stego_img_path)
        if self.calculate_metrics:
            file_name = "sineimage.png"
            available_pixels_list
            sine_array = np.array(list(img.getdata()))
            sine_array[:, 0:3] = 0
            for pixel_index in  available_pixels_list:
                sine_array[pixel_index, 0] = 255

            sine_array=sine_array.reshape(h, w, n)
            sine_image = Image.fromarray(sine_array.astype('uint8'), img.mode)
            sine_image.save(os.path.join(self.algorithm_path_dir, file_name))

        self.is_success = True

    def decode(self):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return

        self.reset_params()
        img = Image.open(self.stego_img_path, 'r')
        w, h = img.size
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size//n
        hidden_bits = ""
        message = ""
        block_bits = ""
        left_bits = ""
        pixel_index = 0
        is_end = False
        for pixel_index in range(total_pixels):
            if is_end:
                break

            j = math.sin((pixel_index * 2 * math.pi / w + 1) * (h - 1) / 2)
            if round(j, self.round_accuracy) != self.sine_phase:
                continue
            
            block_bits = left_bits
            for color in range(3):
                color_MSB_3 = self.__get_MSB_3__(array[pixel_index][color])
                BIT_index = 0
                if color_MSB_3 == '000':
                    BIT_index = 1

                block_bits += str(self.get_bit_value(array[pixel_index][color], BIT_index))

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

        with open(self.metrics_path, "w") as f:
            json.dump(self.json_content, f)

        destination_file = open(self.destination_path, "w")
        destination_file.write(message[:-len(self.end_msg)])
        destination_file.close()
        self.is_success = True
    
    def __get_MSB_3__(self, number):
        number_bit = bin(number)[2:]
        number_bit = '0' * (8 - len(number_bit)) + number_bit
        return number_bit[:3]
    
    def get_bit_value(self, number, n):
        # Create a mask with a 1 at the nth position
        mask = 1 << n

        # Perform bitwise AND operation with the number and mask
        # If the result is non-zero, the bit at position n is 1, otherwise, it's 0
        return (number & mask) >> n

    def __calculate_available_bits__(self, total_pixels, req_bits, w, h):
        pixel_index = 0
        available_bits = 0
        available_pixels_list = []
        for pixel_index in range(total_pixels):
            j = math.sin((pixel_index * 2 * math.pi / w + 1) * (h - 1) / 2)
            if round(j, self.round_accuracy) != self.sine_phase:
                pixel_index += 1
                continue

            available_bits += 3
            available_pixels_list.append(pixel_index)
            if req_bits <= available_bits:
                return available_bits, available_pixels_list

        return available_bits, available_pixels_list