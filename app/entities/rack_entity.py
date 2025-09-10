from dataclasses import dataclass
from typing import List, Optional

from app.entities import DeviceEntity


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

    def has_enough_units(self, needed_units: int) -> bool:
        used_units = sum(device.number_of_units for device in self.devices)
        return used_units + needed_units <= self.number_of_units
    
    def has_enough_power(self, needed_power: int) -> bool:
        used_power = sum(device.power_consumption for device in self.devices)
        return used_power + needed_power <= self.max_power_consumption
