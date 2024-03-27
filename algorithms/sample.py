from math import floor
from skimage import io

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import algorithms.util as util

class sample(steganographyAlgorythm):
    def __init__(self):
        self.stego_img_path = ""
        self.msg_b_len = 0

    def encode(self, img, msg):
        msg_b = self.__text_to_bites(msg)
        stego_img = self.__hide_text(img, msg_b)
        self.stego_img_path = util.save_encode(self, stego_img)

    def decode(self):
        found_text = self.__find_text(self.stego_img_path)
        plain_text = self.__bites_to_text(found_text)
        util.save_decode(self, plain_text)

    def __text_to_bites(self, fileName):
        file = open(fileName,'r')
        dataText = file.read()
        dataTextToBites = ''.join(format(ord(i), '08b') for i in str(dataText))
        return dataTextToBites

    def __hide_text(self, img_path, msg_b):
        self.msg_b_len = len(msg_b)

        img = io.imread(img_path)
        h, w, _ = img.shape
        maxSizeOfSecretText = int(floor(h * w * 3))
        if self.msg_b_len > maxSizeOfSecretText:
            print(f"Text is too large {msg_b}. Max size is {maxSizeOfSecretText}. Cutting text")
            secretText = secretText[:maxSizeOfSecretText]

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

    def __find_text(self, img_path):
        img = io.imread(img_path)
        h, w, _ = img.shape
        foundTextInBin = self.__find_text_in_img(img, h, w)
        return bytes(foundTextInBin, 'utf-8')

    def __bites_to_text(self, bit_text):
        plaintext = ""
        for i in range(0, len(bit_text), 8):
            binary = bit_text[i:i+8]
            ascii = int(binary, 2)
            plaintext += chr(ascii)
        return plaintext

    def __find_text_in_img(self, img, h, w):
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