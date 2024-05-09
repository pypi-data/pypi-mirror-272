from functools import reduce
from numpy.typing import ArrayLike
from typing import Iterable

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

def ket(*args: int | str):
    '''Creates a standard basis vector'''
    if len(args) == 0:
        return np.array([1])
    elif isinstance(args[0], int):
        assert all(b == 0 or b == 1 for b in args)
        x = np.zeros(2 ** len(args))
        x[from_binary(args)] = 1
        return x
    elif isinstance(args[0], str):
        assert len(args) == 1
        x = np.zeros(2 ** len(args[0]))
        x[int(args[0], base=2)] = 1
        return x
    else:
        raise TypeError('ket(...) takes either int or str')

def kron(*arrays: ArrayLike) -> np.ndarray:
    '''Computes the Kronecker product (tensor product) of the given arrays'''
    assert len(arrays) > 0
    return reduce(np.kron, arrays)

def kronpow(array: ArrayLike, n: int) -> np.ndarray:
    '''Applies the Kronecker product n times'''
    assert n > 0
    return reduce(lambda acc, _: np.kron(acc, array), range(n - 1), array)

def from_binary(bits: Iterable[int]) -> int:
    '''Converts a list of bits to the corresponding number when interpreted in base 2'''
    return 0 if len(bits) == 0 else int(''.join(map(str, bits)), base=2)
