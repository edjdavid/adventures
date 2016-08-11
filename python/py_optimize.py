from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
from timeit import Timer
from numba import jit, vectorize
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def func_slow(N):
    d = 0.0
    for i in range(N):
        d += (i % 3 - 1) * i
    return d


def get_range():
    return range(100000, 101000)


def seq_sample(f):
    sum = 0
    for n in get_range():
        sum += f(n)

    print(sum)


def thread_sample(f):
    sum = 0
    # use 1 CPU (because of GIL) with several threads
    # use for mostly IO bound functions
    with ThreadPoolExecutor(max_workers=10) as executor:
        for future in as_completed(executor.submit(f, n)
                                   for n in get_range()):
            sum += future.result()

    print(sum)


def process_sample(f):
    sum = 0
    # use several process to execute the function (def: num of CPU)
    # use for mostly CPU bound functions
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(f, n)
                                   for n in get_range()):
            sum += future.result()

    print(sum)


def process_group(f, items):
    sum = 0
    for i in items:
        sum += f(i)

    return sum


def process_sample_group(f):
    sum = 0
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(process_group, f, g)
                                   for g in grouper(get_range(),
                                                    100)):
            sum += future.result()

    print(sum)


def vectorize_sample(f):
    sum = 0
    for g in grouper(get_range(), 100):
        sum += process_group(f, g)
    print(sum)


def run(f):
    # test on Anaconda Python 2.7.11, i5 3.2GHz x4, 7.7GB RAM

    # Normal
    # JIT
    # JIT, nopython, nogil
    # Cython
    # Cython, nogil

    t1 = Timer(lambda: seq_sample(f))
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))
    # [10.168029069900513, 10.402216911315918, 10.611801147460938]
    # [0.24570488929748535, 0.19139814376831055, 0.18819808959960938]
    # [0.2139570713043213, 0.1826789379119873, 0.18301606178283691]
    # [0.1870899200439453, 0.18561315536499023, 0.1863720417022705]
    # [0.19033217430114746, 0.18671011924743652, 0.1864609718322754]

    t1 = Timer(lambda: thread_sample(f))
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))
    # [19.16162896156311, 20.380229949951172, 21.510963916778564]
    # [0.4485650062561035, 0.4848320484161377, 0.5402340888977051]
    # [0.09081888198852539, 0.09463310241699219, 0.09384393692016602]
    # [0.478787899017334, 0.48709797859191895, 0.5153419971466064]
    # [0.08079195022583008, 0.09981513023376465, 0.08110308647155762]

    t1 = Timer(lambda: process_sample(f))
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))
    # [3.208076000213623, 3.2477550506591797, 3.2287039756774902]
    # [0.5669829845428467, 0.6984729766845703, 0.6910841464996338]
    # [0.5363690853118896, 0.6700029373168945, 0.6537039279937744]
    # [0.14370203018188477, 0.14115595817565918, 0.14736700057983398]
    # [0.14898014068603516, 0.15113091468811035, 0.14404296875]

    t1 = Timer(lambda: process_sample_group(f))
    print('Using processes (grouped data)')
    print(t1.repeat(repeat=3, number=1))
    # [3.6561429500579834, 3.537872076034546, 3.5214269161224365]
    # [0.07229804992675781, 0.07447195053100586, 0.07154178619384766]
    # [0.07124614715576172, 0.07875490188598633, 0.07564306259155273]
    # [0.07690596580505371, 0.06988406181335449, 0.0699930191040039]
    # [0.07497191429138184, 0.07361912727355957, 0.07271409034729004]

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
        import py_optimize_cython

        print('Cython')
        run(py_optimize_cython.func_slow)

        print('Cython, nogil')
        run(py_optimize_cython.func_slow_nogil)

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
    [0.3076341152191162, 0.33128905296325684, 0.31762123107910156]
