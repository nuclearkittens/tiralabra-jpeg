import numpy as np
from PIL import Image

from config import COLOUR_MATRIX, K, MINVAL, MAXVAL
from util.linalg import dct2d

QL = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 48, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

QC = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]
])

HUFFMAN_AC = [
    [(0, 0), '1010'],
    [(0, 1), '00'],
    [(0, 2), '01'],
    [(0, 3), '100'],
    [(0, 4), '1011'],
    [(0, 5), '11010'],
    [(0, 6), '111100'],
    [(0, 7), '11111000'],
    [(0, 8), '1111110110'],
    [(0, 9), '1111111110000010'],
    [(0, 10), '1111111110000011'],
    [(1, 1), '1100'],
    [(1, 2), '111001'],
    [(1, 3), '1111001'],
    [(1, 4), '111110110'],
    [(1, 5), '11111110110'],
    [(1, 6), '1111111110000100'],
    [(1, 7), '1111111110000101'],
    [(1, 8), '1111111110000110'],
    [(1, 9), '1111111110000111'],
    [(1, 10), '1111111110001000'],
    [(2, 1), '11100'],
    [(2, 2), '11111001'],
    [(2, 3), '1111110111'],
    [(2, 4), '111111110100'],
    [(2, 5), '1111111110001001'],
    [(2, 6), '1111111110001010'],
    [(2, 7), '1111111110001011'],
    [(2, 8), '1111111110001100'],
    [(2, 9), '1111111110001101'],
    [(2, 10), '1111111110001110'],
    [(3, 1), '111010'],
    [(3, 2), '111110111'],
    [(3, 3), '111111110101'],
    [(3, 4), '1111111110001111'],
    [(3, 5), '1111111110010000'],
    [(3, 6), '1111111110010001'],
    [(3, 7), '1111111110010010'],
    [(3, 8), '1111111110010011'],
    [(3, 9), '1111111110010100'],
    [(3, 10), '1111111110010101'],
    [(4, 1), '111011'],
    [(4, 2), '1111111000'],
    [(4, 3), '1111111110010110'],
    [(4, 4), '1111111110010111'],
    [(4, 5), '1111111110011000'],
    [(4, 6), '1111111110011001'],
    [(4, 7), '1111111110011010'],
    [(4, 8), '1111111110011011'],
    [(4, 9), '1111111110011100'],
    [(4, 10), '1111111110011101'],
    [(5, 1), '1111010'],
    [(5, 2), '11111110111'],
    [(5, 3), '1111111110011110'],
    [(5, 4), '1111111110011111'],
    [(5, 5), '1111111110100000'],
    [(5, 6), '1111111110100001'],
    [(5, 7), '1111111110100010'],
    [(5, 8), '1111111110100011'],
    [(5, 9), '1111111110100100'],
    [(5, 10), '1111111110100101'],
    [(6, 1), '1111011'],
    [(6, 2), '111111110110'],
    [(6, 3), '1111111110100110'],
    [(6, 4), '1111111110100111'],
    [(6, 5), '1111111110101000'],
    [(6, 6), '1111111110101001'],
    [(6, 7), '1111111110101010'],
    [(6, 8), '1111111110101011'],
    [(6, 9), '1111111110101100'],
    [(6, 10), '1111111110101101'],
    [(7, 1), '11111010'],
    [(7, 2), '111111110111'],
    [(7, 3), '1111111110101110'],
    [(7, 4), '1111111110101111'],
    [(7, 5), '1111111110110000'],
    [(7, 6), '1111111110110001'],
    [(7, 7), '1111111110110010'],
    [(7, 8), '1111111110110011'],
    [(7, 9), '1111111110110100'],
    [(7, 10), '1111111110110101'],
    [(8, 1), '111111000'],
    [(8, 2), '111111111000000'],
    [(8, 3), '1111111110110110'],
    [(8, 4), '1111111110110111'],
    [(8, 5), '1111111110111000'],
    [(8, 6), '1111111110111001'],
    [(8, 7), '1111111110111010'],
    [(8, 8), '1111111110111011'],
    [(8, 9), '1111111110111100'],
    [(8, 10), '1111111110111101'],
    [(9, 1), '111111001'],
    [(9, 2), '1111111110111110'],
    [(9, 3), '1111111110111111'],
    [(9, 4), '1111111111000000'],
    [(9, 5), '1111111111000001'],
    [(9, 6), '1111111111000010'],
    [(9, 7), '1111111111000011'],
    [(9, 8), '1111111111000100'],
    [(9, 9), '1111111111000101'],
    [(9, 10), '1111111111000110'],
    [(10, 1), '111111010']
]

HUFFMAN_DC = [
    [(0, 0), '00'],
    [(0, 1), '010'],
    [(0, 2), '011'],
    [(0, 3), '100'],
    [(0, 4), '101'],
    [(0, 5), '110'],
    [(0, 6), '1110'],
    [(0, 7), '11110'],
    [(0, 8), '111110'],
    [(0, 9), '1111110'],
    [(0, 10), '11111110'],
    [(0, 11), '111111110']
]

def example():
    # im = np.array(Image.open('src/data/rgb2-1024x1024.tif'))
    ch1 = np.random.randint(256, size=(64, 64))
    ch2 = np.random.randint(256, size=(64, 64))
    ch3 = np.random.randint(256, size=(64, 64))
    im = stack_channels(ch1, ch2, ch3)
    ycbcr = rgb2ycbcr(im)
    y, cb, cr = downsample(ycbcr)

    # blocksize = 8
    y_blx = quantise(y, 'luma')
    cb_blx = quantise(cb, 'chroma')
    cr_blx = quantise(cr, 'chroma')

    y_zz = rle(zigzag(y_blx))
    cb_zz = rle(zigzag(cb_blx))
    cr_zz = rle(zigzag(cr_blx))

    y_huff = huffman(y_zz)
    cb_huff = huffman(cb_zz)
    cr_huff = huffman(cr_zz)

    print(y_huff)





def rgb2ycbcr(im):
    rgb = im.astype(np.float32)
    ycbcr = rgb.dot(COLOUR_MATRIX)
    ycbcr[:,:,[1,2]] += K
    return ycbcr.astype(np.uint8)

def ycbcr2rgb(im):
    ycbcr = im.astype(np.float32)
    ycbcr[:,:,[1,2]] -= K
    rgb = ycbcr.dot(np.linalg.inv(COLOUR_MATRIX))
    np.putmask(rgb, rgb > MAXVAL, MAXVAL)
    np.putmask(rgb, rgb < MINVAL, MINVAL)
    return rgb.astype(np.uint8)

def get_channels(im):
    ch1 = im[:,:,0]
    ch2 = im[:,:,1]
    ch3 = im[:,:,2]
    return ch1, ch2, ch3

def stack_channels(ch1, ch2, ch3):
    return np.dstack((ch1, ch2, ch3))

def downsample(im):
    def ds(ch):
        # ch_copy = ch.copy()
        # ch_copy[1::2,:] = ch_copy[::2,:]
        # ch_copy[:,1::2] = ch_copy[:,::2]
        # return ch_copy
        return ch[::2,::2]
    y, cb, cr = get_channels(im)
    cb = ds(cb)
    cr = ds(cr)
    return y, cb, cr

def quantise(ch, mode, blocksize=8):
    blocks = []
    for i in range(ch.shape[0]//blocksize):
        for j in range(ch.shape[1]//8):
            block = ch[
                i*blocksize:(i+1)*blocksize,
                j*blocksize:(j+1)*blocksize
            ]
            block = block.astype(np.int16)-K
            block = dct2d(block.astype(np.float32))
            if mode == 'chroma':
                quantised = block * QC
            elif mode == 'luma':
                quantised = block * QL
            else:
                raise(ValueError)
            blocks.append(quantised.astype(np.int16))

    return blocks

def zigzag(blocks, blocksize=8):
    temp = [[] for _ in range(blocksize*2-1)]
    for i in range(blocksize):
        for j in range(blocksize):
            k = i+j
            if k%2 == 0:
                print(blocks[i][j])
                temp[k].insert(0, blocks[i][j])
            else:
                temp[k].append(blocks[i][j])

    zigzag = []
    # for sublst in temp:
    #     for elem in range(len[sublst]):
    #         print(elem)
    #         zigzag.append(elem)

    return zigzag

def rle(lst):
    i = 0
    n = len(lst)

    res = []
    while i < n:
        count = 1
        while i < n-1 and lst[i] == lst[i+1]:
            count += 1
            i += 1
        res.append((lst[i], count))
        i += 1

    return np.asarray(res)

def get_complement(bitstr):
    complement = ''
    for i in range(len(bitstr)):
        if bitstr[i] == '0':
            complement += '1'
        else:
            complement += '0'

    return complement

def huffman_fwd(arr):
    out = []
    zeros = 0

    for i in range(arr.shape[0]):
        x = arr[i][0]
        if x == 0:
            zeros += arr[i][1]
        elif x < 0:
            out.append(((zeros, len(bin(x)[3:])), x))
            zeros = 0
        else:
            out.append(((zeros, len(bin(x)[2:])), x))
            zeros = 0

    out.append((0, 0))
    return out

def huffman(arr):
    out = huffman_fwd(arr)
    bitstr = ''

    n = len(out)
    for coef in range(n-1):
        cat = out[coef][0]
        base = out[coef][1]
        if coef == 0:
            bitstr += _get_bitstr(cat, base, HUFFMAN_DC)
        else:
            bitstr += _get_bitstr(cat, base, HUFFMAN_AC)

    return bitstr

def _get_bitstr(cat, base, table):
    for code in table:
        if code[0] == cat:
            if base < 0:
                s = get_complement(bin(base[3:]))
            else:
                s = bin(base[2:])
            return code[1] + s

    return ''
