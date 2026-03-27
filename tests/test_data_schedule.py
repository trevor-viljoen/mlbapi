"""Tests for mlbapi.data.schedule (class-based Schedule interface)."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data.schedule import Schedule
from tests.conftest import SCHEDULE_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestScheduleClass:
    def test_valid_params_list(self):
        assert 'date' in Schedule.VALID_SCHEDULE_PARAMS
        assert 'team_id' in Schedule.VALID_SCHEDULE_PARAMS
        assert 'sport_id' in Schedule.VALID_SCHEDULE_PARAMS

    def test_instantiation(self):
        s = Schedule()
        assert isinstance(s, Schedule)


class TestScheduleGetSchedule:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = Schedule.get_schedule(date='06/01/2023')
        assert 'dates' in result

    def test_defaults_sport_id_to_1(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)) as mock_get:
            Schedule.get_schedule(date='06/01/2023')
        params = mock_get.call_args[1].get('params', {})
        assert params.get('sportId') == 1

    def test_explicit_sport_id_not_overridden(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)) as mock_get:
            Schedule.get_schedule(sport_id=11, date='06/01/2023')
        params = mock_get.call_args[1].get('params', {})
        assert params.get('sportId') == 11

    def test_start_date_without_end_date_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='start_date'):
            Schedule.get_schedule(start_date='06/01/2023')

    def test_end_date_without_start_date_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='end_date'):
            Schedule.get_schedule(end_date='06/01/2023')

    def test_start_and_end_date_together_passes(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = Schedule.get_schedule(start_date='06/01/2023', end_date='06/07/2023')
        assert result is not None

    def test_opponent_id_without_team_id_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='opponentId'):
            Schedule.get_schedule(opponent_id=147)

    def test_seasons_as_list_of_ints(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = Schedule.get_schedule(seasons=[2022, 2023])
        assert result is not None

    def test_seasons_as_list_of_strings(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = Schedule.get_schedule(seasons=['2022', '2023'])
        assert result is not None

    def test_seasons_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='seasons must be a list'):
            Schedule.get_schedule(seasons='2023')

    def test_seasons_invalid_value_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            Schedule.get_schedule(seasons=['not_a_year'])

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            Schedule.get_schedule(invalid_param='x')
