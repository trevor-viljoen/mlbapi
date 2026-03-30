"""Tests for mlbapi.data.meta functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import meta as meta_data


GAME_TYPES_DATA = [
    {'id': 'R', 'description': 'Regular Season', 'shortDescription': 'Regular Season'},
    {'id': 'P', 'description': 'Postseason', 'shortDescription': 'Postseason'},
    {'id': 'S', 'description': 'Spring Training', 'shortDescription': 'Spring Training'},
]

STANDINGS_TYPES_DATA = [
    {'id': 'regularSeason', 'description': 'Regular Season Standings'},
    {'id': 'wildCard', 'description': 'Wild Card Standings'},
]


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestGetMeta:
    def test_game_types_returns_json(self):
        with patch('requests.get', return_value=_mock_get(GAME_TYPES_DATA)):
            result = meta_data.get_meta('gameTypes')
        assert result is not None

    def test_standings_types_returns_json(self):
        with patch('requests.get', return_value=_mock_get(STANDINGS_TYPES_DATA)):
            result = meta_data.get_meta('standingsTypes')
        assert result is not None

    def test_stat_groups_valid(self):
        with patch('requests.get', return_value=_mock_get([])):
            result = meta_data.get_meta('statGroups')
        assert result is not None

    def test_all_valid_types_do_not_raise(self):
        for meta_type in meta_data.VALID_META_TYPES:
            with patch('requests.get', return_value=_mock_get([])):
                result = meta_data.get_meta(meta_type)
            assert result is not None

    def test_invalid_meta_type_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            meta_data.get_meta('invalidMetaType')

    def test_url_contains_meta_type(self):
        with patch('requests.get', return_value=_mock_get(GAME_TYPES_DATA)) as mock_get:
            meta_data.get_meta('gameTypes')
        url = mock_get.call_args[0][0]
        assert '/gameTypes' in url

    def test_valid_meta_types_list(self):
        assert 'gameTypes' in meta_data.VALID_META_TYPES
        assert 'standingsTypes' in meta_data.VALID_META_TYPES
        assert 'statGroups' in meta_data.VALID_META_TYPES
        assert 'positions' in meta_data.VALID_META_TYPES
