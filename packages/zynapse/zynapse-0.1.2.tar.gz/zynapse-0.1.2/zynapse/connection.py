import ray
import json
from pydantic import BaseModel, validator
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Task(BaseModel):
    input: List[Dict[str, Any]]

    @validator('input')
    def validate_input(cls, v):
        if not all(isinstance(item, dict) for item in v):
            raise ValueError('Input must be a list of dictionaries')
        return v

class Connection:
    def __init__(self, cluster_url: str, auth_token: str):
        """
        Initialize the Connection object.

        Args:
            cluster_url (str): The URL of the cluster.
            auth_token (str): The authentication token.
        """
        self.cluster_url = cluster_url
        self.auth_token = auth_token
        self.gpus = ray.get([ray.put(gpu) for gpu in ray.get_gpu_ids()])

    def connect(self) -> bool:
        """
        Connect to the cluster.

        Returns:
            bool: True if connected successfully, False otherwise.
        """
        try:
            ray.init(address="auto", _redis_password=self.auth_token)
            return True
        except Exception as e:
            logger.error(f"Error connecting to cluster: {e}")
            return False

    def disconnect(self) -> None:
        """
        Disconnect from the cluster.
        """
        try:
            ray.shutdown()
        except Exception as e:
            logger.error(f"Error disconnecting from cluster: {e}")

    def distribute_tasks(self, tasks: List[Task]) -> List[str]:
        """
        Distribute tasks to the cluster.

        Args:
            tasks (List[Task]): The tasks to distribute.

        Returns:
            List[str]: The task IDs.
        """
        task_ids = []
        for task in tasks:
            obj_ref = ray.put(json.dumps(task.dict(), default=str))
            task_id = ray.get(obj_ref)
            task_ids.append(task_id["id"])
        return task_ids

    @staticmethod
    def _log_error(error: str, module: str) -> None:
        """
        Log an error message.

        Args:
            error (str): The error message.
            module (str): The module name.
        """
        logger.error(f"[{module}]: {error}")