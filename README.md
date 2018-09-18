# Looper
Looper is a service that can be used to run periodic tasks after a certain interval.

Each job runs on a separate thread and when the service is shut down, it waits till all tasks currently being executed are completed.

Inspired by this blog [`here`](https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

## Installation
```sh
python setup.py install
```

## writing a job looks like this

```python
import time

from looper import Looper
from datetime import timedelta

loop = Looper()

@loop.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print "2s job current time : {}".format(time.ctime())

@loop.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
    print "5s job current time : {}".format(time.ctime())


@loop.job(interval=timedelta(seconds=10))
def sample_job_every_10s():
    print "10s job current time : {}".format(time.ctime())

loop.start()
```

## Author
* **Sankalp Jonna**

Email me with any queries: [sankalpjonna@gmail.com](sankalpjonna@gmail.com).
