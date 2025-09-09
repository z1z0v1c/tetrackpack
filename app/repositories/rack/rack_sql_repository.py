from sqlmodel import Session, select

from models.rack import Rack
from repositories.rack.rack_repository import RackRepository


class RackSqlRepository(RackRepository):
    def __init__(self, session: Session):
        self.session = session


    def create_or_update(self, rack: Rack):
        self.session.add(rack)
        self.session.commit()
        self.session.refresh(rack)

        return rack


    def get_all(self, skip: int, limit: int):
        return self.session.exec(select(Rack).offset(skip).limit(limit)).all()


    def get_by_id(self, rack_id: int):
        return self.session.exec(select(Rack).where(Rack.id == rack_id)).first()


    def delete(self, rack: Rack):
        self.session.delete(rack)
        self.session.commit()
