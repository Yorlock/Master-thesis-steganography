from algorithms.sample import sample
import util

import os

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    lsb = sample()
    lsb.encode(util.get_carrier_color(2), util.get_secret_msg(1))
    lsb.decode()