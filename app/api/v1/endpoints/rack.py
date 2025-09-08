from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.rack import create_rack, read_rack, read_racks, update_rack
from app.database.session import get_db
from app.schemas.rack import RackResponse, RackCreate, RackUpdate


router = APIRouter()


@router.post("/", response_model=RackResponse)
def post_rack(rack: RackCreate, db: Session = Depends(get_db)):
    return create_rack(db, rack)


@router.get("/", response_model=List[RackResponse])
def get_racks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_racks(db, skip=skip, limit=limit)


@router.get("/{rack_id}", response_model=RackResponse)
def get_rack(rack_id: int, db: Session = Depends(get_db)):
    rack = read_rack(db, rack_id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return rack


@router.put("/{rack_id}", response_model=RackResponse)
def put_rack(rack_id: int, rack: RackUpdate, db: Session = Depends(get_db)):
    db_rack = update_rack(db, rack_id, rack)
    if not db_rack:
        raise HTTPException(status_code=404, detail="Rack not found")
    
    return db_rack