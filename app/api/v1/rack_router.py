from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.services.rack_service import RackService
from app.injection import get_rack_service
from app.models.schemas.rack_schemas import RackResponse, RackCreate, RackUpdate


router = APIRouter()


@router.post("/", response_model=RackResponse)
async def create_rack(rack: RackCreate, service: RackService = Depends(get_rack_service)):
    return await service.create_rack(rack)


@router.get("/", response_model=List[RackResponse])
async def get_all_racks(service: RackService = Depends(get_rack_service), skip: int = 0, limit: int = 100):
    return await service.get_all_racks(skip=skip, limit=limit)


@router.get("/{id}", response_model=RackResponse)
async def get_rack_by_id(id: int, service: RackService = Depends(get_rack_service)):
    rack = await service.get_rack(id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return rack


@router.put("/{id}", response_model=RackResponse)
async def update_rack_by_id(id: int, rack: RackUpdate, service: RackService = Depends(get_rack_service)):
    db_rack = await service.update_rack(id, rack)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return db_rack


@router.delete("/{id}")
async def delete_rack_by_id(id: int, service: RackService = Depends(get_rack_service)):
    db_rack = await service.delete_rack(id)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return {"message": "Rack deleted successfully"}
