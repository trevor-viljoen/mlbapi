"""Tests for mlbapi.data.sport functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import sport as sport_data


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


SPORTS_DATA = {
    'sports': [
        {'id': 1, 'code': 'mlb', 'link': '/api/v1/sports/1',
         'name': 'Major League Baseball', 'abbreviation': 'MLB', 'sortOrder': 11,
         'activeStatus': True}
    ]
}


class TestGetSports:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(SPORTS_DATA)):
            result = sport_data.get_sports()
        assert result is not None

    def test_with_valid_sport_id_int(self):
        with patch('requests.get', return_value=_mock_get(SPORTS_DATA)):
            result = sport_data.get_sports(sport_id=1)
        assert result is not None

    def test_with_valid_sport_id_string(self):
        with patch('requests.get', return_value=_mock_get(SPORTS_DATA)):
            result = sport_data.get_sports(sport_id='1')
        assert result is not None

    def test_invalid_sport_id_type_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='sport_id'):
            sport_data.get_sports(sport_id=1.5)

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(SPORTS_DATA)):
            result = sport_data.get_sports(fields=['id', 'name'])
        assert result is not None

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='fields'):
            sport_data.get_sports(fields='id,name')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            sport_data.get_sports(invalid_param='x')

    def test_valid_params_list(self):
        assert set(sport_data.VALID_SPORTS_PARAMS) == {'sport_id', 'fields'}
