"""Tests for mlbapi.models.schedule classes."""
import pytest

from mlbapi.models.schedule import Schedule, Date, Game, Teams, HomeTeam, AwayTeam, Status, Venue, Content
from tests.conftest import SCHEDULE_DATA


class TestSchedule:
    def test_creates_from_data(self):
        s = Schedule(SCHEDULE_DATA)
        assert hasattr(s, 'dates')

    def test_dates_is_list(self):
        s = Schedule(SCHEDULE_DATA)
        assert isinstance(s.dates, list)
        assert len(s.dates) == 1

    def test_total_games(self):
        s = Schedule(SCHEDULE_DATA)
        assert s.total_games == 1

    def test_total_items(self):
        s = Schedule(SCHEDULE_DATA)
        assert s.total_items == 1


class TestDate:
    def test_creates_from_data(self):
        date_data = SCHEDULE_DATA['dates'][0]
        d = Date(date_data)
        assert hasattr(d, 'games')

    def test_games_is_list(self):
        date_data = SCHEDULE_DATA['dates'][0]
        d = Date(date_data)
        assert isinstance(d.games, list)
        assert len(d.games) == 1

    def test_events_is_list(self):
        date_data = SCHEDULE_DATA['dates'][0]
        d = Date(date_data)
        assert isinstance(d.events, list)
        assert len(d.events) == 0

    def test_date_value(self):
        date_data = SCHEDULE_DATA['dates'][0]
        d = Date(date_data)
        assert hasattr(d, 'date')


class TestGame:
    def test_creates_from_data(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert hasattr(g, 'game_pk')

    def test_game_pk(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert g.game_pk == 716463

    def test_has_status(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert hasattr(g, 'status')
        assert isinstance(g.status, Status)

    def test_has_teams(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert hasattr(g, 'teams')
        assert isinstance(g.teams, Teams)

    def test_has_venue(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert hasattr(g, 'venue')
        assert isinstance(g.venue, Venue)

    def test_teams_has_home_and_away(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert hasattr(g.teams, 'home')
        assert hasattr(g.teams, 'away')

    def test_home_team_name(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert g.teams.home.team.name == 'Boston Red Sox'

    def test_away_team_name(self):
        game_data = SCHEDULE_DATA['dates'][0]['games'][0]
        g = Game(game_data)
        assert g.teams.away.team.name == 'New York Yankees'


class TestStatus:
    def test_creates_from_data(self):
        data = {'abstractGameState': 'Final', 'detailedState': 'Final',
                'statusCode': 'F', 'startTimeTBD': False}
        s = Status(data)
        assert s.abstract_game_state == 'Final'
        assert s.status_code == 'F'
