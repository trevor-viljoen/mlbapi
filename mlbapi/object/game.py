"""Pydantic models for mlbapi game objects.

All classes inherit from MLBModel which provides:
- camelCase → snake_case normalisation via _normalise_keys
- extra="allow" so unknown API fields are stored automatically
- ClassName(data_dict) positional-arg constructor for backwards compat
"""

from __future__ import annotations

from typing import Any, List, Optional, Union

import inflection
from pydantic import computed_field, field_validator, model_validator

from mlbapi.object import MLBModel
from mlbapi.object.common import (
    DivisionRef, LeagueRecordRef, LeagueRef, PersonRef, SportRef, TeamRef,
    VenueRef,
)


# ---------------------------------------------------------------------------
# Low-level shared types
# ---------------------------------------------------------------------------

class Position(MLBModel):
    """Fielding position descriptor."""


class Status(MLBModel):
    """Player or game status."""


class Venue(MLBModel):
    """Venue reference with extra detail."""


class League(MLBModel):
    """League reference with extra detail."""


class Division(MLBModel):
    """Division with league/sport nesting."""


class Sport(MLBModel):
    """Sport reference."""


class SpringVenue(MLBModel):
    pass


class SpringLeague(MLBModel):
    pass


class Conference(MLBModel):
    pass


class Content(MLBModel):
    pass


class GameStatus(MLBModel):
    pass


class AllPositions(MLBModel):
    pass


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

class Batting(MLBModel):
    pass


class Pitching(MLBModel):
    pass


class Fielding(MLBModel):
    pass


class Stats(MLBModel):
    batting: Optional[Batting] = None
    pitching: Optional[Pitching] = None
    fielding: Optional[Fielding] = None

    @field_validator('batting', mode='before')
    @classmethod
    def _empty_batting(cls, v: Any) -> Any:
        return None if (v is not None and not v) else v


class SeasonStats(Stats):
    pass


class TeamStats(Stats):
    pass


# ---------------------------------------------------------------------------
# Person / Player
# ---------------------------------------------------------------------------

class Person(MLBModel):
    pass


class Player(MLBModel):
    person: Optional[Person] = None
    position: Optional[Position] = None
    all_positions: Optional[List[AllPositions]] = None
    stats: Optional[Stats] = None
    season_stats: Optional[SeasonStats] = None
    status: Optional[Status] = None
    game_status: Optional[GameStatus] = None


# ---------------------------------------------------------------------------
# Defense / Offense
# ---------------------------------------------------------------------------

class Defense(MLBModel):
    pitcher: Optional[PersonRef] = None
    catcher: Optional[PersonRef] = None
    first: Optional[PersonRef] = None
    second: Optional[PersonRef] = None
    third: Optional[PersonRef] = None
    shortstop: Optional[PersonRef] = None
    left: Optional[PersonRef] = None
    center: Optional[PersonRef] = None
    right: Optional[PersonRef] = None
    batter: Optional[PersonRef] = None
    on_deck: Optional[PersonRef] = None
    in_hole: Optional[PersonRef] = None
    team: Optional[TeamRef] = None


class Offense(MLBModel):
    batter: Optional[PersonRef] = None
    on_deck: Optional[PersonRef] = None
    in_hole: Optional[PersonRef] = None
    pitcher: Optional[PersonRef] = None
    first: Optional[PersonRef] = None
    second: Optional[PersonRef] = None
    third: Optional[PersonRef] = None
    team: Optional[TeamRef] = None


# ---------------------------------------------------------------------------
# LineScore
# ---------------------------------------------------------------------------

class Home(MLBModel):
    """Half-inning or team totals for the home side."""


class Away(MLBModel):
    """Half-inning or team totals for the away side."""


class Inning(MLBModel):
    home: Optional[Home] = None
    away: Optional[Away] = None


class LineScoreTeams(MLBModel):
    home: Optional[Home] = None
    away: Optional[Away] = None


class LineScore(MLBModel):
    innings: Optional[List[Inning]] = None
    teams: Optional[LineScoreTeams] = None
    defense: Optional[Defense] = None
    offense: Optional[Offense] = None


# ---------------------------------------------------------------------------
# Record / LeagueRecord
# ---------------------------------------------------------------------------

class LeagueRecord(MLBModel):
    league: Optional[LeagueRef] = None


class Records(MLBModel):
    pass


class Record(MLBModel):
    league_record: Optional[LeagueRecord] = None
    records: Optional[Any] = None

    @field_validator('records', mode='before')
    @classmethod
    def _empty_records(cls, v: Any) -> Any:
        if isinstance(v, dict) and not v:
            return None
        return v


# ---------------------------------------------------------------------------
# Team (full object — not just a reference)
# ---------------------------------------------------------------------------

class Team(MLBModel):
    status: Optional[Status] = None
    venue: Optional[Venue] = None
    spring_venue: Optional[SpringVenue] = None
    league: Optional[League] = None
    division: Optional[Division] = None
    sport: Optional[Sport] = None
    spring_league: Optional[SpringLeague] = None
    conference: Optional[Conference] = None
    record: Optional[Record] = None
    content: Optional[Content] = None


# ---------------------------------------------------------------------------
# BoxScore teams
# ---------------------------------------------------------------------------

class BoxScoreTeam(MLBModel):
    """Away or home team entry inside a boxscore."""

    team: Optional[Team] = None
    team_stats: Optional[TeamStats] = None
    players: Optional[List[Player]] = None
    batters: Optional[List[int]] = None
    pitchers: Optional[List[int]] = None
    bench: Optional[List[int]] = None
    bullpen: Optional[List[int]] = None
    batting_order: Optional[List[int]] = None

    @model_validator(mode='before')
    @classmethod
    def _normalise_keys(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        result: dict = {}
        for k, v in data.items():
            if k == 'players':
                # API returns {"ID592450": {...}, ...} — convert to a list
                result['players'] = list(v.values()) if isinstance(v, dict) else (v or [])
            elif k in ('info', 'note'):
                # placeholder fields — drop for now
                pass
            else:
                result[inflection.underscore(k)] = v
        return result


# Aliases kept for backwards compatibility and test imports
AwayTeam = BoxScoreTeam
HomeTeam = BoxScoreTeam


class Teams(MLBModel):
    """Teams pair — used for both BoxScore and LineScore contexts."""
    away: Optional[BoxScoreTeam] = None
    home: Optional[BoxScoreTeam] = None


# ---------------------------------------------------------------------------
# Official / Info
# ---------------------------------------------------------------------------

class Official(MLBModel):
    official: Optional[PersonRef] = None
    official_type: Optional[str] = None


class Info(MLBModel):
    label: Optional[str] = None
    value: Optional[str] = None

    @computed_field
    @property
    def info(self) -> Union[str, tuple, None]:
        if self.value:
            return (self.label, self.value)
        return self.label


# ---------------------------------------------------------------------------
# BoxScore
# ---------------------------------------------------------------------------

class BoxScore(MLBModel):
    teams: Optional[Teams] = None
    officials: Optional[List[Official]] = None
    info: Optional[List[Info]] = None
    pitching_notes: Optional[List[str]] = None

    @field_validator('pitching_notes', mode='before')
    @classmethod
    def _empty_pitching_notes(cls, v: Any) -> Any:
        if isinstance(v, list) and not v:
            return None
        return v


# ---------------------------------------------------------------------------
# Misc game classes (kept for import compatibility)
# ---------------------------------------------------------------------------

class Umpire(MLBModel):
    pass


class Color(MLBModel):
    pass


class ColorTimestamps(MLBModel):
    pass


class ColorDiff(MLBModel):
    pass


class ContextMetrics(MLBModel):
    pass


class Live(MLBModel):
    pass


class LiveDiff(MLBModel):
    pass


class LiveTimestamps(MLBModel):
    pass


class PlayByPlay(MLBModel):
    pass


class WinProbability(MLBModel):
    pass
