'''Module for image objects.'''
import os
import sys
from datetime import datetime

from PIL import Image
import numpy as np

DATA = 'data'
PREFIX = 'compressed-img-'

class RawImage:
    def __init__(self, fpath):
        self.im = self._load(fpath)
        self.name = os.path.basename(fpath)
        self.size = os.stat(fpath).st_size

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
        self.name = self._generate_name if not name else name

    def _generate_name(self):
        return PREFIX + datetime.now().strftime('%Y%m%d-%H%M%S')

    @property
    def size(self):
        return sys.getsizeof(self.data)
