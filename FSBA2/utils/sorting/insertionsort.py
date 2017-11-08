import sys
sys.path.append(".")
from ._import import *

def insertionsort(l: list, f=None) -> list: 
    """
    insertionsort


    Parameters
    ----------------
    l : list
        list to be sorted
    f : f(a, b) -> int
        comparator function


    Returns
    ---------------
    list 
        The sorted list
    """
    if f is None:
        f = default_cmp

    for i in range(1, len(l)):
        value = l[i]
        j = i
        
        while j > 0 and f(l[j - 1], value) > 0:
            l[j] = l[j - 1]
            j -= 1

        l[j] = value
        
    return l



