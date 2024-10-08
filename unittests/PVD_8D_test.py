import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.PVD_8D import PVD_8D
import util

class Test_PVD_8D(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_PVD_8D_secret_1(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_1_type_0(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))
    
    def test_PVD_8D_secret_1_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_1_large_end_msg(self):
        alg = PVD_8D(end_msg="r$1BlaFft^5fasdSDOda.", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_R_type_0(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="R")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_G_type_0(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="G")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_B_type_0(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="B")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_R_type_1(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="R")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_G_type_1(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="G")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_B_type_1(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="B")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_R_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="R")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_G_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="G")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_color_B_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="B")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_3(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_PVD_8D_secret_4(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

    def test_PVD_8D_secret_5(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    '''
    def test_PVD_8D_secret_5_type_2_high_pixel_difference(self):
        alg = PVD_8D(end_msg="$t3g0", type=2)
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))
    '''

    def test_PVD_8D_secret_5_type_1_high_pixel_difference(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_PVD_8D_secret_3_high_pixel_difference_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(6), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))
    
    def test_PVD_8D_secret_3_type_2_high_pixel_difference_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(6), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_PVD_8D_secret_4_type_0_color_R_message_too_large(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="R", estimation=True)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

    '''
    def test_PVD_8D_secret_4_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))
    '''

    def test_PVD_8D_secret_2_high_pixel_difference(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))
    
    def test_PVD_8D_secret_2_type_0_high_pixel_difference(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, color="")
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))
    
    def test_PVD_8D_secret_2_type_2_high_pixel_difference(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(5), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

if __name__ == '__main__':
    unittest.main()