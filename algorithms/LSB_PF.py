from PIL import Image
from util import AESCipher
import numpy as np
import math
import base64

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class LSB_PF(steganographyAlgorythm):
    def __init__(self, password='12345', color='B', end_msg="$t3g0"):
        self.stego_img_path = ""
        self.destination_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.password = password
        self.colors = ['R', 'G', 'B']
        self.end_msg = end_msg
        if color in self.colors:
            self.color = color

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

        cipher = AESCipher(self.password)
        message = cipher.encrypt(message)
        message += base64.b64encode(str.encode(self.end_msg))
        b_message = ''.join(format(byte, '08b') for byte in message)
        req_bits = len(b_message)
        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4

        total_pixels = array.size//n
        available_bits, pixels_index  = self.__get_MSB_filter__(array, total_pixels)

        if req_bits > available_bits:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return
        
        password_bits = ''.join([format(ord(i), "08b") for i in self.password])
        password_blocks = [int(password_bits[i:i+3], 2) for i in range(0, len(password_bits), 3)]
        blocks_len = len(password_blocks)

        change_color = self.colors.index(self.color)
        index_block = 0
        index_pixel = 0
        for bit in b_message:
            block = password_blocks[index_block % blocks_len]
            index_block += 1
            while total_pixels > index_pixel:
                if pixels_index[index_pixel]:
                    if block == 0: # we cannot do XOR on bit and then modify that bit -> wrong result
                        new_value = int(bit)
                    else:
                        block_value = util.get_bit_value(array[index_pixel][change_color], block)
                        new_value = (block_value ^ int(bit))
                    
                    array[index_pixel][change_color] = (array[index_pixel][change_color] & 254) + new_value
                    index_pixel += 1
                    break
                index_pixel += 1

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
        _, pixels_index  = self.__get_MSB_filter__(array, total_pixels)
        password_bits = ''.join([format(ord(i), "08b") for i in self.password])
        password_blocks = [int(password_bits[i:i+3], 2) for i in range(0, len(password_bits), 3)]
        blocks_len = len(password_blocks)

        hidden_bits = ""
        index_block = 0
        index_pixel = 0
        change_color = self.colors.index(self.color)
        for p in range(total_pixels):
            block = password_blocks[index_block % blocks_len]
            index_block += 1
            while total_pixels > index_pixel:
                if pixels_index[index_pixel]:
                    hide_value = util.get_bit_value(array[index_pixel][change_color], block)
                    if block == 0:
                        hidden_bits += str(hide_value)
                    else:
                        LSB_value = util.get_bit_value(array[index_pixel][change_color], 0)
                        if LSB_value == 1:
                            hidden_bits += str(self.__reverse_value__(hide_value))
                        else:
                            hidden_bits += str(hide_value)

                    index_pixel += 1
                    break
                index_pixel += 1

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
        enc_message = ""
        end_msg_base64 = base64.b64encode(str.encode(self.end_msg)).decode("utf-8")
        for i in range(len(hidden_bits)):
            if enc_message[-len(end_msg_base64):] == end_msg_base64:
                break
            else:
                enc_message += chr(int(hidden_bits[i], 2))

        if end_msg_base64 not in enc_message:
            self.is_success = False
            self.error_msg = "No Hidden Message Found\n"
            return
        
        cipher = AESCipher(self.password)
        message = cipher.decrypt(enc_message[:-len(end_msg_base64)])

        self.destination_path = util.get_decode_path(self)
        destination_file = open(self.destination_path, "w")
        destination_file.write(message)
        destination_file.close()

        self.is_success = True

    def __get_MSB_filter__(self, array, total_pixels):
        colors = [0, 0, 0] #red green blue
        colors_pixels_index = [[], [], []] # red green blue; true = MSB is 1, false = MSB is 0
        bit = 7
        for p in range(total_pixels):
            red = util.get_bit_value(array[p][0], bit)
            green = util.get_bit_value(array[p][1], bit)
            blue = util.get_bit_value(array[p][2], bit)
            colors[0] += red
            colors[1] += green
            colors[2] += blue
            colors_pixels_index[0].append(red == 1)
            colors_pixels_index[1].append(green == 1)
            colors_pixels_index[2].append(blue == 1)

        MSB_filter = colors.index(max(colors))
        return colors[MSB_filter], colors_pixels_index[MSB_filter]
    
    def __reverse_value__(self, value):
        if value == 1:
            return '0'
        return '1'