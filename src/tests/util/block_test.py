import unittest
import numpy as np

from util.block import *
from config import Y, CR

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.mat = np.arange(64).reshape((8, 8))

    def test_slice_blocks(self):
        actual = slice_blocks(self.mat)
        self.assertEqual(actual.all(), self.mat.all())

    def test_combine_blocks(self):
        actual = combine_blocks(slice_blocks(self.mat), 8, 8)
        self.assertEqual(actual.all(), self.mat.all())

    def test_quantise_wrong_mode(self):
        with self.assertRaises(ValueError):
            quantise(self.mat, 'mode', 50)

    def test_quantise_quality_lt50(self):
        actual = quantise(
            quantise(self.mat, Y, 20), Y, 20, True
        )
        self.assertAlmostEqual(actual.all(), self.mat.all())

    def test_quantise_quality_gt50(self):
        actual = quantise(
            quantise(self.mat, CR, 70), CR, 70, True
        )
        self.assertAlmostEqual(actual.all(), self.mat.all())
