from typing import Any

from pydantic import BaseModel


def dump_obj(obj: Any, skip_defaults: bool) -> Any:
    if isinstance(obj, BaseModel):
        return obj.dict(skip_defaults=skip_defaults)
    elif isinstance(obj, (list, set, tuple)):
        return [dump_obj(o, skip_defaults) for o in obj]
    elif isinstance(obj, dict):
        return {k: dump_obj(v, skip_defaults) for k, v in obj.items()}
    return obj
