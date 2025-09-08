from abc import ABC, abstractmethod

from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository(ABC):
    @abstractmethod
    def create_device(self, device: DeviceCreate):
        pass


    @abstractmethod
    def read_devices(self, skip: int = 0, limit: int = 100):
        pass


    @abstractmethod
    def read_device(self, device_id: int):
        pass


    @abstractmethod
    def update_device(self, device_id: int, device: DeviceUpdate):
        pass


    @abstractmethod
    def remove_device(self, device_id: int):
        pass
