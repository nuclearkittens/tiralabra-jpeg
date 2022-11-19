import numpy as np
from PIL import Image

from config import COLOUR_MATRIX
from core.util import rgb2ycbcr, array2im

def main():
    im = Image.open('src/data/rgb2-1024x1024.tif')
    # im.show()

    imarray = np.array(im)
    print(imarray.shape)
    print(im.size)
    # print(imarray.dtype)
    # print(COLOUR_MATRIX)
    # print(np.linalg.inv(COLOUR_MATRIX))

    # im_ycbcr = np.array(im.convert('YCbCr'))
    # print(im_ycbcr.shape, im_ycbcr.size, im_ycbcr)
    ycbcr = rgb2ycbcr(imarray)
    im2 = array2im(ycbcr)

    im2.show()



if __name__ == '__main__':
    main()
