from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Frame:
    def __init__(self, connection, tracker, model, privacy):
        """
        Initialize the Frame object.

        Args:
            connection (Connection): The connection object.
            tracker (Tracker): The tracker object.
            model (Model): The ML model object.
            privacy (Privacy): The privacy preserver object.
        """
        self.connection = connection
        self.tracker = tracker
        self.model = model
        self.privacy = privacy

    def run_model(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run the model on the input data and preserve privacy.

        Args:
            input_data (List[Dict[str, Any]]): The input data.

        Returns:
            List[Dict[str, Any]]: The output data with preserved privacy.
        """
        preserved_data = self.privacy.preserve_privacy(input_data)
        output_data = self.model.run_model(preserved_data)
        return output_data

    @staticmethod
    def _log_error(error: str, module: str) -> None:
        """
        Log an error message.

        Args:
            error (str): The error message.
            module (str): The module name.
        """
        logger.error(f"[{module}]: {error}")
