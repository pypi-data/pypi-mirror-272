def from_binary(*bits: int) -> int:
    '''Converts a list of bits to the corresponding number when interpreted in base 2'''
    return 0 if len(bits) == 0 else int(''.join(map(str, bits)), base=2)
