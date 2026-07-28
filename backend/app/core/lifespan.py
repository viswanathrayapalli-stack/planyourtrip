from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.core.settings import settings
from app.core.log_config import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_logging()

    logger.info("Starting %s", settings.app_name)

    yield

    logger.info("Stopping %s", settings.app_name)