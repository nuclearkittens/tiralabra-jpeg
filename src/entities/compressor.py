'''Module for compressing and decompressing image data.'''
from itertools import accumulate
from bitarray import bitarray, bits2bytes
import numpy as np

from config import AC, DC, LUMA, CHROMA, Y, CB, CR
import util.block as blk
import util.img as img
from util.linalg import dct2d, idct2d, round_to_nearest_int
from entities.encoder import Encoder
from entities.decoder import Decoder
from entities.img import RawImage, CompressedImage

QLTY = 'quality'
DIMS = 'dimensions'
SLICE_LENGTH = 'slice length'
FILLER_BITS = 'filler bits'
PAD = 'padding'
DATA = 'data'

DIR = '/src/data/'
PREFIX = 'compressed'
EXTENSION = '.nonjpeg'

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
        return CompressedImage(self.encoded[DATA], name)

    def _preprocess_im(self, fpath):
        '''Load image, convert from RGB to YCbCr and offset
        luma values.'''
        im = RawImage(fpath)
        _, h, w = im.shape
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
        for key, val in self.data.items():
            h, w = val.shape
            vpad, hpad = img.calc_padding(h, w)
            pad[key] = (vpad, hpad)
            self.data[key] = img.pad(val, vpad, hpad)

            self.data[key] = blk.slice_blocks(self.data[key])
            for i, block in enumerate(self.data[key]):
                self.data[key][i] = dct2d(block)
                self.data[key][i] = blk.quantise(self.data[key][i], key, quality=self.encoded[QLTY])

        self.encoded[PAD] = pad

    def _encode(self):
        '''Entropy encoding using Huffman and RLE. '''
        luma = Encoder(self.data[Y], LUMA).encode()
        chroma = Encoder(np.vstack((self.data[CB], self.data[CR])), CHROMA).encode()
        encoded = {LUMA: luma, CHROMA: chroma}

        ordered = (
            encoded[LUMA][DC], encoded[LUMA][AC],
            encoded[CHROMA][DC], encoded[CHROMA][DC]
        )

        bits = bitarray(''.join(ordered))
        self.encoded[DATA] = bits
        self.encoded[SLICE_LENGTH] = tuple(len(data) for data in ordered)
        self.encoded[FILLER_BITS] = bits2bytes(len(bits))*8 - len(bits)

    def decompress(self, obj):
        '''Extract data from compressed file.'''
        bits = obj.data.to01()
        h, w = obj.info[DIMS]
        quality = obj.info[QLTY]
        slice_len = obj.info[SLICE_LENGTH]
        filler = obj.info[FILLER_BITS]
        padding = obj.info[PAD]

        preprocessed = self._preprocess_compressed(bits, filler, slice_len)
        decoded = self._decode(preprocessed)
        dequant = self._dequantise(decoded)

        im = self._reshape(dequant, padding)

    def _preprocess_compressed(self, bits, filler, slice_len):
        if filler:
            bits = bits[:-filler]

        i, j, k = list(accumulate(slice_len))[:3]

        sliced = {
            LUMA: {
                DC: bits[:i],
                AC: bits[i:i+j]
            },
            CHROMA: {
                DC: bits[i+j:i+j+k],
                AC: bits[i+j+k:]
            }
        }

        return sliced

    def _decode(self, data):
        y = Decoder(data[LUMA], LUMA).decode()
        cb, cr = np.split(
            Decoder(data[CHROMA], CHROMA).decode(), 2
        )

        return {Y: y, CB: cb, CR: cr}

    def _dequantise(self, data, quality, h, w):
        for key, ch in data.items():
            for i, block in enumerate(ch):
                ch[i] = blk.quantise(block, key, quality, inverse=True)
                ch[i] = idct2d(ch[i])

            data[key] = blk.combine_blocks(ch, h, w)

        return data

    def _reshape(self, data, padding):
        data[Y] = img.offset(data[Y], inverse=True)
        data[CB] = img.remove_pad(data[CB], *padding[CB])
        data[CR] = img.remove_pad(data[CR], *padding[CR])

        data[CB] = img.upsample(data[CB])
        data[CR] = img.upsample(data[CR])

        im = img.stack_channels(*data.values())
        return img.ycbcr2rgb(im)



