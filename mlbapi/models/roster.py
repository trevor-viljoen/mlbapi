"""Pydantic models for team roster and coaches endpoints."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel
from mlbapi.models.common import PersonRef


class Position(MLBModel):
    """Position reference."""
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    abbreviation: Optional[str] = None


class RosterStatus(MLBModel):
    """Roster status for a player."""
    code: Optional[str] = None
    description: Optional[str] = None


class RosterEntry(MLBModel):
    """A single entry on a team roster or coaching staff."""
    person: Optional[PersonRef] = None
    jersey_number: Optional[str] = None
    position: Optional[Position] = None
    status: Optional[RosterStatus] = None
    # Coaches-specific fields
    job: Optional[str] = None
    job_id: Optional[str] = None
    title: Optional[str] = None


class Roster(MLBModel):
    """Container returned by ``GET /api/v1/teams/{id}/roster``
    and ``GET /api/v1/teams/{id}/coaches``."""
    roster: Optional[List[RosterEntry]] = None
    team_id: Optional[int] = None
    roster_type: Optional[str] = None
