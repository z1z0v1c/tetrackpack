from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.repository.rack.rack_sql_repository import RackSqlRepository
from app.repository.session import get_rack_repository
from app.schemas.rack import RackResponse, RackCreate, RackUpdate


router = APIRouter()


@router.post("/", response_model=RackResponse)
async def post_rack(rack: RackCreate, repository: RackSqlRepository = Depends(get_rack_repository)):
    return repository.create_rack(rack)


@router.get("/", response_model=List[RackResponse])
async def get_racks(repository: RackSqlRepository = Depends(get_rack_repository), skip: int = 0, limit: int = 100):
    return repository.read_racks(skip=skip, limit=limit)


@router.get("/{rack_id}", response_model=RackResponse)
async def get_rack(rack_id: int, repository: RackSqlRepository = Depends(get_rack_repository)):
    rack = repository.read_rack(rack_id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return rack


@router.put("/{rack_id}", response_model=RackResponse)
async def put_rack(rack_id: int, rack: RackUpdate, repository: RackSqlRepository = Depends(get_rack_repository)):
    db_rack = repository.update_rack(rack_id, rack)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return db_rack


@router.delete("/{rack_id}")
async def delete_rack(rack_id: int, repository: RackSqlRepository = Depends(get_rack_repository)):
    db_rack = repository.remove_rack(rack_id)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return {"message": "Rack deleted successfully"}