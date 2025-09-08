from sqlmodel import Session
from app.models.rack import Rack
from app.schemas.rack import RackCreate


def create_rack(db: Session, rack: RackCreate):
    db_rack = Rack(**rack.model_dump())

    db.add(db_rack)
    db.commit()
    db.refresh(db_rack)

    return db_rack