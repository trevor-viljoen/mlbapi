"""Tests for mlbapi.data.gamepace functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import gamepace as gamepace_data


GAME_PACE_DATA = {
    'teams': [],
    'leagues': [],
    'sports': [
        {
            'season': '2024',
            'hitsPerGame': 8.5,
            'runsPerGame': 4.5,
            'totalGames': 2430,
            'timePerGame': '02:40:00',
            'sport': {'id': 1, 'name': 'Major League Baseball', 'link': '/api/v1/sports/1'},
        }
    ],
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetGamePace:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(GAME_PACE_DATA)):
            result = gamepace_data.get_game_pace(season='2024', sport_id=1)
        assert 'sports' in result

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(GAME_PACE_DATA)):
            result = gamepace_data.get_game_pace(season='2024', team_id=147)
        assert result is not None

    def test_with_league_id(self):
        with patch('requests.get', return_value=_mock_get(GAME_PACE_DATA)):
            result = gamepace_data.get_game_pace(season='2024', league_id=103)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            gamepace_data.get_game_pace(invalid_param='x')

    def test_valid_params_list(self):
        assert set(gamepace_data.VALID_GAME_PACE_PARAMS) == {
            'season', 'team_id', 'league_id', 'league_list_id', 'sport_id',
            'game_type', 'start_date', 'end_date', 'venue_id', 'fields',
        }
