from PIL import Image
import numpy as np
import bpcs
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class BPCS(steganographyAlgorithm):
    def __init__(self, alpha=0.45, calculate_metrics=False):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.algorithm_path_dir = util.get_algorithm_path_dir(self)
        self.stego_img_path = util.get_encode_path(self)
        self.destination_path = util.get_decode_path(self)
        self.metrics_path = util.get_metrics_path(self)
        self.alpha = alpha
        self.is_success = False
        self.error_msg = ""
        self.calculate_metrics = calculate_metrics
        self.json_content = {}

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
        bitplatedir=''
        if self.calculate_metrics:
            bitplatedir = self.algorithm_path_dir

        bpcs.encode(img_path, msg_path, self.stego_img_path, self.alpha, outbitplatedir=bitplatedir)
        self.is_success = True

    def decode(self):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return
        
        self.reset_params()
        bpcs.decode(self.stego_img_path, self.destination_path, self.alpha)
        self.is_success = True