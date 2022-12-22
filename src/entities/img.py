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
    return prefix + datetime.now().strftime('%Y%m%d-%H%M%S')

class RawImage:
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
        im = Image.open(fpath)
        return np.array(im)

    @property
    def shape(self):
        return self.im.shape

class CompressedImage:
    def __init__(self, data, name=None):
        self.data = data[DATA]
        data.pop(DATA)
        self.info = data
        self.name = _generate_name(PREFIX_COMP) if not name else name

    @property
    def size(self):
        return sys.getsizeof(self.data)
