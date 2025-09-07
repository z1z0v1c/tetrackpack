from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.device import create_device, read_devices
from app.database.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse


router = APIRouter()


@router.post("/", response_model=DeviceResponse)
async def post_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, device)


@router.get("/", response_model=List[DeviceResponse])
async def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = read_devices(db, skip=skip, limit=limit)
    return devices