from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional

class IncidentBase(BaseModel):
    title: str = Field(...)
    incident_type: str = Field(...)
    zone: str = Field(...)
    location: str = Field(...)
    description: Optional[str] = Field(None)
    occurred_at: datetime = Field(...)
    status_id: int = Field(1)

class IncidentResponse(IncidentBase):
    id: int
    photo_url: Optional[str]
    video_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class IncidentUpdate(BaseModel):
    title: Optional[str]
    incident_type: Optional[str]
    zone: Optional[str]
    location: Optional[str]
    description: Optional[str]
    occurred_at: Optional[datetime]
    status_id: Optional[int]

class ZoneReport(BaseModel):
    zone: str
    incident_count: int
    by_type: Dict[str, int]
