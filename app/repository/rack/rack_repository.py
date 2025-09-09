from abc import ABC, abstractmethod

from app.schemas.rack import RackCreate, RackUpdate


class RackRepository(ABC):
    @abstractmethod
    def create_rack(self, rack: RackCreate):
        pass


    @abstractmethod
    def read_racks(self, skip: int = 0, limit: int = 100):
        pass


    @abstractmethod
    def read_rack(self, rack_id: int):
        pass


    @abstractmethod
    def update_rack(self, rack_id: int, rack: RackUpdate):
        pass


    @abstractmethod
    def remove_rack(self, rack_id: int):
        pass
