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
        alg = PVD_8D(end_msg="$t3g0", type=1, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_1_type_0(self):
        alg = PVD_8D(end_msg="$t3g0", type=0, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))
    
    def test_PVD_8D_secret_1_type_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=2, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_1_large_end_msg(self):
        alg = PVD_8D(end_msg="r$1BlaFft^5fasdSDOda.", type=1, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVD_8D_secret_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_t_2(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, t=2)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_2_t_4(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, t=4)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVD_8D_secret_3(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_PVD_8D_secret_4(self):
        alg = PVD_8D(end_msg="$t3g0", type=1, t=3)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

if __name__ == '__main__':
    unittest.main()