from typing import List
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.exceptions import DatabaseError
from app.models.db_models import RackModel
from app.repositories import RackRepository


class RackSqlRepository(RackRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_or_update(self, rack: RackModel):
        try:
            self.session.add(rack)  # not awaitable
            await self.session.commit()
            await self.session.refresh(rack)
        except IntegrityError:
            await self.session.rollback()
            raise DatabaseError("Provided serial number already exists")

        return rack.id

    async def get_all(self, skip: int, limit: int):
        racks = await self.session.exec(select(RackModel).offset(skip).limit(limit))
        return racks.all()

    async def get_by_id(self, rack_id: int):
        racks = await self.session.exec(select(RackModel).where(RackModel.id == rack_id))
        return racks.first()

    async def get_by_ids(self, rack_ids: List[int]):
        result = await self.session.exec(select(RackModel).where(RackModel.id.in_(rack_ids)))
        return result.all()

    async def delete(self, rack: RackModel):
        await self.session.delete(rack)
        await self.session.commit()

        return rack.id
