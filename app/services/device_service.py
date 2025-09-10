from app.models.db_models.device_model import Device
from app.repositories.device.device_repository import DeviceRepository
from app.models.schemas.device_schemas import DeviceCreate, DeviceResponse, DeviceUpdate


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    async def get_all_devices(self, skip: int, limit: int):
        db_models = await self.repository.get_all(skip, limit)
        return [
            DeviceResponse.from_entity(db_model.to_entity()) for db_model in db_models
        ]

    async def get_device(self, id: int):
        db_model = await self.repository.get_by_id(id)
        return DeviceResponse.from_entity(db_model.to_entity())

    async def create_device(self, data: DeviceCreate):
        db_model = Device.from_entity(data.to_entity())
        return await self.repository.create_or_update(db_model)

    async def update_device(self, id: int, data: DeviceUpdate):
        db_model = await self.repository.get_by_id(id)
        if not db_model:
            return None

        # skip conversion to entity for now
        device_data = data.model_dump(exclude_unset=True)
        for key, value in device_data.items():
            setattr(db_model, key, value)

        return await self.repository.create_or_update(db_model)

    async def delete_device(self, id: int):
        db_model = await self.repository.get_by_id(id)
        if not db_model:
            return None

        await self.repository.delete(db_model)

        return db_model
