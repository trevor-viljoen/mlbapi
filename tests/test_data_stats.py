"""Tests for mlbapi.data.stats functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import stats as stats_data


STATS_DATA = {
    'stats': [
        {
            'type': {'displayName': 'season'},
            'group': {'displayName': 'hitting'},
            'splits': [
                {
                    'season': '2023',
                    'stat': {'avg': '.307', 'homeRuns': 62, 'rbi': 131},
                    'player': {'id': 592450, 'fullName': 'Aaron Judge'},
                    'team': {'id': 147, 'name': 'New York Yankees'},
                }
            ]
        }
    ]
}

LEADERS_DATA = {
    'leagueLeaders': [
        {
            'leaderCategory': 'homeRuns',
            'season': '2023',
            'gameType': {'id': 'R', 'description': 'Regular Season'},
            'leaders': [
                {
                    'rank': 1,
                    'value': '62',
                    'team': {'id': 147, 'name': 'New York Yankees'},
                    'league': {'id': 103, 'name': 'American League'},
                    'person': {'id': 592450, 'fullName': 'Aaron Judge'},
                }
            ]
        }
    ]
}

STREAKS_DATA = {
    'streaks': []
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetStats:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(STATS_DATA)):
            result = stats_data.get_stats(stats=['season'], group=['hitting'], season='2023')
        assert 'stats' in result

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(STATS_DATA)):
            result = stats_data.get_stats(team_id=147)
        assert result is not None

    def test_with_person_id(self):
        with patch('requests.get', return_value=_mock_get(STATS_DATA)):
            result = stats_data.get_stats(person_id=592450)
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(STATS_DATA)) as mock_get:
            stats_data.get_stats(fields=['stats', 'splits'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'stats,splits'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            stats_data.get_stats(fields='stats,splits')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            stats_data.get_stats(invalid_param='x')

    def test_url_is_stats(self):
        with patch('requests.get', return_value=_mock_get(STATS_DATA)) as mock_get:
            stats_data.get_stats()
        url = mock_get.call_args[0][0]
        assert url.endswith('/stats')


class TestGetStatsLeaders:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(LEADERS_DATA)):
            result = stats_data.get_stats_leaders(leader_categories=['homeRuns'])
        assert 'leagueLeaders' in result

    def test_url_contains_leaders(self):
        with patch('requests.get', return_value=_mock_get(LEADERS_DATA)) as mock_get:
            stats_data.get_stats_leaders()
        url = mock_get.call_args[0][0]
        assert '/stats/leaders' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            stats_data.get_stats_leaders(invalid_param='x')

    def test_valid_params_list(self):
        assert 'leader_categories' in stats_data.VALID_STATS_LEADERS_PARAMS
        assert 'season' in stats_data.VALID_STATS_LEADERS_PARAMS


class TestGetStatsStreaks:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(STREAKS_DATA)):
            result = stats_data.get_stats_streaks()
        assert result is not None

    def test_url_contains_streaks(self):
        with patch('requests.get', return_value=_mock_get(STREAKS_DATA)) as mock_get:
            stats_data.get_stats_streaks()
        url = mock_get.call_args[0][0]
        assert '/stats/streaks' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            stats_data.get_stats_streaks(invalid_param='x')

    def test_valid_params_list(self):
        assert 'streak_type' in stats_data.VALID_STATS_STREAKS_PARAMS
        assert 'season' in stats_data.VALID_STATS_STREAKS_PARAMS
