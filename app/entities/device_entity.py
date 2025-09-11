from dataclasses import dataclass
from typing import Optional


# Could be deleted, do not encapsulates any bussiness logic at the moment
# Kept for consistency with RackEntity
@dataclass
class DeviceEntity:
    def __init__(
        self,
        name: str,
        serial_number: str,
        number_of_units: int,
        power_consumption: int,
        device_type: str,
        id: Optional[int] = None,
        description: Optional[str] = None,
        rack_id: Optional[int] = None,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.description = description
        self.serial_number = serial_number
        self.number_of_units = number_of_units
        self.power_consumption = power_consumption
        self.device_type = device_type
        self.rack_id = rack_id
