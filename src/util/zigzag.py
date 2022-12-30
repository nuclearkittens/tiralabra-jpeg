'''Module for iterating a matrix in a zigzag manner.'''
from math import floor, sqrt
import numpy as np


def move(i, j, size):
    '''Move to the next coordinate in a matrix
    in a zigzag order.'''
    if j < size-1:
        return (max(0, i-1), j+1)
    return (i+1, j)

def _next_square(val):
    '''Return next perfect square of given value.'''
    return (floor(sqrt(val))+1) ** 2

def forward(data):
    '''Iterate over a matrix in a zigzag manner.'''
    i = 0
    j = 0
    for _ in np.nditer(data):
        yield data[j][i]

        size = data.shape[0]
        if (i+j) % 2 == 1:
            i, j = move(i, j, size)
        else:
            j, i = move(j, i, size)

def backward(data, size=None, fill=0):
    '''Reconstruct a matrix from an array.'''
    n = len(data)
    if not size:
        size = _next_square(n)

    data = tuple(data)+(fill,)*(size**2-n)
    res = np.empty((size, size), dtype=int)
    i = 0
    j = 0

    for val in data:
        res[j][i] = val
        if (i+j)%2 == 1:
            i, j = move(i, j, size)
        else:
            j, i = move(j, i, size)

    return res
