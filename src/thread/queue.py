'''
from queue import Queue
from threading import Thread
from src.thread.protection import *
from src.thread.manager import Process, manager_logger



class queue_manager(object):
    def __init__(self, interval=0.1):
        self.queue = Queue()
        self.interval = interval
        self.running = True
        self.random = False

        self.manager = Thread(target=self.stream_handler, args=(self.queue,))
        self.manager.daemon = True
        self.manager.start()

    def stream_handler(self, queue):
        global sleep_state
        # check that packet was correct, retrieve packet instruction and contents
        while self.running:
            try:
                item = queue.get_nowait()
                if len(item) == 3:  # 1: instruction 2: process id 3: other information (exclusive)
                    if item[0] == 'register':
                        manager_logger.debug('got register packet')
                        return Process.register(pid=item[1], p_type=item[2])
                    elif item[0] == 'truncate':
                        manager_logger.info('finished self.sleep() state (hierachy)')
                        return Process.truncate(pid=item[1])
                    else:
                        manager_logger.fatal('error packet: %s, length=%s spliced= %s, %s, %s' % (item, len(item), item[0], item[1], item[2]))
                        self.running = False

                    sleep_state = False

            except Exception:
                self.sleep()

            finally:
                self.sleep()

            if not self.running:
                manager_logger.info('queue was closed.')
                queue.close()
                self.manager.join()

    def sleep(self):

        def sleep_method(interval):
            # internal wrapper for switch method, requires global switch value to be set to true
            global sleep_state
            sleep_state = True
            switch(interval)

        if self.random:
            sleep_method(self.interval*safe_random())
            return

        else:
            sleep_method(self.interval)

    def operation(self, object):
        global sleep_state

        try:
            self.queue.put(object)
            manager_logger.info('accepted object and input into queue, object=%s' % object)
            return self.running

        except Exception as e:
            manager_logger.error(e)
'''
raise NotImplemented
