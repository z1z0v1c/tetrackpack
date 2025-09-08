from fastapi import Depends
from sqlmodel import Session, select

from app.models.device import Device
from app.repository.device.device_repository import DeviceRepository
from app.repository.session import get_session
from app.schemas.device import DeviceCreate, DeviceUpdate

class DeviceSqlRepository(DeviceRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    

    def create_device(self, device: DeviceCreate):
        db_device = Device(**device.model_dump())
    
        self.session.add(db_device)
        self.session.commit()
        self.session.refresh(db_device)
    
        return db_device
    
    
    def read_devices(self, skip: int = 0, limit: int = 100):
        return self.session.exec(select(Device).offset(skip).limit(limit)).all()
    
    
    def read_device(self, device_id: int):
        return self.session.exec(select(Device).where(Device.id == device_id)).first()
    
    
    def update_device(self, device_id: int, device: DeviceUpdate):
        db_device = self.read_device(device_id)
        if not db_device:
            return None
        
        device_data = device.model_dump(exclude_unset=True)
        for key, value in device_data.items():
            setattr(db_device, key, value)
        
        self.session.add(db_device)
        self.session.commit()
        self.session.refresh(db_device)
    
        return db_device
    
    
    def remove_device(self, device_id: int):
        db_device = self.read_device(device_id)
        if not db_device:
            return None
        
        self.session.delete(db_device)
        self.session.commit()
    
        return db_device
