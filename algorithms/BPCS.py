from PIL import Image
import numpy as np
import bpcs

from algorithms.steganographyAlgorythm import steganographyAlgorythm
import util

class BPCS(steganographyAlgorythm):
    def __init__(self, alpha=0.45, save_bitplates=False):
        self.stego_img_path = ""
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.alpha = alpha
        self.save_bitplates = save_bitplates
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

    def reset_params(self):
        self.is_success = False
        self.error_msg = ""

    def encode(self, img_path, msg_path):
        self.stego_img_path = util.get_encode_path(self)
        bitplatedir=''
        if self.save_bitplates:
            bitplatedir = util.get_encode_path_dir(self)

        bpcs.encode(img_path, msg_path, self.stego_img_path, self.alpha, outbitplatedir=bitplatedir)
        self.is_success = True

    def decode(self):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return
        
        self.reset_params()
        destination_path = util.get_decode_path(self)
        bpcs.decode(self.stego_img_path, destination_path, self.alpha)
        self.is_success = True