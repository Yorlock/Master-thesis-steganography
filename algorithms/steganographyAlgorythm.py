from abc import ABC, abstractmethod

class steganographyAlgorythm(ABC):

    @abstractmethod
    def encode(self, img, msg):
        pass

    @abstractmethod
    def decode(self):
        pass