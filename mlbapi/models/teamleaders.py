"""Pydantic models for the team leaders API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel
from mlbapi.models.common import PersonRef, TeamRef, LeagueRef, SportRef


class TeamLeaderEntry(MLBModel):
    """A single entry in a team leaders list."""
    rank: Optional[int] = None
    value: Optional[str] = None
    person: Optional[PersonRef] = None
    team: Optional[TeamRef] = None
    league: Optional[LeagueRef] = None
    sport: Optional[SportRef] = None
    season: Optional[str] = None


class TeamLeaderCategory(MLBModel):
    """Leaders for a single statistical category."""
    leader_category: Optional[str] = None
    season: Optional[str] = None
    game_type: Optional[str] = None
    stat_group: Optional[str] = None
    total_splits: Optional[int] = None
    team: Optional[TeamRef] = None
    leaders: Optional[List[TeamLeaderEntry]] = None


class TeamLeaders(MLBModel):
    """Container returned by ``GET /api/v1/teams/{id}/leaders``."""
    team_leaders: Optional[List[TeamLeaderCategory]] = None
