from fastapi import APIRouter

from app.modules.destination.api import router as destination_router
from app.modules.trip.api import router as trip_router


api_router = APIRouter()

api_router.include_router(destination_router)
api_router.include_router(trip_router)