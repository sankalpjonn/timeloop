from threading import Thread, Event
from datetime import timedelta

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
        stopped = self.stopped
        timeout = self.interval.total_seconds()
        task = self.execute
        
        while not stopped.is_set():
            task(*self.args, **self.kwargs)
            stopped.wait(timeout)
