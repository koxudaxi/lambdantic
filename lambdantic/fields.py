from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Type

from pydantic import BaseConfig, BaseModel
from pydantic.fields import Field as Field_, Shape

if TYPE_CHECKING:
    from pydantic.fields import ValidateReturn


class FieldType(Enum):
    event = 'event'
    context = 'context'
    path_parameter = 'path_parameter'
    query_parameter = 'query_parameter'
    multi_value_query_parameter = 'multi_value_query_parameter'
    header = 'header'
    multi_value_header = 'multi_value_header'
    response = 'response'

    def get_field(self, type_: Type, name: Optional[str] = None) -> Field:
        return Field(name or self.value, type_, self)


class Field(Field_):
    def __init__(self, name: str, type_: Type, field_type: FieldType) -> None:
        super().__init__(
            name=name or field_type.value,
            type_=type_,
            class_validators=None,
            model_config=BaseConfig,
        )
        self.field_type: FieldType = field_type

    def validate(self, value: Any, **kwargs: Any) -> ValidateReturn:  # type: ignore
        values = kwargs.get('values', {})
        loc = kwargs.get('loc', '')
        return super().validate(v=value, values=values, loc=loc)
