from typing import Optional
from sqlmodel import Field, SQLModel


class Rack(SQLModel, table=True):
    """Devices in a data center are placed in a rack"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    serial_number: str = Field(unique=True, index=True)
    number_of_units: int = Field(ge=1, description="Number of units the rack can support")
    max_power_consumption: int = Field(ge=5000, description="Maximum power consumption in watts")