from fastapi import APIRouter

from app.modules.destination.api import router as destination_router
from app.modules.identity.api import router as identity_router
from app.modules.place.api import router as place_router
from app.modules.trip.api import router as trip_router
from app.modules.user.api import router as user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(identity_router)
api_router.include_router(destination_router)
api_router.include_router(place_router)
api_router.include_router(trip_router)
api_router.include_router(user_router)