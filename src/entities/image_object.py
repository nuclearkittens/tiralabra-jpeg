'''An image object module.'''
from copy import deepcopy

import numpy as np
from PIL import Image, ImageChops

from config import COLOUR_MATRIX, K, MINVAL, MAXVAL

class ImageObject:
    '''Class for representing an image.'''
    def __init__(self, fpath, mode='RGB'):
        self._orig = self._load(fpath)
        self._orig_mode = mode
        self._im = deepcopy(self._orig)
        self._mode = mode

    def _load(self, fpath):
        '''Load a TIFF image and convert it to NumPy array.

        args:
            fpath: relative path of the TIFF image.

        return:
            NumPy array with colour channel information.
        '''
        im = Image.open(fpath)
        return np.array(im)

    def rgb2ycbcr(self):
        '''Convert RGB image array to YCbCr colour space,
        as per ITU-T Rec 871.

        args:
            im: RGB image presented as a NxMx3 NumPy array

        return:
            YCbCr image presented as a NxMx3 NumPy array
        '''
        rgb = self._im.astype(np.float32)
        ycbcr = rgb.dot(COLOUR_MATRIX)
        ycbcr[:, :, [1, 2]] += K
        self._im = ycbcr.astype(np.uint8)
        self._mode = 'YCbCr'

    def ycbcr2rgb(self):
        # TODO: deal w/ grayscale imgs?
        # find a workaround for np.putmask (preferably
        # in reasonable time; this is to deal with
        # oversaturated pixels, basically a solution to
        # min(max(0, round(ycbcr)), 255))
        '''Convert YCbCr image array to RGB colour space,
        as per ITU-T Rec 871.

        args:
            im: YcbCr image presented as a NxMx3 NumPy array

        return:
            RGB image presented as a NxMx3 NumPy array
        '''
        ycbcr = self._im.astype(np.float32)
        ycbcr[:, :, [1, 2]] -= K
        rgb = ycbcr.dot(np.linalg.inv(COLOUR_MATRIX))
        np.putmask(rgb, rgb > MAXVAL, MAXVAL)
        np.putmask(rgb, rgb < MINVAL, MINVAL)
        self._im = rgb.astype(np.uint8)
        self._mode = 'RGB'

    def show(self):
        # TODO: check colour space is RGB
        '''Converts an image array to a PIL image and displays it'''
        Image.fromarray(self._im).show()

    def get_channels(self):
        '''Separate the colour channels in RGB or YCbCr image.'''
        ch1 = self._im[:,:,0] # Y or R
        ch2 = self._im[:,:,1] # Cb or G
        ch3 = self._im[:,:,2] # Cr or B
        return ch1, ch2, ch3

    def compile_im(self, ch1, ch2, ch3):
        '''Compile RGB or YCbCr image from individual channels.

        args:
            ch1, ch2, ch3: NxM matrix representaton of a colour channel;
                R/G/B or Y/Cb/Cr, respectively

        return:
            NxMx3 array representation of an image
        '''
        return np.dstack((ch1, ch2, ch3))

    def imdiff(im1, im2):
        '''Difference of two PIL images.'''
        return ImageChops.difference(im1, im2)

    @property
    def im(self):
        return self._im

    @property
    def mode(self):
        return self._mode
