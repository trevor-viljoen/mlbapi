"""Tests for mlbapi.object.team and mlbapi.object.division classes."""
import pytest

from mlbapi.object.team import Teams
from mlbapi.object.division import Divisions
from tests.conftest import TEAMS_DATA, DIVISIONS_DATA


class TestTeams:
    def test_creates_from_data(self):
        t = Teams(TEAMS_DATA)
        assert hasattr(t, 'teams')

    def test_teams_is_list(self):
        t = Teams(TEAMS_DATA)
        assert isinstance(t.teams, list)
        assert len(t.teams) == 1

    def test_team_has_name(self):
        t = Teams(TEAMS_DATA)
        assert t.teams[0].name == 'New York Yankees'

    def test_team_has_id(self):
        t = Teams(TEAMS_DATA)
        assert t.teams[0].id == 147

    def test_team_has_abbreviation(self):
        t = Teams(TEAMS_DATA)
        assert t.teams[0].abbreviation == 'NYY'

    def test_team_has_league(self):
        t = Teams(TEAMS_DATA)
        assert hasattr(t.teams[0], 'league')

    def test_team_has_division(self):
        t = Teams(TEAMS_DATA)
        assert hasattr(t.teams[0], 'division')

    def test_team_has_venue(self):
        t = Teams(TEAMS_DATA)
        assert hasattr(t.teams[0], 'venue')

    def test_team_active_status(self):
        t = Teams(TEAMS_DATA)
        assert t.teams[0].active is True


class TestDivisions:
    def test_creates_from_data(self):
        d = Divisions(DIVISIONS_DATA)
        assert hasattr(d, 'divisions')

    def test_divisions_is_list(self):
        d = Divisions(DIVISIONS_DATA)
        assert isinstance(d.divisions, list)
        assert len(d.divisions) == 1

    def test_division_has_name(self):
        d = Divisions(DIVISIONS_DATA)
        assert d.divisions[0].name == 'American League East'

    def test_division_has_id(self):
        d = Divisions(DIVISIONS_DATA)
        assert d.divisions[0].id == 201

    def test_division_has_abbreviation(self):
        d = Divisions(DIVISIONS_DATA)
        assert d.divisions[0].abbreviation == 'ALE'

    def test_division_has_league(self):
        d = Divisions(DIVISIONS_DATA)
        assert hasattr(d.divisions[0], 'league')

    def test_division_has_sport(self):
        d = Divisions(DIVISIONS_DATA)
        assert hasattr(d.divisions[0], 'sport')

    def test_division_wildcard(self):
        d = Divisions(DIVISIONS_DATA)
        assert d.divisions[0].has_wildcard is True
