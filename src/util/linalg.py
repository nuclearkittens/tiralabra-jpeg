'''Module for linear algebra utility functions.'''

from math import sqrt, cos, pi, ceil, floor
import numpy as np
from scipy.fftpack import idct

def round_to_nearest_int(x):
    if float(x) % 1 < .5:
        return floor(x)
    return ceil(x)

def conv2d(im, kernel, stride=1, pad=0):
    '''"2D convolution.
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

def dct2d_slow(arr):
    '''Naïve method of discrete cosine transform for 2D arrays.'''
    def alpha(u):
        '''Normalisation of a scalar.'''
        return 1/sqrt(2) if u == 0 else 1

    res = np.zeros((arr.shape))
    for u in range(res.shape[0]):
        for v in range(res.shape[1]):
            scalar = .25 * alpha(u) * alpha(v)
            val = float(0)
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    pixel_val = arr[i, j]
                    cos_x = cos((2*i+1) * u * pi / 16)
                    cos_y = cos((2*j+1) * v * pi / 16)
                    val += pixel_val * cos_x * cos_y
            res[u, v] = scalar * val

    return res

def dft(x):
    '''Discrete Fourier Transform.'''
    x = np.asarray(x, dtype=float)
    n = x.shape[0]
    m = np.arange(n)
    k = m.reshape((n, 1))
    a = np.exp(-2j * pi * k * m / n)
    return np.dot(a, x)

def fft(x):
    '''Fast Fourier Transformation using recursion.'''
    x = np.asarray(x, dtype=float)
    n = x.shape[0]

    if n % 2 > 0:
        raise ValueError('n must be a power of two')

    if n <= 2:
        return dft(x)
    else:
        even = fft(x[::2])
        odd = fft(x[1::2])
        a = np.exp(-2j * pi * np.arange(n) / n)
        i = int(n/2)
        return np.concatenate([
            even + a[:i] * odd,
            even + a[i:] * odd
        ])

def dct(x):
    '''1D DCT-II.'''
    n = x.shape[0]
    x_2 = np.empty(2*n, np.float32)
    x_2[:n] = x[:]
    x_2[n:] = x[::-1]

    transform = fft(x_2)
    phi = np.exp(-1j * pi * np.arange(n) / (2*n))

    return np.real(phi * transform[:n])

def dct2d(arr):
    '''2D DCT-II.'''
    m, n = arr.shape
    a = np.empty([m, n], np.float32)
    x = np.empty([m, n], np.float32)

    for i in range(m):
        a[i,:] = dct(arr[i,:])

    for j in range(n):
        x[:,j] = dct(a[:,j])

    return x

def idct2d(arr):
    #TODO: write the algo for this and
    #DO NOT use the scipy.fftpack function
    return idct(idct(arr, norm='ortho', axis=0), norm='ortho', axis=1)
