from skimage import io
from pathlib import Path
import os
import glob

def init_instance(file_path):
    global result_dir_path
    result_dir_path = os.path.join(os.path.dirname(os.path.realpath(file_path)), "results")
    Path(result_dir_path).mkdir(parents=True, exist_ok=True)

    global sample_dir_path
    sample_dir_path = os.path.join(os.path.dirname(os.path.realpath(file_path)), "samples")
    Path(sample_dir_path).mkdir(parents=True, exist_ok=True)

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

def save_encode(algorithm_class, img):
    class_name = type(algorithm_class).__name__

    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)

    number_files = len(glob.glob(destination_path + '\stego*')) + 1
    destination_path = os.path.join(destination_path, rf"stego{number_files}.png")

    io.imsave(destination_path, img)
    return destination_path

def save_decode(algorithm_class, msg):
    class_name = type(algorithm_class).__name__

    destination_path = os.path.join(result_dir_path, rf"{class_name}")
    Path(destination_path).mkdir(parents=True, exist_ok=True)

    number_files = len(glob.glob(destination_path + '\message*')) + 1

    if type(msg) == str:
        destination_path = os.path.join(destination_path, rf"message{number_files}.txt")
        destination_file = open(destination_path, "w")
        destination_file.write(msg)
        destination_file.close()
    else:
        destination_path = os.path.join(destination_path, rf"message{number_files}.png")
        io.imsave(destination_path, msg)

    return destination_path