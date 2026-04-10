"""Pydantic models for the home run derby API endpoint."""

from __future__ import annotations

from typing import Optional

from mlbapi.models import MLBModel


class HomeRunDerby(MLBModel):
    """Home Run Derby data.  Unknown fields are stored via ``extra='allow'``."""
    id: Optional[int] = None
    state: Optional[str] = None
