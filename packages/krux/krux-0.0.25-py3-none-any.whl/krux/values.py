__all__ = ['none_min', 'none_max']


def none_min(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return min(a, b)


def none_max(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return max(a, b)
