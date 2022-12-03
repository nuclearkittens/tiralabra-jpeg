'''A module for image utility functions.'''
import numpy as np
from PIL import Image, ImageChops

from config import COLOUR_MATRIX, K, MINVAL, MAXVAL

def im2arr(fpath):
    '''Load a TIFF image and convert it to NumPy array.

    args:
        fpath: relative path of the TIFF image.

    return:
        NumPy array with colour channel information.
    '''
    im = Image.open(fpath)
    return np.array(im)

def arr2im(im):
    '''Convert NxMx3 array to PIL image object.'''
    return Image.fromarray(im)

def rgb2ycbcr(im):
    '''Convert RGB image array to YCbCr colour space,
    as per ITU-T Rec 871.

    args:
        im: RGB image presented as a NxMx3 NumPy array

    return:
        YCbCr image presented as a NxMx3 NumPy array
    '''
    rgb = im.astype(np.float32)
    ycbcr = rgb.dot(COLOUR_MATRIX)
    ycbcr[:, :, [1, 2]] += K
    return ycbcr.astype(np.uint8)

def ycbcr2rgb(im):
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
    ycbcr = im.astype(np.float32)
    ycbcr[:, :, [1, 2]] -= K
    rgb = ycbcr.dot(np.linalg.inv(COLOUR_MATRIX))
    np.putmask(rgb, rgb > MAXVAL, MAXVAL)
    np.putmask(rgb, rgb < MINVAL, MINVAL)
    return rgb.astype(np.uint8)

def show_im(im):
    # TODO: check colour space is RGB
    '''Converts an image array to a PIL image and displays it'''
    Image.fromarray(im).show()

def downsample(cb, cr):
    # slow, not in use
    # left in here for posterioty's sake
    '''4:2:0 chroma subsampling.

    args:
        cb, cr: chroma channels in NxM matrix presentation

    return:
        subsampled chroma channels in NxM matrix presentation
    '''
    cb_new = np.zeros_like(cb)
    cr_new = np.zeros_like(cr)
    for i in range(0, cb.shape[0], 2):
        for j in range(0, cb.shape[1], 2):
            cb_new[i:i+2, j:j+2] = np.mean(cb[i:i+2, j:j+2])
            cr_new[i:i+2, j:j+2] = np.mean(cb[i:i+2, j:j+2])
    return np.round(cb_new).astype('uint8'), np.round(cr_new).astype('uint8')

def downsample2(cb, cr):
    # another try at subsampling
    # fastest (according to timeit), so currently
    # this version is in use
    '''4:2:0 chroma subsampling.

    args:
        cb, cr: chroma channels in NxM matrix presentation

    return:
        subsampled chroma channels in NxM matrix presentation
    '''
    def _downsample(mat):
        mat2 = mat.copy()
        mat2[1::2,:] = mat2[::2,:]
        mat2[:,1::2] = mat2[:,::2]
        return mat2
    return _downsample(cb), _downsample(cr)

def downsample3(cb, cr):
    # slower than anticipated, not in use
    # left here just because writing the conv2d
    # function was a pain
    '''4:2:0 chroma subsampling. Uses 2D convolution.

    args:
        cb, cr: chroma channels in NxM matrix presentation

    return:
        subsampled chroma channels in NxM matrix presentation
    '''
    ker = np.array([[.25, .25], [.25, .25]])
    return conv2d(cb, ker, stride=2), conv2d(cr, ker, stride=2)

def conv2d(im, kernel, stride=1, pad=0):
    '''2D convolution.

    args:
        im: matrix (NumPy array) representing single colour channel
        kernel: matrix (NumPy array)
        stride: int
        padding: int

    return:
        matrix: convoluted image
    '''
    #TODO: try different padding methods
    # (or write a separate function for this)
    im = np.pad(im, [(pad, pad), (pad, pad)], mode='constant', constant_values=0)
    ker_h, ker_w = kernel.shape
    im_h, im_w = im.shape

    res_h = (im_h-ker_h) // stride+1
    res_w = (im_w-ker_w) // stride+1
    res = np.zeros((res_h, res_w)).astype(np.float32)

    for j in range(res_h):
        for i in range(res_w):
            res[j][i] = np.sum(
                im[j*stride:j*stride+ker_h, i*stride:i*stride+ker_w]*kernel
            ).astype(np.float32)

    return res.astype(np.uint8)

def compile_im(ch1, ch2, ch3):
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
