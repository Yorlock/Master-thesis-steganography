from abc import ABC, abstractmethod

class steganographyAlgorythm(ABC):

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
    
    @abstractmethod
    def encode(self, img, msg):
        pass

    @abstractmethod
    def decode(self):
        pass