"""Tests for mlbapi.object base utilities."""
import pytest
from datetime import datetime

import mlbapi.object
from mlbapi.object import Object, setobjattr, listofobjs


class SimpleObj:
    pass


class TestSetObjAttr:
    def test_sets_string_attribute(self):
        obj = SimpleObj()
        setobjattr(obj, 'name', 'Aaron Judge')
        assert obj.name == 'Aaron Judge'

    def test_sets_int_from_int(self):
        obj = SimpleObj()
        setobjattr(obj, 'jersey_number', 99)
        assert obj.jersey_number == 99

    def test_sets_int_from_string(self):
        # v1.0.0: setobjattr is a thin shim — no type coercion; strings stay strings.
        # Type coercion now belongs in Pydantic field declarations on MLBModel subclasses.
        obj = SimpleObj()
        setobjattr(obj, 'jersey_number', '99')
        assert obj.jersey_number == '99'

    def test_sets_float_from_string(self):
        # v1.0.0: setobjattr no longer coerces strings to floats.
        obj = SimpleObj()
        setobjattr(obj, 'batting_avg', '0.315')
        assert obj.batting_avg == '0.315'

    def test_sets_bool_true(self):
        obj = SimpleObj()
        setobjattr(obj, 'active', True)
        assert obj.active is True

    def test_sets_bool_false(self):
        obj = SimpleObj()
        setobjattr(obj, 'active', False)
        assert obj.active is False

    def test_bool_not_converted_to_int(self):
        obj = SimpleObj()
        setobjattr(obj, 'active', True)
        assert isinstance(obj.active, bool)

    def test_converts_camel_key_to_snake(self):
        obj = SimpleObj()
        setobjattr(obj, 'gameType', 'R')
        assert hasattr(obj, 'game_type')
        assert obj.game_type == 'R'

    def test_parses_datetime_string(self):
        # v1.0.0: setobjattr no longer parses datetime strings; value is stored as-is.
        # Declare the field as datetime on an MLBModel subclass for automatic parsing.
        obj = SimpleObj()
        setobjattr(obj, 'game_date', '2023-06-01T17:10:00Z')
        assert obj.game_date == '2023-06-01T17:10:00Z'

    def test_ordinal_field_stays_string(self):
        obj = SimpleObj()
        setobjattr(obj, 'ordinalNum', '1st')
        assert obj.ordinal_num == '1st'

    def test_set_with_obj_constructor(self):
        class SubObj:
            def __init__(self, data):
                self.value = data

        obj = SimpleObj()
        setobjattr(obj, 'sub', {'key': 'val'}, SubObj)
        assert isinstance(obj.sub, SubObj)
        assert obj.sub.value == {'key': 'val'}


class TestListOfObjs:
    def test_creates_list_of_objects(self):
        class Item:
            def __init__(self, data):
                self.val = data

        result = listofobjs([1, 2, 3], Item)
        assert len(result) == 3
        assert all(isinstance(r, Item) for r in result)
        assert result[0].val == 1

    def test_empty_list(self):
        class Item:
            def __init__(self, data):
                pass

        result = listofobjs([], Item)
        assert result == []


class TestObject:
    def test_basic_dict_creates_attributes(self):
        obj = Object({'name': 'Test', 'id': 1})
        assert obj.name == 'Test'
        assert obj.id == 1

    def test_camel_keys_converted(self):
        obj = Object({'gamePk': 716463, 'gameType': 'R'})
        assert obj.game_pk == 716463
        assert obj.game_type == 'R'

    def test_empty_dict(self):
        obj = Object({})
        assert isinstance(obj, Object)
