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
        self.stop_on_exception = False

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            try:
                self.execute(*self.args, **self.kwargs)
            except:
                if self.stop_on_exception:
                    break
