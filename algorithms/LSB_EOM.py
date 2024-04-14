from PIL import Image
import numpy as np

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class LSB_EOM(steganographyAlgorythm):
    def __init__(self, end_msg="$t3g0"):
        self.stego_img_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.error_msg = ""
        self.end_msg = end_msg

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
        req_bits = len(b_message)

        if req_bits > total_pixels * 3:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size."
            return
        else:
            index=0
            for p in range(total_pixels):
                for q in range(0, 3):
                    if index < req_bits:
                        new_value = (array[p][q] & 254) + int(b_message[index])
                        array[p][q] = new_value
                        index += 1

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

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(0, 3):
                hidden_bits += str(array[p][q] % 2)

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