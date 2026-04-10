"""Pydantic models for the conferences API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Conference(MLBModel):
    """A single MLB conference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    abbreviation: Optional[str] = None
    name_short: Optional[str] = None
    active: Optional[bool] = None
    has_wildcard: Optional[bool] = None


class Conferences(MLBModel):
    """Container returned by ``GET /api/v1/conferences``."""
    conferences: Optional[List[Conference]] = None
