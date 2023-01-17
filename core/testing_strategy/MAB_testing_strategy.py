import numpy as np

from core.services.batch_service import BatchService
from core.logger import get_logger
from core.settings import get_settings

from core.testing_strategy.base_testing_strategy import BaseTestingStrategy, ItemDistribution

EXPLORATION_SHARE_IN_DISTRIBUTION = 0.2

batch_service = BatchService()
settings = get_settings()
logger = get_logger(settings.log_filename)


class MABTestingStrategy(BaseTestingStrategy):
    method = "Multi-Armed Bandits testing strategy"

    def get_distributions(self, item_ids: list[int], total_converting_items: list[dict],
                          total_batches: int) -> list[ItemDistribution]:
        """ Find suitable push_id and assign it to batch"""
        # if no winner - 100% - uniform
        probabilities = None
        if total_converting_items:
            # if winner: assign 80% batches to push-winner, others have 20% each - uniform
            winner = max(total_converting_items, key=lambda d: d['converted'])['push_id']
            loser = min(total_converting_items, key=lambda d: d['converted'])['push_id']
            if winner != loser:
                winner_idx = item_ids.index(winner)
                item_ids.pop(winner_idx)

                probabilities = [EXPLORATION_SHARE_IN_DISTRIBUTION/len(item_ids) for _ in item_ids]
                item_ids.append(winner)
                probabilities.append(1 - EXPLORATION_SHARE_IN_DISTRIBUTION)

        logger.info(f'Push_id distribution {total_converting_items}')
        push_id = np.random.choice(item_ids, p=probabilities)
        return [ItemDistribution(item_id=int(push_id), quantity=1)]