from skimage import io
from pathlib import Path
import os
import glob

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
            os.remove(file)

def clean_all():
    dirs = glob.glob(result_dir_path + '/*')
    for dir in dirs:
        files = glob.glob(dir + '/*')
        for file in files:
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

def get_decode_path(self):
    class_name = type(self).__name__

    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    
    number_files = len(glob.glob(destination_path + '\message*')) + 1
    destination_path = os.path.join(destination_path, rf"message{number_files}{self.msg_extension}")

    return destination_path