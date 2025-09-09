from abc import ABC, abstractmethod

from models.rack import Rack

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
    def delete(self, rack: Rack):
        pass
