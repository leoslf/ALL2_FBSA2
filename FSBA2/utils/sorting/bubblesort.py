import sys
sys.path.append(".")
from ._import import *

def bubblesort(l: list, f=None) -> list:
    """
    bubblesort


    Parameters
    ----------------
    l : list
        list to be sorted
    f : f(a, b) -> int
        comparator function


    Returns
    ----------------
    list
        The sorted list
    """
    if f is None:
        f = default_cmp

    n = len(l) - 1

    swapped = True
    while swapped == True:
        swapped = False
        for i in range(n):
            if f(l[i], l[i + 1]) > 0:
                l[i], l[i + 1] = l[i + 1], l[i]
                swapped = True
        n -= 1

    return l



