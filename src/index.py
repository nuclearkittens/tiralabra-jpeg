import numpy as np
from PIL import Image, ImageChops

import core.util as util

def main():
    im = util.im2arr('src/data/rgb2-1024x1024.tif')
    im_ycbcr = util.rgb2ycbcr(im)
    y = im_ycbcr[:,:,0]
    cb = im_ycbcr[:,:,1]
    cr = im_ycbcr[:,:,2]

    cb1, cr1 = util.downsample(cb, cr)
    cb2, cr2 = util.ds2(cb, cr)
    cb3, cr3 = util.ds3(cb, cr)

    # cb1im = Image.fromarray(cb1)
    # cb2im = Image.fromarray(cb2)
    # cb3im = Image.fromarray(cb3)
    # cr1im = Image.fromarray(cr1)
    # cr2im = Image.fromarray(cr2)
    # cr3im = Image.fromarray(cr3)

    print('cb1 size, shape')
    print(cb1.size, cb1.shape)
    print('cb2 size, shape')
    print(cb2.size, cb2.shape)
    print('cb3 size, shape')
    print(cb3.size, cb3.shape)

    print('cr1 size, shape')
    print(cr1.size, cr1.shape)
    print('cr2 size, shape')
    print(cr2.size, cr2.shape)
    print('cr3 size, shape')
    print(cr3.size, cr3.shape)

    print(cb1, cb2, cb3)

    # im1 = util.arr2im(util.ycbcr2rgb(util.compile_im(y, cb1, cr1)))
    # im2 = util.arr2im(util.ycbcr2rgb(util.compile_im(y, cb2, cr2)))
    # imdiff1 = util.imdiff(im, im1)
    # imdiff2 = util.imdiff(im, im2)
    # util.show_im(im)
    # im1.show()
    # im2.show()
    # imdiff1.show()
    # imdiff2.show()

if __name__ == '__main__':
    main()
