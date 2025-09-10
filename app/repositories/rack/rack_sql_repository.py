from typing import List
from sqlmodel import Session, select

from app.models.db_models import Rack
from app.repositories import RackRepository


class RackSqlRepository(RackRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_or_update(self, rack: Rack):
        self.session.add(rack) # not awaitable
        await self.session.commit()
        await self.session.refresh(rack)

        return rack

    async def get_all(self, skip: int, limit: int):
        racks = await self.session.exec(select(Rack).offset(skip).limit(limit))
        return racks.all()

    async def get_by_id(self, rack_id: int):
        racks = await self.session.exec(select(Rack).where(Rack.id == rack_id))
        return racks.first()

    async def get_by_ids(self, rack_ids: List[int]):
        result = await self.session.exec(select(Rack).where(Rack.id.in_(rack_ids)))
        return result.all()

    async def delete(self, rack: Rack):
        await self.session.delete(rack)
        await self.session.commit()
