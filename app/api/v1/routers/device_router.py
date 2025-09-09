from typing import List
from fastapi import APIRouter, Depends, HTTPException

from services.device_service import DeviceService
from app.injection import get_device_service
from schemas.device_schemas import DeviceCreate, DeviceResponse, DeviceUpdate


router = APIRouter()


@router.post("/", response_model=DeviceResponse)
async def create_device(device: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    return service.create_device(device)


@router.get("/", response_model=List[DeviceResponse])
async def get_all_devices(skip: int = 0, limit: int = 100, service: DeviceService = Depends(get_device_service)):
    devices = service.get_all_devices(skip, limit)
    return devices


@router.get("/{id}", response_model=DeviceResponse)
async def get_device_by_id(id: int, service: DeviceService = Depends(get_device_service)):
    device = service.get_device(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return device


@router.put("/{id}", response_model=DeviceResponse)
def update_device_by_id(id: int, device: DeviceUpdate, service: DeviceService = Depends(get_device_service)):
    db_device = service.update_device(id, device)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return db_device


@router.delete("/{id}")
def delete_device_by_id(id: int, service: DeviceService = Depends(get_device_service)):
    db_device = service.delete_device(id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"message": "Device deleted successfully"}
