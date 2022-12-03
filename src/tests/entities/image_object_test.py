import unittest
import numpy as np
import os.path
from PIL import Image

from config import MINVAL, MAXVAL
from entities.image_object import ImageObject

def mock_im(fpath):
    '''Create a mock image for testing.'''
    a = np.arange(256, dtype='uint8').reshape((16, 16))
    b = np.dstack((a, a, a))
    im = Image.fromarray(b)
    im.save(fp=fpath, format='TIFF')

fpath = 'src/data/test_img.tif'

class TestImageObject(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile(fpath):
            mock_im(fpath)
        self.test_im = ImageObject(fpath)

    def test_image_converted_to_array(self):
        self.assertIsInstance(self.test_im.im, np.ndarray)

    def test_mode_returns_correct_mode(self):
        expected = 'RGB'
        actual = self.test_im.mode
        self.assertEqual(expected, actual)

    def test_rgb2ycbcr(self):
        expected = 'YCbCr'
        self.test_im.rgb2ycbcr()
        actual = self.test_im.mode
        self.assertEqual(expected, actual)

    def test_rgb2ycbcr_converts_to_uint8(self):
        expected = 'uint8'
        self.test_im.rgb2ycbcr()
        actual = self.test_im.im.dtype
        self.assertEqual(expected, actual)

    def test_ycbcr2rgb(self):
        expected = 'RGB'
        self.test_im.rgb2ycbcr()
        self.test_im.ycbcr2rgb()
        actual = self.test_im.mode
        self.assertEqual(expected, actual)

    def test_get_channels(self):
        ch1, ch2, ch3 = self.test_im.get_channels()
        self.assertEqual(self.test_im.im[:,:,0].all(), ch1.all())
        self.assertEqual(self.test_im.im[:,:,1].all(), ch2.all())
        self.assertEqual(self.test_im.im[:,:,2].all(), ch3.all())

    def test_compile_im(self):
        ch1, ch2, ch3 = self.test_im.get_channels()
        expected = self.test_im.im
        actual = self.test_im.compile_im(ch1, ch2, ch3)
        self.assertEqual(expected.all(), actual.all())
