from abc import ABC, abstractmethod

class steganographyAlgorithm(ABC):

    @property
    def is_success(self):
        pass
    
    @is_success.setter
    def is_success(self, value):
        pass

    @property
    def error_msg(self):
        pass
    
    @error_msg.setter
    def error_msg(self, value):
        pass

    @property
    def msg_extension(self):
        pass
    
    @msg_extension.setter
    def msg_extension(self, value):
        pass

    @property
    def stego_extension(self):
        pass
    
    @stego_extension.setter
    def stego_extension(self, value):
        pass
    
    @property
    def stego_img_path(self):
        pass
    
    @stego_img_path.setter
    def stego_img_path(self, value):
        pass

    @property
    def destination_path(self):
        pass
    
    @destination_path.setter
    def destination_path(self, value):
        pass

    @property
    def algorithm_path_dir(self):
        pass
    
    @algorithm_path_dir.setter
    def algorithm_path_dir(self, value):
        pass

    @property
    def metadata_path(self):
        pass
    
    @metadata_path.setter
    def metadata_path(self, value):
        pass

    @property
    def json_content(self):
        pass
    
    @json_content.setter
    def json_content(self, value):
        pass

    @abstractmethod
    def reset_params(self):
        pass

    @abstractmethod
    def encode(self, img, msg):
        pass

    @abstractmethod
    def decode(self):
        pass