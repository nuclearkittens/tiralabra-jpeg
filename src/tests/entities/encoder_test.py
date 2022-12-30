import unittest

from config import *
from entities.encoder import Encoder

def is_binstr(s):
    b = '01'
    for char in s:
        if char not in b:
            return False
    return True

class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data = {
            Y: np.random.randint(16, size=(4, 8, 8)),
            CB: np.random.randint(16, size=(1, 8, 8)),
            CR: np.random.randint(16, size=(1, 8, 8))
        }
        self.luma = Encoder(self.data[Y], LUMA)
        self.chroma = Encoder(np.vstack((self.data[CB], self.data[CR])), CHROMA)

    def test_encoding_returns_binary_string(self):
        luma_str = self.luma.encode()
        chroma_str = self.chroma.encode()
        vals = list(luma_str.values())+list(chroma_str.values())
        for val in vals:
            self.assertTrue(is_binstr(val))
