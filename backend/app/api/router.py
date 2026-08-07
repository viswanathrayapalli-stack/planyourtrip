from fastapi import APIRouter

from app.modules.destination.api import router as destination_router
from app.modules.identity.api import router as identity_router
from app.modules.itinerary.api import router as itinerary_router
from app.modules.place.api import router as place_router
from app.modules.trip.api import router as trip_router
from app.modules.booking.api import router as booking_router
from app.modules.checklist.api import router as checklist_router
from app.modules.note.api import router as note_router
from app.modules.expense.api import router as expense_router
from app.modules.user.api import router as user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(identity_router)
api_router.include_router(destination_router)
api_router.include_router(place_router)
api_router.include_router(trip_router)
api_router.include_router(itinerary_router)
api_router.include_router(booking_router)
api_router.include_router(expense_router)
api_router.include_router(checklist_router)
api_router.include_router(note_router)
api_router.include_router(user_router)