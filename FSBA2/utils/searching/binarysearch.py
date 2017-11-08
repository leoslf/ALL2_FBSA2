from ._import import *

def binarysearch_pos(l: list, value, f = None, lo: int = 0, hi: int = None) -> int:
    """
    binarysearch_pos


    Parameters
    ----------------
    l : list
        list that may contains the value given
    value : 
        value to be searched
    f : f(a, b) -> int
        comparator function
    lo : int
        lower bound of sub-list
    hi : int
        upper bound of sub-list, inclusive


    Returns
    ----------------
    int
        The position / index if value was found, returning -1 otherwise.
    """
    if hi is None:
        hi = len(l) - 1
    if f is None:
        f = default_cmp
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        cmp_result = f(value, l[mid])

        # found
        if cmp_result == 0:
            return mid

        # value < l[mid]
        if cmp_result < 0:
            hi = mid - 1
        # value > l[mid]
        else:
            lo = mid + 1

    return -1

def binarysearch(l: list, value, f = None) -> bool:
    """
    binarysearch


    Parameters
    ----------------
    l : list
        list that may contain the value given
    value : 
        value to be searched
    f : f(a, b) -> int
        comparator function


    Returns
    ----------------
    bool
        the boolean value whether the result was found.
    """
    return binarysearch_pos(l, value, f) != -1

