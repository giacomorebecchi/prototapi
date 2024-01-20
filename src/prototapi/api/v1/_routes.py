from fastapi import APIRouter

from prototapi.api.v1.endpoints.location import location_router

v1_router = APIRouter()

v1_router.include_router(location_router)
