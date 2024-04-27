from math import floor
from skimage import io

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class sample(steganographyAlgorythm):

    def __init__(self):
        self.stego_img_path = ""
        self.destination_path = ""
        self.msg_b_len = 0
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""

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
        msg_b = self.__text_to_bits__(msg_path)
        stego_img = self.__hide_text__(img_path, msg_b)
        self.stego_img_path = util.get_encode_path(self)
        io.imsave(self.stego_img_path, stego_img)

        self.is_success = True

    def decode(self):
        self.reset_params()
        found_text = self.__find_text__(self.stego_img_path)
        plain_text = self.__bits_to_text__(found_text)
        
        self.destination_path = util.get_decode_path(self)
        destination_file = open(self.destination_path, "w")
        destination_file.write(plain_text)
        destination_file.close()

        self.is_success = True

    def __text_to_bits__(self, fileName):
        file = open(fileName,'r')
        dataText = file.read()
        dataTextToBits = ''.join(format(ord(i), '08b') for i in str(dataText))
        return dataTextToBits

    def __hide_text__(self, img_path, msg_b):
        img = io.imread(img_path)
        h, w, _ = img.shape
        maxSizeOfSecretText = int(floor(h * w * 3))
        if len(msg_b) > maxSizeOfSecretText:
            self.error_msg += f"Text is too large {self.msg_b_len}. Max size is {maxSizeOfSecretText}. Cutting text\n" 
            msg_b = msg_b[:maxSizeOfSecretText]

        self.msg_b_len = len(msg_b)
        index = 0
        for i in range(h):
            for j in range(w):
                for k in range(3):
                    if index < self.msg_b_len:
                        img[i][j][k] &= 254
                        img[i][j][k] += int(msg_b[index])
                        index += 1
                    else:
                        return img
        return img

    def __find_text__(self, img_path):
        img = io.imread(img_path)
        h, w, _ = img.shape
        foundTextInBin = self.__find_text_in_img__(img, h, w)
        return bytes(foundTextInBin, 'utf-8')

    def __bits_to_text__(self, bit_text):
        plaintext = ""
        for i in range(0, len(bit_text), 8):
            binary = bit_text[i:i+8]
            ascii = int(binary, 2)
            plaintext += chr(ascii)
        return plaintext

    def __find_text_in_img__(self, img, h, w):
        found = 0
        foundText = ''
        for i in range(h):
            for j in range(w):
                for k in range(3):
                    add = str(img[i][j][k] % 2)
                    foundText += add
                    found += 1
                    if found == self.msg_b_len:
                        return foundText