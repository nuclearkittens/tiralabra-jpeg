import numpy as np
from PIL import Image

def main():
    im = Image.open('src/data/rgb2-1024x1024.tif')
    # im.show()

    imarray = np.array(im)
    # print(imarray.shape)
    # print(im.size)
    # print(imarray.dtype)


if __name__ == '__main__':
    main()
