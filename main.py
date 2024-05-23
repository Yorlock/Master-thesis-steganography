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
from pathlib import Path
import datetime
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
    Path("tmp").mkdir(parents=True, exist_ok=True)
    destroyed_image_path = "tmp/damaged_stego.png"
    result_file_path = "tmp/results.txt"
    result_ranked_file_path = "tmp/results_ranked.txt"
    log_file_path = "tmp/log.txt"

    sets_img_msg = [(i, j) for i in range(1, 11) for j in range(1, 6)]       #i:1-11      j:1-6

    algorithms_list = []
    algorithms_list.append([BF(type=1, color=""), BF(type=2, color=""),BF(type=1, color="R"), BF(type=2, color="R"), BF(type=1, color="G"), BF(type=2, color="G"), BF(type=1, color="B"), BF(type=2, color="B")])
    algorithms_list.append([BPCS()])
    algorithms_list.append([chain_LSB(), chain_LSB(k=1000), chain_LSB(k=2000)])
    algorithms_list.append([LSB_EOM(k=1), LSB_EOM(k=2), LSB_EOM(k=3), LSB_EOM(k=4), LSB_EOM(k=5)])
    algorithms_list.append([LSB_PF(password="12345", color="R"), LSB_PF(password="12345", color="G"), LSB_PF(password="12345", color="B"), LSB_PF(password="ABCDE", color="R"), LSB_PF(password="ABCDE", color="G"), LSB_PF(password="ABCDE", color="B")])
    algorithms_list.append([LSB_SINE(round_accuracy=1, sine_phase=1.0), LSB_SINE(round_accuracy=2, sine_phase=1.0), LSB_SINE(round_accuracy=3, sine_phase=1.0), LSB_SINE(round_accuracy=1, sine_phase=0.0), LSB_SINE(round_accuracy=2, sine_phase=0.0), LSB_SINE(round_accuracy=3, sine_phase=0.0), LSB_SINE(round_accuracy=1, sine_phase=-1.0), LSB_SINE(round_accuracy=2, sine_phase=-1.0), LSB_SINE(round_accuracy=3, sine_phase=-1.0)])
    algorithms_list.append([LSB_SOM(k=1), LSB_SOM(k=2), LSB_SOM(k=3), LSB_SOM(k=4), LSB_SOM(k=5)]) 
    algorithms_list.append([n_RMBR(color="", n=1), n_RMBR(color="", n=2), n_RMBR(color="", n=3), n_RMBR(color="", n=4), n_RMBR(color="R", n=1), n_RMBR(color="R", n=2), n_RMBR(color="R", n=3), n_RMBR(color="R", n=4), n_RMBR(color="G", n=1), n_RMBR(color="G", n=2), n_RMBR(color="G", n=3), n_RMBR(color="G", n=4), n_RMBR(color="B", n=1), n_RMBR(color="B", n=2), n_RMBR(color="B", n=3), n_RMBR(color="", n=4)])
    algorithms_list.append([PVD_8D(color="", type=1), PVD_8D(color="", type=2), PVD_8D(color="R", type=1), PVD_8D(color="R", type=2), PVD_8D(color="G", type=1), PVD_8D(color="G", type=2), PVD_8D(color="B", type=1), PVD_8D(color="B", type=2)])
    algorithms_list.append([PVDMF(color="", type=1), PVDMF(color="", type=2), PVDMF(color="R", type=1), PVDMF(color="R", type=2), PVDMF(color="G", type=1), PVDMF(color="G", type=2), PVDMF(color="B", type=1), PVDMF(color="B", type=2)])
    algorithms_list.append([QVD_8D(color="", type=1, k=3), QVD_8D(color="R", type=1, k=3), QVD_8D(color="G", type=1, k=3), QVD_8D(color="B", type=1, k=3), QVD_8D(color="", type=3, k=4), QVD_8D(color="R", type=3, k=4), QVD_8D(color="G", type=3, k=4), QVD_8D(color="B", type=3, k=4)])

    log_file = open(log_file_path, "w")
    metrics_calculator = metrics.metrics_calculator(log_file, destroyed_image_path, result_file_path, result_ranked_file_path)
    for algorithms in algorithms_list:
        for algorithm in algorithms:
            for i, j in sets_img_msg:
                img_path = util.get_carrier_test_color(i)
                msg_path = util.get_secret_test_msg(j)

                log_file.write(f"{datetime.datetime.now()} {algorithm.json_content}, {img_path}, {msg_path}\n")
                print(f"{datetime.datetime.now()} {algorithm.json_content}, {img_path}, {msg_path}")
                try:
                    algorithm.encode(img_path, msg_path)
                    log_file.write(f"{datetime.datetime.now()} FINISHED: Encode\n")
                    print(f"{datetime.datetime.now()} FINISHED: Encode")
                    algorithm.decode(pipe=None)
                    log_file.write(f"{datetime.datetime.now()} FINISHED: Decode\n")
                    print(f"{datetime.datetime.now()} FINISHED: Decode")

                    if not filecmp.cmp(msg_path, algorithm.destination_path):
                        log_file.write(f"{datetime.datetime.now()} ERROR: decoded message is different from the original one\n")
                        print(f"{datetime.datetime.now()} ERROR: Decoded message is different from the original one")
                    else:
                        metrics_calculator.setup(algorithm, img_path, msg_path)
                        metrics_calculator.run()
                        log_file.write(f"{datetime.datetime.now()} SUCCESS\n")
                        print(f"{datetime.datetime.now()} SUCCESS")
                
                except Exception as e:
                    log_file.write(f"{datetime.datetime.now()} ERROR: {e}\n")
                    print(f"{datetime.datetime.now()} ERROR: {e}")
                
                log_file.write("\n")
                print("")
    
    try:
        #metrics_calculator.binning()
        log_file.write(f"{datetime.datetime.now()} SUCCESS: Binning\n")
        print(f"{datetime.datetime.now()} SUCCESS: Binning")
    except Exception as e:
        log_file.write(f"{datetime.datetime.now()} ERROR: Binning, {e}\n")
        print(f"{datetime.datetime.now()} ERROR: Binning, {e}")

    log_file.close()

if __name__ == '__main__':
    util.init_instance()
    util.clean_result()
    util.clean_all()

    #master_test()