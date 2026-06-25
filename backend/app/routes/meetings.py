from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Meeting
from app.schemas import MeetingCreate, MeetingResponse
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[MeetingResponse])
def list_meetings(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Meeting).all()

@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(404, "Reunión no encontrada")
    return meeting

@router.post("/", response_model=MeetingResponse, status_code=201)
def create_meeting(data: MeetingCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    meeting = Meeting(**data.model_dump())
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(meeting_id: int, data: MeetingCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(404, "Reunión no encontrada")
    for key, val in data.model_dump().items():
        setattr(meeting, key, val)
    db.commit()
    db.refresh(meeting)
    return meeting

@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(404, "Reunión no encontrada")
    db.delete(meeting)
    db.commit()
