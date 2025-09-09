from typing import List
from fastapi import APIRouter, Depends, HTTPException

from services.rack_service import RackService
from dependencies import get_rack_service
from schemas.rack import RackResponse, RackCreate, RackUpdate


router = APIRouter()


@router.post("/", response_model=RackResponse)
async def post_rack(rack: RackCreate, service: RackService = Depends(get_rack_service)):
    return service.create_rack(rack)


@router.get("/", response_model=List[RackResponse])
async def get_racks(service: RackService = Depends(get_rack_service), skip: int = 0, limit: int = 100):
    return service.get_all_racks(skip=skip, limit=limit)


@router.get("/{rack_id}", response_model=RackResponse)
async def get_rack(rack_id: int, service: RackService = Depends(get_rack_service)):
    rack = service.get_rack(rack_id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return rack


@router.put("/{rack_id}", response_model=RackResponse)
async def put_rack(rack_id: int, rack: RackUpdate, service: RackService = Depends(get_rack_service)):
    db_rack = service.update_rack(rack_id, rack)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return db_rack


@router.delete("/{rack_id}")
async def delete_rack(rack_id: int, service: RackService = Depends(get_rack_service)):
    db_rack = service.delete_rack(rack_id)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return {"message": "Rack deleted successfully"}
