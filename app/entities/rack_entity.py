from dataclasses import dataclass, field
from typing import List, Optional

from app.entities.device_entity import DeviceEntity


@dataclass
class RackEntity:
    def __init__(
        self,
        name: str,
        serial_number: str,
        number_of_units: int = 0,
        max_power_consumption: int = 0,
        id: Optional[int] = None,
        description: Optional[str] = None,
        devices: Optional[List[DeviceEntity]] = [],
        **kwargs
    ):
        self.id = id
        self.name = name
        self.description = description
        self.serial_number = serial_number
        self.number_of_units = number_of_units
        self.max_power_consumption = max_power_consumption
        self.devices = devices
