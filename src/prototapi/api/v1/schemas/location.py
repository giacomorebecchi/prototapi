from enum import StrEnum
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, Field

_LOCATION_DISCRIMINATOR = "type"


class LocationType(StrEnum):
    AZURE = "azure"
    S3 = "s3"


class BaseLocation(BaseModel):
    type: LocationType
    description: Optional[str] = None
    metadata: dict[str, Any] = {}


class AzureLocation(BaseLocation):
    type: Literal[LocationType.AZURE] = LocationType.AZURE
    container: str


class S3Location(BaseLocation):
    type: Literal[LocationType.S3] = LocationType.S3
    bucket: str


Location = Annotated[
    Union[
        AzureLocation,
        S3Location,
    ],
    Field(discriminator=_LOCATION_DISCRIMINATOR),
]
