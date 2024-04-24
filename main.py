from algorithms.sample import sample
from algorithms.LSB_EOM import LSB_EOM
from algorithms.LSB_SOM import LSB_SOM
from algorithms.LSB_PF import LSB_PF
from algorithms.LSB_SINE import LSB_SINE
from algorithms.BPCS import BPCS
from algorithms.chain_LSB import chain_LSB
import util

# define object and run it  in the provided sample
def example1():
    lsb = chain_LSB()
    lsb.encode(util.get_carrier_color(2), util.get_secret_msg(2))
    util.check_error(lsb)
    lsb.decode()
    util.check_error(lsb)

# define multiple objects and run them in the provided sample
def example2():
    algorithms = [BPCS(alpha=0.45), LSB_EOM(end_msg="G$:+.3", k=1), LSB_SOM(k=1)]
    for algorithm in algorithms:
        algorithm.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        util.check_error(algorithm)
        algorithm.decode()
        util.check_error(algorithm)

# define multiple objects and run them in the specified sample range
def example3():
    algorithms = [LSB_EOM(end_msg="G$:+.3"), LSB_SOM(), BPCS(alpha=0.45)]
    for algorithm in algorithms:
        for i in range(1,5):
            algorithm.encode(util.get_carrier_color(i), util.get_secret_msg(i))
            util.check_error(algorithm)
            algorithm.decode()
            util.check_error(algorithm)

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    #util.clean_all()

    example1()