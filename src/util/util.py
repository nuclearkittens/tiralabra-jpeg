def uint2binstr(val, size):
    return bin(val)[2:][-size:].zfill(size)

def int2binstr(x):
    def flip(binstr):
        return ''.join(map(lambda x: '0' if x == 1 else '1', binstr))

    if x == 0:
        return ''

    binstr = bin(abs(x))[2:]
    return binstr if x > 0 else flip(binstr)

def flatten(lst):
    return [elem for sublst in lst for elem in sublst]

def calc_bits(x):
    x = abs(x)
    res = 0

    while x > 0:
        x >>= 1
        res += 1

    return res