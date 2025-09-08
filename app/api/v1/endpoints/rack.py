from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.rack import create_rack
from app.database.session import get_db
from app.schemas.rack import RackResponse, RackCreate


router = APIRouter()


@router.post("/", response_model=RackResponse)
def post_rack(rack: RackCreate, db: Session = Depends(get_db)):
    return create_rack(db, rack)