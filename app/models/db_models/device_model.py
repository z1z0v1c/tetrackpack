from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from app.entities import DeviceEntity
from app.models.db_models.rack_model import RackModel


class DeviceType(str, Enum):
    SERVER = "server"
    SWITCH = "switch"
    ROUTER = "router"
    STORAGE = "storage"
    OTHER = "other"


class DeviceModel(SQLModel, table=True):
    """Device represents servers, switches, etc."""

    __tablename__ = "devices"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    serial_number: str = Field(unique=True, max_length=255)
    number_of_units: int = Field(ge=1)
    power_consumption: int = Field(ge=1)
    device_type: DeviceType = Field(default=DeviceType.SERVER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    rack_id: Optional[int] = Field(default=None, foreign_key="racks.id")
    rack: Optional[RackModel] = Relationship(back_populates="devices")

    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(**self.model_dump())

    @classmethod
    def from_entity(cls, entity: DeviceEntity) -> "DeviceModel":
        return cls(**entity.__dict__)
