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
        lsb = LSB_EOM(k=1)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), lsb.destination_path))

    def test_LSB_EOM_secret_1_k_1_large_end_msg(self):
        lsb = LSB_EOM(k=1, end_msg="r$1BlaOda.")
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), lsb.destination_path))

    def test_LSB_EOM_secret_1_k_2(self):
        lsb = LSB_EOM(k=2)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), lsb.destination_path))

    def test_LSB_EOM_secret_2_k_1(self):
        lsb = LSB_EOM(k=1)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(2))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), lsb.destination_path))

    def test_LSB_EOM_secret_2_k_3(self):
        lsb = LSB_EOM(k=3)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(2))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), lsb.destination_path))
    
    def test_LSB_EOM_secret_3_k_1(self):
        lsb = LSB_EOM(k=1)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(3))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), lsb.destination_path))

    def test_LSB_EOM_secret_4_k_1_message_too_large(self):
        lsb = LSB_EOM(k=1)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(4))
        self.assertFalse(lsb.is_success)

    def test_LSB_EOM_secret_4_k_5(self):
        lsb = LSB_EOM(k=5)
        lsb.encode(util.get_carrier_color(1), util.get_secret_msg(3))
        self.assertTrue(lsb.is_success)
        lsb.decode()
        self.assertTrue(lsb.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), lsb.destination_path))

if __name__ == '__main__':
    unittest.main()