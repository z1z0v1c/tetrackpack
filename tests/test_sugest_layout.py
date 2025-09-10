import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock
from app.models.db_models import Rack, Device, DeviceType
from app.models.schemas import RackLayoutsResponse, RackLayoutsResponse

@pytest.fixture
def sample_racks():
    return [
        Rack(id=1, name="Rack A", number_of_units=42, max_power_consumption=5000),
        Rack(id=2, name="Rack B", number_of_units=48, max_power_consumption=6000),
        Rack(id=3, name="Rack C", number_of_units=36, max_power_consumption=4000),
        Rack(id=4, name="Rack D", number_of_units=24, max_power_consumption=3000),
    ]

@pytest.fixture
def sample_devices():
    return [
        Device(id=1, name="Server A", number_of_units=4, power_consumption=2000, device_type=DeviceType.SERVER),
        Device(id=2, name="Server B", number_of_units=2, power_consumption=800, device_type=DeviceType.SERVER),
        Device(id=3, name="Server C", number_of_units=1, power_consumption=100, device_type=DeviceType.SERVER),
        Device(id=4, name="Storage A", number_of_units=3, power_consumption=1200, device_type=DeviceType.STORAGE),
        Device(id=5, name="Storage B", number_of_units=6, power_consumption=1800, device_type=DeviceType.STORAGE),
        Device(id=6, name="Switch A", number_of_units=1, power_consumption=300, device_type=DeviceType.SWITCH),
        Device(id=7, name="Router A", number_of_units=1, power_consumption=200, device_type=DeviceType.ROUTER),
    ]

@pytest.mark.asyncio
async def test_suggest_layout_single_rack(rack_service, mock_rack_repository, mock_device_repository, sample_racks, sample_devices):
    single_rack = [sample_racks[0]]
    few_devices = sample_devices[:3]
    
    mock_rack_repository.get_by_ids.return_value = single_rack
    mock_device_repository.get_by_ids.return_value = few_devices
    
    result = await rack_service.suggest_layout([1], [1, 2, 3])
    
    assert len(result.layout) == 1
    assert set(result.layout[0].devices) == {1, 2, 3}