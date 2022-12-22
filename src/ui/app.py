'''Core functionality of the application.'''
import numpy as np

from config import TITLE, INSTRUCTIONS, YES, NO, QUIT, LUMA, CHROMA, Y, CB, CR, AC, DC
from ui.console_io import ConsoleIO
from ui.example import Example
from entities.block import Block
from entities.downsampler import Downsampler
from entities.image_object import ImageObject

import util.block as blk
import util.img as img
from util.linalg import dct2d
from entities.encoder import Encoder
from entities.decoder import Decoder

class App:
    '''Handle UI functionality for the command line application.'''
    def __init__(self):
        self._running = False
        self._io = ConsoleIO()
        self._ds = Downsampler()
        self._block = Block()

        im = ImageObject('src/data/rgb2-1024x1024.tif')
        self._example = Example(self._io, im, self._ds, self._block)

    def run(self):
        '''Run the application.'''
        self._running = True
        self._io.write(TITLE)
        self._io.write(INSTRUCTIONS)
        while self._running:
            prompt = '\nrun the example (y/n)?: '
            cmd = self._io.read(prompt)
            if cmd.lower() == YES:
                self._io.write('\nrunning example...')
                self._example.run()
            elif cmd.lower() == NO:
                self._run()
            elif cmd.lower() == QUIT:
                self._quit()
            else:
                self._io.write('\ninvalid input!')

    def _run(self):
        '''Run the application.'''
        self._io.write('\nonly example available!')

    def _quit(self):
        '''Quit the application.'''
        self._io.write('\nquitting app...')
        self._running = False

    def compress(self, fpath, size, quality):
        '''Compress a TIFF image using the JPEG
        compression algorithm.'''
        # load image and convert to array
        im = img.load_im(fpath)
        _, orig_h, orig_w = im.shape

        # convert from RGB to YCbCr, downsample, and offset
        ycbcr = img.rgb2ycbcr(im)
        y, cb, cr = img.downsample(ycbcr)
        data = {
            Y: y,
            CB: cb,
            CR: cr
        }
        data[Y] = img.offset(y)

        # add padding
        pad = {}
        for key, val in data.items():
            h, w = val.shape
            vpad, hpad = img.calc_padding(h, w)
            pad[key] = (vpad, hpad)
            data[key] = img.pad(val, vpad, hpad)

        # slice into blocks and apply DCT and quantisation
            data[key] = blk.slice_blocks(data[key])
            for i, block in enumerate(data[key]):
                data[key][i] = dct2d(block)
                data[key][i] = blk.quantise(data[key][i], key, quality=quality)

        # entropy encoding using Huffman and RLE
        luma = Encoder(data[Y], LUMA).encode()
        chroma = Encoder(np.vstack((data[CB], data[CR])), CHROMA).encode()
        encoded = {LUMA: luma, CHROMA: chroma}

        ordered = (
            encoded[LUMA][DC], encoded[LUMA][AC],
            encoded[CHROMA][DC], encoded[CHROMA][DC]
        )


