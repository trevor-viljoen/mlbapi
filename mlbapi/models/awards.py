"""Pydantic models for the awards API endpoint."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class Award(MLBModel):
    """A single MLB award."""
    id: Optional[str] = None
    name: Optional[str] = None
    home_league: Optional[Dict[str, Any]] = None
    sport: Optional[Dict[str, Any]] = None
    votes: Optional[List[Any]] = None
    notes: Optional[str] = None


class Awards(MLBModel):
    """Container returned by ``GET /api/v1/awards``."""
    awards: Optional[List[Award]] = None
