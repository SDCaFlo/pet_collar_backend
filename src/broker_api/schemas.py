from pydantic import BaseModel, Field
from datetime import datetime, timezone

class GeolocationCreate(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    altitude: int
    timestamp: datetime = Field(
        default_factory = lambda: datetime.now(timezone.utc)
    )


class CreateResponse(BaseModel):
    id: str

    class Config:
        from_attributes = True


class DeviceLocationResponse(BaseModel):
    id: str
    device_id: str
    latitude: float
    longitude: float
    altitude: int
    timestamp: datetime 

    class Config:
        from_attributes = True