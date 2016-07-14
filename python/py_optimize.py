from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
from timeit import Timer
from numba import jit
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


def seq_sample():
    sum = 0
    for n in get_range():
        sum += func_slow(n)

    print(sum)


def thread_sample():
    sum = 0
    # use 1 CPU (because of GIL) with several threads
    # use for mostly IO bound functions
    with ThreadPoolExecutor(max_workers=10) as executor:
        for future in as_completed(executor.submit(func_slow, n)
                                   for n in get_range()):
            sum += future.result()

    print(sum)


def process_sample():
    sum = 0
    # use several process to execute the function (def: num of CPU)
    # use for mostly CPU bound functions
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(func_slow, n)
                                   for n in get_range()):
            sum += future.result()

    print(sum)


def process_group(items):
    sum = 0
    for i in items:
        sum += func_slow(i)

    return sum


def process_sample_group():
    sum = 0
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(process_group, g)
                                   for g in grouper(get_range(),
                                                    100)):
            sum += future.result()

    print(sum)


def run():
    # test on Anaconda Python 2.7.11, i5 3.2GHz x4, 7.7GB RAM

    # Normal
    # JIT
    # JIT, nopython, nogil

    t1 = Timer(lambda: seq_sample())
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))
    # [10.168029069900513, 10.402216911315918, 10.611801147460938]
    # [0.24570488929748535, 0.19139814376831055, 0.18819808959960938]
    # [0.2139570713043213, 0.1826789379119873, 0.18301606178283691]

    t1 = Timer(lambda: thread_sample())
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))
    # [19.16162896156311, 20.380229949951172, 21.510963916778564]
    # [0.4485650062561035, 0.4848320484161377, 0.5402340888977051]
    # [0.09081888198852539, 0.09463310241699219, 0.09384393692016602]

    t1 = Timer(lambda: process_sample())
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))
    # [3.208076000213623, 3.2477550506591797, 3.2287039756774902]
    # [8.317075967788696, 8.151933908462524, 8.201157093048096]
    # [8.269657135009766, 8.970659971237183, 8.789407968521118]

    t1 = Timer(lambda: process_sample_group())
    print('Using processes (grouped data)')
    print(t1.repeat(repeat=3, number=1))
    # [3.6561429500579834, 3.537872076034546, 3.5214269161224365]
    # [0.07229804992675781, 0.07447195053100586, 0.07154178619384766]
    # [0.07124614715576172, 0.07875490188598633, 0.07564306259155273]


if __name__ == '__main__':
    _func_slow = func_slow

    print('No JIT')
    run()

    func_slow = _func_slow
    func_slow = jit(func_slow)

    print('Numba JIT')
    run()

    func_slow = _func_slow
    func_slow = jit(func_slow, nopython=True, nogil=True)

    print('Numba JIT, nopython with nogil')
    run()
