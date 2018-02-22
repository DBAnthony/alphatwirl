# Tai Sakuma <tai.sakuma@gmail.com>
import multiprocessing

from alphatwirl import progressbar

##__________________________________________________________________||
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, lock, progressReporter):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.lock = lock
        self.progressReporter = progressReporter

    def run(self):
        progressbar._progress_reporter = self.progressReporter
        while True:
            message = self.task_queue.get()
            if message is None:
                self.task_queue.task_done()
                break
            task_idx, package = message
            result = package.task(*package.args, **package.kwargs)
            self.task_queue.task_done()
            self.result_queue.put((task_idx, result))

##__________________________________________________________________||
