from util.util import *

SLICE_LEN = 15

def encode(arr):
    nonzero = -1
    for i, elem in enumerate(arr):
        if elem != 0:
            nonzero = i

    res = dict()
    run_length = 0
    for i, elem in enumerate(arr):
        if i > nonzero:
            res[(0, 0)] = int2binstr(0)
            break
        elif elem == 0 and run_length < SLICE_LEN:
            run_length += 1
        else:
            size = calc_bits(elem)
            res [(run_length, size)] = int2binstr(elem)
            run_length = 0

    return res
