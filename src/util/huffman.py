'''Huffman encoding.'''
import collections

from config import HUFFMAN_CATEGORIES, HUFFMAN_TABLES, EOB, ZRL, DC, AC

DC_MAX = 2048
AC_MAX = 1024

SLICE_LENGTH = 16

def encode(val, mode):
    '''Encode Huffman coding of given value.

    args:
        val: int/tuple: DC/AC coefficient
        mode: luma or chroma

    return:
        str: encoded binary string
    '''

    def get_index(table, val):
        '''Get index of given value.'''
        for i, row in enumerate(table):
            for j, elem in enumerate(row):
                if val == elem:
                    return (i, j)
        raise ValueError(f'{val} not in table')

    # differential DC if val is an integer
    if not isinstance(val, collections.Iterable):
        if abs(val) >= DC_MAX:
            raise ValueError(f'invalid DC value: {val}')
        size, idx = get_index(HUFFMAN_CATEGORIES, val)
        if size == 0:
            return HUFFMAN_TABLES[DC][mode][size]
        return HUFFMAN_TABLES[DC][mode][size] + '{:0{pad}b}'.format(idx, pad=size)

    val = tuple(val)
    if val in (EOB, ZRL):
        return HUFFMAN_TABLES[AC][mode][val]

    # run length AC if val is tuple
    run, cat = val
    if abs(cat) >= AC_MAX or cat == 0:
        raise ValueError('invalid AC value')

    # get the size and index from the Huffman category table by
    # using the (non-zero) category value; concatenate into bin str
    size, idx = get_index(HUFFMAN_CATEGORIES, cat)
    return HUFFMAN_TABLES[AC][mode][(run, size)] + '{:0{pad}b}'.format(idx, pad=size)

def decode(binstr, curr, mode):
    '''Decode given binary string.'''
    pass
