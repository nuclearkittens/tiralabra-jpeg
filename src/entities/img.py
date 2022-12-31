'''Module for image objects.'''
import os
import sys
from datetime import datetime

from PIL import Image
import numpy as np

DATA = 'data'
PREFIX_COMP = 'compressed-img-'
PREXIF_RAW = 'raw-img-'

def _generate_name(prefix):
    '''Generate a name for an image object using a
    predetermined prefix and the current time.
    '''
    return prefix + datetime.now().strftime('%Y%m%d-%H%M%S')

class RawImage:
    '''Class for a raw image data object. Can be either a TIFF file
    or a NumPy 3D array.
    '''
    def __init__(self, fpath=None, im=None):
        if fpath:
            self.im = self._load(fpath)
            self.size = os.stat(fpath).st_size
            self.name = os.path.basename(fpath)
        else:
            self.im = im
            self.size = im.itemsize
            self.name = _generate_name(PREXIF_RAW)

    def _load(self, fpath):
        '''Load an image from file.'''
        im = Image.open(fpath)
        return np.array(im)

    @property
    def shape(self):
        '''Shape (height, width, dimension) of the image.'''
        return self.im.shape

class CompressedImage:
    '''Class for image data compressed with the JPEG algorithm.'''
    def __init__(self, data, name=None):
        self.data = data[DATA]
        data.pop(DATA)
        self.info = data
        self.name = _generate_name(PREFIX_COMP) if not name else name

    @property
    def size(self):
        '''Return the image size in bytes.'''
        return sys.getsizeof(self.data)
