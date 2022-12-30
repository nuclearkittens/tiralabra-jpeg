import unittest
import numpy as np

from util.block import *

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.arr = np.random.randint(256, size=(16, 16))

    def test_slice_blocks(self):
        pass