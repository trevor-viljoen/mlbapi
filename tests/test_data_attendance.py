"""Tests for mlbapi.data.attendance functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import attendance as attendance_data


ATTENDANCE_DATA = {
    'records': [
        {
            'openingDay': '2023-03-30',
            'attendanceHigh': 47000,
            'attendanceHighDate': '2023-07-04',
            'attendanceLow': 15000,
            'attendanceLowDate': '2023-04-10',
            'attendanceTotal': 2500000,
            'attendanceAverage': 30000,
            'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'},
            'year': '2023',
        }
    ],
    'aggregateTotals': {
        'openingDay': '2023-03-30',
        'attendanceTotal': 2500000,
        'attendanceAverage': 30000,
        'year': '2023',
    }
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetAttendance:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance()
        assert 'records' in result

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(team_id=147)
        assert result is not None

    def test_with_league_id(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(league_id=103)
        assert result is not None

    def test_with_season(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(season='2023')
        assert result is not None

    def test_with_date(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(date='06/01/2023')
        assert result is not None

    def test_with_game_type(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(game_type='R')
        assert result is not None

    def test_with_league_list_id(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)):
            result = attendance_data.get_attendance(league_list_id='MLB')
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(ATTENDANCE_DATA)) as mock_get:
            attendance_data.get_attendance(fields=['records', 'aggregateTotals'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'records,aggregateTotals'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            attendance_data.get_attendance(fields='records')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            attendance_data.get_attendance(invalid_param='x')

    def test_valid_params_list(self):
        assert set(attendance_data.VALID_ATTENDANCE_PARAMS) == {
            'team_id', 'league_id', 'season', 'date', 'league_list_id', 'game_type', 'fields'
        }
