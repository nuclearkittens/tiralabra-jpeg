'''Image class module.'''
from config import COLOUR_MATRIX, K

import numpy as np
from PIL import Image

class ImageArray:
    '''Class for image objects.'''
    def __init__(self, fpath):
        self._mode = None
        self._im = self._load_im(fpath)

    def _load_im(self, fpath):
        '''Load a TIFF image and convert it to NumPy array.

        args:
            fpath: relative path of the TIFF image.

        return:
            NumPy array with colour channel information.
        '''
        im = Image.open(fpath)
        self._mode = im.mode
        return np.array(im)

    def rgb2ycbcr(self):
        '''Convert RGB image array to YCbCr colour space,
        as per ITU-T Rec 871.'''
        rgb = self._im.astype(np.float32)
        ycbcr = rgb.dot(COLOUR_MATRIX)
        ycbcr[:,:,[1,2]] += K
        self._im = ycbcr.astype(np.uint8)
        self._mode = 'YCbCr'

    def ycbcr2rgb(self):
        pass

    def save_jpeg(self, fpath):
        pass

    @property
    def im(self):
        '''NumPy array converted to PIL image.'''
        im = Image.fromarray(self._im)
        if im.mode != self._mode:
            im.convert(self._mode)
        return im

    @property
    def imarray(self):
        '''Numpy array representation of the image.'''
        return self._im

    @property
    def mode(self):
        '''Colour space of the image.'''
        return self._mode
