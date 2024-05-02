import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.chain_LSB import chain_LSB
import util

class Test_chain_LSB(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_chain_LSB_secret_1(self):
        alg = chain_LSB(k=0, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_chain_LSB_secret_1_large_end_msg(self):
        alg = chain_LSB(k=0, end_msg="r$1BlaFft^5fasdSDOda.")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_chain_LSB_secret_2(self):
        alg = chain_LSB(k=0, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_chain_LSB_secret_2_k_10(self):
        alg = chain_LSB(k=10, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_chain_LSB_secret_3(self):
        alg = chain_LSB(k=0, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_chain_LSB_secret_4_message_too_large(self):
        alg = chain_LSB(k=0, end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

if __name__ == '__main__':
    unittest.main()