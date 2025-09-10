from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.entities import RackEntity


class RackCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    max_power_consumption: int

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


class RackFullResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    max_power_consumption: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity: RackEntity):
        return cls(**entity.__dict__)


class RackLayoutResponse(BaseModel):
    rack_id: int
    devices: List[int]
    utilization: float


class RackLayoutsResponse(BaseModel):
    layout: List[RackLayoutResponse]
