"""Tests for mlbapi.utils"""
import pytest

import mlbapi.utils
import mlbapi.exceptions


class TestCheckKwargs:
    def test_valid_keys_passes(self):
        assert mlbapi.utils.check_kwargs(['a', 'b'], ['a', 'b', 'c'],
                                         mlbapi.exceptions.ParameterException) is True

    def test_invalid_key_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='invalid_key'):
            mlbapi.utils.check_kwargs(['invalid_key'], ['a', 'b'],
                                      mlbapi.exceptions.ParameterException)

    def test_none_valid_params_skips_check(self):
        assert mlbapi.utils.check_kwargs(['anything'], None,
                                         mlbapi.exceptions.ParameterException) is True

    def test_empty_keys_always_passes(self):
        assert mlbapi.utils.check_kwargs([], ['a', 'b'],
                                         mlbapi.exceptions.ParameterException) is True

    def test_subset_of_valid_keys(self):
        assert mlbapi.utils.check_kwargs(['a'], ['a', 'b', 'c'],
                                         mlbapi.exceptions.ParameterException) is True


class TestToPythonVar:
    def test_camel_to_snake(self):
        assert mlbapi.utils.to_python_var('gameType') == 'game_type'

    def test_multi_word_camel(self):
        assert mlbapi.utils.to_python_var('startTimecode') == 'start_timecode'

    def test_already_snake(self):
        assert mlbapi.utils.to_python_var('game_type') == 'game_type'

    def test_single_word(self):
        assert mlbapi.utils.to_python_var('game') == 'game'


class TestToApiKeys:
    def test_snake_to_camel(self):
        result = mlbapi.utils.to_api_keys({'game_type': 'R', 'team_id': 147})
        assert result == {'gameType': 'R', 'teamId': 147}

    def test_single_key(self):
        result = mlbapi.utils.to_api_keys({'sport_id': 1})
        assert result == {'sportId': 1}

    def test_empty_dict(self):
        assert mlbapi.utils.to_api_keys({}) == {}

    def test_values_are_preserved(self):
        result = mlbapi.utils.to_api_keys({'start_date': '06/01/2023'})
        assert result['startDate'] == '06/01/2023'


class TestValidTimecode:
    def test_valid_timecode(self):
        assert mlbapi.utils.valid_timecode('20230601_193000') is True

    def test_invalid_format_hyphen(self):
        assert mlbapi.utils.valid_timecode('2023-06-01') is False

    def test_invalid_format_slash(self):
        assert mlbapi.utils.valid_timecode('06/01/2023') is False

    def test_empty_string(self):
        assert mlbapi.utils.valid_timecode('') is False

    def test_partial_timecode(self):
        assert mlbapi.utils.valid_timecode('20230601') is False


class TestToCommaDelimitedString:
    def test_list_of_ints(self):
        result = mlbapi.utils.to_comma_delimited_string([103, 104], int)
        assert result == '103,104'

    def test_list_of_string_ints(self):
        result = mlbapi.utils.to_comma_delimited_string(['103', '104'], int)
        assert result == '103,104'

    def test_mixed_list(self):
        result = mlbapi.utils.to_comma_delimited_string([103, '104'], int)
        assert result == '103,104'

    def test_single_int_value(self):
        result = mlbapi.utils.to_comma_delimited_string(103, int)
        assert result == '103'

    def test_single_string_value(self):
        result = mlbapi.utils.to_comma_delimited_string('103', int)
        assert result == '103'

    def test_invalid_value_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.utils.to_comma_delimited_string(['not_a_number'], int)

    def test_single_invalid_value_raises(self):
        with pytest.raises(mlbapi.exceptions.ParameterException):
            mlbapi.utils.to_comma_delimited_string('not_a_number', int)
