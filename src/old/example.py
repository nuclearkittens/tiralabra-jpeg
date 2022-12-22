'''Example of how the JPEG conversion works.'''
from timeit import default_timer as timer

from config import YES


class Example:
    '''JPEG conversion example script.'''
    def __init__(self, io, im, downsampler, block):
        self._io = io
        self._im = im
        self._ds = downsampler
        self._block = block

    def run(self):
        '''Run the example.'''
        self._io.write('\nloading test image: src/data/rgb2-1024x1024.tif')
        self._show_im()
        self._print_im_info()

        self._io.write('\nconverting RGB to YCbCr...')
        self._im.rgb2ycbcr()
        self._show_im()
        self._print_im_info()

        y, cb, cr = self._im.get_channels()
        self._io.write('\ndownsampling chroma channels...')
        cb0, cr0 = self._downsample(cb, cr, 0)

        # slow methods:
        # cb1, cr1 = self._downsample(cb, cr, 1)
        # cb2, cr2 = self._downsample(cb, cr, 2)

        #TODO

        self._io.write('**example finished**')

    def _downsample(self, cb, cr, method):
        self._io.write(f'\nchroma subsampling: method #{method}')
        start = timer()
        new_cb, new_cr = self._ds.downsample(cb, cr, method)
        stop = timer()
        time = stop-start
        h, w = new_cb.shape
        self._io.write(f'chroma channels: h: {h}, w: {w}')
        self._io.write(f'subsampling took {time} seconds')
        return new_cb, new_cr

    def _split_blocks(self):
        pass

    def _show_im(self):
        cmd = self._io.read('show image (y/n)?: ')
        if cmd.lower() == YES:
            self._io.show_im(self._im.im)

    def _print_im_info(self):
        h, w, ch = self._im.im.shape
        mode = self._im.mode
        size = self._im.im.size
        self._io.write(f'image dimensions: w: {w}, h: {h}; size: {size}')
        self._io.write(f'colour space: {mode}; channels: {ch}')
