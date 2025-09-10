from app.models.db_models import Rack
from app.repositories import RackRepository
from app.models.schemas import RackCreate, RackResponse, RackUpdate


class RackService:
    def __init__(self, repository: RackRepository):
        self.repository = repository

    async def create_rack(self, data: RackCreate):
        db_model = Rack.from_entity(data.to_entity())
        return await self.repository.create_or_update(db_model)

    async def get_all_racks(self, skip: int, limit: int):
        db_models = await self.repository.get_all(skip, limit)
        return [
            RackResponse.from_entity(db_model.to_entity()) for db_model in db_models
        ]

    async def get_rack(self, id: int):
        db_model = await self.repository.get_by_id(id)
        return RackResponse.from_entity(db_model.to_entity())

    async def update_rack(self, rack_id: int, data: RackUpdate):
        db_model = await self.repository.get_by_id(rack_id)
        if not db_model:
            return None

        # Keep for now
        rack_data = data.model_dump(exclude_unset=True)
        for key, value in rack_data.items():
            setattr(db_model, key, value)

        return await self.repository.create_or_update(db_model)

    async def delete_rack(self, rack_id: int):
        db_model = await self.repository.get_by_id(rack_id)
        if not db_model:
            return None

        await self.repository.delete(db_model)

        return db_model
