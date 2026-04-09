"""Pydantic models for the stats API endpoint."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class StatSplit(MLBModel):
    """A single statistical split row."""
    season: Optional[str] = None
    stat: Optional[Dict[str, Any]] = None
    team: Optional[Dict[str, Any]] = None
    player: Optional[Dict[str, Any]] = None
    league: Optional[Dict[str, Any]] = None
    sport: Optional[Dict[str, Any]] = None
    game_type: Optional[str] = None
    num_teams: Optional[int] = None
    rank: Optional[int] = None
    position: Optional[Dict[str, Any]] = None


class StatsGroup(MLBModel):
    """A group of stats (one entry in the ``stats`` array)."""
    group: Optional[Dict[str, Any]] = None
    exemptions: Optional[List[Any]] = None
    splits: Optional[List[StatSplit]] = None


class Stats(MLBModel):
    """Container returned by ``GET /api/v1/stats``."""
    stats: Optional[List[StatsGroup]] = None


class LeaderEntry(MLBModel):
    """A single entry in a leader category."""
    person: Optional[Dict[str, Any]] = None
    team: Optional[Dict[str, Any]] = None
    league: Optional[Dict[str, Any]] = None
    sport: Optional[Dict[str, Any]] = None
    stat: Optional[Dict[str, Any]] = None
    season: Optional[str] = None
    rank: Optional[int] = None
    value: Optional[Any] = None


class LeaderCategory(MLBModel):
    """Leaders for a single stat category."""
    leader_category: Optional[str] = None
    season: Optional[str] = None
    game_type: Optional[Any] = None
    leaders: Optional[List[LeaderEntry]] = None


class StatsLeaders(MLBModel):
    """Container returned by ``GET /api/v1/stats/leaders``."""
    league_leaders: Optional[List[LeaderCategory]] = None
