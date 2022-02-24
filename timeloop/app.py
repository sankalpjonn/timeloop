import logging
import signal
import sys
import time
from datetime import timedelta

from timeloop.exceptions import ServiceExit
from timeloop.helpers import service_shutdown
from timeloop.job import Job


class Timeloop():
    def __init__(self):
        self.jobs = []
        logger = logging.getLogger('timeloop')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def _add_job(self, func, interval, *args, **kwargs):
        j = Job(interval, func, *args, **kwargs)
        self.jobs.append(j)

    def _block_main_thread(self):
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)

        while True:
            try:
                time.sleep(1)
            except ServiceExit:
                self.stop()
                break

    def _start_jobs(self, block):
        for j in self.jobs:
            j.daemon = not block
            j.start()
            self.logger.info("Registered job {}".format(j.execute))

    def _stop_jobs(self):
        for j in self.jobs:
            self.logger.info("Stopping job {}".format(j.execute))
            j.stop()

    def job(self, interval: timedelta, num_executions: int = Job.UNLIMITED_EXECUTION, initial_delay: timedelta = None):
        if initial_delay is None:
            initial_delay = interval

        def decorator(f):
            self._add_job(f, interval, num_executions=num_executions, initial_delay=initial_delay)
            return f

        return decorator

    def stop(self):
        self._stop_jobs()
        self.logger.info("Timeloop exited.")

    def start(self, block=False):
        self.logger.info("Starting Timeloop..")
        self._start_jobs(block=block)

        self.logger.info("Timeloop now started. Jobs will run based on the interval set")
        if block:
            self._block_main_thread()
