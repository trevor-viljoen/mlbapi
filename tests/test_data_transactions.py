"""Tests for mlbapi.data.transactions functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import transactions as transactions_data


TRANSACTIONS_DATA = {
    'transactions': [
        {
            'id': 123456,
            'person': {'id': 592450, 'fullName': 'Aaron Judge', 'link': '/api/v1/people/592450'},
            'toTeam': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'},
            'fromTeam': None,
            'date': '2023-01-15',
            'effectiveDate': '2023-01-15',
            'resolutionDate': '2023-01-15',
            'typeCode': 'SC',
            'typeDesc': 'Signed Contract',
            'description': 'New York Yankees signed Aaron Judge.',
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetTransactions:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions()
        assert 'transactions' in result

    def test_with_team_id(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions(team_id=147)
        assert result is not None

    def test_with_player_id(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions(player_id=592450)
        assert result is not None

    def test_with_date(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions(date='01/15/2023')
        assert result is not None

    def test_with_date_range(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions(
                start_date='01/01/2023', end_date='01/31/2023'
            )
        assert result is not None

    def test_with_sport_id(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)):
            result = transactions_data.get_transactions(sport_id=1)
        assert result is not None

    def test_with_fields_list(self):
        with patch('requests.get', return_value=_mock_get(TRANSACTIONS_DATA)) as mock_get:
            transactions_data.get_transactions(fields=['transactions', 'person'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'transactions,person'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            transactions_data.get_transactions(fields='transactions')

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            transactions_data.get_transactions(invalid_param='x')

    def test_valid_params_list(self):
        assert set(transactions_data.VALID_TRANSACTIONS_PARAMS) == {
            'team_id', 'player_id', 'date', 'start_date', 'end_date', 'sport_id', 'fields'
        }
