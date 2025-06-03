from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import date

class EventNotFoundException(Exception):
    def __init__(self, event_id: int):
        self.event_id = event_id

class InvalidDateException(Exception):
    def __init__(self, date: str):
        self.date = date

# Exception Handlers (to be included in main.py)
def event_not_found_exception_handler(request: Request, exc: EventNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Event with ID {exc.event_id} not found."}
    )

def invalid_date_exception_handler(request: Request, exc: InvalidDateException):
    return JSONResponse(
        status_code=400,
        content={"detail": f"The event date '{exc.date}' is invalid or in the past."}
    )
