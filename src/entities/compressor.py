'''Module for compressing and decompressing image data.'''
from bitarray import bitarray, bits2bytes
import numpy as np

from config import AC, DC, LUMA, CHROMA, Y, CB, CR

import util.block as blk
import util.img as img
from util.linalg import dct2d

from entities.encoder import Encoder
from entities.img import RawImage, CompressedImage

QLTY = 'quality'
DIMS = 'dimensions'
SLICE_LENGTH = 'slice length'
FILLER_BITS = 'filler bits'
PAD = 'padding'
DATA = 'data'

class Compressor:
    '''Compress and decompress image data.'''
    def __init__(self):
        self.data = {}
        self.encoded = {}

    def compress(self, fpath, quality, name=None):
        '''Compress image to given quality.'''
        self.__init__()
        self.encoded[QLTY] = quality
        self._preprocess_im(fpath)
        self._process_blocks()
        self._encode()
        return CompressedImage(self.encoded, name)

    def _preprocess_im(self, fpath):
        '''Load image, convert from RGB to YCbCr and offset
        luma values.'''
        im = RawImage(fpath=fpath)
        h, w, _ = im.shape
        self.encoded[DIMS] = (h, w)

        ycbcr = img.rgb2ycbcr(im.im)
        y, cb, cr = img.downsample(ycbcr)
        self.data[Y] = img.offset(y)
        self.data[CB] = cb
        self.data[CR] = cr

    def _process_blocks(self):
        '''Add padding, slice the data into blocks and apply
        DCT and quantisation.'''
        pad = {}
        for key, ch in self.data.items():
            h, w = ch.shape
            vpad, hpad = img.calc_padding(h, w)
            pad[key] = (vpad, hpad)
            self.data[key] = img.pad(ch, vpad, hpad)
            self.data[key] = blk.slice_blocks(self.data[key])

            for i, block in enumerate(self.data[key]):
                self.data[key][i] = dct2d(block)
                self.data[key][i] = blk.quantise(self.data[key][i], key, quality=self.encoded[QLTY])

            self.data[key] = np.rint(self.data[key]).astype(int)

        self.encoded[PAD] = pad

    def _encode(self):
        '''Entropy encoding using Huffman and RLE. '''
        luma = Encoder(self.data[Y], LUMA).encode()
        chroma = Encoder(np.vstack((self.data[CB], self.data[CR])), CHROMA).encode()
        encoded = {LUMA: luma, CHROMA: chroma}

        ordered = (
            encoded[LUMA][DC], encoded[LUMA][AC],
            encoded[CHROMA][DC], encoded[CHROMA][AC]
        )

        bits = bitarray(''.join(ordered))
        self.encoded[DATA] = bits
        self.encoded[SLICE_LENGTH] = tuple(len(data) for data in ordered)
        self.encoded[FILLER_BITS] = bits2bytes(len(bits))*8 - len(bits)
