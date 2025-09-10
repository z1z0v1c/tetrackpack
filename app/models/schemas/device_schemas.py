from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional

from app.entities import DeviceEntity

class DeviceType(str, Enum):
    SERVER = "server"
    SWITCH = "switch"
    ROUTER = "router"
    STORAGE = "storage"
    OTHER = "other"


class DeviceCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: Annotated[int, Field(ge=1)]
    power_consumption: Annotated[int, Field(ge=10)]
    device_type: DeviceType

    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(**self.model_dump())


class DeviceUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    power_consumption: Optional[int] = None

    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(**self.model_dump())
    

class DeviceFullResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    serial_number: str
    number_of_units: int
    power_consumption: int
    device_type: DeviceType

    model_config = ConfigDict(from_attributes=True)
