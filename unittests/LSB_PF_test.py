import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.LSB_PF import LSB_PF
import util

class Test_LSB_PF(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_LSB_PF_secret_1(self):
        alg = LSB_PF(password='12345', color='B', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_PF_secret_1_color_R(self):
        alg = LSB_PF(password='12345', color='R', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_PF_secret_1_color_G(self):
        alg = LSB_PF(password='12345', color='G', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_LSB_PF_secret_2(self):
        alg = LSB_PF(password='12345', color='B', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_PF_secret_2_large_password(self):
        alg = LSB_PF(password='dF4%^6hFdsyU6$@2gj88&;.:l', color='B', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_PF_secret_2_large_end_msg(self):
        alg = LSB_PF(password='12345', color='B', end_msg="r$1BlaFft^5fasdSDOda.")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_LSB_PF_secret_3_message_too_large(self):
        alg = LSB_PF(password='12345', color='B', end_msg="$t3g0")
        alg.encode(util.get_carrier_color(1), util.get_secret_msg(3))
        self.assertFalse(alg.is_success)

if __name__ == '__main__':
    unittest.main()