from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.repository.device.device_sql_repository import DeviceSqlRepository
from app.repository.session import get_device_repository
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate


router = APIRouter()


@router.post("/", response_model=DeviceResponse)
async def post_device(device: DeviceCreate, repository: DeviceSqlRepository = Depends(get_device_repository)):
    return repository.create_device(device)


@router.get("/", response_model=List[DeviceResponse])
async def get_devices(skip: int = 0, limit: int = 100, repository: DeviceSqlRepository = Depends(get_device_repository)):
    devices = repository.read_devices(skip=skip, limit=limit)
    return devices


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, repository: DeviceSqlRepository = Depends(get_device_repository)):
    device = repository.read_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def put_device(device_id: int, device: DeviceUpdate, repository: DeviceSqlRepository = Depends(get_device_repository)):
    db_device = repository.update_device(device_id, device)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return db_device


@router.delete("/{device_id}")
def delete_device(device_id: int, repository: DeviceSqlRepository = Depends(get_device_repository)):
    db_device = repository.remove_device(device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"message": "Device deleted successfully"}
