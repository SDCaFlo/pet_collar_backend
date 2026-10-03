from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from broker_api.db import get_db
from broker_api.models import Geolocation
from broker_api.schemas import DeviceLocationResponse

router = APIRouter(prefix='/devices', tags=['devices'])

@router.get("/{device_id}/locations", response_model=list[DeviceLocationResponse])
def get_locations(
    device_id: str,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)):

    stmt = select(Geolocation).where(Geolocation.device_id == device_id)
    if start:
        stmt = stmt.where(Geolocation.timestamp >= start)
    if end:
        stmt = stmt.where(Geolocation.timestamp <= end)
    stmt = stmt.order_by(Geolocation.timestamp.desc()).limit(limit)

    return db.scalars(stmt).all()


@router.get("/{device_id}/latest", response_model=DeviceLocationResponse)
def get_last_location(
    device_id: str,
    db: Session = Depends(get_db)
):
    stmt = (
        select(Geolocation)
        .where(Geolocation.device_id == device_id)
        .order_by(Geolocation.timestamp.desc())
        .limit(1)
    )

    row = db.scalars(stmt).first()

    if not row:
        raise HTTPException(404, "Dispositivo sin datos")
    return row


@router.get("/ids", response_model=list[str])
def get_devices(
    db: Session = Depends(get_db)
):
    stmt = (
        select(Geolocation.device_id)
        .distinct().order_by(Geolocation.device_id)
    )

    devices = db.scalars(stmt).all()
    return devices

