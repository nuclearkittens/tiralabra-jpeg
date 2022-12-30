'''Module for encoding/decoding differential (DC) and
run-length (AC) values.'''
from itertools import groupby, accumulate

from config import EOB, ZRL

SLICE_LENGTH = 16

def encode_differential(data):
    '''Iterate through data points and append the
    difference between the current and previous
    element to the resulting sequence.
    '''
    # res = []
    # for i, elem in enumerate(data):
    #     if i:
    #         res.append(elem-data[i-1])
    #     else:
    #         res.append(elem)
    # return tuple(res)
    res = (elem-data[i-1] if i else elem for i, elem in enumerate(data))
    return res

def decode_differential(data):
    '''Return decoded DC values by accumulating the
    sums of data points.'''
    return accumulate(data)

def encode_run_length(data):
    '''Iterate through grouped data points (length, key pairs)
    and append the run-length encoded data to the resulting
    list.
    '''
    groups = [(len(tuple(group)), key) for key, group in groupby(data)]
    res = []
    borrow_pair = False

    if groups[-1][1] == 0:
        del groups[-1]

    for i, (l, key) in enumerate(groups):
        if borrow_pair:
            l -= 1
            borrow_pair = False

        if l == 0:
            continue

        if key == 0:
            while l >= SLICE_LENGTH:
                res.append(ZRL)
                l -= SLICE_LENGTH
            res.append((l, groups[i+1][1]))
            borrow_pair = True
        else:
            res.extend(((0, key),)*l)

    return res + [EOB]

def decode_run_length(data):
    '''Decode run-length encoded data and return the
    original values.
    '''
    res = tuple(elem for l, k in data for elem in [0]*l+[k])
    return res[:-1]
