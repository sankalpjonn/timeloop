from threading import Thread, Event
from datetime import timedelta
from time import sleep

class Job(Thread):
    def __init__(self, interval: timedelta, execute, offset: timedelta=None, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval: timedelta = interval
        self.execute = execute
        self.offset: timedelta = offset
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        if self.offset:
            sleep(self.offset.total_seconds())
            self.execute(*self.args, **self.kwargs)
        
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
