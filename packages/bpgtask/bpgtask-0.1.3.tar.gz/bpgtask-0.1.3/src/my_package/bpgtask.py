import typing
from dataclasses import dataclass
from typing import List


import requests


from flytekit.core.context_manager import ExecutionParameters
from flytekit.core.interface import Interface
from flytekit.core.python_function_task import PythonInstanceTask
from flytekit.core.task import TaskPlugins
from flytekit.exceptions.user import FlyteRecoverableException
from flytekit.loggers import logger
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile

T = typing.TypeVar("T")
class BpgTask(PythonInstanceTask[T]):
    """

    Parameters
    ----------
    name: str
        name of job.
    application_file:  str
        path to job's main file, can also support s3 uri.
        Ex.
        python/reporting_etl/src/job/aggregated_metrics/job_name/main.py
        s3a://reporting-databahn/job_name/main.py
    language: str
        language of application. Supports Scala and Python
    image: str
        spark image, defaults to 035088524874.dkr.ecr.us-west-2.amazonaws.com/reporting-databahn-spark-image.
    queue_name: str
        YuniKorn queue name.
        https://rokt.atlassian.net/wiki/spaces/DP/pages/2816606362/Schedule+Spark+Application+on+Kubernetes+using+YuniKorn
    spark_config: SparkConfig
        extra spark configurations. This will overwrite anything in DEFAULT_SPARK_CONFIG.
    arguments: list[str]
        application arguments.
    driver: PodSpec
        pod specs for driver.
    executor: ExecutorSpec
        pod specs and number of executor.
    dynamic_allocation: DynamicAllocationConfig
        dynamic allocation configuration for autoscaling executors.
    ephemeral_volumes: list[int]
        volume configuration for spark memory spills, each item in list represent size of volume in gb.
        Ex. [1, 2]
    poll_interval: int
        time to wait before checking job status in seconds.
    max_execution_time: int
        max amount of time to allow jobs to run in seconds.
    """

    def __init__(
        self,
        name: str,
        bpg_endpoint: str,
        debug: bool = False,
        # job_name: str,
        # application_file: str,
        # language: str,
        # image: str,
        # queue_name: str,

        task_config: T = None,
        **kwargs,
    ):
        self._debug = debug
        # self._job_name = job_name
        # self._application_file = application_file
        # self._language = language
        # self._image = image
        # self._queue_name = queue_name
        self._bpg_endpoint = bpg_endpoint

        super().__init__(
            name,
            task_config,
            interface=Interface(inputs=None, outputs=None),
            **kwargs,
        )

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def bpg_endpoint(self) -> str:
        return self._bpg_endpoint

    def execute(self, **kwargs) -> typing.Optional[str]:
        """
        Executes the given script by substituting the inputs and outputs and extracts the outputs from the filesystem
        """
        logger.info(f"Running BpgTask {self._name} with debug={self._debug}")

        # task_id = 'id-123'
        response = requests.get(self.bpg_endpoint)
        task_id = response.status_code
        print('BpgTask.execute() ===>', task_id)

        return task_id
