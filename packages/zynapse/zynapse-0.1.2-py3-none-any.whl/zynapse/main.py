import ray
from zynapse import Zynapse, Task, Contribution
from zynapse.tracking import ContributionsDataFrame
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ray.init()
    zynapse = Zynapse("cluster_url", "auth_token", "user_id")
    zynapse.connect()
    input_data = [{"input": [1, 2, 3]} for _ in range(1000)]
    tasks = [Task(input=input_data)]
    zk_proof, token_amount = zynapse.run(tasks[0].input)
    logger.info(f"Zero-knowledge proofs: {zk_proof}")
    logger.info(f"Rewarded {token_amount} tokens")
    contributions = [
        Contribution(contribution_type="compute_time", amount=10),
        Contribution(contribution_type="memory_usage", amount=5),
        Contribution(contribution_type="gpu_usage", amount=2),
    ]
    contributions_df = ContributionsDataFrame(contributions)
    grouped_contributions = contributions_df.group_by_contribution_type()
    logger.info(grouped_contributions)
    zynapse.disconnect()