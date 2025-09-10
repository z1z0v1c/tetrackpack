from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from app.entities import RackEntity


class Rack(SQLModel, table=True):
    """Devices in a data center are placed in a rack"""

    __tablename__ = "racks"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    serial_number: str = Field(unique=True, index=True)
    number_of_units: int = Field(
        ge=1, description="Number of units the rack can support"
    )
    max_power_consumption: int = Field(
        ge=5000, description="Maximum power consumption in watts"
    )
    total_power_conssumption: int = Field(
        default=0, description="Total power consumption in watts"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    devices: List["Device"] = Relationship(back_populates="rack")  # type: ignore

    def to_entity(self) -> RackEntity:
        return RackEntity(**self.model_dump())

    @classmethod
    def from_entity(cls, entity: RackEntity):
        return cls(**entity.__dict__)
