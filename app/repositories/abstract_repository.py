from abc import ABC, abstractmethod
from typing import List

from sqlmodel import SQLModel

class AbstractRepository(ABC):
    @abstractmethod
    async def create_or_update(self, model: SQLModel):
        pass

    @abstractmethod
    async def get_all(self, skip: int, limit: int):
        pass

    @abstractmethod
    async def get_by_id(self, id: int):
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]):
        pass

    @abstractmethod
    async def delete(self, model: SQLModel):
        pass
