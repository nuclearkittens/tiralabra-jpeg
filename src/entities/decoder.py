'''Decoder module for JPEG compression.'''
import numpy as np

from config import EOB, AC, DC, BLOCKSIZE
import util.huffman as huff
import util.run_length as rle
import util.zigzag as zz

class Decoder:
    '''Decoder for JPEG compression.

    params:
        data: dict: DC/AC data as bitstrings
        mode: luma or chroma
        dc: list: DC values of blocks
        ac: list: AC values of blocks
    '''
    def __init__(self, data, mode):
        self._data = data
        self._mode = mode
        self._dc = None
        self._ac = None

    def decode(self):
        res = {}
        res = np.array(
            tuple(zz.backward((dc, )+ac, size=BLOCKSIZE)
            for dc, ac in zip(self.dc, self.ac))
        )
        return res

    def _calc_dc(self):
        self._dc = tuple(rle.decode_differential(
            huff.decode(self.data[DC], DC, self.mode)
        ))

    def _calc_ac(self):
        def split_iter(iter, splitter):
            res = []
            for elem in iter:
                res.append(elem)
                if elem == splitter:
                    yield res
                    res = []

        self._ac = tuple(
            rle.decode_run_length(data) for data in split_iter(
                huff.decode(self.data[AC], AC, self.mode), EOB
            )
        )

    @property
    def data(self):
        return self._data

    @property
    def mode(self):
        return self._mode

    @property
    def dc(self):
        if not self._dc:
            self._calc_dc()
        return self._dc

    @property
    def ac(self):
        if not self._ac:
            self._calc_ac()
        return self._ac
