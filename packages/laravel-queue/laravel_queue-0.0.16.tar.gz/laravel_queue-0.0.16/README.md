# Laravel Queue for Python

Currently:

- only supports reading
- only supports queues in postgres

### Create a Queue Object

```
from laravel_queue import Queue

connection_string = "postgresql://user:password@host:5432/db"
queue = Queue(connection_string)

```

#### Queue Args:

    connection: str or sqlalchemy.engine.base.Engine
    queue: str, default 'python', the queue name in the database
    jobs_table: str, default 'jobs.jobs', the table name for the jobs
    failed_jobs_table: str, default 'jobs.failed_jobs', the table name for the failed jobs

### Read Jobs from Queue

```
jobs = queue.jobs  ## List of jobs in queue object
```

### Running Jobs

```
while queue.jobs:
    jobs = queue.jobs
    for job in jobs:
        job.run(function) ## run any function
```

function can be any function to run for this job
Using the while loop allows any new jobs placed on the queue while processing to be carried out next.

#### Passing Params

To pass params in laravel to the python function, specify a `param_map` in the run function.

```
# laravel:
$this->groupId = 12;

# python
def function(group_id):
    pass

job.run(function, param_map={
    'groupId': 'group_id'
})
```

Additionally, you can specify a `cache_lock_uid`
This can be either a str or a list of strings.
This is to be used for managing the job cache if you are using the `ShouldBeUnique` or `ShouldBeUniqueUntilProcessing` properties in Laravel
The `cache_lock_uid` should resemble what you have set `uniqueId()` to in laravel.
If a list is sent, you can specify parameters to be filled with `$`:

```
# Laravel:
$this->param1 = 1
$this->param2 = 2

public function uniqueId(): string
    {
        return $this->param1 . '-' . $this->param2;
    }


# Python
job.run(function_name,
    param_map = {
        'param1': 'param1',
        'param2': param2'
    }
    cache_lock_uid = ['$param1', '-', '$param2'])

## $param1 and $param2 will be swapped in with the cooresponding value.

```

To use cache locks, you must specify the database as your cache for queue. You can do this as so:

```
public function uniqueVia(): Repository
    {
        return Cache::driver('database');
    }
```

If using the `ShouldBeUniqueUntilProcessing` property, you must specify that in you job runner as well.
By default (`unique_until_processing=False`), the cache lock will be relased after processing, emulating the `ShouldBeUnique` laravel property.
Setting this `unique_until_processing=True` will relase this lock at the start of the job, like `ShouldBeUniqueUntilProcessing`
