from app.models.db_models import Rack
from app.repositories import RackRepository, DeviceRepository
from app.models.schemas import RackCreate, RackResponse, RackUpdate


class RackService:
    def __init__(self, rack_repository: RackRepository, device_repository: DeviceRepository):
        self.rack_repository = rack_repository
        self.device_repository = device_repository

    async def create_rack(self, data: RackCreate):
        db_model = Rack.from_entity(data.to_entity())
        return await self.rack_repository.create_or_update(db_model)

    async def get_all_racks(self, skip: int, limit: int):
        db_models = await self.rack_repository.get_all(skip, limit)
        return [
            RackResponse.from_entity(db_model.to_entity()) for db_model in db_models
        ]

    async def get_rack(self, id: int):
        db_model = await self.rack_repository.get_by_id(id)
        return RackResponse.from_entity(db_model.to_entity())

    async def update_rack(self, rack_id: int, data: RackUpdate):
        db_model = await self.rack_repository.get_by_id(rack_id)
        if not db_model:
            return None

        # Keep for now
        rack_data = data.model_dump(exclude_unset=True)
        for key, value in rack_data.items():
            setattr(db_model, key, value)

        return await self.rack_repository.create_or_update(db_model)

    async def place_device(self, id: int, device_id: int):
        rack_model = await self.rack_repository.get_by_id(id)
        device_model = await self.device_repository.get_by_id(device_id)

        if not rack_model or not device_model:
            return None

        rack_entity = rack_model.to_entity()

        if not rack_entity.has_enough_units(device_model.number_of_units):
            raise ValueError("Not enough rack units available")

        if not rack_entity.has_enough_power(device_model.power_consumption):
            raise ValueError("Rack power capacity exceeded")

        device_model.rack_id = rack_model.id
        return await self.device_repository.update(device_model)

    async def delete_rack(self, rack_id: int):
        db_model = await self.rack_repository.get_by_id(rack_id)
        if not db_model:
            return None

        await self.rack_repository.delete(db_model)

        return db_model
