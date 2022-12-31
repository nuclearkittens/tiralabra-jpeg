import unittest
import os
import numpy as np

from util.img import create_random_im
from entities.img import *

fpath = 'src/tests/data/test_im.tif'

def mock_im(size):
    ch1 = np.random.randint(256, size=size, dtype=np.uint8)
    ch2 = np.random.randint(256, size=size, dtype=np.uint8)
    ch3 = np.random.randint(256, size=size, dtype=np.uint8)
    return np.dstack((ch1, ch2, ch3))

class TestImageObj(unittest.TestCase):
    def setUp(self):
        self.imarray = mock_im((64, 64))
        self.im = create_random_im(fpath, (64, 64))

    def tearDown(self):
        if os.path.exists(fpath):
            os.remove(fpath)

    def test_create_raw_image_from_file(self):
        raw_im = RawImage(fpath=fpath)
        self.assertIsInstance(raw_im.im, np.ndarray)
        self.assertGreater(raw_im.size, 0)
        self.assertTrue(raw_im.name in fpath)

    def test_create_raw_image_from_array(self):
        raw_im = RawImage(im=self.imarray)
        self.assertIsInstance(raw_im.im, np.ndarray)
        self.assertGreater(raw_im.size, 0)
        self.assertTrue(PREXIF_RAW in raw_im.name)

    def test_raw_image_has_shape(self):
        self.assertIsNotNone(RawImage(im=self.imarray).shape)

    def test_create_compressed_image(self):
        data = {
            DATA: 'mock data',
            'info': 'mock info'
        }
        compr_im = CompressedImage(data, 'test')
        self.assertGreater(compr_im.size, 0)
