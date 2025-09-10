from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.repositories import (
    RackRepository,
    DeviceRepository,
    DeviceSqlRepository,
    RackSqlRepository,
)
from app.services import RackService, DeviceService


engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def get_db_session():
    async with AsyncSession(engine) as db_session:
        yield db_session


def get_device_repository(db_session: AsyncSession = Depends(get_db_session)):
    return DeviceSqlRepository(db_session)


def get_rack_repository(db_session: AsyncSession = Depends(get_db_session)):
    return RackSqlRepository(db_session)


def get_device_service(repository: DeviceRepository = Depends(get_device_repository)):
    return DeviceService(repository)


def get_rack_service(
    rack_repository: RackRepository = Depends(get_rack_repository),
    device_repository: DeviceRepository = Depends(get_device_repository),
):
    return RackService(rack_repository, device_repository)
