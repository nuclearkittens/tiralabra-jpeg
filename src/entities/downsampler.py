'''Module for downsampling YCbCr images.'''
import numpy as np

from util.linalg import conv2d

class Downsampler:
    '''Downsampler for chroma subsampling.'''
    def downsample(self, cb, cr, method=0):
        '''4:2:0 chroma subsampling.

        args:
            cb, cr: chroma channels in NxM matrix presentation
            method: 0, 1, or 2; method of downsampling
        '''
        if method == 0:
            cb, cr = self._ds(cb), self._ds(cr)
        elif method == 1:
            cb, cr = self._ds1(cb, cr)
        elif method == 2:
            cb, cr = self._ds2(cb, cr)
        return cb, cr

    def _ds1(self, cb, cr):
        # slow, not in use
        # left in here for posterioty's sake
        '''4:2:0 chroma subsampling.'''
        cb_new = np.zeros_like(cb)
        cr_new = np.zeros_like(cr)
        for i in range(0, cb.shape[0], 2):
            for j in range(0, cb.shape[1], 2):
                cb_new[i:i+2, j:j+2] = np.mean(cb[i:i+2, j:j+2])
                cr_new[i:i+2, j:j+2] = np.mean(cb[i:i+2, j:j+2])
        return np.round(cb_new).astype('uint8'), np.round(cr_new).astype('uint8')

    def _ds2(self, cb, cr):
        # slower than anticipated, not in use
        # left here just because writing the conv2d
        # function was a pain
        '''4:2:0 chroma subsampling. Uses 2D convolution.'''
        ker = np.array([[.25, .25], [.25, .25]])
        return conv2d(cb, ker, stride=2), conv2d(cr, ker, stride=2)

    def _ds(self, ch):
        # another try at subsampling
        # fastest (according to timeit), so currently
        # this version is in use
        '''4:2:0 chroma subsampling.'''
        # return ch[::2,::2]
        mat = ch.copy()
        mat[1::2,:] = mat[::2,:]
        mat[:,1::2] = mat[:,::2]
        return mat
