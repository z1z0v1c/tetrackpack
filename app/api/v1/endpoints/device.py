from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.device import create_device
from app.database.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse


router = APIRouter()


@router.post("/", response_model=DeviceResponse)
def post_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, device)