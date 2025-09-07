from sqlmodel import Session, select

from app.models.device import Device
from app.schemas.device import DeviceCreate


def create_device(db: Session, device: DeviceCreate):
    db_device = Device(**device.model_dump())

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device


def read_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(Device).offset(skip).limit(limit)).all()


def read_device(db: Session, device_id: int):
    return db.exec(select(Device).where(Device.id == device_id)).first()