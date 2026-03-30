"""Tests for mlbapi.data request and URL construction logic."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.data
import mlbapi.exceptions


class TestGetApiUrl:
    def test_basic_endpoint(self):
        url = mlbapi.data.get_api_url('game')
        assert url == 'https://statsapi.mlb.com/api/v1/game'

    def test_with_primary_key(self):
        url = mlbapi.data.get_api_url('game', primary_key=716463)
        assert url == 'https://statsapi.mlb.com/api/v1/game/716463'

    def test_with_context(self):
        url = mlbapi.data.get_api_url('game', context='boxscore', primary_key=716463)
        assert url == 'https://statsapi.mlb.com/api/v1/game/716463/boxscore'

    def test_with_secondary_key(self):
        url = mlbapi.data.get_api_url('game', context='boxscore',
                                      primary_key=716463, secondary_key=999)
        assert url == 'https://statsapi.mlb.com/api/v1/game/716463/boxscore/999'

    def test_unsupported_endpoint_raises(self):
        with pytest.raises(mlbapi.exceptions.ImplementationException, match='not yet implemented'):
            mlbapi.data.get_api_url('unsupported_endpoint')

    def test_schedule_endpoint(self):
        url = mlbapi.data.get_api_url('schedule')
        assert url == 'https://statsapi.mlb.com/api/v1/schedule'

    def test_standings_endpoint(self):
        url = mlbapi.data.get_api_url('standings')
        assert url == 'https://statsapi.mlb.com/api/v1/standings'

    def test_teams_endpoint(self):
        url = mlbapi.data.get_api_url('teams')
        assert url == 'https://statsapi.mlb.com/api/v1/teams'

    def test_divisions_endpoint(self):
        url = mlbapi.data.get_api_url('divisions')
        assert url == 'https://statsapi.mlb.com/api/v1/divisions'

    def test_sports_endpoint(self):
        url = mlbapi.data.get_api_url('sports')
        assert url == 'https://statsapi.mlb.com/api/v1/sports'

    def test_api_version_override(self):
        url = mlbapi.data.get_api_url('game', primary_key=716463,
                                      context='feed/live', api_version='v1.1')
        assert url == 'https://statsapi.mlb.com/api/v1.1/game/716463/feed/live'

    def test_default_version_is_v1(self):
        url = mlbapi.data.get_api_url('game')
        assert '/v1/' in url

    # Corrected endpoint paths
    def test_conferences_endpoint(self):
        url = mlbapi.data.get_api_url('conferences')
        assert url == 'https://statsapi.mlb.com/api/v1/conferences'

    def test_venues_endpoint(self):
        url = mlbapi.data.get_api_url('venues')
        assert url == 'https://statsapi.mlb.com/api/v1/venues'

    def test_seasons_endpoint(self):
        url = mlbapi.data.get_api_url('seasons')
        assert url == 'https://statsapi.mlb.com/api/v1/seasons'

    def test_home_run_derby_endpoint(self):
        url = mlbapi.data.get_api_url('homeRunDerby', primary_key=716463)
        assert url == 'https://statsapi.mlb.com/api/v1/homeRunDerby/716463'


class TestGetJsonData:
    def test_successful_request_returns_json(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {'key': 'value'}
        with patch('requests.get', return_value=mock_resp):
            result = mlbapi.data.get_json_data({}, 'https://example.com')
        assert result == {'key': 'value'}

    def test_request_with_params(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {'key': 'value'}
        with patch('requests.get', return_value=mock_resp) as mock_get:
            result = mlbapi.data.get_json_data({}, 'https://example.com',
                                               sport_id=1)
        assert result == {'key': 'value'}
        mock_get.assert_called_once()
        _, call_kwargs = mock_get.call_args
        assert 'params' in call_kwargs

    def test_api_error_message_raises_object_not_found(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            'message': 'Object not found',
            'messageNumber': 11
        }
        with patch('requests.get', return_value=mock_resp):
            with pytest.raises(mlbapi.exceptions.ObjectNotFoundException):
                mlbapi.data.get_json_data({}, 'https://example.com')

    def test_network_error_raises_request_exception(self):
        import requests
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError('connection failed')):
            with pytest.raises(mlbapi.exceptions.RequestException):
                mlbapi.data.get_json_data({}, 'https://example.com')

    def test_json_decode_error_propagates(self):
        import json
        mock_resp = MagicMock()
        mock_resp.url = 'https://statsapi.mlb.com/api/v1/test'
        mock_resp.json.side_effect = json.decoder.JSONDecodeError('msg', 'doc', 0)
        with patch('requests.get', return_value=mock_resp):
            with pytest.raises(json.decoder.JSONDecodeError):
                mlbapi.data.get_json_data({}, 'https://example.com')


class TestRequest:
    def test_invalid_param_raises_parameter_exception(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.data.request('game', valid_params=['timecode'], invalid_param='x')

    def test_no_valid_params_allows_anything(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {'result': True}
        with patch('requests.get', return_value=mock_resp):
            result = mlbapi.data.request('game', valid_params=None, any_param='x')
        assert result == {'result': True}

    def test_request_sets_user_agent_header(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        with patch('requests.get', return_value=mock_resp) as mock_get:
            mlbapi.data.request('game')
        _, call_kwargs = mock_get.call_args
        headers = call_kwargs.get('headers', {})
        assert 'User-Agent' in headers
        assert 'mlbapi/' in headers['User-Agent']
