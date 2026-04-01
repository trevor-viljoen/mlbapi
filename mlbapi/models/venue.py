"""Pydantic models for the venues object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Venue(MLBModel):
    pass


class Venues(MLBModel):
    venues: Optional[List[Venue]] = None
