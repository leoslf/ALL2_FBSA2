def hex2tuple(s):
    return tuple(int(s[i:i+2], 16) for i in range(0, len(s), 2))
