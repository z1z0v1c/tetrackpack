from sqlmodel import Session, select

from models.device_models import Device
from repository.device.device_repository import DeviceRepository

class DeviceSqlRepository(DeviceRepository):
    def __init__(self, session: Session):
        self.session = session
    

    def create_or_update(self, device: Device):
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)

        return device
    
    
    def get_all(self, skip: int, limit: int):
        return self.session.exec(select(Device).offset(skip).limit(limit)).all()
    
    
    def get_by_id(self, device_id: int):
        return self.session.exec(select(Device).where(Device.id == device_id)).first()
    
    
    def delete(self, device: Device):
        self.session.delete(device)
        self.session.commit()
