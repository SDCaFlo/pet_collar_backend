from sqlalchemy import Column, String, Float, DateTime, Integer, Index
from broker_api.db import Base
import uuid

class Geolocation(Base):
    __tablename__ = "geolocations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    __table_args_ = (
        Index("idx_deviceid_timestamp", device_id, timestamp)
    )