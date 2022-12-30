# import unittest
# import numpy as np

# from old.downsampler import Downsampler

# class TestDownsampler(unittest.TestCase):
#     def setUp(self):
#         self.test_mat = np.random.randint(256, size=(8, 8))
#         self.test_ds = Downsampler()

#     def test_invalid_method(self):
#         actual, _ = self.test_ds.downsample(self.test_mat, self.test_mat, 3)
#         self.assertEqual(actual.all(), self.test_mat.all())

#     def test_method_0(self):
#         cb_act, cr_act = self.test_ds.downsample(self.test_mat, self.test_mat)
#         cb_exp = cr_exp = self.test_ds._ds(self.test_mat)
#         self.assertEqual(cb_act.all(), cb_exp.all())
#         self.assertEqual(cr_act.all(), cr_exp.all())

#     def test_method_1(self):
#         cb_act, cr_act = self.test_ds.downsample(self.test_mat, self.test_mat, 1)
#         cb_exp, cr_exp = self.test_ds._ds1(self.test_mat, self.test_mat)
#         self.assertEqual(cb_act.all(), cb_exp.all())
#         self.assertEqual(cr_act.all(), cr_exp.all())

#     def test_method_2(self):
#         cb_act, cr_act = self.test_ds.downsample(self.test_mat, self.test_mat, 2)
#         cb_exp, cr_exp = self.test_ds._ds2(self.test_mat, self.test_mat)
#         self.assertEqual(cb_act.all(), cb_exp.all())
#         self.assertEqual(cr_act.all(), cr_exp.all())
