from pathlib import Path
import os
import glob
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

def init_instance():
    global result_dir_path
    result_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results")
    Path(result_dir_path).mkdir(parents=True, exist_ok=True)

    sample_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "samples")

    global carrier_color_dir_path
    carrier_color_dir_path = os.path.join(sample_dir_path, "carrier", "color-images")

    global carrier_mono_dir_path
    carrier_mono_dir_path = os.path.join(sample_dir_path, "carrier", "mono-images")

    global secret_color_dir_path
    secret_color_dir_path = os.path.join(sample_dir_path, "secret", "color-images")

    global secret_msg_dir_path
    secret_msg_dir_path = os.path.join(sample_dir_path, "secret", "messages")

    global secret_mono_dir_path
    secret_mono_dir_path = os.path.join(sample_dir_path, "secret", "color-images")

def clean_result():
    dirs = glob.glob(result_dir_path + '/*')
    for dir in dirs:
        files = glob.glob(dir + '/*')
        for file in files:
            if os.path.isdir(file):
                insidedir = glob.glob(file + '/*')
                for f in insidedir:
                    os.remove(f)
                os.rmdir(file)
            else:
                os.remove(file)

def clean_all():
    dirs = glob.glob(result_dir_path + '/*')
    for dir in dirs:
        files = glob.glob(dir + '/*')
        for file in files:
            if os.path.isdir(file):
                insidedir = glob.glob(file + '/*')
                for f in insidedir:
                    os.remove(f)
                os.rmdir(file)
            else:
                os.remove(file)
        os.rmdir(dir)

def get_carrier_color(sample_number):
    return os.path.join(carrier_color_dir_path, rf"sample{str(sample_number)}.png")

def get_carrier_mono(sample_number):
    return os.path.join(carrier_mono_dir_path, rf"sample{str(sample_number)}.png")

def get_secret_color(sample_number):
    return os.path.join(secret_color_dir_path, rf"sample{str(sample_number)}.png")

def get_secret_msg(sample_number):
    return os.path.join(secret_msg_dir_path, rf"sample{str(sample_number)}.txt")

def get_secret_mono(sample_number):
    return os.path.join(secret_mono_dir_path, rf"sample{str(sample_number)}.png")

def get_encode_path(self):
    class_name = type(self).__name__
    
    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)

    number_files = len(glob.glob(destination_path + '\stego*')) + 1
    destination_path = os.path.join(destination_path, rf"stego{number_files}{self.stego_extension}")

    return destination_path

def get_encode_path_dir(self):
    if self.stego_img_path == '':
        raise Exception('No stego image path')

    class_name = type(self).__name__
    dirname = os.path.splitext(self.stego_img_path)[0]
    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)

    destination_path = os.path.join(destination_path, dirname)

    return destination_path

def get_decode_path(self):
    class_name = type(self).__name__

    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    
    number_files = len(glob.glob(destination_path + '\message*')) + 1
    destination_path = os.path.join(destination_path, rf"message{number_files}{self.msg_extension}")

    return destination_path

def check_error(self):
    class_name = type(self).__name__
    print(rf"{class_name}: {self.is_success}")
    if self.error_msg != "":
        print(rf"{class_name}: {self.error_msg}")

def get_bit_value(number, n):
        # Create a mask with a 1 at the nth position
        mask = 1 << n

        # Perform bitwise AND operation with the number and mask
        # If the result is non-zero, the bit at position n is 1, otherwise, it's 0
        return (number & mask) >> n

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]