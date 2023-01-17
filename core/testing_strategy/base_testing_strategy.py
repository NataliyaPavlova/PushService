from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ItemDistribution:
    item_id: int
    quantity: int


class BaseTestingStrategy(ABC):
    method = "AB testing"

    @abstractmethod
    def get_distributions(self, item_ids: list[int], total_converting_items: list[dict],
                          total_batches: int) -> list[ItemDistribution]:
        pass
