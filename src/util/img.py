'''Module for image utility functions.'''
import numpy as np
from PIL import Image

from config import COLOUR_MATRIX, K, MINVAL, MAXVAL, BLOCKSIZE

def create_random_im(fpath, size):
    ch1 = np.random.randint(256, size=size, dtype=np.uint8)
    ch2 = np.random.randint(256, size=size, dtype=np.uint8)
    ch3 = np.random.randint(256, size=size, dtype=np.uint8)
    arr = np.dstack((ch1, ch2, ch3))
    im = Image.fromarray(arr)
    im.save(fp=fpath, format='TIFF')

def rgb2ycbcr(im):
    rgb = im.astype(np.float32)
    ycbcr = rgb.dot(COLOUR_MATRIX)
    ycbcr[:,:,[1,2]] += K
    return ycbcr.astype(np.uint8)

def ycbcr2rgb(im):
    ycbcr = im.astype(np.float32)
    ycbcr[:,:,[1,2]] -= K
    rgb = ycbcr.dot(np.linalg.inv(COLOUR_MATRIX))
    np.putmask(rgb, rgb > MAXVAL, MAXVAL)
    np.putmask(rgb, rgb < MINVAL, MINVAL)
    return rgb.astype(np.uint8)

def get_channels(im):
    ch1 = im[:,:,0]
    ch2 = im[:,:,1]
    ch3 = im[:,:,2]
    return ch1, ch2, ch3

def stack_channels(chs):
    return np.dstack(tuple(chs))

def downsample(im):
    def ds(ch):
        # ch_copy = ch.copy()
        # ch_copy[1::2,:] = ch_copy[::2,:]
        # ch_copy[:,1::2] = ch_copy[:,::2]
        # return ch_copy
        return ch[::2,::2]
    y, cb, cr = get_channels(im)
    cb = ds(cb)
    cr = ds(cr)
    return y, cb, cr

def offset(ch, inverse=False):
    '''Offset pixel values from [0, 255] to [-128, 128].'''
    if inverse:
        ch += K
    else:
        ch -= K
    return ch

def pad(im, vpad, hpad):
    '''Add padding to images.'''
    if vpad:
        im = _vertical_pad(im, vpad)
    if hpad:
        im = _horizontal_pad(im, hpad)
    return im

def calc_padding(h, w, blocksize=BLOCKSIZE):
    '''Check whether image needs padding.'''
    pad = [0, 0]
    vpad = h % blocksize
    hpad = w % blocksize
    if vpad != 0:
        pad[0] = blocksize-vpad
    if hpad != 0:
        pad[1] = blocksize-hpad
    return tuple(pad)

def _vertical_pad(im, pad):
    '''Add vertical padding by repeating last column of the image.'''
    return np.concatenate((im, np.repeat(im[-1:], pad, 0)), axis=0)

def _horizontal_pad(im, pad):
    '''Add horizontal padding by repeating last row of the image.'''
    return np.concatenate((im, np.repeat(im[:,-1:], pad, 1)), axis=1)

def remove_pad(im, hpad, vpad):
    '''Remove padding from reconstructed image.'''
    if hpad > 0:
        im = im[:-hpad,:,:]
    if vpad > 0:
        im = im[:,:-vpad,:]
    return im
