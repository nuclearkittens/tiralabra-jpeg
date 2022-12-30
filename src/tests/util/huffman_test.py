import unittest
from random import randint
from config import *
import util.huffman as huff

def is_binstr(s):
    b = '01'
    for char in s:
        if char not in b:
            return False
    return True

class TestHuffman(unittest.TestCase):
    def test_valid_dc_value(self):
        x = randint(-2047, 2047)
        self.assertTrue(is_binstr(huff.encode(x, LUMA)))

    def test_invalid_dc_value(self):
        x = 2048
        with self.assertRaises(ValueError):
            huff.encode(x, LUMA)

    def test_valid_ac_value(self):
        x = (randint(0, 15), randint(-1023, 1023))
        self.assertTrue(is_binstr(huff.encode(x, LUMA)))

    def test_invalid_ac_value(self):
        x = (randint(0, 15), 1024)
        with self.assertRaises(ValueError):
            huff.encode(x, LUMA)

    def test_eob(self):
        x = EOB
        expected = (
            HUFFMAN_TABLES[AC][LUMA][EOB],
            HUFFMAN_TABLES[AC][CHROMA][EOB]
        )
        actual = (
            huff.encode(x, LUMA), huff.encode(x, CHROMA)
        )
        self.assertEqual(actual, expected)

    def test_zrl(self):
        x = ZRL
        expected = (
            HUFFMAN_TABLES[AC][LUMA][ZRL],
            HUFFMAN_TABLES[AC][CHROMA][ZRL]
        )
        actual = (
            huff.encode(x, LUMA), huff.encode(x, CHROMA)
        )
        self.assertEqual(actual, expected)

    def test_dc_size_is_zero(self):
        x = 0
        expected = HUFFMAN_TABLES[DC][LUMA][0]
        actual = huff.encode(x, LUMA)
        self.assertEqual(actual, expected)
