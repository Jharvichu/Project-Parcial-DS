from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.Incident import IncidentResponse, ZoneReport
from app.models.incident_model import Incident

router = APIRouter()

UPLOADS_DIR = Path(__file__).resolve().parents[3] / "uploads"
PHOTO_DIR = UPLOADS_DIR / "photos"
VIDEO_DIR = UPLOADS_DIR / "videos"
PHOTO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_PHOTO_EXT: Set[str] = {".jpg", ".jpeg", ".png"}
ALLOWED_VIDEO_EXT: Set[str] = {".mp4", ".mov", ".avi"}


def validate_status(status_id: int) -> None:
    if status_id < 1 or status_id > 3:
        raise HTTPException(status_code=400, detail="status_id inválido")


def validate_upload(file: Optional[UploadFile], allowed_extensions: Set[str]) -> None:
    if file is None or not file.filename:
        return
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Formato no permitido: {suffix}")


async def save_upload(file: Optional[UploadFile], dest_dir: Path) -> Optional[str]:
    if file is None or not file.filename:
        return None
    validate_upload(file, ALLOWED_PHOTO_EXT if dest_dir == PHOTO_DIR else ALLOWED_VIDEO_EXT)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{Path(file.filename).name}"
    destination = dest_dir / filename
    destination.write_bytes(await file.read())
    return str(destination.relative_to(Path(__file__).resolve().parents[3]))


class IncidentUpdate(BaseModel):
    title: Optional[str]
    incident_type: Optional[str]
    zone: Optional[str]
    location: Optional[str]
    description: Optional[str]
    occurred_at: Optional[datetime]
    status_id: Optional[int]


@router.post("/", response_model=IncidentResponse)
async def create_incident(
    title: str = Form(...),
    incident_type: str = Form(...),
    zone: str = Form(...),
    location: str = Form(...),
    description: Optional[str] = Form(None),
    occurred_at: datetime = Form(...),
    status_id: int = Form(1),
    photo: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    validate_status(status_id)
    photo_url = await save_upload(photo, PHOTO_DIR)
    video_url = await save_upload(video, VIDEO_DIR)

    incident = Incident(
        title=title,
        incident_type=incident_type,
        zone=zone,
        location=location,
        description=description,
        occurred_at=occurred_at,
        status_id=status_id,
        photo_url=photo_url,
        video_url=video_url,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.get("/", response_model=List[IncidentResponse])
def get_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    updates = payload.dict(exclude_unset=True)
    if "status_id" in updates:
        validate_status(updates["status_id"])

    for field, value in updates.items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}")
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    db.delete(incident)
    db.commit()
    return {"detail": "Incidente eliminado"}


@router.get("/report-by-zone", response_model=List[ZoneReport])
def report_by_zone(zone: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Incident)
    if zone:
        query = query.filter(Incident.zone == zone)
    incidents = query.all()

    summary: Dict[str, ZoneReport] = {}
    for incident in incidents:
        zone_name = incident.zone
        if zone_name not in summary:
            summary[zone_name] = ZoneReport(zone=zone_name, incident_count=0, by_type={})
        zone_report = summary[zone_name]
        zone_report.incident_count += 1
        zone_report.by_type[incident.incident_type] = (
            zone_report.by_type.get(incident.incident_type, 0) + 1
        )

    return list(summary.values())
