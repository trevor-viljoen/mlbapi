"""Tests for mlbapi.data.gameday (schedule) functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import schedule as schedule_data
from tests.conftest import SCHEDULE_DATA


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetSchedule:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(date='06/01/2023')
        assert 'dates' in result

    def test_defaults_sport_id_to_1(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)) as mock_get:
            schedule_data.get_schedule(date='06/01/2023')
        call_kwargs = mock_get.call_args[1]
        params = call_kwargs.get('params', {})
        assert params.get('sportId') == 1

    def test_explicit_sport_id_not_overridden(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)) as mock_get:
            schedule_data.get_schedule(sport_id=11, date='06/01/2023')
        call_kwargs = mock_get.call_args[1]
        params = call_kwargs.get('params', {})
        assert params.get('sportId') == 11

    def test_start_date_without_end_date_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='start_date'):
            schedule_data.get_schedule(start_date='06/01/2023')

    def test_end_date_without_start_date_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='end_date'):
            schedule_data.get_schedule(end_date='06/01/2023')

    def test_start_and_end_date_together_passes(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(start_date='06/01/2023', end_date='06/07/2023')
        assert result is not None

    def test_opponent_id_without_team_id_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='opponentId'):
            schedule_data.get_schedule(opponent_id=147)

    def test_seasons_as_list_of_ints(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(seasons=[2022, 2023])
        assert result is not None

    def test_seasons_as_list_of_strings(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(seasons=['2022', '2023'])
        assert result is not None

    def test_seasons_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='seasons must be a list'):
            schedule_data.get_schedule(seasons='2023')

    def test_seasons_invalid_value_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            schedule_data.get_schedule(seasons=['not_a_year'])

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            schedule_data.get_schedule(invalid_param='x')

    def test_team_id_param(self):
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(team_id=147, date='06/01/2023')
        assert result is not None

    def test_opponent_id_with_team_id_passes(self):
        # opponent_id validation only runs when start_date/end_date checks pass
        # and opponent_id check comes in elif chain
        with patch('requests.get', return_value=_mock_get(SCHEDULE_DATA)):
            result = schedule_data.get_schedule(team_id=147, opponent_id=111, date='06/01/2023')
        assert result is not None
