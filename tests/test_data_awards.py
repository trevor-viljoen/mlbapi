"""Tests for mlbapi.data.awards functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import awards as awards_data


AWARDS_DATA = {
    'awards': [
        {
            'id': 'MLBHOF',
            'name': 'Baseball Hall of Fame',
            'description': 'Hall of Fame Inductee',
            'league': {'id': 103, 'name': 'American League'},
            'sport': {'id': 1, 'name': 'Major League Baseball'},
        }
    ]
}

RECIPIENTS_DATA = {
    'awards': [
        {
            'id': 'MLBHOF',
            'name': 'Baseball Hall of Fame',
            'recipient': {'id': 592450, 'fullName': 'Aaron Judge'},
            'season': '2023',
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetAwards:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)):
            result = awards_data.get_awards()
        assert 'awards' in result

    def test_with_sport_id(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)):
            result = awards_data.get_awards(sport_id=1)
        assert result is not None

    def test_with_league_id(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)):
            result = awards_data.get_awards(league_id=103)
        assert result is not None

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)):
            result = awards_data.get_awards(season='2023')
        assert result is not None

    def test_with_hydrate(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)):
            result = awards_data.get_awards(hydrate='person')
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(AWARDS_DATA)) as mock_get:
            awards_data.get_awards(fields=['awards', 'name'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'awards,name'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            awards_data.get_awards(fields='awards,name')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            awards_data.get_awards(invalid_param='x')


class TestGetAwardRecipients:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(RECIPIENTS_DATA)):
            result = awards_data.get_award_recipients('MLBHOF')
        assert 'awards' in result

    def test_url_contains_award_id_and_recipients(self):
        with patch('requests.get', return_value=_mock_get(RECIPIENTS_DATA)) as mock_get:
            awards_data.get_award_recipients('MLBHOF')
        url = mock_get.call_args[0][0]
        assert '/awards/MLBHOF/recipients' in url

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(RECIPIENTS_DATA)):
            result = awards_data.get_award_recipients('MLBHOF', season='2023')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            awards_data.get_award_recipients('MLBHOF', invalid_param='x')

    def test_valid_params_list(self):
        assert set(awards_data.VALID_AWARDS_PARAMS) == {
            'award_id', 'sport_id', 'league_id', 'season', 'hydrate', 'fields'
        }
