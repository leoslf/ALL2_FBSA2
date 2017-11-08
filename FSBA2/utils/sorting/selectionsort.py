from ._import import *

def selectionsort(l: list, f = None) -> list:
    """
    selectionsort


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

    for i in range(len(l) - 1):
        min_index = i
        for j in range(i + 1, len(l)):
            if f(l[j], l[min_index]) < 0:
                min_index = j

        l[min_index], l[i] = l[i], l[min_index]
    return l

