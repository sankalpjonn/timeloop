import logging, sys, signal, time

from exceptions import ServiceExit
from job import Job
from helpers import service_shutdown

class Looper():
    def __init__(self):
        self.jobs = []
        logger = logging.getLogger('looper')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def _add_task(self, func, interval, *args, **kwargs):
        j = Job(interval, func, *args, **kwargs)
        self.jobs.append(j)

    def job(self, interval):
        def decorator(f):
            self._add_task(f, interval)
            return f
        return decorator

    def start(self):
        try:
            signal.signal(signal.SIGTERM, service_shutdown)
            signal.signal(signal.SIGINT, service_shutdown)

            self.logger.info("Starting looper..")
            for j in self.jobs:
                self.logger.info("Registered task {}".format(j.execute))
                j.start()
            self.logger.info("Looper now started. Tasks will run based on the interval set")

            # block main thead
            while True:
                time.sleep(1)

        except ServiceExit:
            for j in self.jobs:
                self.logger.info("Stopping task {}".format(j.execute))
                j.stop()
