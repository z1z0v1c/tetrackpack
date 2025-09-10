from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.exceptions import DatabaseError
from app.injection import get_device_service
from app.models.schemas import (
    DeviceCreateRequest,
    DeviceFullResponse,
    DeviceUpdateRequest,
)
from app.services import DeviceService


router = APIRouter()


@router.post("/", response_model=int)
async def create_device(
    data: DeviceCreateRequest, service: DeviceService = Depends(get_device_service)
):
    try:
        id = await service.create_device(data)
    except DatabaseError as error:
        raise HTTPException(status_code=400, detail=f"{error}")

    return {"id": id, "message": "Device created successfully"}


@router.get("/", response_model=List[DeviceFullResponse])
async def get_all_devices(
    skip: int = 0,
    limit: int = 100,
    service: DeviceService = Depends(get_device_service),
):
    return await service.get_all_devices(skip, limit)


@router.get("/{id}", response_model=DeviceFullResponse)
async def get_device_by_id(
    id: int, service: DeviceService = Depends(get_device_service)
):
    device = await service.get_device(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.put("/{id}", response_model=int)
async def update_device_by_id(
    id: int,
    device: DeviceUpdateRequest,
    service: DeviceService = Depends(get_device_service),
):
    db_device = await service.update_device(id, device)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return db_device


@router.delete("/{id}")
async def delete_device_by_id(
    id: int, service: DeviceService = Depends(get_device_service)
):
    db_device = await service.delete_device(id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"message": "Device deleted successfully"}
