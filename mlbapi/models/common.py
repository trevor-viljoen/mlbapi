"""Shared primitive Pydantic reference types used across multiple object modules.

These are lightweight "ref" models that represent the minimal shape of a
nested object as returned by the MLB StatsAPI (usually just id/name/link).
Because MLBModel has extra="allow", any additional fields returned by the API
are stored automatically.
"""

from __future__ import annotations

from typing import Optional

from mlbapi.models import MLBModel


class PersonRef(MLBModel):
    """Minimal person reference (id, fullName, link)."""
    id: Optional[int] = None
    full_name: Optional[str] = None
    link: Optional[str] = None


class TeamRef(MLBModel):
    """Minimal team reference (id, name, link)."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


class LeagueRef(MLBModel):
    """Minimal league reference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    abbreviation: Optional[str] = None


class DivisionRef(MLBModel):
    """Minimal division reference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


class SportRef(MLBModel):
    """Minimal sport reference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    abbreviation: Optional[str] = None


class VenueRef(MLBModel):
    """Minimal venue reference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


class ConferenceRef(MLBModel):
    """Minimal conference reference."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


class LeagueRecordRef(MLBModel):
    """Win/loss/pct league record."""
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    pct: Optional[str] = None
