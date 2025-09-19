from typing import AsyncGenerator
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.repositories import (
    AbstractRepository,
    DeviceSqlRepository,
    RackSqlRepository,
)
from app.services import RackService, DeviceService


engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_device_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> DeviceSqlRepository:
    return DeviceSqlRepository(db_session)


def get_rack_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> RackSqlRepository:
    return RackSqlRepository(db_session)


def get_device_service(
    repository: AbstractRepository = Depends(get_device_repository),
) -> DeviceService:
    return DeviceService(repository)


def get_rack_service(
    rack_repository: AbstractRepository = Depends(get_rack_repository),
    device_repository: AbstractRepository = Depends(get_device_repository),
) -> RackService:
    return RackService(rack_repository, device_repository)
