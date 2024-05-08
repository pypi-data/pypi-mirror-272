from dataclasses import dataclass
from uuid import uuid4, UUID
import phpserialize
import json
import warnings
from datetime import datetime


@dataclass
class Job:
    '''
        Job class to represent a job in the database queue
    '''
    id: int
    uuid: UUID = uuid4()
    display_name: str = ''
    job: str = ''
    max_tries: int = None
    max_exceptions: int = None
    backoff: int = None
    timeout: int = None
    retry_until: int = None
    sentry_trace_parent_data: str = None
    command_name: str = None
    command: dict = None
    existing_job: bool = False
    raw_record: dict = None
    queue: any = None
    params: dict = None

    @classmethod
    def from_psycopg2(cls, record, queue=None, args_map=None, ):
        '''
            Creates a Job object from a record returned by psycopg2
        '''
        raw_record = record
        payload = json.loads(record[1])
        command = cls.__php_serialized_to_dict(payload['data']['command'])
        job = cls(
            id=record[0],
            uuid=payload['uuid'],
            display_name=payload['displayName'],
            job=payload['job'],
            max_tries=payload['maxTries'],
            max_exceptions=payload['maxExceptions'],
            backoff=payload['backoff'],
            timeout=payload['timeout'],
            retry_until=payload['retryUntil'],
            command_name=payload['data']['commandName'],
            command=command,
            existing_job=True,
            raw_record=raw_record,
            queue=queue
        )
        return job

    @classmethod
    def __php_serialized_to_dict(cls, command: str) -> dict:
        command = phpserialize.loads(command.encode(
            'utf-8'), object_hook=phpserialize.phpobject)
        command_dict = command._asdict()
        command_dict_formatted = {}
        for key in command_dict:
            val = command_dict[key]
            key = key.replace(b'\x00', b'')
            if isinstance(key, bytes):
                key = key.decode()
            if isinstance(val, bytes):
                val = val.decode()
            command_dict_formatted[key] = val

        return command_dict_formatted

    def __get_params_from_command(self, param_map: dict) -> dict:
        params = {}
        for map_key in param_map:
            for command_key in self.command:
                if map_key in command_key:
                    params[param_map[map_key]] = self.command[command_key]
        self.params = params
        return params

    def __get_cache_uid_from_config(self, cache_lock_uid: list) -> str:
        params = self.params
        cache_uid = None
        if cache_lock_uid:
            cache_uid = str(self.command_name.split('\\')[-1])
            for var in cache_lock_uid:
                if var.startswith('$'):
                    if not var[1:] in params:
                        raise ValueError(
                            'Variable {} not found in the job parameters'.format(var))
                    value = params[var[1:]]
                    if not value is None:
                        cache_uid = cache_uid + str(value)
                else:
                    cache_uid = cache_uid + var
        return cache_uid

    def run(self,
            function: any,
            param_map: dict = {},
            cache_lock_uid: str | list = None,
            unique_until_processing: bool = False) -> bool:
        '''
            Runs the job
            function: any, the function to run
            param_map: dict, a map of the parameters to pass to the function
            cache_lock_uid: str, the cache lock uid to use for the job
            unique_until_processing: bool, 
                False will release the cache lock after job completion. True will release at start of job processing.

            Returns True if the job is successful, False if the job fails
            On fail, fails the job.
        '''
        params = self.__get_params_from_command(param_map)

        if unique_until_processing:
            self.__release_lock(cache_lock_uid)

        try:
            function(**params)
            result = True
            self.__complete()
            return True
        except Exception as e:
            self.__fail(str(e))
            result = False

        if not unique_until_processing:
            self.__release_lock(cache_lock_uid)

        self.__complete()
        return result

    def __release_lock(self, cache_lock_uid: str | list = None):
        '''
            Releases the lock on the job

        '''
        if not cache_lock_uid:
            return
        if isinstance(cache_lock_uid, list):
            cache_lock_uid = self.__get_cache_uid_from_config(cache_lock_uid)

        connection = self.queue.connection
        cursor = connection.cursor()
        delete = "delete from {} where key like '%{}'".format(
            self.queue.cache_table, cache_lock_uid)
        cursor.execute(delete)
        connection.commit()
        cursor.close()

    def __fail(self, exception: str):
        '''
            Fails the job, moving the record to the failed_jobs table and completing the job

            exception: str, the exception message to save in the failed_jobs table
        '''
        connection = self.queue.connection
        cursor = connection.cursor()
        exception = exception.replace("'", "''")
        insert = "INSERT INTO {} (connection, queue, payload, exception, failed_at) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.queue.failed_jobs_table,
            'database',
            self.queue.queue,
            self.raw_record[1],
            exception,
            datetime.now().isoformat()
        )
        cursor.execute(insert)
        connection.commit()
        cursor.close()

    def __complete(self):
        '''
            Completes the job
            Removes the job from the jobs table and updates the queue object
        '''

        connection = self.queue.connection
        cursor = connection.cursor()
        drop = "DELETE FROM {} WHERE id = {}".format(
            self.queue.jobs_table, self.id)
        cursor.execute(drop)
        connection.commit()
        cursor.close()

        self.queue.read()


class Queue:
    def __init__(self, connection: any,
                 queue: str = 'python',
                 jobs_table: str = 'jobs.jobs',
                 failed_jobs_table: str = 'jobs.failed_jobs',
                 cache_table: str = 'jobs.cache_locks'):
        '''
        connection: str or sqlalchemy.engine.base.Engine
        queue: str, default 'python', the queue name in the database
        jobs_table: str, default 'jobs.jobs', the table name for the jobs
        failed_jobs_table: str, default 'jobs.failed_jobs', the table name for the failed jobs
        cache_table: str, default 'jobs.cache_locks', the table name for the cache
        '''
        self.connection = self.__connect(connection)
        self.queue = queue
        self.jobs_table = jobs_table
        self.failed_jobs_table = failed_jobs_table
        self.cache_table = cache_table
        self.jobs = []
        self.read()

    def read(self) -> list:
        '''
            Reads the jobs from the database queue
            returns a list of jobs
        '''
        cursor = self.connection.cursor()
        select = "SELECT id, payload FROM {} WHERE queue = '{}'".format(
            self.jobs_table, self.queue)
        cursor.execute(select)
        records = cursor.fetchall()
        cursor.close()
        jobs = []
        if records:
            jobs = [Job.from_psycopg2(record, queue=self)
                    for record in records]
        self.jobs = jobs
        return jobs

    def dispatch(self, job: Job):
        '''
            Dispatches a job to the database queue
            @todo: Implement the dispatch method
        '''
        if job.__existing_job:
            raise ValueError('Job already exists in the database')
        warnings.warn(
            'The dispatch method is not yet implemented. The job will not be dispatched to the queue.',
            UserWarning
        )

    def __connect(self, connection: any) -> any:
        if not isinstance(connection, str):
            connection = connection.url.render_as_string(hide_password=False)
        return self.__connect_with_psycopg2(connection)

    def __connect_with_psycopg2(self, connection_string: str):
        try:
            import psycopg2
        except ImportError:
            raise ImportError('psycopg2 is required by python-laravel-queue.')
        try:
            connection = psycopg2.connect(connection_string)
            return connection
        except:
            raise ValueError(
                'Invalid connection string. Must be in the format: postgresql://user:password@host:5432/db')
