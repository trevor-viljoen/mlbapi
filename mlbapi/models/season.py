"""Pydantic models for the seasons API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Season(MLBModel):
    """A single MLB season."""
    season_id: Optional[str] = None
    has_wildcard: Optional[bool] = None
    pre_season_start_date: Optional[str] = None
    pre_season_end_date: Optional[str] = None
    season_start_date: Optional[str] = None
    season_end_date: Optional[str] = None
    regular_season_start_date: Optional[str] = None
    regular_season_end_date: Optional[str] = None
    last_date1st_half: Optional[str] = None
    all_star_date: Optional[str] = None
    first_date2nd_half: Optional[str] = None
    post_season_start_date: Optional[str] = None
    post_season_end_date: Optional[str] = None
    off_season_start_date: Optional[str] = None
    off_season_end_date: Optional[str] = None


class Seasons(MLBModel):
    """Container returned by ``GET /api/v1/seasons``."""
    seasons: Optional[List[Season]] = None
