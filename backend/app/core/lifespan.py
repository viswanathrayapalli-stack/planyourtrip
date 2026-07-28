from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.app_name}")

    yield

    print("Shutting down PlanYourTrip")