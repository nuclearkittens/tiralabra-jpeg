import unittest
import numpy as np
from scipy.signal import convolve2d
from scipy.fftpack import dct

import util.linalg

def dct2d(mat):
    '''Scipy 2D DCT-II.'''
    res = dct(dct(mat, norm='ortho', axis=0), norm='ortho', axis=1)
    return np.asarray(res)

class TestLinAlg(unittest.TestCase):
    def setUp(self):
        self.x = np.random.random(1024)
        self.mat = np.random.randint(256, size=(16, 16))

    def test_conv2d(self):
        ker = np.array([[.25, .25], [.25, .25]])
        expected = convolve2d(self.mat, ker)
        actual = util.linalg.conv2d(self.mat, ker)
        self.assertAlmostEqual(expected.all(), actual.all())

    def test_dft(self):
        self.assertTrue(np.allclose(
            util.linalg.dft(self.x), np.fft.fft(self.x)
        ))

    def test_fft(self):
        self.assertTrue(np.allclose(
            util.linalg.fft(self.x), np.fft.fft(self.x)
        ))

    def test_fft_value_error(self):
        with self.assertRaises(ValueError):
            x = np.random.random(13)
            util.linalg.fft(x)

    def test_dct(self):
        actual = util.linalg.dct(self.x)
        expected = dct(self.x)
        self.assertAlmostEqual(actual.all(), expected.all())

    def test_dct2d_slow(self):
        actual = util.linalg.dct2d_slow(self.mat)
        expected = dct2d(self.mat)
        self.assertAlmostEqual(actual.all(), expected.all())

    def test_dct2d(self):
        actual = util.linalg.dct2d(self.mat)
        expected = dct2d(self.mat)
        self.assertAlmostEqual(actual.all(), expected.all())
