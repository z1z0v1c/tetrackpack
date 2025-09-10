from app.models.db_models import Device
from app.repositories import DeviceRepository
from app.models.schemas import DeviceCreateRequest, DeviceFullResponse, DeviceUpdateRequest


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    async def get_all_devices(self, skip: int, limit: int):
        db_models = await self.repository.get_all(skip, limit)
        return [
            DeviceFullResponse.model_validate(db_model) for db_model in db_models
        ]

    async def get_device(self, id: int):
        db_model = await self.repository.get_by_id(id)
        return DeviceFullResponse.model_validate(db_model)

    async def create_device(self, data: DeviceCreateRequest):
        db_model = Device.from_entity(data.to_entity())
        return await self.repository.create_or_update(db_model)

    async def update_device(self, id: int, data: DeviceUpdateRequest):
        db_model = await self.repository.get_by_id(id)
        if not db_model:
            return None

        device_data = data.model_dump(exclude_unset=True)
        for key, value in device_data.items():
            setattr(db_model, key, value)

        return await self.repository.create_or_update(db_model)

    async def delete_device(self, id: int):
        db_model = await self.repository.get_by_id(id)
        if not db_model:
            return None

        return await self.repository.delete(db_model)

