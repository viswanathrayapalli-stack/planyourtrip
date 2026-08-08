from pydantic import BaseModel


class ItineraryGenerateRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: str
    travelers: int


class ItineraryGenerateResponse(BaseModel):
    itinerary: str