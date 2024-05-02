import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.QVD_8D import QVD_8D
import util

class Test_QVD_8D(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_QVD_8D_secret_1(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_QVD_8D_secret_1_large_end_msg(self):
        alg = QVD_8D(end_msg="r$1BlaFft^5fasdSDOda.")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_QVD_8D_secret_2(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_3(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_QVD_8D_secret_4(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

    def test_QVD_8D_secret_5(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_QVD_8D_secret_5_high_pixel_difference(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_QVD_8D_secret_3_high_pixel_difference_2(self):
        alg = QVD_8D(end_msg="$t3g0")
        alg.encode(util.get_carrier_color(6), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

if __name__ == '__main__':
    unittest.main()