import unittest
import filecmp
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from algorithms.PVDMF import PVDMF
import util

class Test_PVDMF(unittest.TestCase):

    def setUp(self):
        util.init_instance()
        util.clean_result()
    
    def tearDown(self):
        util.clean_all()

    def test_PVDMF_secret_1_type_1(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVDMF_secret_2_type_1(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_1_large_end_msg(self):
        alg = PVDMF(end_msg="r$1BlaFft^5fasdSDOda.", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVDMF_secret_2_type_1_color_R(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="R")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_1_color_G(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="G")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_1_color_B(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="B")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_3_type_1(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_PVDMF_secret_4_type_1_message_too_large(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="", estimation=True)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

    def test_PVDMF_secret_5_type_1(self):
        alg = PVDMF(end_msg="$t3g0", type=1, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

    def test_PVDMF_secret_1_type_2(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(1))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(1), alg.destination_path))

    def test_PVDMF_secret_2_type_2(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_2_large_end_message(self):
        alg = PVDMF(end_msg="r$1BlaFft^5fasdSDOda.", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_2_color_R(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="R")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_2_color_G(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="G")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_2_type_2_color_B(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="B")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(2))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(2), alg.destination_path))

    def test_PVDMF_secret_3_type_2(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(3))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(3), alg.destination_path))

    def test_PVDMF_secret_4_type_2(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(4), alg.destination_path))

    def test_PVDMF_secret_4_type_2_color_G_message_too_large(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="G", estimation=True)
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(4))
        self.assertFalse(alg.is_success)

    def test_PVDMF_secret_5_type_2(self):
        alg = PVDMF(end_msg="$t3g0", type=2, color="")
        alg.encode(util.get_carrier_color(2), util.get_secret_msg(5))
        self.assertTrue(alg.is_success)
        alg.decode()
        self.assertTrue(alg.is_success)
        self.assertTrue(filecmp.cmp(util.get_secret_msg(5), alg.destination_path))

if __name__ == '__main__':
    unittest.main()