from sqlmodel import Session, select

from app.models.db_models.device_model import Device
from app.repositories.device.device_repository import DeviceRepository


class DeviceSqlRepository(DeviceRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_or_update(self, device: Device):
        self.session.add(device)  # not awaitable
        await self.session.commit()
        await self.session.refresh(device)

        return device.id  # just for now

    async def get_all(self, skip: int, limit: int):
        devices = await self.session.exec(select(Device).offset(skip).limit(limit))
        return devices.all()

    async def get_by_id(self, device_id: int):
        devices = await self.session.exec(select(Device).where(Device.id == device_id))
        return devices.first()

    async def delete(self, device: Device):
        await self.session.delete(device)
        await self.session.commit()
