from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

from pydantic import BaseConfig
from pydantic.fields import Field as Field_

if TYPE_CHECKING:
    from pydantic.fields import ValidateReturn


class Field(Field_):
    def __init__(self, name: str, type_: Type) -> None:
        super().__init__(
            name=name, type_=type_, class_validators=None, model_config=BaseConfig
        )

    def validate(self, value: Any, **kwargs: Any) -> ValidateReturn:  # type: ignore
        values = kwargs.get('values', {})
        loc = kwargs.get('loc', '')
        return super().validate(v=value, values=values, loc=loc)
