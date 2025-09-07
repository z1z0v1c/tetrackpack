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

class DeviceResponse(DeviceBase):
    id: int
    
    class Config:
        orm_mode = True