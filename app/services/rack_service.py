from typing import List, Optional
from app.models.db_models import RackModel
from app.models.schemas.rack_schemas import RackLayoutResponse, RackLayoutsResponse
from app.repositories import AbstractRepository
from app.models.schemas import RackCreateRequest, RackFullResponse, RackUpdateRequest


class RackService:
    def __init__(
        self, rack_repository: AbstractRepository, device_repository: AbstractRepository
    ) -> None:
        self.rack_repository = rack_repository
        self.device_repository = device_repository

    async def create_rack(self, data: RackCreateRequest) -> int:
        db_model = RackModel.from_entity(data.to_entity())
        return await self.rack_repository.create_or_update(db_model)

    async def get_all_racks(self, skip: int, limit: int) -> list[RackFullResponse]:
        db_models = await self.rack_repository.get_all(skip, limit)
        return [
            RackFullResponse.from_entity(db_model.to_entity()) for db_model in db_models
        ]

    async def get_rack(self, id: int) -> Optional[RackFullResponse]:
        db_model = await self.rack_repository.get_by_id(id)
        if not db_model:
            return None

        return RackFullResponse.model_validate(db_model)

    async def update_rack(self, rack_id: int, data: RackUpdateRequest) -> Optional[int]:
        db_model = await self.rack_repository.get_by_id(rack_id)
        if not db_model:
            return None

        # Keep for now
        rack_data = data.model_dump(exclude_unset=True)
        for key, value in rack_data.items():
            setattr(db_model, key, value)

        return await self.rack_repository.create_or_update(db_model)

    async def place_device(self, id: int, device_id: int) -> Optional[int]:
        rack_model = await self.rack_repository.get_by_id(id)
        device_model = await self.device_repository.get_by_id(device_id)

        if not rack_model or not device_model:
            return None

        rack_entity = rack_model.to_entity()

        if not rack_entity.has_enough_units(device_model.number_of_units):
            raise Exception("Not enough rack units available")

        if not rack_entity.has_enough_power(device_model.power_consumption):
            raise Exception("Rack power capacity exceeded")

        device_model.rack_id = rack_model.id
        return await self.device_repository.update(device_model)

    async def suggest_layout(
        self, rack_ids: List[int], device_ids: List[int]
    ) -> RackLayoutsResponse:
        racks = await self.rack_repository.get_by_ids(rack_ids)
        devices = await self.device_repository.get_by_ids(device_ids)

        if len(racks) != len(rack_ids):
            raise Exception("Some racks not found")
        if len(devices) != len(device_ids):
            raise Exception("Some devices not found")

        layout = {rack.id: [] for rack in racks}
        used_units = {rack.id: 0 for rack in racks}
        used_power = {rack.id: 0 for rack in racks}

        sorted_devices = sorted(
            devices, key=lambda d: d.power_consumption, reverse=True
        )

        for device in sorted_devices:
            best_rack_id = None
            min_utilization = float("inf")

            for rack in racks:
                if (
                    used_units[rack.id] + device.number_of_units <= rack.number_of_units
                    and used_power[rack.id] + device.power_consumption
                    <= rack.max_power_consumption
                ):

                    current_utilization = (
                        used_power[rack.id] / rack.max_power_consumption * 100
                    )

                    if current_utilization < min_utilization:
                        min_utilization = current_utilization
                        best_rack_id = rack.id

            if best_rack_id:
                used_power[best_rack_id] += device.power_consumption
                used_units[best_rack_id] += device.number_of_units
                layout[best_rack_id].append(device.id)

            layouts = []
            for rack in racks:
                utilization = used_power[rack.id] / rack.max_power_consumption * 100

                layouts.append(
                    RackLayoutResponse(
                        rack_id=rack.id,
                        devices=layout[rack.id],
                        utilization=round(utilization, 2),
                    )
                )

        return RackLayoutsResponse(layout=layouts)

    async def delete_rack(self, rack_id: int) -> Optional[int]:
        db_model = await self.rack_repository.get_by_id(rack_id)
        if not db_model:
            return None

        return await self.rack_repository.delete(db_model)
