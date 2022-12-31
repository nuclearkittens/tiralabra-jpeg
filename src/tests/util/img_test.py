import unittest
import os
import numpy as np

import util.img as img

fpath = 'src/tests/data/test_im.tif'

def mock_im(size):
    ch1 = np.random.randint(256, size=size, dtype=np.uint8)
    ch2 = np.random.randint(256, size=size, dtype=np.uint8)
    ch3 = np.random.randint(256, size=size, dtype=np.uint8)
    return np.dstack((ch1, ch2, ch3))

class TestImageUtil(unittest.TestCase):
    def setUp(self):
        self.im = mock_im((64, 64))

    def tearDown(self):
        if os.path.exists(fpath):
            os.remove(fpath)

    def test_create_im(self):
        img.create_random_im(fpath, (64, 64))
        self.assertTrue(os.path.exists(fpath))

    def test_colour_space_conversion(self):
        ycbcr = img.rgb2ycbcr(self.im)
        rgb = img.ycbcr2rgb(ycbcr)
        self.assertEqual(self.im.all(), rgb.all())

    def test_stack_channels(self):
        ch1, ch2, ch3 = img.get_channels(self.im)
        stacked = img.stack_channels((ch1, ch2, ch3))
        self.assertEqual(self.im.all(), stacked.all())

    def test_sampling(self):
        y, cb, cr = img.downsample(self.im)
        im_h, im_w, _ = self.im.shape
        cb_h, _ = cb.shape
        _, cr_w = cr.shape
        self.assertEqual(cb.shape, cr.shape)
        self.assertEqual(cb_h, im_h//2)
        self.assertEqual(cr_w, im_w//2)
        self.assertEqual(y.all(), self.im[:,:,0].all())

    def test_offset(self):
        actual = self.im[:,:,0]
        expected = img.offset(img.offset(actual), True)
        self.assertEqual(actual.all(), expected.all())

    def test_padding_no_padding(self):
        h, w, _ = self.im.shape
        vpad, hpad = img.calc_padding(h, w)
        padded = img.pad(self.im, vpad, hpad)
        self.assertEqual(self.im.all(), padded.all())

    def test_padding_and_removal(self):
        h, w, _ = self.im.shape
        vpad, hpad = img.calc_padding(h, w, 5)
        padded = img.pad(self.im, vpad, hpad)
        unpadded = img.remove_pad(self.im, hpad, vpad)
        self.assertEqual(self.im.all(), unpadded.all())
