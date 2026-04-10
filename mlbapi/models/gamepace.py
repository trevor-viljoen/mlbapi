"""Pydantic models for the gamePace API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel
from mlbapi.models.common import TeamRef, LeagueRef, SportRef


class PrPortalCalculatedFields(MLBModel):
    """Supplemental pace calculations from the PR portal."""
    total7_inn_games: Optional[int] = None
    total9_inn_games: Optional[int] = None
    total_extra_inn_games: Optional[int] = None
    time_per7_inn_game: Optional[str] = None
    time_per9_inn_game: Optional[str] = None
    time_per_extra_inn_game: Optional[str] = None


class GamePaceEntry(MLBModel):
    """Pace statistics for a single team, league, or sport."""
    season: Optional[str] = None
    hits_per9_inn: Optional[float] = None
    runs_per9_inn: Optional[float] = None
    pitches_per9_inn: Optional[float] = None
    plate_appearances_per9_inn: Optional[float] = None
    hits_per_game: Optional[float] = None
    runs_per_game: Optional[float] = None
    innings_played_per_game: Optional[float] = None
    pitches_per_game: Optional[float] = None
    pitchers_per_game: Optional[float] = None
    plate_appearances_per_game: Optional[float] = None
    total_game_time: Optional[str] = None
    total_innings_played: Optional[float] = None
    total_hits: Optional[int] = None
    total_runs: Optional[int] = None
    total_plate_appearances: Optional[int] = None
    total_pitchers: Optional[int] = None
    total_pitches: Optional[int] = None
    total_games: Optional[int] = None
    total7_inn_games: Optional[int] = None
    total9_inn_games: Optional[int] = None
    total_extra_inn_games: Optional[int] = None
    time_per_game: Optional[str] = None
    time_per_pitch: Optional[str] = None
    time_per_hit: Optional[str] = None
    time_per_run: Optional[str] = None
    time_per_plate_appearance: Optional[str] = None
    time_per9_inn: Optional[str] = None
    time_per77_plate_appearances: Optional[str] = None
    total_extra_inn_time: Optional[str] = None
    time_per7_inn_game_without_extra_inn: Optional[str] = None
    total9_inn_games_completed_early: Optional[int] = None
    total9_inn_games_without_extra_inn: Optional[int] = None
    total9_inn_games_scheduled: Optional[int] = None
    hits_per_run: Optional[float] = None
    pitches_per_pitcher: Optional[float] = None
    team: Optional[TeamRef] = None
    league: Optional[LeagueRef] = None
    sport: Optional[SportRef] = None
    pr_portal_calculated_fields: Optional[PrPortalCalculatedFields] = None


class GamePace(MLBModel):
    """Container returned by ``GET /api/v1/gamePace``."""
    teams: Optional[List[GamePaceEntry]] = None
    leagues: Optional[List[GamePaceEntry]] = None
    sports: Optional[List[GamePaceEntry]] = None
