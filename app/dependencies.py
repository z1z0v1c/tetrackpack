from fastapi import Depends
from sqlmodel import create_engine, Session

from config import settings
from repository.device.device_sql_repository import DeviceSqlRepository
from repository.rack.rack_sql_repository import RackSqlRepository


engine = create_engine(settings.DATABASE_URL, echo=True)


def get_db_session():
    with Session(engine) as db_session:
        yield db_session


def get_device_repository(db_session: Session = Depends(get_db_session)):
    return DeviceSqlRepository(db_session)


def get_rack_repository(db_session: Session = Depends(get_db_session)):
    return RackSqlRepository(db_session)