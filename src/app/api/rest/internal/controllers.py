from fastapi import APIRouter

from app.api.rest import internal

internal_api = APIRouter()

internal_api.include_router(internal.v1.votes.api.router, prefix="/v1/votes", tags=["votes"])
