from fastapi import APIRouter
import logging

from pydantic import BaseModel

router = APIRouter()


class HealthCheckAPIResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthCheckAPIResponse)
def health_check():
    logging.info("Health check endpoint called.")
    return {"status": "healthy"}
