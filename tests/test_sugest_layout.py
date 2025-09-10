import pytest
from fastapi import HTTPException
from app.models.db_models import Rack, Device, DeviceType
from app.models.schemas import RackLayoutsResponse

@pytest.fixture
def sample_racks():
    return [
        Rack(id=1, name="Rack A", number_of_units=42, max_power_consumption=5000),
        Rack(id=2, name="Rack B", number_of_units=48, max_power_consumption=6000),
    ]

@pytest.fixture
def sample_devices():
    return [
        Device(id=1, name="Server 1", number_of_units=2, power_consumption=800, device_type=DeviceType.SERVER),
        Device(id=2, name="Switch 1", number_of_units=1, power_consumption=300, device_type=DeviceType.SWITCH),
    ]

