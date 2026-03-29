"""Tests for mlbapi.data.venue functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import venue as venue_data


VENUES_DATA = {
    'venues': [
        {'id': 3313, 'name': 'Yankee Stadium', 'link': '/api/v1/venues/3313'}
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetVenues:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(VENUES_DATA)):
            result = venue_data.get_venues()
        assert 'venues' in result

    def test_with_venue_ids_list(self):
        with patch('requests.get', return_value=_mock_get(VENUES_DATA)) as mock_get:
            venue_data.get_venues(venue_ids=[3313, 4214])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('venueIds') == '3313,4214'

    def test_venue_ids_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            venue_data.get_venues(venue_ids=3313)

    def test_venue_ids_invalid_value_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            venue_data.get_venues(venue_ids=['abc', 'xyz'])

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(VENUES_DATA)):
            result = venue_data.get_venues(season='2023')
        assert result is not None

    def test_with_hydrate(self):
        with patch('requests.get', return_value=_mock_get(VENUES_DATA)):
            result = venue_data.get_venues(hydrate='location')
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(VENUES_DATA)) as mock_get:
            venue_data.get_venues(fields=['id', 'name'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'id,name'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            venue_data.get_venues(fields='id,name')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            venue_data.get_venues(invalid_param='x')

    def test_valid_params_list(self):
        assert set(venue_data.VALID_VENUE_PARAMS) == {
            'venue_ids', 'season', 'hydrate', 'fields'
        }
