import datetime
from threading import Thread, Event


class Job(Thread):
    UNLIMITED_EXECUTION = None

    NUM_EXEC_KEYWORD = "num_executions"
    INITIAL_DELAY_KEYWORD = "initial_delay"

    def __init__(self, interval: datetime.timedelta, execute, *args, **kwargs):
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
        # to preserve the existing interface, get delay_execution from kwargs
        if Job.INITIAL_DELAY_KEYWORD in kwargs.keys():
            self.initial_delay = kwargs.pop(Job.INITIAL_DELAY_KEYWORD)
        else:
            self.initial_delay = interval

        self.kwargs = kwargs
        self.__counter = 0

    def stop(self):
        self.stopped.set()
        self.join()

    def _set_check_counter_and_stop(self):
        self.__counter += 1
        if self.num_executions and self.__counter >= self.num_executions:
            self.stopped.set()

    def run(self):
        if not self.stopped.wait(self.initial_delay.total_seconds()):
            self.execute(*self.args, **self.kwargs)
            self._set_check_counter_and_stop()
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
            self._set_check_counter_and_stop()