# Timeloop
Timeloop is a service that can be used to run periodic tasks after a certain interval.

Each job runs on a separate thread and when the service is shut down, it waits till all tasks currently being executed are completed.

Inspired by this blog [`here`](https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

## Installation
```sh
pip install timeloop
```

## Writing jobs
The jobs run the first time after the first wait interval.

```python
import time

from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print("2s job current time : {}".format(time.ctime()))

@tl.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
    print("5s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(seconds=10))
def sample_job_every_10s():
    print("10s job current time : {}".format(time.ctime()))
```

## Jobs that only run a certain amount of time
By default, all jobs run until they are stopped. At times you may want to run a job only once or twice.

```python
import time

from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=10), num_executions=2)
def run_me_twice_with_10s_pause():
    print("10s job current time : {}".format(time.ctime()))
```

## Jobs with a different initial interval
At times, you want 
```python
@tl.job(interval=timedelta(seconds=1), initial_delay=timedelta(seconds=10))
def run_after10s_and_then_every_second():
    print("job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(seconds=1), num_executions=2, initial_delay=timedelta(seconds=10))
def run_after10s_and_then_after_1second_then_stop():
    print("job current time : {}".format(time.ctime()))
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
