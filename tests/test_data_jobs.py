"""Tests for mlbapi.data.jobs functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import jobs as jobs_data


JOBS_DATA = {
    'roster': [
        {
            'position': {'code': 'UMP', 'name': 'Umpire'},
            'status': {'code': 'A', 'description': 'Active'},
            'person': {'id': 427151, 'fullName': 'Joe Umpire'},
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetJobs:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_jobs()
        assert result is not None

    def test_with_job_type(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_jobs(job_type='UMP')
        assert result is not None

    def test_with_sport_id(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_jobs(sport_id=1)
        assert result is not None

    def test_with_date(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_jobs(date='06/01/2023')
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)) as mock_get:
            jobs_data.get_jobs(fields=['roster'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'roster'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            jobs_data.get_jobs(fields='roster')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            jobs_data.get_jobs(invalid_param='x')


class TestGetUmpires:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_umpires()
        assert result is not None

    def test_url_contains_umpires(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)) as mock_get:
            jobs_data.get_umpires()
        url = mock_get.call_args[0][0]
        assert '/jobs/umpires' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            jobs_data.get_umpires(invalid_param='x')


class TestGetDatacasters:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_datacasters()
        assert result is not None

    def test_url_contains_datacasters(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)) as mock_get:
            jobs_data.get_datacasters()
        url = mock_get.call_args[0][0]
        assert '/jobs/datacasters' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            jobs_data.get_datacasters(invalid_param='x')


class TestGetOfficialScorers:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)):
            result = jobs_data.get_official_scorers()
        assert result is not None

    def test_url_contains_official_scorers(self):
        with patch('requests.get', return_value=_mock_get(JOBS_DATA)) as mock_get:
            jobs_data.get_official_scorers()
        url = mock_get.call_args[0][0]
        assert '/jobs/officialScorers' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            jobs_data.get_official_scorers(invalid_param='x')

    def test_valid_params_list(self):
        assert set(jobs_data.VALID_JOBS_PARAMS) == {
            'job_type', 'sport_id', 'date', 'fields'
        }
