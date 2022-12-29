import numpy as np
from config import QL, QC, Y, CB, CR, BLOCKSIZE

def slice_blocks(ch, blocksize=BLOCKSIZE):
    '''Slice a 2D array into N x M blocks.'''
    h, _ = ch.shape
    return ch.reshape(
        h//blocksize, blocksize, -1, blocksize
    ).swapaxes(1, 2).reshape(-1, blocksize, blocksize)

def combine_blocks(blocks, h, w):
    '''Reconstruct an image from N x M -sized blocks.'''
    _, n, m = blocks.shape
    return blocks.reshape(
        h // n, -1, n, m
    ).swapaxes(1, 2).reshape(h, w)

def quantise(block, mode, quality, inverse=False):
    '''Apply quantisation to a block.

    args:
        block: N x N square matrix
        mode: luma or chroma
        quality: float: desired quality of compressed image
        inverse: bool: perform dequantisation if True
    return:
        (de)quantised block
    '''
    if mode == Y:
        qtable = QL
    elif mode in (CB, CR):
        qtable = QC
    else:
        raise ValueError('mode has to be either chroma or luma')

    k = 5000/quality if quality < 50 else 200-2*quality
    q = qtable*k/100

    if inverse:
        return block*q
    return block/q
