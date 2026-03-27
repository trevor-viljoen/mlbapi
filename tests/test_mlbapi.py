"""Integration tests for the top-level mlbapi public API."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi
import mlbapi.exceptions
from mlbapi.object.game import BoxScore, LineScore
from mlbapi.object.gameday import Schedule
from mlbapi.object.standings import Standings
from mlbapi.object.team import Teams
from mlbapi.object.division import Divisions
from tests.conftest import (
    BOXSCORE_DATA, LINESCORE_DATA, SCHEDULE_DATA,
    STANDINGS_DATA, TEAMS_DATA, DIVISIONS_DATA,
)


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestBoxscorePublicAPI:
    def test_returns_boxscore_object(self):
        with patch('requests.get', return_value=_mock_get(BOXSCORE_DATA)):
            result = mlbapi.boxscore(716463)
        assert isinstance(result, BoxScore)

    def test_has_teams(self):
        with patch('requests.get', return_value=_mock_get(BOXSCORE_DATA)):
            result = mlbapi.boxscore(716463)
        assert hasattr(result, 'teams')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.boxscore(716463, invalid_param='x')


class TestLinescorePublicAPI:
    def test_returns_linescore_object(self):
        with patch('requests.get', return_value=_mock_get(LINESCORE_DATA)):
            result = mlbapi.linescore(716463)
        assert isinstance(result, LineScore)

    def test_has_innings(self):
        with patch('requests.get', return_value=_mock_get(LINESCORE_DATA)):
            result = mlbapi.linescore(716463)
        assert isinstance(result.innings, list)
        assert len(result.innings) == 2

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.linescore(716463, invalid_param='x')


class TestPlayByPlayPublicAPI:
    def test_returns_data(self):
        data = {'allPlays': [], 'currentPlay': {}}
        with patch('requests.get', return_value=_mock_get(data)):
            result = mlbapi.play_by_play(716463)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.play_by_play(716463, invalid_param='x')


class TestLiveDiffPublicAPI:
    def test_returns_data(self):
        data = {'diff': []}
        with patch('requests.get', return_value=_mock_get(data)):
            result = mlbapi.live_diff(716463)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.live_diff(716463, invalid_param='x')


class TestSchedulePublicAPI:
    def test_returns_schedule_object(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = mlbapi.schedule(date='06/01/2023')
        assert isinstance(result, Schedule)

    def test_has_dates(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = mlbapi.schedule(date='06/01/2023')
        assert isinstance(result.dates, list)
        assert len(result.dates) == 1

    def test_date_has_games(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = mlbapi.schedule(date='06/01/2023')
        assert len(result.dates[0].games) == 1

    def test_game_pk(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = mlbapi.schedule(date='06/01/2023')
        assert result.dates[0].games[0].game_pk == 716463

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.schedule(invalid_param='x')

    def test_start_date_without_end_date_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.schedule(start_date='06/01/2023')


class TestTeamsPublicAPI:
    def test_returns_teams_object(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = mlbapi.teams()
        assert isinstance(result, Teams)

    def test_teams_list_has_items(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = mlbapi.teams()
        assert len(result.teams) == 1
        assert result.teams[0].name == 'New York Yankees'

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.teams(invalid_param='x')


class TestDivisionsPublicAPI:
    def test_returns_divisions_object(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = mlbapi.divisions()
        assert isinstance(result, Divisions)

    def test_divisions_list_has_items(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = mlbapi.divisions()
        assert len(result.divisions) == 1
        assert result.divisions[0].name == 'American League East'

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.divisions(invalid_param='x')


class TestStandingsPublicAPI:
    def test_returns_standings_object(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = mlbapi.standings()
        assert isinstance(result, Standings)

    def test_records_list_has_items(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = mlbapi.standings()
        assert len(result.records) == 1

    def test_team_records(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = mlbapi.standings()
        assert len(result.records[0].team_records) == 1
        assert result.records[0].team_records[0].wins == 30

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.standings(invalid_param='x')


class TestPackageMetadata:
    def test_version_is_set(self):
        assert mlbapi.__version__ is not None

    def test_title_is_set(self):
        assert mlbapi.__title__ == 'mlbapi'

    def test_author_is_set(self):
        assert mlbapi.__author__ == 'Trevor Viljoen'
