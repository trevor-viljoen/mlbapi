"""Tests for mlbapi.data.game functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import game as game_data
from tests.conftest import BOXSCORE_DATA, LINESCORE_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetBoxscore:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(BOXSCORE_DATA)):
            result = game_data.get_boxscore(716463)
        assert 'teams' in result

    def test_with_timecode(self):
        with patch('requests.get', return_value=_mock_get(BOXSCORE_DATA)) as mock_get:
            game_data.get_boxscore(716463, timecode='20230601_193000')
        call_kwargs = mock_get.call_args[1]
        assert 'timecode' in str(call_kwargs.get('params', ''))

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_boxscore(716463, invalid_param='x')

    def test_valid_params_list(self):
        assert set(game_data.VALID_BOXSCORE_PARAMS) == {'game_pk', 'timecode', 'fields'}


class TestGetLinescore:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(LINESCORE_DATA)):
            result = game_data.get_linescore(716463)
        assert 'innings' in result

    def test_with_timecode(self):
        with patch('requests.get', return_value=_mock_get(LINESCORE_DATA)):
            result = game_data.get_linescore(716463, timecode='20230601_193000')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_linescore(716463, bad_param='x')


class TestGetPlayByPlay:
    def test_returns_json(self):
        data = {'allPlays': [], 'currentPlay': {}, 'scoringPlays': []}
        with patch('requests.get', return_value=_mock_get(data)):
            result = game_data.get_play_by_play(716463)
        assert 'allPlays' in result

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_play_by_play(716463, invalid='x')


class TestGetLive:
    def test_returns_json(self):
        data = {'gamePk': 716463, 'gameData': {}, 'liveData': {}}
        with patch('requests.get', return_value=_mock_get(data)):
            result = game_data.get_live(716463)
        assert result['gamePk'] == 716463

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_live(716463, invalid='x')

    def test_uses_v1_1(self):
        data = {'gamePk': 716463, 'gameData': {}, 'liveData': {}}
        with patch('requests.get', return_value=_mock_get(data)) as mock_get:
            game_data.get_live(716463)
        url = mock_get.call_args[0][0]
        assert 'v1.1' in url


class TestGetLiveDiff:
    def test_returns_json(self):
        data = {'diff': []}
        with patch('requests.get', return_value=_mock_get(data)):
            result = game_data.get_live_diff(716463)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_live_diff(716463, invalid='x')

    def test_valid_params_list(self):
        assert set(game_data.VALID_LIVE_DIFF_PARAMS) == {'game_pk', 'start_timecode', 'end_timecode'}

    def test_uses_v1_1(self):
        data = {'diff': []}
        with patch('requests.get', return_value=_mock_get(data)) as mock_get:
            game_data.get_live_diff(716463)
        url = mock_get.call_args[0][0]
        assert 'v1.1' in url


class TestGetColor:
    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_color(716463, invalid='x')


class TestGetColorDiff:
    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_color_diff(716463, invalid='x')


class TestGetContent:
    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_content(716463, invalid='x')

    def test_valid_params_list(self):
        assert set(game_data.VALID_CONTENT_PARAMS) == {'game_pk', 'highlight_limit'}


class TestGetContextMetrics:
    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_context_metrics(716463, invalid='x')


class TestGetWinProbability:
    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            game_data.get_win_probability(716463, invalid='x')


class TestGetLiveTimestamps:
    def test_returns_json(self):
        data = ['20230601_190000', '20230601_191000']
        with patch('requests.get', return_value=_mock_get(data)):
            result = game_data.get_live_timestamps(716463)
        assert result is not None

    def test_uses_v1_1(self):
        data = ['20230601_190000']
        with patch('requests.get', return_value=_mock_get(data)) as mock_get:
            game_data.get_live_timestamps(716463)
        url = mock_get.call_args[0][0]
        assert 'v1.1' in url


class TestGetColorTimestamps:
    def test_returns_json(self):
        data = ['20230601_190000']
        with patch('requests.get', return_value=_mock_get(data)):
            result = game_data.get_color_timestamps(716463)
        assert result is not None
