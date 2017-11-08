from ._import import *

def qsort(l: list, f=None, lo=0, hi=None) -> list:
    """
    Quicksort
    ---------
    Quicksort: A kind of Divide and Conquer sorting algorithm that first selects a value, i.e. the pivot value.

    The role of the pivot is to help splitting the list, with aid of the partition function, which divides the sub-list into three partitions: <pivot, the pivot itself and then >= pivot.

    It will then recursive call on the <pivot and >=pivot partitions until there is 0 or 1 elements in the sub-list (recursion base case)

    In this implementation, the first element in sub-list is picked as the pivot.


    Parameters
    ----------------
    l : list
        list to be sorted
    f : f(a, b) -> int
        comparator function f(a, b) that compares two elements, returns negative if a < b; 0 if a == b, positive if a > b
    lo : int
        lower bound of sub-list being sorted
    hi : int
        upper bound of sub-list being sorted, inclusive
        


    Returns
    ----------------
    list
        The sorted list.
    """


    # using function return as default argument is not allowed in python, None is used as placeholder
    if hi is None:
        hi = len(l) - 1

    if hi - lo <= 1:
        return l

    if f is None:
        f = default_cmp

    print("quicksort(",l[lo:hi + 1],", %d, %d)" %(lo, hi))

    pivot = __partition(f, l, lo, hi, lo)
    qsort(l, f, lo, pivot - 1)
    qsort(l, f, pivot + 1, hi)
    
    return l

def __partition(f, l, lo, hi, pivot_idx) -> int:
    """
    Partition function
    ------------------
    Partition function: A helper function of quicksort that puts the given pivot (by index) to correct position in the sub-list.

    sub-list: (defined with lo <= x <= hi, where x is the element in the sub-list)

    correct position of pivot: the position with the elements with lower indices are less than pivot, else in the higher indices.

    Parameters
    ---------
    f : f(a, b) -> int
        comparator function
    l : list
        list to be sorted
    lo : int
        lower bound
    hi : int
        upper bound
    pivot_idx : int
        original index of pivot chosen


    Returns
    -------
    int 
        The new index of the pivot chosen.
    """
    if not (lo <= pivot_idx <= hi):
        raise ValueError("pivot must lie between lo and hi inclusive")

    if lo == hi:
        return lo

    

    # swap the pivot to the lower bound
    l[lo], l[pivot_idx] = l[pivot_idx], l[lo]
    
    

    # now continue as it picks lower bound as pivot
    pivot = l[lo]

    # initialize i and j with index just 1 higher than the pivot
    i = j = lo + 1
    # i: index points to the first element in sublist that >= pivot
    # j: index points to the element to be compared with the pivot

    # loop until j approaches upper bound
    while j <= hi: # cleaner to use while loop in python
        # swap if l[j] < pivot 
        if f(l[j], pivot) <= 0:
            l[i], l[j] = l[j], l[i]
            i += 1
        j += 1
    
    # swap the pivot to the correct position
    # although the value originally on index i - 1 might be closer to pivot, but this is more efficient than performing array insertion, left shifting and place pivot into the correct position.
    l[lo], l[i - 1] = l[i - 1], l[lo]

    # return the index just before the (>=) partition, i.e. the pivot index
    return i - 1


