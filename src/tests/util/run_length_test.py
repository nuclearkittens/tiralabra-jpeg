import unittest
import numpy as np

import util.run_length as rle

class TestRunLength(unittest.TestCase):
    def test_differential_encoding(self):
        data = list(np.arange(8))
        res = list(rle.encode_differential(data))
        expected = [0, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(expected, res)

    def test_differential_decoding(self):
        data = list(np.arange(4))
        res = list(rle.decode_differential(
            rle.encode_differential(data)
        ))
        self.assertEqual(data, res)

    def test_run_length(self):
        lengths = list(np.random.randint(16, size=8))
        keys = list(np.random.randint(16, size=8))
        data = list(zip(lengths, keys))
        res = list(rle.decode_run_length(
            rle.encode_run_length(data)
        ))
        self.assertEqual(data, res)
