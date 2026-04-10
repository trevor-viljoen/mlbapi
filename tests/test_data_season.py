"""Tests for mlbapi.data.season functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import season as season_data


SEASONS_DATA = {
    'seasons': [
        {
            'seasonId': '2023',
            'hasWildcard': True,
            'preSeasonStartDate': '2023-02-24',
            'seasonStartDate': '2023-03-30',
            'regularSeasonStartDate': '2023-03-30',
            'regularSeasonEndDate': '2023-10-01',
            'seasonEndDate': '2023-11-04',
            'offseasonStartDate': '2023-11-06',
            'offSeasonEndDate': '2024-01-01',
            'seasonLevelGamedayType': 'P',
            'gameLevelGamedayType': 'P',
            'qualifierPlateAppearances': 502.0,
            'qualifierOutsPitched': 162.0,
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetSeasons:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_seasons()
        assert 'seasons' in result

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_seasons(season='2023')
        assert result is not None

    def test_with_sport_id(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_seasons(sport_id=1)
        assert result is not None

    def test_with_division_id(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_seasons(division_id=201)
        assert result is not None

    def test_with_league_id(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_seasons(league_id=103)
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)) as mock_get:
            season_data.get_seasons(fields=['seasonId', 'seasonStartDate'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'seasonId,seasonStartDate'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            season_data.get_seasons(fields='seasonId')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            season_data.get_seasons(invalid_param='x')

    def test_valid_params_list(self):
        assert set(season_data.VALID_SEASON_PARAMS) == {
            'season', 'sport_id', 'division_id', 'league_id',
            'with_game_type_dates', 'fields'
        }


class TestGetAllSeasons:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)):
            result = season_data.get_all_seasons()
        assert result is not None

    def test_url_contains_all(self):
        with patch('requests.get', return_value=_mock_get(SEASONS_DATA)) as mock_get:
            season_data.get_all_seasons(sport_id=1)
        url = mock_get.call_args[0][0]
        assert '/seasons/all' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            season_data.get_all_seasons(invalid_param='x')
