from models.device_models import Device
from repository.device.device_repository import DeviceRepository
from schemas.device_schemas import DeviceCreate, DeviceUpdate


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository


    def get_all_devices(self, skip: int, limit: int):
        return self.repository.get_all(skip, limit)

    
    def get_device(self, device_id: int):
        return self.repository.get_by_id(device_id)

    
    def create_device(self, device: DeviceCreate):
        db_device = Device(**device.model_dump())

        return self.repository.create_or_update(db_device)
    

    def update_device(self, device_id: int, device: DeviceUpdate):
        db_device = self.repository.get_by_id(device_id)
        if not db_device:
            return None
        
        device_data = device.model_dump(exclude_unset=True)
        for key, value in device_data.items():
            setattr(db_device, key, value)

        return self.repository.create_or_update(db_device)
    
    
    def delete_device(self, device_id: int):
        db_device = self.repository.get_by_id(device_id)
        if not db_device:
            return None
        
        self.repository.delete(db_device)

        return db_device
        