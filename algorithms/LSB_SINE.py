from PIL import Image
import numpy as np
import math
import os

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class LSB_SINE(steganographyAlgorythm):
    def __init__(self, end_msg="$t3g0", round_accuracy=2, sine_phase=1.0, save_sineimage=False):
        self.stego_img_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.end_msg = end_msg
        self.save_sineimage = save_sineimage
        if not isinstance(round_accuracy, int):
            self.round_accuracy = 2
            self.error_msg += "Parameter round_accuracy was set to 2."
        elif round_accuracy < 1 or round_accuracy > 10:
            self.round_accuracy = 2
            self.error_msg += "Parameter round_accuracy was set to 2."
        else:
            self.round_accuracy = round_accuracy
        
        if not isinstance(sine_phase, float):
            self.sine_value = 1.0
            self.error_msg += "Parameter sine_value was set to 1.0."
        elif sine_phase > 1.0 or sine_phase < -1.0:
            self.sine_value = 1.0
            self.error_msg += "Parameter sine_value was set to 1.0."
        else:
            self.sine_value = sine_phase

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
        self.stego_img_path = util.get_encode_path(self)
        enc_img.save(self.stego_img_path)

        if self.save_sineimage:
            file_name = "sineimage.png"
            save_sineimagedir = util.get_encode_path_dir(self)
            available_pixels_list
            sine_array = np.array(list(img.getdata()))
            sine_array[:, 0:3] = 0
            for pixel_index in  available_pixels_list:
                sine_array[pixel_index, 0] = 255

            sine_array=sine_array.reshape(h, w, n)
            sine_image = Image.fromarray(sine_array.astype('uint8'), img.mode)
            sine_image.save(os.path.join(save_sineimagedir, file_name))

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
        pixel_index = 0
        for pixel_index in range(total_pixels):
            j = math.sin((pixel_index * 2 * math.pi / w + 1) * (h - 1) / 2)
            if round(j, self.round_accuracy) != self.sine_value:
                continue

            for color in range(3):
                color_MSB_3 = self.__get_MSB_3__(array[pixel_index][color])
                BIT_index = 0
                if color_MSB_3 == '000':
                    BIT_index = 1

                hidden_bits += str(util.get_bit_value(array[pixel_index][color], BIT_index))

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            if message[-len(self.end_msg):] == self.end_msg:
                break
            else:
                message += chr(int(hidden_bits[i], 2))

        if self.end_msg not in message:
            self.is_success = False
            self.error_msg = "No Hidden Message Found\n"
            return
        
        destination_path = util.get_decode_path(self)
        destination_file = open(destination_path, "w")
        destination_file.write(message[:-len(self.end_msg)])
        destination_file.close()

        self.is_success = True
    
    def __get_MSB_3__(self, number):
        bit_8 = util.get_bit_value(number, 7)
        bit_7 = util.get_bit_value(number, 6)
        bit_6 = util.get_bit_value(number, 5)
        return rf"{bit_8}{bit_7}{bit_6}"
    
    def __calculate_available_bits__(self, total_pixels, req_bits, w, h):
        pixel_index = 0
        available_bits = 0
        available_pixels_list = []
        for pixel_index in range(total_pixels):
            j = math.sin((pixel_index * 2 * math.pi / w + 1) * (h - 1) / 2)
            if round(j, self.round_accuracy) != self.sine_value:
                pixel_index += 1
                continue

            available_bits += 3
            available_pixels_list.append(pixel_index)
            if req_bits <= available_bits:
                return available_bits, available_pixels_list

        return available_bits, available_pixels_list