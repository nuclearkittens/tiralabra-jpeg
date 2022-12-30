import unittest
import numpy as np

import util.zigzag as zz

class TestZigzag(unittest.TestCase):
    def test_next_square(self):
        x = 5
        sq = 9
        self.assertEqual(sq, zz._next_square(x))

    def test_forward(self):
        mat = np.arange(16).reshape((4, 4))
        actual = list(zz.forward(mat))
        expected = [0, 1, 4, 8, 5, 2, 3, 6, 9, 12, 13, 10, 7, 11, 14, 15]
        self.assertEqual(actual, expected)

    def test_backward(self):
        expected = np.arange(16).reshape((4, 4))
        actual = zz.backward(list(zz.forward(expected)))
        self.assertEqual(actual.all(), expected.all())
