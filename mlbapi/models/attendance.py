"""Pydantic models for the attendance API endpoint."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class AttendanceRecord(MLBModel):
    """Attendance record for a team/season combination."""
    open_date_home: Optional[str] = None
    attendance_total: Optional[int] = None
    attendance_total_away: Optional[int] = None
    attendance_games_home: Optional[int] = None
    attendance_games_away: Optional[int] = None
    game_type: Optional[Dict[str, Any]] = None
    team: Optional[Dict[str, Any]] = None
    year: Optional[str] = None


class Attendance(MLBModel):
    """Container returned by ``GET /api/v1/attendance``."""
    records: Optional[List[AttendanceRecord]] = None
    agg_total: Optional[List[Any]] = None
    total_capacity: Optional[int] = None
