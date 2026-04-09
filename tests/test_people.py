"""Tests for People/Person Pydantic model and mlbapi.data.people functions."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.models.people import Person, People
from mlbapi.data import people as people_data

PEOPLE_FIXTURE = {
    'people': [
        {
            'id': 660271,
            'fullName': 'Shohei Ohtani',
            'firstName': 'Shohei',
            'lastName': 'Ohtani',
            'primaryNumber': '17',
            'active': True,
            'primaryPosition': {
                'code': '10',
                'name': 'Pitcher',
                'type': 'Pitcher',
                'abbreviation': 'P',
            },
            'batSide': {'code': 'L', 'description': 'Left'},
            'pitchHand': {'code': 'R', 'description': 'Right'},
        }
    ]
}


def _mock_get(data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    return mock_resp


class TestPeopleModel:
    def test_isinstance_people(self):
        result = People(PEOPLE_FIXTURE)
        assert isinstance(result, People)

    def test_people_list_length(self):
        result = People(PEOPLE_FIXTURE)
        assert isinstance(result.people, list)
        assert len(result.people) == 1

    def test_person_id(self):
        result = People(PEOPLE_FIXTURE)
        assert result.people[0].id == 660271

    def test_person_full_name(self):
        result = People(PEOPLE_FIXTURE)
        assert result.people[0].full_name == 'Shohei Ohtani'

    def test_person_active(self):
        result = People(PEOPLE_FIXTURE)
        assert result.people[0].active is True

    def test_person_nested_position(self):
        result = People(PEOPLE_FIXTURE)
        pos = result.people[0].primary_position
        assert pos is not None
        assert pos.name == 'Pitcher'
        assert pos.abbreviation == 'P'

    def test_person_bat_side(self):
        result = People(PEOPLE_FIXTURE)
        bat = result.people[0].bat_side
        assert bat is not None
        assert bat.code == 'L'

    def test_person_pitch_hand(self):
        result = People(PEOPLE_FIXTURE)
        ph = result.people[0].pitch_hand
        assert ph is not None
        assert ph.code == 'R'

    def test_person_model_instance(self):
        result = People(PEOPLE_FIXTURE)
        assert isinstance(result.people[0], Person)

    def test_empty_people(self):
        result = People({'people': []})
        assert result.people == []


class TestPeopleDataParams:
    def test_valid_people_params(self):
        assert set(people_data.VALID_PEOPLE_PARAMS) >= {
            'person_ids', 'season', 'sport_id', 'hydrate', 'fields'
        }

    def test_valid_person_params(self):
        assert set(people_data.VALID_PERSON_PARAMS) >= {
            'person_id', 'season', 'hydrate', 'fields'
        }

    def test_valid_people_search_params(self):
        assert set(people_data.VALID_PEOPLE_SEARCH_PARAMS) >= {
            'names', 'sport_id', 'active', 'hydrate', 'fields'
        }


class TestGetPeople:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_FIXTURE)):
            result = people_data.get_people(person_ids=[660271])
        assert 'people' in result

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.get_people(invalid_param='x')


class TestSearchPeople:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_FIXTURE)):
            result = people_data.search_people(names='Ohtani')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.search_people(names='Ohtani', invalid_param='x')
