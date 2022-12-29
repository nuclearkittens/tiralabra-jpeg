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
        str: encoded bit string
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

    # FIXME: something is wrong here ):
    # check if end of block or zero run length

    val = tuple(val)
    if val in (EOB, ZRL):
        return HUFFMAN_TABLES[AC][mode][val]

    # run length AC if val is tuple
    run, cat = val
    if abs(cat) >= AC_MAX or cat == 0:
        raise ValueError('invalid AC value')

    # get the size and index from the Huffman
    # category table by using the (non-zero)
    # category value; concatenate into bin str
    size, idx = get_index(HUFFMAN_CATEGORIES, cat)
    return HUFFMAN_TABLES[AC][mode][(run, size)] + '{:0{pad}b}'.format(idx, pad=size)

# def decode(bitstr, curr, mode):
#     '''Decode given bit string.

#     args:
#         bitstr: str: encoded bit string
#         curr: AC or DC (type of current)
#         mode: chroma or luma

#     return:
#         generator with decoded value (int/DC or tuple/AC)
#     '''
#     def get_diff_value(idx, size):
#         diff = bitstr[idx:idx+size]
#         return int(diff, 2)

#     res = []
#     inv_huff = HUFFMAN_TABLES[curr][mode].inv
#     i = 0
#     print('decoding huffman...')
#     n = len(bitstr)
#     print(n)
#     while i < n:
#         print(f'i: {i}')
#         # slice the string into smaller slices
#         left = n-i
#         k = SLICE_LENGTH if left > SLICE_LENGTH else left
#         sliced = bitstr[i:i+k]

#         while sliced:
#             # check if sliced str is in the inverse mapping
#             # of the Huffman tables; yield decoded val
#             l = len(sliced)
#             if sliced in inv_huff:
#                 key = inv_huff[sliced]
#                 if curr == DC:
#                     size = key
#                     if size == 0:
#                         # yield 0
#                         res.append(0)
#                     else:
#                         k = get_diff_value(i+l, size)
#                         # yield HUFFMAN_CATEGORIES[size][k]
#                         res.append(HUFFMAN_CATEGORIES[size][k])
#                 else:
#                     run, size = key
#                     if key in (EOB, ZRL):
#                         yield key
#                     else:
#                         k = get_diff_value(i+l, size)
#                         # yield (run, HUFFMAN_CATEGORIES[size][k])
#                         res.append((run, HUFFMAN_CATEGORIES[size][k]))
#                 # skip over decoded bits
#                 i += l+size
#                 break
#             sliced = sliced[:-1]

#     return res

def decode(bit_seq, dc_ac, layer_type):
    """Decode a bit sequence encoded by JPEG baseline Huffman table.

    Arguments:
        bit_seq {str} -- The encoded bit sequence.
        dc_ac {DC or AC} -- The type of current.
        layer_type {LUMINANCE or CHROMINANCE} -- The layer type of bit sequence.

    Raises:
        IndexError -- When there is not enough bits in bit sequence to decode
            DIFF value codeword.
        KeyError -- When not able to find any prefix in current slice of bit
            sequence in Huffman table.

    Returns:
        Generator -- A generator and its item is decoded value which could be an
            integer (differential DC) or a tuple (run-length-encoded AC).
    """

    def diff_value(idx, size):
        if idx >= len(bit_seq) or idx + size > len(bit_seq):
            raise IndexError('There is not enough bits to decode DIFF value '
                             'codeword.')
        fixed = bit_seq[idx:idx + size]
        return int(fixed, 2)

    current_idx = 0
    print(len(bit_seq))
    while current_idx < len(bit_seq):
        #   1. Consume next 16 bits as `current_slice`.
        #   2. Try to find the `current_slice` in Huffman table.
        #   3. If found, yield the corresponding key and go to step 4.
        #      Otherwise, remove the last element in `current_slice` and go to
        #      step 2.
        #   4. Consume next n bits, where n is the category (size) in returned
        #      key yielded in step 3. Use those info to decode the data.
        remaining_len = len(bit_seq) - current_idx
        current_slice = bit_seq[
            current_idx:
            current_idx + (16 if remaining_len > 16 else remaining_len)
        ]
        err_cache = current_slice
        while current_slice:
            if (current_slice in
                    HUFFMAN_TABLES[dc_ac][layer_type].inv):
                key = (HUFFMAN_TABLES[dc_ac][layer_type]
                       .inv[current_slice])
                print(f'slice: {current_slice}, key: {key}')
                if dc_ac == DC:  # DC
                    size = key
                    if size == 0:
                        yield 0
                    else:
                        yield HUFFMAN_CATEGORIES[size][diff_value(
                            current_idx + len(current_slice),
                            size
                        )]
                else:  # AC
                    run, size = key
                    if key in (EOB, ZRL):
                        yield key
                    else:
                        yield (run, HUFFMAN_CATEGORIES[size][diff_value(
                            current_idx + len(current_slice),
                            size
                        )])

                current_idx += len(current_slice) + size
                # print(current_idx)
                break
            current_slice = current_slice[:-1]
        else:
            raise KeyError(
                f'Cannot find any prefix of {err_cache} in Huffman table.'
            )