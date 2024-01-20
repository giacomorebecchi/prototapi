from contextlib import nullcontext as does_not_raise
from enum import StrEnum
from typing import Annotated, Literal, Union

import pytest
from pydantic import BaseModel, Field

from prototapi.api.utils import dynamic_discrimination


class Type(StrEnum):
    A = "a"
    B = "b"
    C = "c"


class MyModelA(BaseModel):
    type: Literal[Type.A] = Type.A
    a: str


class MyModelB(BaseModel):
    type: Literal[Type.B] = Type.B


class MyModelCorD(BaseModel):
    type: Literal[Type.C, "d"]


class MyNotValidModel(BaseModel):
    type: str


@pytest.mark.parametrize(
    argnames=["annotation", "expected"],
    argvalues=[
        [
            Annotated[
                Union[MyModelA, MyModelB, MyModelCorD],
                Field(discriminator="type"),
            ],
            does_not_raise(
                {
                    Type.A: MyModelA,
                    Type.B: MyModelB,
                    Type.C: MyModelCorD,
                    "d": MyModelCorD,
                }
            ),
        ],
    ],
)
def test_from_discriminator_to_dict(annotation, expected):
    with expected as result:
        assert (
            dynamic_discrimination.from_discriminator_to_dict(annotation=annotation)
            == result
        )
