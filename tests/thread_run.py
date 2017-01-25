import time
from matplotlib import pyplot as plt
from src.thread_indexer import *

timings = []
if __name__ == '__main__':
    freeze_support()

    for i in range(1000):
        start = time.clock()
        print('starting test number %s . . .' % (i+1))
        ThreadIndex('C:\\', silent=True, use_blacklist=True).run()
        print('finished test in %s seconds.' % (time.clock() - start))
        timings.append((time.clock() - start))

    print(timings)
    plt.plot(timings)
    plt.ylabel('time (seconds)')
    plt.xlabel('instance')
    plt.axis([0, 1000, 0, 10])
    plt.title('100 thread test results')
    print('total time %s' % sum(timings))
    print('average %s' % (sum(timings)/1000))
    plt.show()