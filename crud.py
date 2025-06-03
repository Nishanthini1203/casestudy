from sqlalchemy.orm import Session
from models import Event
from schemas import EventCreate, EventUpdate
from fastapi import HTTPException
from datetime import date

def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

def get_all_events(db: Session):
    return db.query(Event).all()

def update_event(db: Session, event_id: int, updates: EventUpdate):
    event = get_event(db, event_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int):
    event = get_event(db, event_id)
    db.delete(event)
    db.commit()
    return {"message": "Deleted successfully"}

def get_events_by_type(db: Session, event_type: str):
    return db.query(Event).filter(Event.event_type == event_type).all()

def get_upcoming_events(db: Session):
    return db.query(Event).filter(Event.event_date > date.today()).all()

def search_by_title(db: Session, keyword: str):
    return db.query(Event).filter(Event.title.ilike(f"%{keyword}%")).all()
