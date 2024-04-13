from algorithms.sample import sample
from algorithms.LSB import LSB
import util

# define object and run it  in the provided sample
def example1():
    lsb = LSB()
    lsb.encode(util.get_carrier_color(2), util.get_secret_msg(1))
    lsb.decode()

# define multiple objects and run them in the provided sample
def example2():
    algorithms = [sample(), sample()]
    for algorithm in algorithms:
        algorithm.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        algorithm.decode()

# define multiple objects and run them in the specified sample range
def example3():
    algorithms = [sample(), sample()]
    for algorithm in algorithms:
        for i in range(1,4):
            algorithm.encode(util.get_carrier_color(i), util.get_secret_msg(i))
            algorithm.decode()

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    
    example2()