from enum import Enum
from pydantic import BaseModel
from typing import Optional

from app.entities import DeviceEntity


class DeviceType(str, Enum):
    SERVER = "server"
    SWITCH = "switch"
    ROUTER = "router"
    STORAGE = "storage"
    OTHER = "other"


class DeviceBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    power_consumption: int
    device_type: DeviceType


class DeviceCreate(DeviceBase):
    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(**self.model_dump())


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    power_consumption: Optional[int] = None

    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(**self.model_dump())


class DeviceResponse(DeviceBase):
    id: int

    @classmethod
    def from_entity(cls, entity: DeviceEntity):
        return cls(**entity.__dict__)

    class Config:
        orm_mode = True
