import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.n_RMBR import n_RMBR
import util

class Test_n_RMBR(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_n_RMBR_secret_1(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_n_RMBR_secret_2(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_n_1(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=1)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_n_2(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=2)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_n_3(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_color_R(self):
        alg = n_RMBR(end_msg="$t3g0", color="R", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_color_G(self):
        alg = n_RMBR(end_msg="$t3g0", color="G", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_color_B(self):
        alg = n_RMBR(end_msg="$t3g0", color="B", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_2_color_G_n_2(self):
        alg = n_RMBR(end_msg="$t3g0", color="G", n=2)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_n_RMBR_secret_3(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_n_RMBR_secret_4(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

    def test_n_RMBR_secret_5(self):
        alg = n_RMBR(end_msg="$t3g0", color="", n=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_n_RMBR_secret_4_message_too_large(self):
        alg = n_RMBR(end_msg="$t3g0", color="R", n=1)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

if __name__ == '__main__':
    unittest.main()