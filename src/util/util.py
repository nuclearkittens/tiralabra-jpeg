import numpy as np

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
    return res
