from typing import Optional
from pydantic import BaseModel


class RackBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    number_of_units: int
    max_power_consumption: int


class RackCreate(RackBase):
    pass


class RackUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    number_of_units: Optional[int] = None
    max_power_consumption: Optional[int] = None


class RackResponse(RackBase):
    id: int
    
    class Config:
        orm_mode = True
