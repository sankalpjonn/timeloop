from threading import Thread, Event
from datetime import timedelta


class Job(Thread):
    def __init__(self, interval, run_on_start, execute, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval = interval
        self.run_on_start = run_on_start
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        if self.run_on_start:
            self.execute(*self.args, **self.kwargs)

        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
