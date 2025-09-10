from abc import ABC, abstractmethod

from app.models.db_models import Device


class DeviceRepository(ABC):
    @abstractmethod
    def create_or_update(self, device: Device):
        pass

    @abstractmethod
    def get_all(self, skip: int, limit: int):
        pass

    @abstractmethod
    def get_by_id(self, device_id: int):
        pass

    @abstractmethod
    def delete(self, device: Device):
        pass
