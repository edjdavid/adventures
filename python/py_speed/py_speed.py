import os
from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
from timeit import Timer
from numba import jit, vectorize
from func import func_slow, grouper


def get_range():
    return range(100000, 101000)


def seq_sample(f):
    sum_ = 0
    for n in get_range():
        sum_ += f(n)

    print(sum_)


def thread_sample(f):
    sum_ = 0
    # use 1 CPU (because of GIL) with several threads
    # use for mostly IO bound functions
    with ThreadPoolExecutor(max_workers=10) as executor:
        for future in as_completed(executor.submit(f, n)
                                   for n in get_range()):
            sum_ += future.result()

    print(sum_)


def process_sample(f):
    sum_ = 0
    # use several process to execute the function (def: num of CPU)
    # use for mostly CPU bound functions
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(f, n)
                                   for n in get_range()):
            sum_ += future.result()

    print(sum_)


def process_group(f, items):
    sum_ = 0
    for i in items:
        sum_ += f(i)

    return sum_


def process_sample_group(f):
    sum_ = 0
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(process_group, f, g)
                                   for g in grouper(get_range(),
                                                    100)):
            sum_ += future.result()

    print(sum_)


def vectorize_sample(f):
    sum_ = 0
    for g in grouper(get_range(), 100):
        sum_ += process_group(f, g)
    print(sum_)


def run(f):
    t1 = Timer(lambda: seq_sample(f))
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))

    t1 = Timer(lambda: thread_sample(f))
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))

    t1 = Timer(lambda: process_sample(f))
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))

    t1 = Timer(lambda: process_sample_group(f))
    print('Using processes (grouped data)')
    print(t1.repeat(repeat=3, number=1))

if __name__ == '__main__':
    print('No JIT')
    run(func_slow)

    jit_func = jit()(func_slow)

    print('Numba JIT')
    run(jit_func)

    jit_nogil_func = jit(nopython=True, nogil=True)(func_slow)

    print('Numba JIT, nopython with nogil')
    run(jit_nogil_func)

    try:
        import pyximport
        pyximport.install()
        import py_speed_cython

        print('Cython')
        run(py_speed_cython.func_slow)

        print('Cython, nogil')
        run(py_speed_cython.func_slow_nogil)

    except ImportError:
        print("Cython compiler not found. Skipping.")

    vec_auto_func = vectorize()(func_slow)
    t1 = Timer(lambda: vectorize_sample(vec_auto_func))
    print('Numba vectorize (default config, DUFunc)')
    print(t1.repeat(repeat=3, number=1))
    # [0.2374260425567627, 0.18294596672058105, 0.18335509300231934]

    vec_pl_func = vectorize(['int32(int32)', 'float64(float64)'],
                            target='parallel')(func_slow)
    t1 = Timer(lambda: vectorize_sample(vec_pl_func))
    print('Numba vectorize (target parallel)')
    print(t1.repeat(repeat=3, number=1))
    # [0.3076341152191162, 0.33128905296325684, 0.31762123107910156]
