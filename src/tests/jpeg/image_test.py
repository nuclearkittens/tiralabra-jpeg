import unittest
import numpy as np
import os.path
from PIL import Image

from config import MINVAL, MAXVAL
from jpeg.image import ImageArray

def mock_im(fpath):
    '''Create a mock image for testing.'''
    a = np.arange(256, dtype='uint8').reshape((16, 16))
    b = np.dstack((a, a, a))
    im = Image.fromarray(b)
    im.save(fp=fpath, format='TIFF')

fpath = 'src/data/test_img.tif'

class TestImageArray(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile(fpath):
            mock_im(fpath)
        self.test_im = ImageArray(fpath)

    def test_image_converted_to_array(self):
        self.assertIsInstance(self.test_im._im, np.ndarray)

    def test_im_returns_pil_image(self):
        self.assertIsInstance(self.test_im.im, Image.Image)

    def test_imarray_returns_array(self):
        self.assertIsInstance(self.test_im.imarray, np.ndarray)

    def test_mode_returns_correct_mode(self):
        expected = 'RGB'
        actual = self.test_im.mode
        self.assertEqual(expected, actual)

    def test_rgb2ycbcr_valid_input(self):
        expected = 'YCbCr'
        actual = self.test_im.rgb2ycbcr()
        self.assertEqual(expected, actual)

    def test_rgb2ycbcr_invalid_input(self):
        expected = 'test'
        self.test_im._mode = 'test'
        actual = self.test_im.rgb2ycbcr()
        self.assertEqual(expected, actual)

    def test_rgb2ycbcr_converts_to_uint8(self):
        expected = 'uint8'
        self.test_im.rgb2ycbcr()
        actual = self.test_im.imarray.dtype
        self.assertEqual(expected, actual)
