from typing import Tuple, List, Dict, Any
from .connection import Connection, Task
from .tracking import Tracker, Rewards, Contributions
from .frame import Frame
from .models import Model, Privacy
import time
import traceback
import logging

logger = logging.getLogger(__name__)

class Zynapse:
    def __init__(self, cluster_url: str, auth_token: str, user_id: str):
        """
        Initialize the Zynapse object.

        Args:
            cluster_url (str): The URL of the cluster.
            auth_token (str): The authentication token.
            user_id (str): The user ID.
        """
        self.connection = Connection(cluster_url, auth_token)
        self.tracker = Tracker(user_id)
        self.model = Model("default_model", "1.0")
        self.privacy = Privacy()
        self.frame = Frame(self.connection, self.tracker, self.model, self.privacy)
        self.rewards = Rewards(self.tracker)
        self.contributions = Contributions(self.tracker)

    def connect(self) -> bool:
        """
        Connect to the cluster.

        Returns:
            bool: True if connected successfully, False otherwise.
        """
        return self.connection.connect()

    def disconnect(self) -> None:
        """
        Disconnect from the cluster.
        """
        self.connection.disconnect()

    def run(self, input_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], int]:
        """
        Run the model on the input data.

        Args:
            input_data (List[Dict[str, Any]]): The input data.

        Returns:
            Tuple[List[Dict[str, str]], int]: The output data and the token amount.
        """
        try:
            start_time = time.time()
            tasks = [Task(input=input_data)]
            zk_proof = self.frame.run_model(tasks[0].input)
            token_amount = self.rewards.reward_tokens("user123")
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"Execution time: {execution_time} seconds")
            self.contributions.contribute("compute_time", execution_time)
            return zk_proof, token_amount
        except Exception as e:
            logger.error(f"Error running SDK: {e}")
            traceback.print_exc()
            return [], 0

    @staticmethod
    def _log_error(error: str, module: str) -> None:
        """
        Log an error message.

        Args:
            error (str): The error message.
            module (str): The module name.
        """
        logger.error(f"[{module}]: {error}")
