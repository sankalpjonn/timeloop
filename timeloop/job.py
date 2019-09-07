from threading import Thread, Event
from datetime import timedelta
from time import time

class Job(Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        next_period = self.interval.total_seconds()
        next_time = time()

        while not self.stopped.wait(next_period):
            self.execute(*self.args, **self.kwargs)
            next_time += self.interval.total_seconds()
            next_period = next_time - time()
