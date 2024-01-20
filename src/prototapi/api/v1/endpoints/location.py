from fastapi import APIRouter

from prototapi.api import _constants
from prototapi.api.v1.schemas import location

location_router = APIRouter(prefix=_constants.LOCATIONS, tags=["Locations"])


@location_router.get(path="/{type}")
async def get_location(type: location.LocationType):
    ...
