"""Tests for mlbapi.data.standings functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import standings as standings_data
from tests.conftest import STANDINGS_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetStandings:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings()
        assert 'records' in result

    def test_with_standings_type(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings(standings_type='regularSeason')
        assert result is not None

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings(season='2023')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            standings_data.get_standings(invalid_param='x')

    def test_league_id_as_list_of_ints(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings(league_id=[103, 104])
        assert result is not None

    def test_league_id_as_list_of_strings(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings(league_id=['103', '104'])
        assert result is not None

    def test_league_id_mixed_list(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)):
            result = standings_data.get_standings(league_id=[103, '104'])
        assert result is not None

    def test_league_id_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='must be a list'):
            standings_data.get_standings(league_id=103)

    def test_league_id_invalid_string_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            standings_data.get_standings(league_id=['not_an_int'])

    def test_league_id_becomes_comma_delimited(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_DATA)) as mock_get:
            standings_data.get_standings(league_id=[103, 104])
        call_kwargs = mock_get.call_args[1]
        params = call_kwargs.get('params', {})
        # leagueId is passed as a comma-delimited string in params
        assert params.get('leagueId') == '103,104'
