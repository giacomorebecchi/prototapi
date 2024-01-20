from enum import StrEnum
from typing import Annotated, Literal, Union, _AnnotatedAlias, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo


def from_discriminator_to_dict(annotation: _AnnotatedAlias) -> dict[StrEnum, BaseModel]:
    if not (
        get_origin(annotation) is Annotated
        and len(args := get_args(annotation)) == 2
        and get_origin(union := args[0]) is Union
        and isinstance(field_info := args[1], FieldInfo)
        and (discriminator := field_info.discriminator) is not None
        and all(map(lambda x: issubclass(x, BaseModel), (models := get_args(union))))
        and all(map(lambda x: discriminator in x.model_fields.keys(), models))
    ):
        raise TypeError(
            "`annotation` is not a valid type. The required annotation is of type:"
            " Annotated[Union[BaseModel], Field(discriminator=...)]"
        )

    annotations = {
        model.model_fields[discriminator].annotation: model for model in models
    }
    if not all(
        map(
            lambda x: get_origin(x) is Literal
            and all(map(lambda val: isinstance(val, str), get_args(x))),
            annotations.keys(),
        ),
    ):
        raise TypeError(
            "All models in the union must be of type Literal with str values"
        )

    return {
        arg: model
        for annotation, model in annotations.items()
        for arg in get_args(annotation)
    }
