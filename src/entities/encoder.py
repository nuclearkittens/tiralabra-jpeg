'''Encoder module for JPEG compression.'''
import util.huffman as huff
import util.run_length as rle
import util.zigzag as zz

from config import DC, AC

class Encoder:
    '''Encoder for JPEG compression.

    params:
        data: dict: luminance and chrominance data of
            an image channel
        mode: luma or chroma
        dc: list: DC values for blocks
        ac: list: AC values for blocks
    '''
    def __init__(self, data, mode):
        self._data = data
        self._mode = mode
        self._dc = None
        self._ac = None

    def encode(self):
        '''Encode DC and AC using predetermined JPEG
        Huffman tables.'''
        res = {}
        # s = ''
        # for val in self.dc:
        #     s += huff.encode(val, self.mode)
        # res[DC] = s
        res[DC] = ''.join(huff.encode(val, self.mode) for val in self.dc)

        # s = ''
        # for val in self.ac:
        #     s += huff.encode(val, self.mode)
        # res[AC] = s
        res[AC] = ''.join(huff.encode(val, self.mode) for val in self.ac)

        return res

    def _calc_dc(self):
        self._dc = tuple(rle.encode_differential(self.data[:, 0, 0]))

    def _calc_ac(self):
        self._ac = []
        for block in self._data:
            self._ac.extend(
                rle.encode_run_length(
                    tuple(zz.forward(block))[1:]
                )
            )

    @property
    def data(self):
        '''Return chrominance and luminance data points.'''
        return self._data

    @property
    def mode(self):
        '''Return the mode of the channel (luminance or chrominance).'''
        return self._mode

    @property
    def dc(self):
        '''Calculate and return the DC values.'''
        if not self._dc:
            self._calc_dc()
        return self._dc

    @dc.setter
    def dc(self, val):
        '''Set the DC values.'''
        self._dc = val

    @property
    def ac(self):
        '''Calculate and return the AC values.'''
        if not self._ac:
            self._calc_ac()
        return self._ac

    @ac.setter
    def ac(self, val):
        '''Set the AC values.'''
        self._ac = val
