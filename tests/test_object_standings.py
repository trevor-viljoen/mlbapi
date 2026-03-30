"""Tests for mlbapi.object.standings classes."""
import pytest

from mlbapi.object.standings import (
    Standings, Record, TeamRecord, Streak, LeagueRecord, Records,
    SplitRecord, DivisionRecord, OverallRecord, ExpectedRecord,
    League, Division, Sport,
)
from tests.conftest import STANDINGS_DATA


class TestStandings:
    def test_creates_from_data(self):
        s = Standings(STANDINGS_DATA)
        assert hasattr(s, 'records')

    def test_records_is_list(self):
        s = Standings(STANDINGS_DATA)
        assert isinstance(s.records, list)
        assert len(s.records) == 1

    def test_json_method_returns_dict(self):
        s = Standings(STANDINGS_DATA)
        result = s.json()
        assert isinstance(result, dict)


class TestRecord:
    def test_creates_from_data(self):
        record_data = STANDINGS_DATA['records'][0]
        r = Record(record_data)
        assert hasattr(r, 'standings_type')

    def test_has_league(self):
        record_data = STANDINGS_DATA['records'][0]
        r = Record(record_data)
        assert hasattr(r, 'league')
        assert isinstance(r.league, League)

    def test_has_division(self):
        record_data = STANDINGS_DATA['records'][0]
        r = Record(record_data)
        assert hasattr(r, 'division')
        assert isinstance(r.division, Division)

    def test_has_sport(self):
        record_data = STANDINGS_DATA['records'][0]
        r = Record(record_data)
        assert hasattr(r, 'sport')
        assert isinstance(r.sport, Sport)

    def test_team_records_is_list(self):
        record_data = STANDINGS_DATA['records'][0]
        r = Record(record_data)
        assert isinstance(r.team_records, list)
        assert len(r.team_records) == 1


class TestTeamRecord:
    def test_creates_from_data(self):
        team_record_data = STANDINGS_DATA['records'][0]['teamRecords'][0]
        tr = TeamRecord(team_record_data)
        assert hasattr(tr, 'team')

    def test_has_streak(self):
        team_record_data = STANDINGS_DATA['records'][0]['teamRecords'][0]
        tr = TeamRecord(team_record_data)
        assert hasattr(tr, 'streak')
        assert isinstance(tr.streak, Streak)

    def test_has_league_record(self):
        team_record_data = STANDINGS_DATA['records'][0]['teamRecords'][0]
        tr = TeamRecord(team_record_data)
        assert hasattr(tr, 'league_record')
        assert isinstance(tr.league_record, LeagueRecord)

    def test_has_records(self):
        team_record_data = STANDINGS_DATA['records'][0]['teamRecords'][0]
        tr = TeamRecord(team_record_data)
        assert hasattr(tr, 'records')
        assert isinstance(tr.records, Records)

    def test_wins_losses(self):
        team_record_data = STANDINGS_DATA['records'][0]['teamRecords'][0]
        tr = TeamRecord(team_record_data)
        assert tr.wins == 30
        assert tr.losses == 22


class TestRecords:
    def test_split_records_is_list(self):
        records_data = STANDINGS_DATA['records'][0]['teamRecords'][0]['records']
        r = Records(records_data)
        assert isinstance(r.split_records, list)
        assert len(r.split_records) == 2

    def test_division_records_is_list(self):
        records_data = STANDINGS_DATA['records'][0]['teamRecords'][0]['records']
        r = Records(records_data)
        assert isinstance(r.division_records, list)

    def test_overall_records_is_list(self):
        records_data = STANDINGS_DATA['records'][0]['teamRecords'][0]['records']
        r = Records(records_data)
        assert isinstance(r.overall_records, list)

    def test_league_records_is_list(self):
        records_data = STANDINGS_DATA['records'][0]['teamRecords'][0]['records']
        r = Records(records_data)
        assert isinstance(r.league_records, list)

    def test_expected_records_is_list(self):
        records_data = STANDINGS_DATA['records'][0]['teamRecords'][0]['records']
        r = Records(records_data)
        assert isinstance(r.expected_records, list)


class TestStreak:
    def test_creates_from_data(self):
        data = {'streakType': 'wins', 'streakNumber': 3, 'streakCode': 'W3'}
        s = Streak(data)
        assert s.streak_type == 'wins'
        assert s.streak_number == 3
        assert s.streak_code == 'W3'
