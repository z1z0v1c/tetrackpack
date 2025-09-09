from sqlmodel import Session, select

from models.rack import Rack
from repository.rack.rack_repository import RackRepository
from schemas.rack import RackCreate, RackUpdate


class RackSqlRepository(RackRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_rack(self, rack: RackCreate):
        db_rack = Rack(**rack.model_dump())

        self.session.add(db_rack)
        self.session.commit()
        self.session.refresh(db_rack)

        return db_rack


    def read_racks(self, skip: int = 0, limit: int = 100):
        return self.session.exec(select(Rack).offset(skip).limit(limit)).all()


    def read_rack(self, rack_id: int):
        return self.session.exec(select(Rack).where(Rack.id == rack_id)).first()


    def update_rack(self, rack_id: int, rack: RackUpdate):
        db_rack = self.read_rack(rack_id)
        if not db_rack:
            return None

        rack_data = rack.model_dump(exclude_unset=True)
        for key, value in rack_data.items():
            setattr(db_rack, key, value)

        self.session.add(db_rack)
        self.session.commit()
        self.session.refresh(db_rack)

        return db_rack


    def remove_rack(self, rack_id: int):
        db_rack = self.read_rack(rack_id)
        if not db_rack:
            return None

        self.session.delete(db_rack)
        self.session.commit()

        return db_rack