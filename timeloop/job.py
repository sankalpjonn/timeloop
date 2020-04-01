from threading import Thread, Event
from datetime import timedelta


class Job(Thread):
    def __init__(self, interval, init_on_start, execute, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval = interval
        self.init_on_start = init_on_start
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        if self.init_on_start:
            self.execute(*self.args, **self.kwargs)

        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
