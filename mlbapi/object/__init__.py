"""Base Pydantic model for all mlbapi objects.

All API response models inherit from MLBModel. It handles:
  - camelCase → snake_case key normalisation (via a pre-validator)
  - Forward-compatibility: unknown API fields are stored as attributes
    (extra='allow'), so new fields in the API don't raise errors
  - Output serialisation: model_dump(by_alias=True) reconstructs camelCase

Backwards-compatibility shims (listofobjs, setobjattr, Object) are retained
so that any third-party code that imported them continues to work, but they
are no longer used internally.
"""

from __future__ import annotations

from typing import Any, Optional, Type

import inflection
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel


class MLBModel(BaseModel):
    """Base model for all mlbapi response objects."""

    model_config = ConfigDict(
        populate_by_name=True,   # accept snake_case kwarg init as well as alias
        alias_generator=to_camel,  # declared fields serialise back to camelCase
        extra="allow",           # unknown fields stored & accessible as attrs
    )

    @model_validator(mode="before")
    @classmethod
    def _normalise_keys(cls, data: Any) -> Any:
        """Convert every camelCase key in the raw API dict to snake_case.

        This runs before Pydantic validates fields, so both declared fields
        and extra fields end up with Pythonic snake_case names.
        """
        if isinstance(data, dict):
            return {inflection.underscore(k): v for k, v in data.items()}
        return data

    def __init__(self, _data: Any = None, **kwargs: Any) -> None:
        """Accept either a positional dict (legacy API) or keyword arguments."""
        if _data is not None and isinstance(_data, dict) and not kwargs:
            super().__init__(**_data)
        else:
            super().__init__(**kwargs)

    def json(self) -> dict:
        """Return a plain dict representation. Use model_dump() for new code."""
        return self.model_dump()


# ---------------------------------------------------------------------------
# Backwards-compatibility shims
# ---------------------------------------------------------------------------

def listofobjs(values: list, obj: Type) -> list:
    """Deprecated helper — use a typed List[] field on an MLBModel instead."""
    if hasattr(obj, "model_validate"):
        return [obj.model_validate(v) for v in values]
    return [obj(v) for v in values]


def setobjattr(obj: Any, key: str, value: Any,
               set_obj: Optional[Type] = None) -> None:
    """Deprecated helper — use MLBModel subclasses instead."""
    key = inflection.underscore(key)
    if set_obj is not None:
        if hasattr(set_obj, "model_validate"):
            setattr(obj, key, set_obj.model_validate(value))
        else:
            setattr(obj, key, set_obj(value))
    elif isinstance(value, (dict, list)):
        setattr(obj, key, value)
    else:
        setattr(obj, key, value)


# Keep the old Object name available for any code that imported it.
Object = MLBModel
