"""Tests for mlbapi.client.Client — the sole public entry point."""
import pytest
from unittest.mock import MagicMock, call, patch

import requests

import mlbapi
from mlbapi import (
    Client,
    ParameterException,
    RequestException,
    ObjectNotFoundException,
)
from mlbapi.models.game import BoxScore, LineScore
from mlbapi.models.schedule import Schedule
from mlbapi.models.standings import Standings
from mlbapi.models.team import Teams
from mlbapi.models.division import Divisions
from tests.conftest import (
    BOXSCORE_DATA, LINESCORE_DATA, SCHEDULE_DATA,
    STANDINGS_DATA, TEAMS_DATA, DIVISIONS_DATA,
)


def _mock_response(data):
    m = MagicMock()
    m.json.return_value = data
    return m


def _client(data):
    """Return a Client with an injected mock session returning *data*."""
    session = MagicMock(spec=requests.Session)
    session.get.return_value = _mock_response(data)
    return Client(session=session)


# ---------------------------------------------------------------------------
# Module interface
# ---------------------------------------------------------------------------

class TestModuleInterface:
    def test_client_importable_from_mlbapi(self):
        from mlbapi import Client
        assert Client is not None

    def test_version_importable(self):
        assert mlbapi.__version__ is not None
        assert isinstance(mlbapi.__version__, str)

    def test_exceptions_importable_from_mlbapi(self):
        from mlbapi import (
            MLBAPIException, RequestException, ImplementationException,
            ObjectNotFoundException, ParameterException,
        )

    def test_no_module_level_schedule_function(self):
        assert not hasattr(mlbapi, 'schedule')

    def test_no_module_level_boxscore_function(self):
        assert not hasattr(mlbapi, 'boxscore')

    def test_no_hidden_default_client(self):
        assert not hasattr(mlbapi, '_default')


# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------

class TestConstructor:
    def test_default_base_url(self):
        assert Client()._base_url == 'https://statsapi.mlb.com/api'

    def test_custom_base_url(self):
        assert Client(base_url='https://example.com/api')._base_url == 'https://example.com/api'

    def test_default_timeout_none(self):
        assert Client()._timeout is None

    def test_custom_timeout(self):
        assert Client(timeout=30)._timeout == 30

    def test_default_session_none(self):
        assert Client()._session is None

    def test_injected_session_stored(self):
        s = requests.Session()
        assert Client(session=s)._session is s

    def test_repr_default(self):
        r = repr(Client())
        assert 'Client(' in r
        assert 'statsapi.mlb.com' in r

    def test_repr_with_timeout(self):
        assert 'timeout=30' in repr(Client(timeout=30))

    def test_repr_with_session(self):
        s = requests.Session()
        assert 'session=<Session>' in repr(Client(session=s))


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------

class TestContextManager:
    def test_enter_returns_client(self):
        with Client() as client:
            assert isinstance(client, Client)

    def test_enter_creates_session_when_none(self):
        c = Client()
        assert c._session is None
        with c:
            assert c._session is not None

    def test_exit_closes_session_it_created(self):
        with patch('requests.Session') as MockSession:
            mock_session = MockSession.return_value
            mock_session.headers = {}
            c = Client()
            with c:
                pass
            mock_session.close.assert_called_once()
        assert c._session is None

    def test_exit_does_not_close_injected_session(self):
        mock_session = MagicMock(spec=requests.Session)
        mock_session.get.return_value = _mock_response(BOXSCORE_DATA)
        c = Client(session=mock_session)
        with c:
            pass
        mock_session.close.assert_not_called()

    def test_context_manager_makes_real_call(self):
        with patch('requests.Session') as MockSession:
            mock_session = MockSession.return_value
            mock_session.headers = {}
            mock_session.get.return_value = _mock_response(BOXSCORE_DATA)
            with Client() as client:
                result = client.boxscore(716463)
        assert isinstance(result, BoxScore)


# ---------------------------------------------------------------------------
# Session injection — verifies session.get() is used, not requests.get()
# ---------------------------------------------------------------------------

class TestSessionInjection:
    def test_session_get_called_not_requests_get(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(BOXSCORE_DATA)
        client = Client(session=session)
        with patch('requests.get') as global_get:
            client.boxscore(716463)
        session.get.assert_called_once()
        global_get.assert_not_called()

    def test_timeout_forwarded(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(BOXSCORE_DATA)
        Client(timeout=15, session=session).boxscore(716463)
        _, kwargs = session.get.call_args
        assert kwargs.get('timeout') == 15

    def test_no_timeout_kwarg_when_none(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(BOXSCORE_DATA)
        Client(session=session).boxscore(716463)
        _, kwargs = session.get.call_args
        assert 'timeout' not in kwargs


# ---------------------------------------------------------------------------
# Default client falls back to requests.get (no session provided)
# ---------------------------------------------------------------------------

class TestDefaultHTTP:
    def test_uses_requests_get_when_no_session(self):
        with patch('requests.get', return_value=_mock_response(BOXSCORE_DATA)) as mock:
            Client().boxscore(716463)
        mock.assert_called_once()


# ---------------------------------------------------------------------------
# Game endpoints
# ---------------------------------------------------------------------------

class TestBoxscore:
    def test_returns_boxscore(self):
        assert isinstance(_client(BOXSCORE_DATA).boxscore(716463), BoxScore)

    def test_has_teams(self):
        result = _client(BOXSCORE_DATA).boxscore(716463)
        assert hasattr(result, 'teams')

    def test_away_team_name(self):
        result = _client(BOXSCORE_DATA).boxscore(716463)
        assert result.teams.away.team.name == 'New York Yankees'

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(BOXSCORE_DATA).boxscore(716463, not_valid='x')


class TestLinescore:
    def test_returns_linescore(self):
        assert isinstance(_client(LINESCORE_DATA).linescore(716463), LineScore)

    def test_innings_count(self):
        result = _client(LINESCORE_DATA).linescore(716463)
        assert isinstance(result.innings, list)
        assert len(result.innings) == 2

    def test_current_inning(self):
        result = _client(LINESCORE_DATA).linescore(716463)
        assert result.current_inning == 9

    def test_count_fields(self):
        result = _client(LINESCORE_DATA).linescore(716463)
        assert result.balls == 2
        assert result.strikes == 1
        assert result.outs == 2

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(LINESCORE_DATA).linescore(716463, not_valid='x')


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

class TestSchedule:
    def test_returns_schedule(self):
        assert isinstance(_client(SCHEDULE_DATA).schedule(date='2023-06-01'), Schedule)

    def test_dates_list(self):
        result = _client(SCHEDULE_DATA).schedule(date='2023-06-01')
        assert isinstance(result.dates, list)
        assert len(result.dates) == 1

    def test_games_in_date(self):
        result = _client(SCHEDULE_DATA).schedule(date='2023-06-01')
        assert len(result.dates[0].games) == 1

    def test_game_pk(self):
        result = _client(SCHEDULE_DATA).schedule(date='2023-06-01')
        assert result.dates[0].games[0].game_pk == 716463

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(SCHEDULE_DATA).schedule(not_valid='x')

    def test_start_date_without_end_raises(self):
        with pytest.raises(ParameterException):
            _client(SCHEDULE_DATA).schedule(start_date='2023-06-01')

    def test_end_date_without_start_raises(self):
        with pytest.raises(ParameterException):
            _client(SCHEDULE_DATA).schedule(end_date='2023-06-01')

    def test_opponent_id_without_team_id_raises(self):
        with pytest.raises(ParameterException):
            _client(SCHEDULE_DATA).schedule(opponent_id=147)

    def test_default_sport_id_added(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response(SCHEDULE_DATA)
        Client(session=session).schedule()
        _, kwargs = session.get.call_args
        params = kwargs.get('params', {})
        assert 'sportId' in params


# ---------------------------------------------------------------------------
# Standings
# ---------------------------------------------------------------------------

class TestStandings:
    def test_returns_standings(self):
        assert isinstance(_client(STANDINGS_DATA).standings(), Standings)

    def test_records_count(self):
        assert len(_client(STANDINGS_DATA).standings().records) == 1

    def test_team_records(self):
        result = _client(STANDINGS_DATA).standings()
        tr = result.records[0].team_records[0]
        assert tr.wins == 30
        assert tr.losses == 22

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(STANDINGS_DATA).standings(not_valid='x')


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

class TestTeams:
    def test_returns_teams(self):
        assert isinstance(_client(TEAMS_DATA).teams(), Teams)

    def test_team_count(self):
        assert len(_client(TEAMS_DATA).teams().teams) == 1

    def test_team_name(self):
        assert _client(TEAMS_DATA).teams().teams[0].name == 'New York Yankees'

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(TEAMS_DATA).teams(not_valid='x')


# ---------------------------------------------------------------------------
# Divisions
# ---------------------------------------------------------------------------

class TestDivisions:
    def test_returns_divisions(self):
        assert isinstance(_client(DIVISIONS_DATA).divisions(), Divisions)

    def test_division_count(self):
        assert len(_client(DIVISIONS_DATA).divisions().divisions) == 1

    def test_division_name(self):
        assert _client(DIVISIONS_DATA).divisions().divisions[0].name == 'American League East'

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(DIVISIONS_DATA).divisions(not_valid='x')


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_object_not_found(self):
        error_data = {'message': 'Object not found', 'messageNumber': 11}
        with pytest.raises(ObjectNotFoundException):
            _client(error_data).boxscore(999999)

    def test_network_error_raises_request_exception(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = requests.exceptions.ConnectionError('network down')
        with pytest.raises(RequestException):
            Client(session=session).boxscore(716463)
