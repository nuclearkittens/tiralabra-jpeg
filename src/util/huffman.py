'''Huffman encoding.'''
from config import HUFFMAN_CATEGORIES, HUFFMAN_TABLES, EOB, ZRL

DC = 'DC'
AC = 'AC'
DC_MAX = 2048
AC_MAX = 1024

SLICE_LENGTH = 16

def encode(val, mode):
    '''Encode Huffman coding of given value.

    args:
        val: int/tuple: DC/AC coefficient
        mode: luma or chroma

    return:
        str: encoded bit string
    '''

    def get_index(table, val):
        '''Get index of given value.'''
        for i, row in enumerate(table):
            for j, elem in enumerate(row):
                if val == elem:
                    return (i, j)
        raise ValueError(f'{val} not in {table}')

    # differential DC if val is an integer
    if isinstance(val, int):
        if abs(val) >= DC_MAX:
            raise ValueError('invalid DC value')
        size, idx = get_index(HUFFMAN_CATEGORIES, val)
        if size == 0:
            return HUFFMAN_TABLES[DC][mode][size]
        return HUFFMAN_TABLES[DC][mode][size] + '{:{pad}b'.format(idx, pad=size)

    # check if end of block or zero run length
    if val in (EOB, ZRL):
        return HUFFMAN_TABLES[AC][mode][val]

    # run length AC if val is tuple
    run, cat = val
    if abs(cat) >= AC_MAX or cat == 0:
        raise ValueError('invalid AC value')

    size, idx = get_index(HUFFMAN_CATEGORIES, cat)
    return HUFFMAN_TABLES[AC][mode][(run, size)] + '{:{pad}b'.format(idx, pad=size)

def decode(bitstr, curr, mode):
    '''Decode given bit string.

    args:
        bitstr: str: encoded bit string
        curr: AC or DC (type of current)
        mode: chroma or luma

    return:
        generator with decoded value (int/DC or tuple/AC)
    '''
    def get_diff_value(idx, size):
        diff = bitstr[idx:idx+size]
        return int(diff, 2)

    i = 0
    while i < len(bitstr):
        left = len(bitstr) - i
        k = SLICE_LENGTH if left > SLICE_LENGTH else left
        sliced = bitstr[i:i+k]

        while sliced:
            if sliced in HUFFMAN_TABLES[curr][mode].inv:
                key = HUFFMAN_TABLES[curr][mode].inv[sliced]
                if curr == DC:
                    size = key
                    if size == 0:
                        yield 0
                    else:
                        k = get_diff_value(i+len(sliced), size)
                        yield HUFFMAN_CATEGORIES[size][k]
                else:
                    run, size = key
                    if key in (EOB, ZRL):
                        yield key
                    else:
                        k = get_diff_value(i+len(sliced), size)
                        yield (run, HUFFMAN_CATEGORIES[size][k])
                i += len(sliced)+size
                break

        sliced = sliced[:-1]
