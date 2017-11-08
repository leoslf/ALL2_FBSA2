import sys
sys.path.append(".")
from ._import import *

def msort(l: list, f=None) -> list:
    """
    mergesort
    =========
    Mergesort


    Parameters
    ----------------
    l : list
        list to be sorted

    f : f(a, b) -> int
        comparator function


    Returns
    ----------------
    list
        The sorted list.
    """
    if f is None:
        f = default_cmp 
    return list(__msort(deque(l), f))


def __msort(q: deque, f) -> deque:
    """
    __msort
    ========


    Parameters
    ----------------
    q : deque
        sub-list to be sorted
    
    f : f(a, b) -> int
        Comparator function


    Returns
    ----------------
    deque
        The merged sorted sub-list
    """

    n = len(q)
    if n < 2:
        return q
    n //= 2
    return merge(__msort(deque(islice(q, n)), f), __msort(deque(islice(q, n, None)), f), f)

def merge(a: deque, b: deque, f) -> deque:
    """
    Merge Function
    ==============
    Merge Function


    Parameters
    ----------------
    a : deque
        The first sorted sub-list
    b : deque
        The second sorted sub-list
    f : f(a, b) -> int 
        Comparator function


    Returns
    ----------------
    deque
        Merged sorted sublist
    """
    ret = deque()

    while len(a) > 0 and len(b) > 0:
        ret.append((a if f(a[0], b[0]) < 0 else b).popleft())

    return ret + (a if len(a) > 0 else b)



