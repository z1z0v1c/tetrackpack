from sqlmodel import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate


def create_device(db: Session, device: DeviceCreate):
    db_device = Device(**device.model_dump())

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device