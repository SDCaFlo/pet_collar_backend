from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from broker_api.db import get_db
from broker_api.models import Geolocation
from broker_api.schemas import GeolocationCreate, CreateResponse

router = APIRouter(prefix='/geolocation', tags=['geolocation'])

@router.post("/create", response_model=CreateResponse, status_code=201)
def create_geolocation(data: GeolocationCreate, db: Session = Depends(get_db)):
    record = Geolocation(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record