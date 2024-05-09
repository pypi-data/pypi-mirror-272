from functools import reduce
from numpy.typing import ArrayLike, NDArray
from typing import Any, cast

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
        x[from_binary(*cast(tuple[int, ...], args))] = 1
        return x
    else:
        assert len(args) == 1
        x = np.zeros(2 ** len(args[0]))
        x[int(args[0], base=2)] = 1
        return x

def kron(*arrays: ArrayLike) -> NDArray[Any]:
    '''Computes the Kronecker product (tensor product) of the given arrays'''
    assert len(arrays) > 0
    return reduce(np.kron, arrays)

def kronpow(array: ArrayLike, n: int) -> NDArray[Any]:
    '''Applies the Kronecker product n times'''
    assert n > 0
    return reduce(lambda acc, _: np.kron(acc, array), range(n - 1), array)

def from_binary(*bits: int) -> int:
    '''Converts a list of bits to the corresponding number when interpreted in base 2'''
    return 0 if len(bits) == 0 else int(''.join(map(str, bits)), base=2)
