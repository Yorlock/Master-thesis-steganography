from algorithms.sample import sample
import algorithms.util as util

import os

if __name__ == '__main__':
    util.init_instance(__file__)
    util.clean_result()
    lsb = sample()
    lsb.encode(os.path.join(util.sample_dir_path, 'carrier\color-images\sample2.png'), os.path.join(util.sample_dir_path, 'secret\messages\sample1.txt'))
    lsb.decode()