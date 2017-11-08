import numbers

def default_cmp(a, b):
    if all(isinstance(x, numbers.Number) for x in (a, b)):
        return a - b

    a = str(a)
    b = str(b)
    if all(x.isdigit() for x in (a, b)):
        return float(a) - float(b)
    else:
        if a == b:
            return 0
        elif a < b:
            return -1
        else:
            return 1

