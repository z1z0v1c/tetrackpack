from typing import List
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.exceptions import DatabaseError
from app.models.db_models import Device
from app.repositories import DeviceRepository


class DeviceSqlRepository(DeviceRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_or_update(self, device: Device):
        try:
            self.session.add(device)  # not awaitable
            await self.session.commit()
            await self.session.refresh(device)
        except IntegrityError:
            await self.session.rollback()
            raise DatabaseError("Provided serial number already exists")

        return device.id

    async def get_all(self, skip: int, limit: int):
        devices = await self.session.exec(select(Device).offset(skip).limit(limit))
        return devices.all()

    async def get_by_id(self, device_id: int):
        devices = await self.session.exec(select(Device).where(Device.id == device_id))
        return devices.first()

    async def get_by_ids(self, device_ids: List[int]):
        result = await self.session.exec(
            select(Device).where(Device.id.in_(device_ids))
        )
        return result.all()

    async def delete(self, device: Device):
        await self.session.delete(device)
        await self.session.commit()

        return device.id
