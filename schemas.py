from pydantic import BaseModel, Field, validator
from datetime import date
from utils import is_future_date

class EventBase(BaseModel):
    title: str = Field(..., min_length=1)
    event_type: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    event_date: date
    organizer_contact: str | None = None
    reminder: bool = False

    @validator('event_date')
    def date_must_be_future(cls, value):
        if not is_future_date(value):
            raise ValueError("Event date must be in the future.")
        return value

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: str | None = None
    event_type: str | None = None
    location: str | None = None
    event_date: date | None = None
    is_active: bool | None = None
    organizer_contact: str | None = None
    reminder: bool | None = None

    @validator('event_date')
    def date_must_be_future(cls, value):
        if value and not is_future_date(value):
            raise ValueError("Updated event date must be in the future.")
        return value

class EventOut(EventBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
