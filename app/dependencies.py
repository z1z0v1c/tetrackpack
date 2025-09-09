from fastapi import Depends
from sqlmodel import create_engine, Session

from repositories.rack.rack_repository import RackRepository
from services.rack_service import RackService
from services.device_service import DeviceService
from repositories.device.device_repository import DeviceRepository
from config import settings
from repositories.device.device_sql_repository import DeviceSqlRepository
from repositories.rack.rack_sql_repository import RackSqlRepository


engine = create_engine(settings.DATABASE_URL, echo=True)


def get_db_session():
    with Session(engine) as db_session:
        yield db_session


def get_device_repository(db_session: Session = Depends(get_db_session)):
    return DeviceSqlRepository(db_session)


def get_rack_repository(db_session: Session = Depends(get_db_session)):
    return RackSqlRepository(db_session)


def get_device_service(repository: DeviceRepository = Depends(get_device_repository)):
    return DeviceService(repository)


def get_rack_service(repository: RackRepository = Depends(get_rack_repository)):
    return RackService(repository)
