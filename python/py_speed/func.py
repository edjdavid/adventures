
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


def func_slow(N):
    d = 0.0
    for i in range(N):
        d += (i % 3 - 1) * i
    return d


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
