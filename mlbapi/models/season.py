"""Pydantic models for the seasons object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Season(MLBModel):
    pass


class Seasons(MLBModel):
    seasons: Optional[List[Season]] = None
