import time
from matplotlib import pyplot as plt
from src.thread_indexer import *

timings = []
if __name__ == '__main__':
    freeze_support()

    for i in range(100):
        start = time.clock()
        ThreadIndex('C:\\', blacklist=True, silent_mode=True).run()
        timings.append((time.clock() - start))

    print(timings)
    plt.plot(timings)
    plt.ylabel('time (seconds)')
    plt.xlabel('instance')
    plt.axis([0, 100, 0, 10])
    plt.title('100 thread test results')
    print('total time %s' % sum(timings))
    print('average %s' % (sum(timings)/100))
    plt.show()