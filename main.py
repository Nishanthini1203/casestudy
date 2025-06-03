from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal
from exceptions import EventNotFoundException
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new event
@app.post("/events/", response_model=schemas.EventOut, status_code=201)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)


# Get all events
@app.get("/events/", response_model=list[schemas.EventOut])
def get_all_events(db: Session = Depends(get_db)):
    return crud.get_all_events(db)


# List upcoming events (event_date > today)
@app.get("/events/upcoming", response_model=list[schemas.EventOut])
def list_upcoming_events(db: Session = Depends(get_db)):
    return crud.get_upcoming_events(db)


# Filter by event type
@app.get("/events/type/{event_type}", response_model=list[schemas.EventOut])
def get_events_by_type(event_type: str, db: Session = Depends(get_db)):
    return crud.get_events_by_type(db, event_type)


# Get event by ID (must be last among /events/ paths)
@app.get("/events/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFoundException(event_id)
    return event


# Update an event
@app.put("/events/{event_id}", response_model=schemas.EventOut)
@app.put("/events/{event_id}", response_model=schemas.EventOut)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    return crud.update_event(db, event_id, event)


# Delete an event
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    result = crud.delete_event(db, event_id)
    if not result:
        raise EventNotFoundException(event_id)
    return {"message": f"Event {event_id} deleted successfully"}


# Custom Exception Handler
@app.exception_handler(EventNotFoundException)
def event_not_found_exception_handler(request, exc: EventNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Event with ID {exc.event_id} not found."}
    )
