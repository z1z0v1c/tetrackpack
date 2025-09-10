from typing import Optional
from pydantic import BaseModel

from app.entities.rack_entity import RackEntity


class RackBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    max_power_consumption: int


class RackCreate(RackBase):
    def to_entity(self) -> RackEntity:
        return RackEntity(**self.model_dump())


class RackUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    max_power_consumption: Optional[int] = None
    
    def to_entity(self) -> RackEntity:
        return RackEntity(**self.model_dump())

class RackResponse(RackBase):
    id: int

    @classmethod
    def from_entity(cls, entity: RackEntity):
        return cls(**entity.__dict__)
    
    class Config:
        orm_mode = True
