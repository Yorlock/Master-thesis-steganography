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
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_QVD_8D_secret_1_large_end_msg(self):
        alg = QVD_8D(end_msg="r$1BlaFft^5fasdSDOda.", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_QVD_8D_secret_2(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_type_0(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=2, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_type_1(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=3, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_type_2(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=4, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_color_R(self):
        alg = QVD_8D(end_msg="$t3g0", color='R', type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_color_G(self):
        alg = QVD_8D(end_msg="$t3g0", color='G', type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_color_B(self):
        alg = QVD_8D(end_msg="$t3g0", color='B', type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_color_B_type_2(self):
        alg = QVD_8D(end_msg="$t3g0", color='B', type=4, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_k_1(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=1)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_k_2(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=2)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_k_3(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_k_3_type_1(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_2_k_3_color_R(self):
        alg = QVD_8D(end_msg="$t3g0", color="R", type=1, k=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_QVD_8D_secret_3(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_QVD_8D_secret_4(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

    def test_QVD_8D_secret_5(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_QVD_8D_secret_4_color_R_message_too_large(self):
        alg = QVD_8D(end_msg="$t3g0", color='R', type=1, k=4, estimation=True)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

    def test_QVD_8D_secret_5_high_pixel_difference(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_QVD_8D_secret_3_high_pixel_difference_2(self):
        alg = QVD_8D(end_msg="$t3g0", color="", type=1, k=4)
        alg.encode(util.get_carrier_color(6), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

if __name__ == '__main__':
    unittest.main()