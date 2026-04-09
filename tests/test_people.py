"""Tests for mlbapi.models.people and mlbapi.data.people."""
import pytest
from unittest.mock import patch, MagicMock

import mlbapi.exceptions
from mlbapi.data import people as people_data
from mlbapi.models.people import Handedness, People, Person, Position


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

PERSON_DATA = {
    'id': 592450,
    'fullName': 'Aaron Judge',
    'link': '/api/v1/people/592450',
    'firstName': 'Aaron',
    'lastName': 'Judge',
    'primaryNumber': '99',
    'birthDate': '1992-04-26',
    'currentAge': 31,
    'birthCity': 'Linden',
    'birthStateProvince': 'CA',
    'birthCountry': 'USA',
    'height': "6' 7\"",
    'weight': 282,
    'active': True,
    'useName': 'Aaron',
    'middleName': 'James',
    'boxscoreName': 'Judge',
    'gender': 'M',
    'isPlayer': True,
    'isVerified': True,
    'draftYear': 2013,
    'mlbDebutDate': '2016-08-13',
    'nameFirstLast': 'Aaron Judge',
    'nameSlug': 'aaron-judge-592450',
    'firstLastName': 'Aaron Judge',
    'lastFirstName': 'Judge, Aaron',
    'lastInitName': 'Judge, A',
    'initLastName': 'A. Judge',
    'fullFMLName': 'Aaron James Judge',
    'fullLFMName': 'Judge, Aaron James',
    'strikeZoneTop': 3.71,
    'strikeZoneBottom': 1.89,
    'primaryPosition': {
        'code': '9',
        'name': 'Outfielder',
        'type': 'Outfielder',
        'abbreviation': 'RF',
    },
    'batSide': {'code': 'R', 'description': 'Right'},
    'pitchHand': {'code': 'R', 'description': 'Right'},
}

PEOPLE_DATA = {
    'copyright': 'Copyright 2023 MLB',
    'people': [PERSON_DATA],
}

PEOPLE_RESPONSE = {'people': [PERSON_DATA]}


def _mock_get(data):
    resp = MagicMock()
    resp.json.return_value = data
    return resp


# ===========================================================================
# Model tests
# ===========================================================================

class TestPosition:
    def test_code(self):
        p = Position(PERSON_DATA['primaryPosition'])
        assert p.code == '9'

    def test_name(self):
        p = Position(PERSON_DATA['primaryPosition'])
        assert p.name == 'Outfielder'

    def test_type(self):
        p = Position(PERSON_DATA['primaryPosition'])
        assert p.type == 'Outfielder'

    def test_abbreviation(self):
        p = Position(PERSON_DATA['primaryPosition'])
        assert p.abbreviation == 'RF'


class TestHandedness:
    def test_code(self):
        h = Handedness(PERSON_DATA['batSide'])
        assert h.code == 'R'

    def test_description(self):
        h = Handedness(PERSON_DATA['batSide'])
        assert h.description == 'Right'


class TestPerson:
    def test_id(self):
        p = Person(PERSON_DATA)
        assert p.id == 592450

    def test_full_name(self):
        p = Person(PERSON_DATA)
        assert p.full_name == 'Aaron Judge'

    def test_first_name(self):
        p = Person(PERSON_DATA)
        assert p.first_name == 'Aaron'

    def test_last_name(self):
        p = Person(PERSON_DATA)
        assert p.last_name == 'Judge'

    def test_primary_number(self):
        p = Person(PERSON_DATA)
        assert p.primary_number == '99'

    def test_current_age(self):
        p = Person(PERSON_DATA)
        assert p.current_age == 31

    def test_weight(self):
        p = Person(PERSON_DATA)
        assert p.weight == 282

    def test_active(self):
        p = Person(PERSON_DATA)
        assert p.active is True

    def test_is_player(self):
        p = Person(PERSON_DATA)
        assert p.is_player is True

    def test_draft_year(self):
        p = Person(PERSON_DATA)
        assert p.draft_year == 2013

    def test_strike_zone_top(self):
        p = Person(PERSON_DATA)
        assert abs(p.strike_zone_top - 3.71) < 1e-4

    def test_strike_zone_bottom(self):
        p = Person(PERSON_DATA)
        assert abs(p.strike_zone_bottom - 1.89) < 1e-4

    def test_primary_position_is_position(self):
        p = Person(PERSON_DATA)
        assert isinstance(p.primary_position, Position)

    def test_primary_position_code(self):
        p = Person(PERSON_DATA)
        assert p.primary_position.code == '9'

    def test_bat_side_is_handedness(self):
        p = Person(PERSON_DATA)
        assert isinstance(p.bat_side, Handedness)

    def test_bat_side_code(self):
        p = Person(PERSON_DATA)
        assert p.bat_side.code == 'R'

    def test_pitch_hand_is_handedness(self):
        p = Person(PERSON_DATA)
        assert isinstance(p.pitch_hand, Handedness)

    def test_no_position_when_missing(self):
        p = Person({'id': 1, 'fullName': 'Test Player'})
        assert p.primary_position is None

    def test_no_bat_side_when_missing(self):
        p = Person({'id': 1, 'fullName': 'Test Player'})
        assert p.bat_side is None

    def test_name_slug(self):
        p = Person(PERSON_DATA)
        assert p.name_slug == 'aaron-judge-592450'

    def test_repr(self):
        p = Person(PERSON_DATA)
        assert 'Person' in repr(p)


class TestPeople:
    def test_people_list(self):
        pp = People(PEOPLE_DATA)
        assert isinstance(pp.people, list)
        assert len(pp.people) == 1

    def test_copyright(self):
        pp = People(PEOPLE_DATA)
        assert pp.copyright == 'Copyright 2023 MLB'

    def test_first_person_id(self):
        pp = People(PEOPLE_DATA)
        assert pp.people[0].id == 592450

    def test_empty_people(self):
        pp = People({'people': []})
        assert pp.people == []

    def test_missing_people_key(self):
        pp = People({})
        assert pp.people == []


# ===========================================================================
# Data layer tests
# ===========================================================================

class TestValidParamLists:
    def test_people_params_exist(self):
        assert hasattr(people_data, 'VALID_PEOPLE_PARAMS')
        assert isinstance(people_data.VALID_PEOPLE_PARAMS, list)
        assert len(people_data.VALID_PEOPLE_PARAMS) > 0

    def test_people_search_params_exist(self):
        assert hasattr(people_data, 'VALID_PEOPLE_SEARCH_PARAMS')
        assert isinstance(people_data.VALID_PEOPLE_SEARCH_PARAMS, list)
        assert len(people_data.VALID_PEOPLE_SEARCH_PARAMS) > 0

    def test_person_stats_params_exist(self):
        assert hasattr(people_data, 'VALID_PERSON_STATS_PARAMS')
        assert isinstance(people_data.VALID_PERSON_STATS_PARAMS, list)
        assert len(people_data.VALID_PERSON_STATS_PARAMS) > 0

    def test_person_params_exist(self):
        assert hasattr(people_data, 'VALID_PERSON_PARAMS')

    def test_people_params_contains_expected_keys(self):
        assert 'season' in people_data.VALID_PEOPLE_PARAMS
        assert 'fields' in people_data.VALID_PEOPLE_PARAMS

    def test_search_params_contains_names(self):
        assert 'names' in people_data.VALID_PEOPLE_SEARCH_PARAMS

    def test_stats_params_contains_stats(self):
        assert 'stats' in people_data.VALID_PERSON_STATS_PARAMS


class TestGetPeople:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)):
            result = people_data.get_people()
        assert 'people' in result

    def test_with_person_ids_list(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)) as mock_get:
            people_data.get_people(person_ids=[592450, 660271])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('personIds') == '592450,660271'

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.get_people(invalid_param='x')

    def test_fields_list_joined(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)) as mock_get:
            people_data.get_people(fields=['id', 'fullName'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'id,fullName'

    def test_fields_not_list_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.get_people(fields='id,fullName')


class TestGetPerson:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)):
            result = people_data.get_person(592450)
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.get_person(592450, invalid_param='x')


class TestSearchPeople:
    def test_returns_json(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)):
            result = people_data.search_people(names='Judge')
        assert result is not None

    def test_invalid_param_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            people_data.search_people(invalid_param='x')

    def test_fields_list_joined(self):
        with patch('requests.get', return_value=_mock_get(PEOPLE_RESPONSE)) as mock_get:
            people_data.search_people(names='Judge', fields=['id', 'fullName'])
        params = mock_get.call_args[1].get('params', {})
        assert params.get('fields') == 'id,fullName'
