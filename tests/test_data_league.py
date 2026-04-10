"""Tests for mlbapi.data.league functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import league as league_data


LEAGUES_DATA = {
    'leagues': [
        {
            'id': 103,
            'name': 'American League',
            'link': '/api/v1/league/103',
            'abbreviation': 'AL',
            'nameShort': 'American',
            'seasonState': 'offseason',
            'hasWildCard': True,
            'hasSplitSeason': False,
            'numGames': 162,
            'numTeams': 16,
            'season': '2024',
            'active': True,
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetLeague:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(LEAGUES_DATA)):
            result = league_data.get_league(103)
        assert 'leagues' in result

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(LEAGUES_DATA)):
            result = league_data.get_league(103, season='2024')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            league_data.get_league(103, invalid_param='x')

    def test_valid_params_list(self):
        assert set(league_data.VALID_LEAGUE_PARAMS) == {
            'league_id', 'league_ids', 'season', 'seasons', 'expand', 'fields'
        }


class TestGetLeagueAllStars:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get({})):
            result = league_data.get_league_all_stars(103)
        assert result is not None

    def test_write_ins_uses_different_context(self):
        with patch('requests.get', return_value=_mock_get({})) as mock_get:
            league_data.get_league_all_stars(103, write_ins=True)
        url = mock_get.call_args[0][0]
        assert 'allStarWriteIns' in url

    def test_default_uses_final_vote_context(self):
        with patch('requests.get', return_value=_mock_get({})) as mock_get:
            league_data.get_league_all_stars(103)
        url = mock_get.call_args[0][0]
        assert 'allStarFinalVote' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            league_data.get_league_all_stars(103, invalid_param='x')

    def test_valid_params_list(self):
        assert set(league_data.VALID_LEAGUE_ALLSTAR_PARAMS) == {
            'league_ids', 'season', 'fields'
        }
