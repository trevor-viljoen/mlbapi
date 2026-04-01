"""Tests for mlbapi.teams static lookup."""

import pytest
from mlbapi import team_id, TEAMS
from mlbapi.teams import _LOOKUP


class TestTEAMS:
    def test_has_30_teams(self):
        assert len(TEAMS) == 30

    def test_each_entry_has_required_keys(self):
        required = {'id', 'name', 'full_name', 'abbreviation', 'city'}
        for team in TEAMS:
            assert required <= set(team.keys()), team

    def test_ids_are_unique(self):
        ids = [t['id'] for t in TEAMS]
        assert len(ids) == len(set(ids))

    def test_abbreviations_are_unique(self):
        abbrs = [t['abbreviation'] for t in TEAMS]
        assert len(abbrs) == len(set(abbrs))


class TestTeamId:
    def test_abbreviation_uppercase(self):
        assert team_id('NYY') == 147

    def test_abbreviation_lowercase(self):
        assert team_id('nyy') == 147

    def test_nickname(self):
        assert team_id('Yankees') == 147

    def test_nickname_lowercase(self):
        assert team_id('yankees') == 147

    def test_full_name(self):
        assert team_id('New York Yankees') == 147

    def test_full_name_lowercase(self):
        assert team_id('new york yankees') == 147

    def test_city(self):
        assert team_id('Boston') == 111

    def test_city_lowercase(self):
        assert team_id('boston') == 111

    def test_unknown_returns_none(self):
        assert team_id('unknown') is None

    def test_empty_string_returns_none(self):
        assert team_id('') is None

    def test_strips_whitespace(self):
        assert team_id('  NYY  ') == 147

    # Spot-check each division
    def test_al_east(self):
        assert team_id('BAL') == 110
        assert team_id('BOS') == 111
        assert team_id('TB') == 139
        assert team_id('TOR') == 141

    def test_al_central(self):
        assert team_id('CWS') == 145
        assert team_id('CLE') == 114
        assert team_id('DET') == 116
        assert team_id('KC') == 118
        assert team_id('MIN') == 142

    def test_al_west(self):
        assert team_id('HOU') == 117
        assert team_id('LAA') == 108
        assert team_id('OAK') == 133
        assert team_id('SEA') == 136
        assert team_id('TEX') == 140

    def test_nl_east(self):
        assert team_id('ATL') == 144
        assert team_id('MIA') == 146
        assert team_id('NYM') == 121
        assert team_id('PHI') == 143
        assert team_id('WSH') == 120

    def test_nl_central(self):
        assert team_id('CHC') == 112
        assert team_id('CIN') == 113
        assert team_id('MIL') == 158
        assert team_id('PIT') == 134
        assert team_id('STL') == 138

    def test_nl_west(self):
        assert team_id('ARI') == 109
        assert team_id('COL') == 115
        assert team_id('LAD') == 119
        assert team_id('SD') == 135
        assert team_id('SF') == 137
