"""Pydantic models for the schedule/gameday object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.object import MLBModel
from mlbapi.object.common import LeagueRecordRef


class Status(MLBModel):
    pass


class LeagueRecord(MLBModel):
    pass


class Venue(MLBModel):
    pass


class Content(MLBModel):
    pass


class Team(MLBModel):
    pass


class ScheduleTeam(MLBModel):
    league_record: Optional[LeagueRecord] = None
    team: Optional[Team] = None


class AwayTeam(ScheduleTeam):
    pass


class HomeTeam(ScheduleTeam):
    pass


class Teams(MLBModel):
    away: Optional[AwayTeam] = None
    home: Optional[HomeTeam] = None


class Event(MLBModel):
    pass


class Game(MLBModel):
    status: Optional[Status] = None
    teams: Optional[Teams] = None
    venue: Optional[Venue] = None
    content: Optional[Content] = None


class Date(MLBModel):
    games: Optional[List[Game]] = None
    events: Optional[List[Event]] = None


class Schedule(MLBModel):
    dates: Optional[List[Date]] = None
