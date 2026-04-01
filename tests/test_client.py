"""Tests for mlbapi.client.Client."""
import pytest
from unittest.mock import MagicMock, patch

import requests

import mlbapi
import mlbapi.exceptions
from mlbapi.client import Client
from mlbapi.object.game import BoxScore, LineScore
from mlbapi.object.gameday import Schedule
from mlbapi.object.standings import Standings
from mlbapi.object.team import Teams
from mlbapi.object.division import Divisions
from tests.conftest import (
    BOXSCORE_DATA, LINESCORE_DATA, SCHEDULE_DATA,
    STANDINGS_DATA, TEAMS_DATA, DIVISIONS_DATA,
)


def _mock_response(data):
    mock = MagicMock()
    mock.json.return_value = data
    return mock


# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------

class TestClientConstructor:
    def test_default_base_url(self):
        c = Client()
        assert c._base_url == 'https://statsapi.mlb.com/api'

    def test_custom_base_url(self):
        c = Client(base_url='https://example.com/api')
        assert c._base_url == 'https://example.com/api'

    def test_default_timeout_is_none(self):
        c = Client()
        assert c._timeout is None

    def test_custom_timeout(self):
        c = Client(timeout=30)
        assert c._timeout == 30

    def test_default_session_is_none(self):
        c = Client()
        assert c._session is None

    def test_injected_session_stored(self):
        session = requests.Session()
        c = Client(session=session)
        assert c._session is session

    def test_module_level_client_is_client_instance(self):
        assert isinstance(mlbapi._default, Client)


# ---------------------------------------------------------------------------
# Session injection — mock session bypasses requests.get entirely
# ---------------------------------------------------------------------------

class TestSessionInjection:
    def _client_with_mock(self, data):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(data)
        return Client(session=session), session

    def test_session_get_called_not_requests_get(self):
        client, session = self._client_with_mock(BOXSCORE_DATA)
        with patch('requests.get') as mock_global:
            result = client.boxscore(716463)
        session.get.assert_called_once()
        mock_global.assert_not_called()

    def test_boxscore_via_session(self):
        client, _ = self._client_with_mock(BOXSCORE_DATA)
        result = client.boxscore(716463)
        assert isinstance(result, BoxScore)

    def test_linescore_via_session(self):
        client, _ = self._client_with_mock(LINESCORE_DATA)
        result = client.linescore(716463)
        assert isinstance(result, LineScore)

    def test_schedule_via_session(self):
        client, _ = self._client_with_mock(SCHEDULE_DATA)
        result = client.schedule(date='2023-06-01')
        assert isinstance(result, Schedule)

    def test_standings_via_session(self):
        client, _ = self._client_with_mock(STANDINGS_DATA)
        result = client.standings()
        assert isinstance(result, Standings)

    def test_teams_via_session(self):
        client, _ = self._client_with_mock(TEAMS_DATA)
        result = client.teams()
        assert isinstance(result, Teams)

    def test_timeout_forwarded_to_session(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(BOXSCORE_DATA)
        client = Client(timeout=15, session=session)
        client.boxscore(716463)
        _, kwargs = session.get.call_args
        assert kwargs.get('timeout') == 15


# ---------------------------------------------------------------------------
# Default client uses requests.get (backwards compat)
# ---------------------------------------------------------------------------

class TestDefaultClientUsesRequestsGet:
    def test_no_session_uses_requests_get(self):
        client = Client()
        with patch('requests.get', return_value=_mock_response(BOXSCORE_DATA)) as mock_get:
            result = client.boxscore(716463)
        mock_get.assert_called_once()
        assert isinstance(result, BoxScore)


# ---------------------------------------------------------------------------
# Parameter validation
# ---------------------------------------------------------------------------

class TestParameterValidation:
    def _client(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(SCHEDULE_DATA)
        return Client(session=session)

    def test_invalid_param_raises(self):
        client = self._client()
        with pytest.raises(mlbapi.exceptions.ParameterException):
            client.boxscore(716463, not_a_real_param='x')

    def test_schedule_start_date_without_end_raises(self):
        client = self._client()
        with pytest.raises(mlbapi.exceptions.ParameterException):
            client.schedule(start_date='2023-06-01')

    def test_schedule_end_date_without_start_raises(self):
        client = self._client()
        with pytest.raises(mlbapi.exceptions.ParameterException):
            client.schedule(end_date='2023-06-01')

    def test_schedule_opponent_id_without_team_id_raises(self):
        client = self._client()
        with pytest.raises(mlbapi.exceptions.ParameterException):
            client.schedule(opponent_id=147)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_object_not_found_raises(self):
        error_data = {'message': 'Object not found', 'messageNumber': 11}
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(error_data)
        client = Client(session=session)
        with pytest.raises(mlbapi.exceptions.ObjectNotFoundException):
            client.boxscore(999999)

    def test_network_error_raises_request_exception(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = requests.exceptions.ConnectionError('down')
        client = Client(session=session)
        with pytest.raises(mlbapi.exceptions.RequestException):
            client.boxscore(716463)


# ---------------------------------------------------------------------------
# Module-level convenience functions still work (backwards compat)
# ---------------------------------------------------------------------------

class TestModuleLevelFunctions:
    def test_boxscore(self):
        with patch('requests.get', return_value=_mock_response(BOXSCORE_DATA)):
            result = mlbapi.boxscore(716463)
        assert isinstance(result, BoxScore)

    def test_linescore(self):
        with patch('requests.get', return_value=_mock_response(LINESCORE_DATA)):
            result = mlbapi.linescore(716463)
        assert isinstance(result, LineScore)

    def test_schedule(self):
        with patch('requests.get', return_value=_mock_response(SCHEDULE_DATA)):
            result = mlbapi.schedule(date='2023-06-01')
        assert isinstance(result, Schedule)

    def test_standings(self):
        with patch('requests.get', return_value=_mock_response(STANDINGS_DATA)):
            result = mlbapi.standings()
        assert isinstance(result, Standings)

    def test_teams(self):
        with patch('requests.get', return_value=_mock_response(TEAMS_DATA)):
            result = mlbapi.teams()
        assert isinstance(result, Teams)

    def test_divisions(self):
        with patch('requests.get', return_value=_mock_response(DIVISIONS_DATA)):
            result = mlbapi.divisions()
        assert isinstance(result, Divisions)
