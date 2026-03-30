"""Tests for mlbapi.data.division functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import division as division_data
from tests.conftest import DIVISIONS_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetDivisions:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = division_data.get_divisions()
        assert 'divisions' in result

    def test_with_division_id_int(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = division_data.get_divisions(division_id=201)
        assert result is not None

    def test_with_division_id_string(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = division_data.get_divisions(division_id='201')
        assert result is not None

    def test_with_league_id(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = division_data.get_divisions(league_id=103)
        assert result is not None

    def test_with_sport_id(self):
        with patch('requests.get', return_value=_mock_get(DIVISIONS_DATA)):
            result = division_data.get_divisions(sport_id=1)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            division_data.get_divisions(invalid_param='x')

    def test_invalid_type_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            division_data.get_divisions(division_id=[201, 202])

    def test_valid_params_list(self):
        assert set(division_data.VALID_DIVISION_PARAMS) == {'division_id', 'league_id', 'sport_id'}
