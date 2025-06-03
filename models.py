from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    organizer_contact = Column(String, nullable=True)
    reminder = Column(Boolean, default=False)
