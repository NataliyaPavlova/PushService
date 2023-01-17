import math

from core.testing_strategy.base_testing_strategy import BaseTestingStrategy, ItemDistribution


class ABTestingStrategy(BaseTestingStrategy):
    def get_distributions(self, item_ids: list[int], total_converting_items: list[dict],
                          total_batches: int) -> list[ItemDistribution]:
        batches_on_item = math.ceil(total_batches / len(item_ids))
        distribution = []
        total_distributed_batches = 0

        current_batches_on_item = batches_on_item
        for item_id in item_ids:
            total_distributed_batches += batches_on_item
            if total_distributed_batches > total_batches:
                current_batches_on_item -= total_batches - total_distributed_batches

            distribution.append(ItemDistribution(item_id, current_batches_on_item))

        return distribution
