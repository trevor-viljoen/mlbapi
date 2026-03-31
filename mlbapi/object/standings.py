"""Pydantic models for the standings object layer."""

from __future__ import annotations

from typing import Any, List, Optional

from mlbapi.object import MLBModel
from mlbapi.object.game import Team


class League(MLBModel):
    pass


class Division(MLBModel):
    pass


class Sport(MLBModel):
    pass


class Streak(MLBModel):
    pass


class LeagueRecord(MLBModel):
    league: Optional[League] = None


class SplitRecord(MLBModel):
    pass


class DivisionRecord(MLBModel):
    division: Optional[Division] = None


class OverallRecord(MLBModel):
    pass


class LeagueRecordEntry(MLBModel):
    league: Optional[League] = None


class ExpectedRecord(MLBModel):
    pass


class Records(MLBModel):
    split_records: Optional[List[SplitRecord]] = None
    division_records: Optional[List[DivisionRecord]] = None
    overall_records: Optional[List[OverallRecord]] = None
    league_records: Optional[List[LeagueRecordEntry]] = None
    expected_records: Optional[List[ExpectedRecord]] = None


class StandingsType(MLBModel):
    pass


class TeamRecord(MLBModel):
    team: Optional[Team] = None
    streak: Optional[Streak] = None
    league_record: Optional[LeagueRecord] = None
    records: Optional[Records] = None


class StandingsRecord(MLBModel):
    league: Optional[League] = None
    division: Optional[Division] = None
    sport: Optional[Sport] = None
    team_records: Optional[List[TeamRecord]] = None


class Standings(MLBModel):
    records: Optional[List[StandingsRecord]] = None


# Backwards-compatibility alias — tests and external code import 'Record'
Record = StandingsRecord
