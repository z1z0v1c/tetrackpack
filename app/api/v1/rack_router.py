from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.services import RackService
from app.injection import get_rack_service
from app.models.schemas import RackResponse, RackLayoutsResponse, RackCreateRequest, RackUpdateRequest, RackLayoutRequest


router = APIRouter()


@router.post("/", response_model=RackResponse)
async def create_rack(
    rack: RackCreateRequest, service: RackService = Depends(get_rack_service)
):
    return await service.create_rack(rack)

@router.post("/layout", response_model=RackLayoutsResponse)
async def suggest_layout(
    data: RackLayoutRequest, service: RackService = Depends(get_rack_service)
):
    try:
        layout = await service.suggest_layout(data.rack_ids, data.device_ids)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")

    return layout

@router.get("/", response_model=List[RackResponse])
async def get_all_racks(
    service: RackService = Depends(get_rack_service), skip: int = 0, limit: int = 100
):
    return await service.get_all_racks(skip=skip, limit=limit)


@router.get("/{id}", response_model=RackResponse)
async def get_rack_by_id(id: int, service: RackService = Depends(get_rack_service)):
    rack = await service.get_rack(id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")

    return rack


@router.put("/{id}", response_model=RackResponse)
async def update_rack_by_id(
    id: int, rack: RackUpdateRequest, service: RackService = Depends(get_rack_service)
):
    db_rack = await service.update_rack(id, rack)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")

    return db_rack


@router.put("/{id}/place/{device_id}")
async def place_device(
    id: int, device_id: int, service: RackService = Depends(get_rack_service)
):
    try:
        device = await service.place_device(id, device_id)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"{ex}")

    if not device:
        raise HTTPException(status_code=404, detail="Rack or device not found")
    
    return {"message": "Device placed successfully"}

@router.delete("/{id}")
async def delete_rack_by_id(id: int, service: RackService = Depends(get_rack_service)):
    db_rack = await service.delete_rack(id)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")

    return {"message": "Rack deleted successfully"}
