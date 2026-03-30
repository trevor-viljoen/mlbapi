"""Tests for mlbapi.data.homerunderby functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import homerunderby as hrd_data


HRD_DATA = {
    'gameId': 12345,
    'state': 'final',
    'bracket': {},
    'pool': {},
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetHomeRunDerby:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)):
            result = hrd_data.get_homerunderby(12345)
        assert result is not None

    def test_url_contains_game_pk(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)) as mock_get:
            hrd_data.get_homerunderby(12345)
        url = mock_get.call_args[0][0]
        assert '/homeRunDerby/12345' in url

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)) as mock_get:
            hrd_data.get_homerunderby(12345, fields=['gameId', 'state'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'gameId,state'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            hrd_data.get_homerunderby(12345, fields='gameId,state')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            hrd_data.get_homerunderby(12345, invalid_param='x')


class TestGetHomeRunDerbyBracket:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)):
            result = hrd_data.get_homerunderby_bracket(12345)
        assert result is not None

    def test_url_contains_bracket(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)) as mock_get:
            hrd_data.get_homerunderby_bracket(12345)
        url = mock_get.call_args[0][0]
        assert '/homeRunDerby/12345/bracket' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            hrd_data.get_homerunderby_bracket(12345, invalid_param='x')


class TestGetHomeRunDerbyPool:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)):
            result = hrd_data.get_homerunderby_pool(12345)
        assert result is not None

    def test_url_contains_pool(self):
        with patch('requests.get', return_value=_mock_get(HRD_DATA)) as mock_get:
            hrd_data.get_homerunderby_pool(12345)
        url = mock_get.call_args[0][0]
        assert '/homeRunDerby/12345/pool' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            hrd_data.get_homerunderby_pool(12345, invalid_param='x')

    def test_valid_params_list(self):
        assert hrd_data.VALID_HOMERUNDERBY_PARAMS == ['fields']
