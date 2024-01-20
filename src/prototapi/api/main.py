from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from prototapi import __project_name__, __version__
from prototapi.api import _constants
from prototapi.api.v1._routes import v1_router

_API_HEALTHCHECK = "OK"
_API_DESCRIPTION = "PrototAPI"
_API_STATUS = "active"

origins = [
    "http://localhost:5173",
]

app = FastAPI(title=_constants.APPLICATION_NAME)
app.include_router(
    v1_router, prefix=_constants.API + _constants.APP_PREFIX + _constants.V1
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    path=_constants.HEALTHCHECK,
    summary=f"Get the healthcheck of {_constants.APPLICATION_NAME}",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def healthcheck() -> str:
    """
    Get the healthcheck of the application

    Returns
    -------
    str
        A message to ensure that the application is active
    """

    return _API_HEALTHCHECK


@app.get(
    path=_constants.STATUS,
    summary=f"Get the status of {_constants.APPLICATION_NAME}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
async def status() -> dict:
    """
    Get the status of the application

    Returns
    -------
    str
        A message containing the status of the application
    """

    return {
        "name": __project_name__,
        "version": __version__,
        "description": _API_DESCRIPTION,
        "status": _API_STATUS,
    }
