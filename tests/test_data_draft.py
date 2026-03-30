"""Tests for mlbapi.data.draft functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import draft as draft_data


DRAFT_DATA = {
    'drafts': {
        'draftYear': 2023,
        'rounds': [
            {
                'round': '1',
                'picks': [
                    {
                        'bisPlayerId': 12345,
                        'pickRound': '1',
                        'pickNumber': 1,
                        'roundPickNumber': 1,
                        'rank': 1,
                        'pickValue': '10.0',
                        'signingBonus': '10.0',
                        'home': {'city': 'New York', 'state': 'NY', 'country': 'USA'},
                        'scoutingReport': 'Elite prospect',
                        'school': {'name': 'UCLA', 'schoolClass': 'JR', 'city': 'Los Angeles',
                                   'country': 'USA'},
                        'blurb': 'Top prospect',
                        'headshotLink': '/headshots/12345.jpg',
                        'person': {
                            'id': 694973, 'fullName': 'Top Pick', 'link': '/api/v1/people/694973'
                        },
                        'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'},
                        'isDrafted': True,
                        'isPass': False,
                    }
                ]
            }
        ]
    }
}

PROSPECTS_DATA = {
    'drafts': {'rounds': []}
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetDraft:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)):
            result = draft_data.get_draft(2023)
        assert 'drafts' in result

    def test_url_contains_year(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)) as mock_get:
            draft_data.get_draft(2023)
        url = mock_get.call_args[0][0]
        assert '/draft/2023' in url

    def test_with_round(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)):
            result = draft_data.get_draft(2023, round='1')
        assert result is not None

    def test_with_limit(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)):
            result = draft_data.get_draft(2023, limit=50)
        assert result is not None

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)):
            result = draft_data.get_draft(2023, team_id=147)
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)) as mock_get:
            draft_data.get_draft(2023, fields=['drafts', 'rounds'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'drafts,rounds'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            draft_data.get_draft(2023, fields='drafts,rounds')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            draft_data.get_draft(2023, invalid_param='x')


class TestGetDraftProspects:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PROSPECTS_DATA)):
            result = draft_data.get_draft_prospects()
        assert result is not None

    def test_url_contains_prospects(self):
        with patch('requests.get', return_value=_mock_get(PROSPECTS_DATA)) as mock_get:
            draft_data.get_draft_prospects()
        url = mock_get.call_args[0][0]
        assert '/draft/prospects' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            draft_data.get_draft_prospects(invalid_param='x')


class TestGetDraftLatest:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)):
            result = draft_data.get_draft_latest(2023)
        assert result is not None

    def test_url_contains_year_and_latest(self):
        with patch('requests.get', return_value=_mock_get(DRAFT_DATA)) as mock_get:
            draft_data.get_draft_latest(2023)
        url = mock_get.call_args[0][0]
        assert '/draft/2023/latest' in url

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            draft_data.get_draft_latest(2023, invalid_param='x')

    def test_valid_params_list(self):
        assert 'team_id' in draft_data.VALID_DRAFT_PARAMS
        assert 'round' in draft_data.VALID_DRAFT_PARAMS
        assert 'limit' in draft_data.VALID_DRAFT_PARAMS
