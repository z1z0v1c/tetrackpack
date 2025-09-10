from abc import ABC, abstractmethod
from typing import List

from app.models.db_models import Rack


class RackRepository(ABC):
    @abstractmethod
    def create_or_update(self, rack: Rack):
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def get_by_id(self, rack_id: int):
        pass

    @abstractmethod
    def get_by_ids(self, rack_ids: List[int]):
        pass

    @abstractmethod
    def delete(self, rack: Rack):
        pass
