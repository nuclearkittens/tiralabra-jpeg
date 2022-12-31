import unittest
import os

from util.img import create_random_im
from entities.img import CompressedImage
from entities.compressor import Compressor

fpath = 'src/tests/data/test_im.tif'

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = Compressor()
        self.im = create_random_im(fpath, (64, 64))

    def tearDown(self):
        if os.path.exists(fpath):
            os.remove(fpath)

    def test_compressor_returns_compressed_image_obj(self):
        im_compr = self.compressor.compress(fpath, 50)
        self.assertIsInstance(im_compr, CompressedImage)
