from src.logger import *
from src.thread.protection import *

manager_logger = logging.getLogger('photo.process_manager')

class _Process:
    def __init__(self):
        self.parent = 0
        self.process_count = check_process_count(True, True)
        self.frame = {}
        self._process_list = []

    def get_frame(self):
        self.frame = {}
        x = 0
        for line in os.popen('tasklist').readlines()[3:]:
            if 'python' in line.split()[0]:
                self.frame.update({x: (line.split()[0], int(line.split()[1]))})
                x += 1
            else:
                continue

    def get_processes(self):
        # fetches current process list
        return sorted(self._process_list)

    def register(self, pid, p_type):
        if len(self._process_list) > self.process_count + 1:
            manager_logger.error('failed to authenticate process, max processes already registered.')
            return False

        else:
            if p_type == 'parent':
                self.parent = pid

            self._process_list.append((pid, p_type))
            manager_logger.info('current process authentication object: %s' % self._process_list)
            return True

    def truncate(self, pid):
        try:
            frozen_length = len(self._process_list)
            for process in self._process_list:
                if pid == process[0]:
                    self._process_list.remove(process)
                    break
                else:
                    continue

            if len(self._process_list) == frozen_length:
                raise ValueError

        except ValueError:
            Fatal('Process could not be found by manager.', True,
                  'p_id= %s' % str(pid),
                  'p_list= %s' % self._process_list)

        finally:
            if not self.stability_check():
                Fatal('Process instability violation.', True)

    def stability_check(self):
        instability_level = 0
        manager_logger.info('parent=%s child_process: %s' % (self.parent, self._process_list))
        # simple check, are the process list size and allowed process instance size the same
        frame = [process[1][1] for process in list(self.frame.items())]
        manager_logger.info('current process frame: %s' % frame)

        if len(self.get_processes()) <= (self.process_count):  # process count does not include parent, thus 1 is added
            selection_size = random.randint(1, 6)
            random_candidates = get_candidates(self.process_count, selection_size)

            for candidate in random_candidates:
                if self._process_list[candidate][0] in frame:
                    manager_logger.debug('checked process: %s presence within process list, Success' % self._process_list[candidate][0])
                    pass
                else:
                    manager_logger.error('could not find registered process: %s' % (self._process_list[candidate][0]))
                    instability_level += 1

        else:
            return False

        return False if instability_level > 0 else True

    def alert(self, e_code):
        if e_code == 0x1:
            self._process_list = []
            return simple_error('Keyboard interrupt caused for process threads to be destroyed', True, 'process.kb_error')


Process = _Process()
del _Process

