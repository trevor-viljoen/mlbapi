"""Tests for mlbapi.data.conference functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import conference as conference_data


CONFERENCES_DATA = {
    'conferences': [
        {'id': 203, 'name': 'American League', 'link': '/api/v1/conferences/203'}
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetConferences:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(CONFERENCES_DATA)):
            result = conference_data.get_conferences()
        assert 'conferences' in result

    def test_with_conference_id(self):
        with patch('requests.get', return_value=_mock_get(CONFERENCES_DATA)):
            result = conference_data.get_conferences(conference_id=203)
        assert result is not None

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(CONFERENCES_DATA)):
            result = conference_data.get_conferences(season='2023')
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(CONFERENCES_DATA)) as mock_get:
            conference_data.get_conferences(fields=['id', 'name'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'id,name'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            conference_data.get_conferences(fields='id,name')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            conference_data.get_conferences(invalid_param='x')

    def test_valid_params_list(self):
        assert set(conference_data.VALID_CONFERENCE_PARAMS) == {
            'conference_id', 'season', 'fields'
        }
