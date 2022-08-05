# Timeloop
Timeloop is a service that can be used to run periodic tasks after a certain interval.

Each job runs on a separate thread and when the service is shut down, it waits till all tasks currently being executed are completed.

Inspired by this blog [`here`](https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

## Fork
This fork aims to provide some improvements to the original library. Mainly to be able to set a start time or start offset for tasks.

## Installation
Has to be installed manually atm. Since it is just a fork of the original and I still have to set that up and want to respect the work of Sankalp Jonna. Feel free to help tho!

## Writing jobs
```python
import time

from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print "2s job current time : {}".format(time.ctime())

@tl.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
    print "5s job current time : {}".format(time.ctime())


# Added support for initial offset!
@tl.job(interval=timedelta(seconds=10), offset=timedelta(hours=1))
def sample_job_after_an_hour_every_10s():
    print "after an hour 10s job current time : {}".format(time.ctime())
```

## Start time loop in separate thread
By default timeloop starts in a separate thread.

Please do not forget to call ```tl.stop``` before exiting the program, Or else the jobs wont shut down gracefully.

```python
tl.start()

while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    tl.stop()
    break
```

## Start time loop in main thread
Doing this will automatically shut down the jobs gracefully when the program is killed, so no need to  call ```tl.stop```
```python
tl.start(block=True)
```

## Author
* **Sankalp Jonna**

Email me with any queries: [sankalpjonna@gmail.com](sankalpjonna@gmail.com).
