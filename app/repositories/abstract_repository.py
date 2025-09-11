from abc import ABC, abstractmethod
from typing import List

from sqlmodel import SQLModel

class AbstractRepository(ABC):
    @abstractmethod
    def create_or_update(self, model: SQLModel):
        pass

    @abstractmethod
    def get_all(self, skip: int, limit: int):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_by_ids(self, ids: List[int]):
        pass

    @abstractmethod
    def delete(self, model: SQLModel):
        pass
