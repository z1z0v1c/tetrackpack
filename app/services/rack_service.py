from app.models.db_models.rack_model import Rack
from app.repositories.rack.rack_repository import RackRepository
from app.models.schemas.rack_schemas import RackCreate, RackUpdate


class RackService:
    def __init__(self, repository: RackRepository):
        self.repository = repository


    def create_rack(self, rack: RackCreate):
        db_rack = Rack(**rack.model_dump())
        
        return self.repository.create_or_update(db_rack)
    

    def get_all_racks(self, skip: int, limit: int):
        return self.repository.get_all(skip, limit)
    

    def get_rack(self, rack_id: int):
        return self.repository.get_by_id(rack_id)


    def update_rack(self, rack_id: int, rack: RackUpdate):
        db_rack = self.repository.get_by_id(rack_id)
        if not db_rack:
            return None

        rack_data = rack.model_dump(exclude_unset=True)
        for key, value in rack_data.items():
            setattr(db_rack, key, value)

        return self.repository.create_or_update(db_rack)

    
    def delete_rack(self, rack_id: int):
        db_rack = self.repository.get_by_id(rack_id)
        if not db_rack:
            return None
        
        self.repository.delete(db_rack)