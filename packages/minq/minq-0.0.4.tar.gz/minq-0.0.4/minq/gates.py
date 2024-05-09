import numpy as np

I = np.identity(2)
'''Identity transform'''

X = np.array([
    [0, 1],
    [1, 0],
])
'''Bit-flip transform'''

Z = np.array([
    [1, 0],
    [0, -1],
])
'''Phase-flip transform'''

H = (1 / np.sqrt(2)) * np.array([
    [1, 1],
    [1, -1],
])
'''Hadamard transform'''
