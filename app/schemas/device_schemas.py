from pydantic import BaseModel
from typing import Optional


class DeviceBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    power_consumption: int


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    power_consumption: Optional[int] = None


class DeviceResponse(DeviceBase):
    id: int
    
    class Config:
        orm_mode = True