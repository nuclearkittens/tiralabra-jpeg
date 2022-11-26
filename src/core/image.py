# obsolete; functions & methods moved to util
# will be deleted

'''Image module.'''

class ImageArray:
    '''Class for image objects.'''

    def __init__(self, fpath):
        self._mode = None
        self._im = self._load_im(fpath)

    def _load_im(self, fpath):
        '''Load a TIFF image and convert it to NumPy array.

        args:
            fpath: relative path of the TIFF image.

        return:
            NumPy array with colour channel information.
        '''
        im = Image.open(fpath)
        self._mode = im.mode
        return np.array(im)

    def rgb2ycbcr(self):
        # TODO: handling grayscale imgs
        '''Convert RGB image array to YCbCr colour space,
        as per ITU-T Rec 871.'''
        if self._mode == 'RGB':
            self._rgb2ycbcr()
            self._mode = 'YCbCr'
        # elif self._mode == 'L':
        #     self._gray2ycbcr()
        else:
            print('image mode is not RGB')
        return self._mode

    def _rgb2ycbcr(self):
        rgb = self._im.astype(np.float32)
        ycbcr = rgb.dot(COLOUR_MATRIX)
        ycbcr[:, :, [1, 2]] += K
        self._im = ycbcr.astype(np.uint8)

    def _gray2ycbcr(self):
        # TODO: dummy channels for Cb and Cr
        # use this if mode == 'L'
        pass

    def ycbcr2rgb(self):
        # TODO: deal w/ grayscale imgs?
        # find a workaround for np.putmask (preferably
        # in reasonable time; this is to deal with
        # oversaturated pixels, basically a solution to
        # min(max(0, round(ycbcr)), 255))
        '''Convert YCbCr image array to RGB colour space,
        as per ITU-T Rec 871.'''
        if self._mode != 'YCbCr':
            print('image mode is not YCbCr')
            return
        ycbcr = self._im.astype(np.float32)
        ycbcr[:, :, [1, 2]] -= K
        rgb = ycbcr.dot(np.linalg.inv(COLOUR_MATRIX))
        np.putmask(rgb, rgb > MAXVAL, MAXVAL)
        np.putmask(rgb, rgb < MINVAL, MINVAL)
        self._im = rgb.astype(np.uint8)
        self._mode = 'RGB'

    def save_jpeg(self, fpath):
        pass

    def plot(self):
        '''Display the PIL image.'''
        self.im.show()

    def downsample(self):
        '''4:2:0 chroma subsampling.'''
        pass

    @property
    def im(self):
        '''NumPy array converted to PIL image.'''
        im = Image.fromarray(self._im)
        if im.mode != self._mode:
            im.convert(self._mode)
        return im

    @property
    def imarray(self):
        '''NumPy array representation of the image.'''
        return self._im

    @property
    def mode(self):
        '''Colour space of the image.'''
        return self._mode
