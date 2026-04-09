#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi models package.

Provides MLBModel, a lightweight base class for structured MLB API response
objects.  Each subclass declares a ``FIELDS`` class-level dict that maps
API response keys (camelCase strings) to ``(attr_name, converter)`` tuples.
Any key not listed in ``FIELDS`` is silently ignored, keeping objects clean.
"""

import inflection


class MLBModel:
    """Base class for all mlbapi model objects.

    Subclasses declare a ``FIELDS`` class attribute::

        FIELDS = {
            'id':       ('id',   int),
            'fullName': ('full_name', str),
        }

    The constructor accepts a raw API response dict and sets only the
    attributes declared in ``FIELDS``, applying the converter function.
    """

    FIELDS: dict = {}

    def __init__(self, data: dict):
        if not isinstance(data, dict):
            return
        fields = self.__class__.FIELDS
        if fields:
            for api_key, (attr, converter) in fields.items():
                raw = data.get(api_key)
                if raw is not None:
                    try:
                        setattr(self, attr, converter(raw))
                    except (TypeError, ValueError):
                        setattr(self, attr, raw)
        else:
            # Fallback: set all keys as snake_case attributes without conversion
            for key, value in data.items():
                setattr(self, inflection.underscore(key), value)

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        pairs = ', '.join(f'{k}={v!r}' for k, v in list(attrs.items())[:4])
        return f'{self.__class__.__name__}({pairs})'
