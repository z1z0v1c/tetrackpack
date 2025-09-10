from typing import List, Optional
from pydantic import BaseModel

from app.entities import RackEntity


class RackBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    max_power_consumption: int


class RackCreateRequest(RackBase):
    def to_entity(self) -> RackEntity:
        return RackEntity(**self.model_dump())


class RackUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    max_power_consumption: Optional[int] = None

    def to_entity(self) -> RackEntity:
        return RackEntity(**self.model_dump())

class RackLayoutRequest(BaseModel):
    rack_ids: List[int]
    device_ids: List[int]


class RackResponse(RackBase):
    id: int

    @classmethod
    def from_entity(cls, entity: RackEntity):
        return cls(**entity.__dict__)

    class Config:
        orm_mode = True

class RackLayoutResponse(BaseModel):
    rack_id: int
    devices: List[int]
    utilization: float  # percentage 0.0 - 100.0

class RackLayoutsResponse(BaseModel):
    layout: List[RackLayoutResponse]