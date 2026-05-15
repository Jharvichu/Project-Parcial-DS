from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from app.database import Base


class Incident(Base):
    __tablename__ = "incident"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    incident_type = Column(String(100), nullable=False)
    zone = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    occurred_at = Column(DateTime, nullable=False)
    status_id = Column(Integer, nullable=False, default=1)
    photo_url = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
