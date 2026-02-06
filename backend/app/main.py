from fastapi import FastAPI

from app.routes import health
from app.core.logging import setup_logging
from app.database.schema import create_db_and_tables

from contextlib import asynccontextmanager

from app.routes import users


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
