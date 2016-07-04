from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
from timeit import Timer
from numba import jit


def func_slow(N):
    d = 0.0
    for i in range(N):
        d += (i % 3 - 1) * i
    return d


def seq_sample():
    sum = 0
    for n in range(100000, 101000):
        sum += func_slow(n)

    print(sum)


def thread_sample():
    sum = 0
    # use 1 CPU (because of GIL) with several threads
    # use for mostly IO bound functions
    with ThreadPoolExecutor(max_workers=10) as executor:
        for future in as_completed(executor.submit(func_slow, n)
                                   for n in range(100000, 101000)):
            sum += future.result()

    print(sum)


def process_sample():
    sum = 0
    # use several process to execute the function (def: num of CPU)
    # use for mostly CPU bound functions
    with ProcessPoolExecutor() as executor:
        for future in as_completed(executor.submit(func_slow, n)
                                   for n in range(100000, 101000)):
            sum += future.result()

    print(sum)

if __name__ == '__main__':
    _func_slow = func_slow
    # test on Anaconda Python 2.7.11, i5 3.2GHz x4, 7.7GB RAM
    t1 = Timer(lambda: seq_sample())
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))
    # [10.168029069900513, 10.402216911315918, 10.611801147460938]

    t1 = Timer(lambda: thread_sample())
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))
    # [19.16162896156311, 20.380229949951172, 21.510963916778564]

    t1 = Timer(lambda: process_sample())
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))
    # [3.208076000213623, 3.2477550506591797, 3.2287039756774902]

    func_slow = _func_slow
    func_slow = jit(func_slow)

    print('Numba JIT')
    t1 = Timer(lambda: seq_sample())
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))
    # [0.24570488929748535, 0.19139814376831055, 0.18819808959960938]

    t1 = Timer(lambda: thread_sample())
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))
    # [0.4485650062561035, 0.4848320484161377, 0.5402340888977051]

    t1 = Timer(lambda: process_sample())
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))
    # [0.5851070880889893, 0.7296948432922363, 0.7194869518280029]

    func_slow = _func_slow
    func_slow = jit(func_slow, nopython=True, nogil=True)

    print('Numba JIT, nopython with nogil')
    t1 = Timer(lambda: seq_sample())
    print('Sequential run')
    print(t1.repeat(repeat=3, number=1))
    # [0.2139570713043213, 0.1826789379119873, 0.18301606178283691]

    t1 = Timer(lambda: thread_sample())
    print('Using threads')
    print(t1.repeat(repeat=3, number=1))
    # [0.09081888198852539, 0.09463310241699219, 0.09384393692016602]

    t1 = Timer(lambda: process_sample())
    print('Using processes')
    print(t1.repeat(repeat=3, number=1))
    # [0.5592410564422607, 0.6949498653411865, 0.7256579399108887]
