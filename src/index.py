# import timeit
# import numpy as np
# from PIL import Image, ImageChops

# import jpeg.util as util
from app.app import App
from app.console_io import ConsoleIO

def main():
    app = App(ConsoleIO())
    app.run()

if __name__ == '__main__':
    main()
    # read an image and convert it from RGB to YCbCr
    # im = util.im2arr('src/data/rgb2-1024x1024.tif')
    # im_ycbcr = util.rgb2ycbcr(im)

    # # separate colour channels
    # y = im_ycbcr[:,:,0]
    # cb = im_ycbcr[:,:,1]
    # cr = im_ycbcr[:,:,2]

    # #times of the different downsampling functions
    # print('downsampling v. 1:')
    # print(timeit.timeit('util.downsample(cb, cr)', number=1, globals=globals()))
    # print('downsampling v. 2:')
    # print(timeit.timeit('util.downsample2(cb, cr)', number=1, globals=globals()))
    # print('downsampling v. 3:')
    # print(timeit.timeit('util.downsample3(cb, cr)', number=1, globals=globals()))
