from algorithms.LSB_EOM import LSB_EOM
from algorithms.LSB_SOM import LSB_SOM
from algorithms.LSB_PF import LSB_PF
from algorithms.QVD_8D import QVD_8D
from algorithms.PVD_8D import PVD_8D
from algorithms.LSB_SINE import LSB_SINE
from algorithms.BPCS import BPCS
from algorithms.chain_LSB import chain_LSB
from algorithms.n_RMBR import n_RMBR
from algorithms.PVDMF import PVDMF
from algorithms.BF import BF
import util
import metrics
import json
import filecmp

# define object and run it  in the provided sample
def example1():
    lsb = BF(type=1, color="", save_metadata=True)
    lsb.encode(util.get_carrier_color(1), util.get_secret_msg(0))
    util.check_error(lsb)
    lsb.decode()
    util.check_error(lsb)

    f = open(lsb.metadata_path, "r")
    data = json.load(f)
    f.close()
    print(data['milli_sec_elapsed_encode'])
    print(data['settings']['type'])
    print(data['settings'])

# define multiple objects and run them in the provided sample
def example2():
    algorithms = [LSB_EOM(end_msg="G$:+.3", k=1), LSB_SOM(k=1), chain_LSB()]

    metrics_calculator = metrics.metrics_calculator()
    for algorithm in algorithms:
        algorithm.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        util.check_error(algorithm)
        algorithm.decode()
        util.check_error(algorithm)
        metrics_calculator.setup(algorithm, util.get_carrier_color(2), util.get_secret_msg(1))
        metrics_calculator.run()

# define multiple objects and run them in the specified sample range
def example3():
    algorithms = [LSB_EOM(end_msg="G$:+.3"), LSB_SOM(), BPCS(alpha=0.45)]
    for algorithm in algorithms:
        for i in range(1,5):
            algorithm.encode(util.get_carrier_color(i), util.get_secret_msg(i))
            util.check_error(algorithm)
            algorithm.decode()
            util.check_error(algorithm)

def master_test():
    algorithms_list = []
    algorithms_list.append([LSB_EOM(end_msg="G$:+.3", k=1), LSB_EOM(k=2), LSB_EOM(k=3)])
    algorithms_list.append([LSB_SOM(k=1), LSB_SOM(k=2), LSB_SOM(k=3)])
    algorithms_list.append([LSB_PF(color='R'), LSB_PF(color='G'), LSB_PF(color='B')])

    metrics_calculator = metrics.metrics_calculator()
    for algorithms in algorithms_list:
        for algorithm in algorithms:
            for i in range(1,5):
                try:
                    algorithm.encode(util.get_carrier_test_color(i), util.get_secret_test_msg(i))
                    util.check_error(algorithm)
                    algorithm.decode()

                    if filecmp.cmp(util.get_secret_test_msg(i), algorithm.destination_path):
                        print("Decoded msg is different from the original one")
                        raise Exception()

                    util.check_error(algorithm)
                    metrics_calculator.setup(algorithm, util.get_carrier_test_color(i), util.get_secret_test_msg(i))
                    metrics_calculator.run()
                
                except:
                    #add log file
                    print("Something went wrong")

    #metrics_calculator.binarize()

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    #util.clean_all()

    master_test()