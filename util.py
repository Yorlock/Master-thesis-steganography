from pathlib import Path
import os
import glob

def init_instance():
    global result_dir_path
    result_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results")
    Path(result_dir_path).mkdir(parents=True, exist_ok=True)
    sample_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "samples")
    global carrier_color_dir_path
    carrier_color_dir_path = os.path.join(sample_dir_path, "carrier")
    global secret_msg_dir_path
    secret_msg_dir_path = os.path.join(sample_dir_path, "secret")
    global carrier_test_color_dir_path
    carrier_test_color_dir_path = os.path.join(sample_dir_path, "carrier_test")
    global secret_test_msg_dir_path
    secret_test_msg_dir_path = os.path.join(sample_dir_path, "secret_test")

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

def get_secret_msg(sample_number):
    return os.path.join(secret_msg_dir_path, rf"sample{str(sample_number)}.txt")

def get_carrier_test_color(sample_number):
    return os.path.join(carrier_test_color_dir_path, rf"sample{str(sample_number)}.png")

def get_secret_test_msg(sample_number):
    return os.path.join(secret_test_msg_dir_path, rf"sample{str(sample_number)}.txt")

def get_algorithm_path_dir(self):
    class_name = type(self).__name__
    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    number_files = len(glob.glob(destination_path + rf'\algorithm*')) + 1
    dirname = rf'algorithm{number_files}'
    destination_path = os.path.join(destination_path, dirname)
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    return destination_path

def get_encode_path(self):
    if self.algorithm_path_dir == '':
        raise Exception('No stego image path')

    destination_path = os.path.join(self.algorithm_path_dir, rf"stego{self.stego_extension}")
    return destination_path

def get_decode_path(self):
    if self.algorithm_path_dir == '':
        raise Exception('No stego image path')

    destination_path = os.path.join(self.algorithm_path_dir, rf"message{self.msg_extension}")
    return destination_path

def get_metadata_path(self):
    if self.algorithm_path_dir == '':
        raise Exception('No stego image path')
    
    destination_path = os.path.join(self.algorithm_path_dir, rf"metadata.json")
    return destination_path

def check_error(self):
    if self.algorithm_path_dir == '':
        raise Exception('No stego image path')
    
    class_name = type(self).__name__
    print(rf"{class_name}: {self.is_success}")
    if self.error_msg != "":
        print(rf"{class_name}: {self.error_msg}")