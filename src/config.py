'''Environmental variables.'''
import numpy as np

''' ITU-R BT.601 conversion'''
KR = 0.299
KG = 0.587
KB = 0.114

COLOUR_MATRIX = np.array([
    [KR, -0.5*(KR/(1-KB)), 0.5],
    [KG, -0.5*(KG/(1-KB)), -0.5*(KG/(1-KR))],
    [KB, 0.5, -0.5*(KB/(1-KR))], 
])

MINVAL = 0
MAXVAL = 255
K = round((MAXVAL-MINVAL)/2)
