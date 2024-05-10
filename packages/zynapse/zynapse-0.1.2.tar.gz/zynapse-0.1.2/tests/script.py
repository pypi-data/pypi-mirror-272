import unittest
from unittest.mock import MagicMock
from zynapse import Zynapse, Task, Contribution
from zynapse.connection import Connection
from zynapse.tracking import Tracker, Rewards, Contributions
from zynapse.frame import Frame
from zynapse.models import Model, Privacy

class TestZynapse(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock(spec=Connection)
        self.tracker_mock = MagicMock(spec=Tracker)
        self.model_mock = MagicMock(spec=Model)
        self.privacy_mock = MagicMock(spec=Privacy)
        self.frame_mock = MagicMock(spec=Frame)
        self.rewards_mock = MagicMock(spec=Rewards)
        self.contributions_mock = MagicMock(spec=Contributions)

        self.zynapse = Zynapse(
            "cluster_url",
            "auth_token",
            "user_id",
            connection=self.connection_mock,
            tracker=self.tracker_mock,
            model=self.model_mock,
            privacy=self.privacy_mock,
            frame=self.frame_mock,
            rewards=self.rewards_mock,
            contributions=self.contributions_mock,
        )

    def test_connect(self):
        self.zynapse.connect()
        self.connection_mock.connect.assert_called_once_with()

    def test_disconnect(self):
        self.zynapse.disconnect()
        self.connection_mock.disconnect.assert_called_once_with()

    def test_run(self):
        input_data = [{"input": [1, 2, 3]} for _ in range(1000)]
        tasks = [Task(input=input_data)]
        zk_proof = "zero_knowledge_proof"
        token_amount = 10
        contribution_data = [
            {"contribution_type": "compute_time", "amount": 10},
            {"contribution_type": "memory_usage", "amount": 5},
            {"contribution_type": "gpu_usage", "amount": 2},
        ]

        contribution = Contribution(contribution_data)

        self.frame_mock.run_model.return_value = zk_proof
        self.rewards_mock.reward_tokens.return_value = token_amount
        self.contributions_mock.contribute.return_value = None

        result, tokens = self.zynapse.run(tasks[0].input)

        self.assertEqual(result, zk_proof)
        self.assertEqual(tokens, token_amount)
        self.frame_mock.run_model.assert_called_once_with(input_data)
        self.rewards_mock.reward_tokens.assert_called_once_with("user123")
        self.contributions_mock.contribute.assert_called_once_with(contribution)


if __name__ == "__main__":
    unittest.main()