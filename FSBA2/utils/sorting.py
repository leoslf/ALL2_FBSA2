from .comparator import *

def msort(l, f=None):
    if f is None:
        f = default_cmp
    return __msort(l, f)

def __msort(l, f):
    if len(l) <= 1:
        return l
    m = len(l) // 2
    return merge(__msort(l[:m], f), __msort(l[m:], f), f)

def merge(a, b, f):
    ret = []
    while len(a) > 0 and len(b) > 0:
        ret.append((a if f(a[0], b[0]) < 0 else b).pop(0))
    ret.extend(a if len(a) > 0 else b)
    return ret



