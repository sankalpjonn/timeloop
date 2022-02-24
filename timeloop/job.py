from threading import Thread, Event


class Job(Thread):
    UNLIMITED_EXECUTION = None

    NUM_EXEC_KEYWORD = "num_executions"

    def __init__(self, interval, execute, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        # to preserve the existing interface, get num_executions from kwargs
        if Job.NUM_EXEC_KEYWORD in kwargs.keys():
            self.num_executions = kwargs.pop(Job.NUM_EXEC_KEYWORD)
        else:
            self.num_executions = Job.UNLIMITED_EXECUTION

        self.kwargs = kwargs
        self.__counter = 0

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
            self.__counter += 1
            if self.num_executions and self.__counter >= self.num_executions:
                self.stopped.set()
