def hex2tuple(s):
    return tuple(int(s[i:i+2], 16) for i in range(0, len(s), 2))

def divi(n, divisor) -> int:
    assert divisor != 0
    return int(n / divisor)

def scalei(n, scale) -> int:
    return int(n * scale)
