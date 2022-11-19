'''A module for utility functions.'''

import numpy as np
from PIL import Image

def load_tiff(fpath):
    '''Load a TIFF image and convert it to NumPy array.

    args:
        fpath: relative path of the TIFF image

    return:
        NumPy array with colour channel information
    '''
    im = Image.open(fpath)
    return np.array(im)

def array2im(arr):
    '''Convert a NumPy array to PIL image.

    args:
        arr: NumPy array

    return:
        PIL image object
    '''
    return Image.fromarray(arr)

def _normalise(arr):
    # TODO: catch exception: dtype != uint8
    '''Normalises image array data to correspond to
    floating point pixel values between [0,1].

    args:
        arr: NumPy array containing image data

    return:
        NumPy array with normalised image data
    '''
    imarray = arr.astype(np.float32)
    return imarray/255

def rgb2ycbcr(arr):
    pass

def ycbcr2rgb(arr):
    pass

def save_jpeg(im):
    pass
