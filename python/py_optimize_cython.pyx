def func_slow(long N):
    cdef double d
    cdef long i
    d = 0.0
    for i in range(N):
        d += (i % 3 - 1) * i
    return d

def func_slow_nogil(long N):
    cdef double d
    cdef long i
    with nogil:
        d = 0.0
        for i in range(N):
            d += (i % 3 - 1) * i
    return d
