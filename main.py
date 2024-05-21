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
    log_file = open("log.txt", "w")
    algorithms_list = []
    algorithms_list.append([BF()])
    algorithms_list.append([BPCS()])
    #algorithms_list.append([chain_LSB()])
    algorithms_list.append([LSB_EOM()])
    algorithms_list.append([LSB_PF()])
    algorithms_list.append([LSB_SINE()])
    algorithms_list.append([LSB_SOM()]) 
    algorithms_list.append([n_RMBR()])
    algorithms_list.append([PVD_8D()])
    algorithms_list.append([PVDMF()])
    algorithms_list.append([QVD_8D()])

    metrics_calculator = metrics.metrics_calculator()
    for algorithms in algorithms_list:
        for algorithm in algorithms:
            for i in range(1,2):
                try:
                    algorithm.encode(util.get_carrier_test_color(i), util.get_secret_test_msg(i))
                    algorithm.decode(pipe=None)

                    if not filecmp.cmp(util.get_secret_test_msg(i), algorithm.destination_path):
                        log_file.write(f"WARNING: {algorithm.json_content}, {util.get_carrier_test_color(i)}, {util.get_secret_test_msg(i)}, Decoded message is different from the original one\n")
                        print(f"{algorithm.json_content}, i={i}: Decoded message is different from the original one")
                    else:
                        metrics_calculator.setup(algorithm, util.get_carrier_test_color(i), util.get_secret_test_msg(i))
                        metrics_calculator.run()
                        log_file.write(f"SUCCESS: {algorithm.json_content}, {util.get_carrier_test_color(i)}, {util.get_secret_test_msg(i)}\n")
                
                except:
                    log_file.write(f"ERROR: {algorithm.json_content}, {util.get_carrier_test_color(i)}, {util.get_secret_test_msg(i)}\n")
                    print(f"{algorithm.json_content}: Something went wrong")
    log_file.close()
    #metrics_calculator.binning()

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    #util.clean_all()

    master_test()