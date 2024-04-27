import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.LSB_SINE import LSB_SINE
import util

class Test_LSB_SINE(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_LSB_SINE_secret_1(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=2, sine_phase=1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_SINE_secret_1_accuracy_4(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=4, sine_phase=1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_SINE_secret_2_message_too_large(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=2, sine_phase=1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertFalse(alg.is_success)

    def test_LSB_SINE_secret_2_accuracy_1(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=1, sine_phase=1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_SINE_secret_2__accuracy_1_phase_0(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=1, sine_phase=0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_SINE_secret_2_accuracy_1_phase_minus_1(self):
        alg = LSB_SINE(end_msg="$t3g0", round_accuracy=1, sine_phase=-1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_SINE_secret_2_large_end_msg_accuracy_1(self):
        alg = LSB_SINE( end_msg="r$1BlaFft^5fasdSDOda.", round_accuracy=1, sine_phase=1.0)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

if __name__ == '__main__':
    unittest.main()