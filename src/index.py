import timeit
# import numpy as np
# from PIL import Image, ImageChops

import jpeg.util as util

def main():
    # read an image and convert it from RGB to YCbCr
    im = util.im2arr('src/data/rgb2-1024x1024.tif')
    im_ycbcr = util.rgb2ycbcr(im)

    # separate colour channels
    y = im_ycbcr[:,:,0]
    cb = im_ycbcr[:,:,1]
    cr = im_ycbcr[:,:,2]

    # cb1, cr1 = util.downsample(cb, cr)
    # cb2, cr2 = util.ds2(cb, cr)
    # cb3, cr3 = util.ds3(cb, cr)

    # print('cb1 size, shape')
    # print(cb1.size, cb1.shape)
    # print('cb2 size, shape')
    # print(cb2.size, cb2.shape)
    # print('cb3 size, shape')
    # print(cb3.size, cb3.shape)

    # print('cr1 size, shape')
    # print(cr1.size, cr1.shape)
    # print('cr2 size, shape')
    # print(cr2.size, cr2.shape)
    # print('cr3 size, shape')
    # print(cr3.size, cr3.shape)

    # print(cb1, cb2, cb3)

if __name__ == '__main__':
    # main()
    # read an image and convert it from RGB to YCbCr
    im = util.im2arr('src/data/rgb2-1024x1024.tif')
    im_ycbcr = util.rgb2ycbcr(im)

    # separate colour channels
    y = im_ycbcr[:,:,0]
    cb = im_ycbcr[:,:,1]
    cr = im_ycbcr[:,:,2]

    #times of the different downsampling functions
    print('downsampling v. 1:')
    print(timeit.timeit('util.downsample(cb, cr)', number=1, globals=globals()))
    print('downsampling v. 2:')
    print(timeit.timeit('util.ds2(cb, cr)', number=1, globals=globals()))
    print('downsampling v. 3:')
    print(timeit.timeit('util.ds3(cb, cr)', number=1, globals=globals()))
