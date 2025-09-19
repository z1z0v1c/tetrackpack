from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.exceptions import DatabaseError
from app.services import RackService
from app.injection import get_rack_service
from app.models.schemas import (
    RackFullResponse,
    RackSimpleResponse,
    RackLayoutsResponse,
    RackCreateRequest,
    RackUpdateRequest,
    RackLayoutRequest,
)


router = APIRouter()


@router.post("/")
async def create_rack(
    data: RackCreateRequest, service: RackService = Depends(get_rack_service)
) -> RackSimpleResponse:
    try:
        rack_id = await service.create_rack(data)
    except DatabaseError as error:
        raise HTTPException(status_code=400, detail=f"{error}")

    return {"id": rack_id, "detail": "Device created successfully"}


@router.post("/layout")
async def suggest_layout(
    data: RackLayoutRequest, service: RackService = Depends(get_rack_service)
) -> RackLayoutsResponse:
    try:
        layout = await service.suggest_layout(data.rack_ids, data.device_ids)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")

    return layout


@router.get("/")
async def get_all_racks(
    service: RackService = Depends(get_rack_service), skip: int = 0, limit: int = 100
) -> List[RackFullResponse]:
    return await service.get_all_racks(skip=skip, limit=limit)


@router.get("/{id}", response_model=RackFullResponse)
async def get_rack_by_id(
    id: int, service: RackService = Depends(get_rack_service)
) -> RackFullResponse:
    rack = await service.get_rack(id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")

    return rack


@router.put("/{id}")
async def update_rack_by_id(
    id: int, data: RackUpdateRequest, service: RackService = Depends(get_rack_service)
) -> RackSimpleResponse:
    try:
        rack_id = await service.update_rack(id, data)
    except DatabaseError as error:
        raise HTTPException(status_code=400, detail=f"{error}")

    if not rack_id:
        raise HTTPException(status_code=404, detail="Rack not found")

    return {"id": rack_id, "detail": "Rack updated successfully"}


@router.put("/{id}/place/{device_id}")
async def place_device(
    id: int, device_id: int, service: RackService = Depends(get_rack_service)
) -> RackSimpleResponse:
    try:
        device = await service.place_device(id, device_id)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")

    if not device:
        raise HTTPException(status_code=404, detail="Rack or device not found")

    return {"id": id, "detail": f"Device {device_id} placed successfully"}


@router.delete("/{id}")
async def delete_rack_by_id(
    id: int, service: RackService = Depends(get_rack_service)
) -> RackSimpleResponse:
    rack_id = await service.delete_rack(id)
    if not rack_id:
        raise HTTPException(status_code=404, detail="Rack not found")

    return {"id": rack_id, "detail": "Rack deleted successfully"}
