from abc import ABC, abstractmethod
from typing import List

from app.models.db_models import DeviceModel


class DeviceRepository(ABC):
    @abstractmethod
    def create_or_update(self, device: DeviceModel):
        pass

    @abstractmethod
    def get_all(self, skip: int, limit: int):
        pass

    @abstractmethod
    def get_by_id(self, device_id: int):
        pass

    @abstractmethod
    def get_by_ids(self, device_ids: List[int]):
        pass

    @abstractmethod
    def delete(self, device: DeviceModel):
        pass
