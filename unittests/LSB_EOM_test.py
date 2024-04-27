import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.LSB_EOM import LSB_EOM
import util

class Test_LSB_EOM(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_LSB_EOM_secret_1_k_1(self):
        alg = LSB_EOM(k=1, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_EOM_secret_1_k_1_large_end_msg(self):
        alg = LSB_EOM(k=1, end_msg="r$1BlaFft^5fasdSDOda.")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_EOM_secret_1_k_2(self):
        alg = LSB_EOM(k=2, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_EOM_secret_2_k_1(self):
        alg = LSB_EOM(k=1, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_EOM_secret_2_k_3(self):
        alg = LSB_EOM(k=3, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))
    
    def test_LSB_EOM_secret_3_k_1(self):
        alg = LSB_EOM(k=1, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_LSB_EOM_secret_4_k_1_message_too_large(self):
        alg = LSB_EOM(k=1, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

    def test_LSB_EOM_secret_4_k_5(self):
        alg = LSB_EOM(k=5, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

if __name__ == '__main__':
    unittest.main()