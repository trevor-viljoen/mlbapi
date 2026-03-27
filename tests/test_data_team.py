"""Tests for mlbapi.data.team functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import team as team_data
from tests.conftest import TEAMS_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetTeams:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams()
        assert 'teams' in result

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams(team_id=147)
        assert result is not None

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams(season='2023')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            team_data.get_teams(invalid_param='x')

    def test_league_ids_as_list_of_ints(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams(league_ids=[103, 104])
        assert result is not None

    def test_league_ids_as_list_of_strings(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams(league_ids=['103', '104'])
        assert result is not None

    def test_league_ids_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='must be a list'):
            team_data.get_teams(league_ids=103)

    def test_league_ids_invalid_string_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            team_data.get_teams(league_ids=['not_an_int'])

    def test_league_ids_becomes_comma_delimited(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)) as mock_get:
            team_data.get_teams(league_ids=[103, 104])
        call_kwargs = mock_get.call_args[1]
        params = call_kwargs.get('params', {})
        assert 'leagueIds' in params
        assert params['leagueIds'] == '103,104'

    def test_active_status_param(self):
        with patch('requests.get', return_value=_mock_get(TEAMS_DATA)):
            result = team_data.get_teams(active_status='ACTIVE')
        assert result is not None
