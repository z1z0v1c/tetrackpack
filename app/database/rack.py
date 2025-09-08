from sqlmodel import Session, select
from app.models.rack import Rack
from app.schemas.rack import RackCreate


def create_rack(db: Session, rack: RackCreate):
    db_rack = Rack(**rack.model_dump())

    db.add(db_rack)
    db.commit()
    db.refresh(db_rack)

    return db_rack


def read_racks(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(Rack).offset(skip).limit(limit)).all()


def read_rack(db: Session, rack_id: int):
    return db.exec(select(Rack).where(Rack.id == rack_id)).first()