from .comparator import *

def linearsearch_pos(l: list, value, f=None) -> int:
    """
    linearsearch_pos


    Parameters
    ----------------
    l : list
        the list that may contain value given
    value :
        the value to be searched
    f : f(a, b) -> int
        comparator function


    Returns
    ----------------
    int
        the position of first match of value, returning -1 if not found
    """
    if f is None:
        f = default_cmp

    for i, x in enumerate(l):
        if f(x, value) == 0:
            return i
    return -1

def linearsearch(l: list, value, f=None) -> bool:
    """
    linearsearch


    Parameters
    ----------------
    l : list
        list that may contain value given
    value :
        value to be searched
    f : f(a, b) -> int
        comparator function

    Returns
    ----------------
    bool
        the state whether the value was found
    """
    return linearsearch_pos(l, value, f) != -1

def linearsearch_table(l: list, filter_str, f=None) -> list:
    assert len(l) > 0

    ret = [False] * len(l)

    if f is None:
        f = default_cmp

    for i in range(len(l)):
         ret[i] = linearsearch(l[i], filter_str, f)

    return ret
