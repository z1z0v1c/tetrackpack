from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.exceptions import DatabaseError
from app.injection import get_device_service
from app.models.schemas import (
    DeviceCreateRequest,
    DeviceFullResponse,
    DeviceUpdateRequest,
    DeviceSimpleResponse,
)
from app.services import DeviceService


router = APIRouter()


@router.post("/", response_model=DeviceSimpleResponse)
async def create_device(
    data: DeviceCreateRequest, service: DeviceService = Depends(get_device_service)
):
    try:
        device_id = await service.create_device(data)
    except DatabaseError as error:
        raise HTTPException(status_code=400, detail=f"{error}")

    return {"id": device_id, "detail": "Device created successfully"}


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


@router.put("/{id}", response_model=DeviceSimpleResponse)
async def update_device_by_id(
    id: int,
    device: DeviceUpdateRequest,
    service: DeviceService = Depends(get_device_service),
):
    device_id = await service.update_device(id, device)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"id": device_id, "detail": "Device updated successfully"}


@router.delete("/{id}", response_model=DeviceSimpleResponse)
async def delete_device_by_id(
    id: int, service: DeviceService = Depends(get_device_service)
):
    device_id = await service.delete_device(id)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")

    return {"id": device_id, "detail": "Device deleted successfully"}
