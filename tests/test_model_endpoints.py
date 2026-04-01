"""Tests for new object classes: conference, season, venue, draft, stats,
homerunderby, attendance, awards, jobs, transactions."""
import pytest

from mlbapi.models.conference import Conference, Conferences
from mlbapi.models.season import Season, Seasons
from mlbapi.models.venue import Venue, Venues
from mlbapi.models.draft import Draft
from mlbapi.models.stats import Stats, StatsLeaders
from mlbapi.models.homerunderby import HomeRunDerby
from mlbapi.models.attendance import Attendance
from mlbapi.models.awards import Award, Awards
from mlbapi.models.jobs import Job, Jobs
from mlbapi.models.transactions import Transaction, Transactions


CONFERENCES_DATA = {
    'conferences': [
        {'id': 203, 'name': 'American League', 'link': '/api/v1/conferences/203'}
    ]
}

SEASONS_DATA = {
    'seasons': [
        {
            'seasonId': '2023',
            'hasWildcard': True,
            'seasonStartDate': '2023-03-30',
            'seasonEndDate': '2023-11-04',
        }
    ]
}

VENUES_DATA = {
    'venues': [
        {'id': 3313, 'name': 'Yankee Stadium', 'link': '/api/v1/venues/3313'}
    ]
}

DRAFT_DATA = {
    'drafts': {
        'draftYear': 2023,
        'rounds': [{'round': '1', 'picks': []}],
    }
}

STATS_DATA = {
    'stats': [
        {
            'type': {'displayName': 'season'},
            'group': {'displayName': 'hitting'},
            'splits': [],
        }
    ]
}

LEADERS_DATA = {
    'leagueLeaders': [
        {'leaderCategory': 'homeRuns', 'season': '2023', 'leaders': []}
    ]
}

HRD_DATA = {
    'gameId': 12345,
    'state': 'final',
}

ATTENDANCE_DATA = {
    'records': [{'year': '2023', 'attendanceTotal': 2500000}],
    'aggregateTotals': {'attendanceTotal': 2500000},
}

AWARDS_DATA = {
    'awards': [
        {'id': 'MLBHOF', 'name': 'Baseball Hall of Fame'}
    ]
}

JOBS_DATA = {
    'roster': [
        {'position': {'code': 'UMP'}, 'person': {'id': 427151, 'fullName': 'Joe Umpire'}}
    ]
}

TRANSACTIONS_DATA = {
    'transactions': [
        {
            'id': 123456,
            'typeCode': 'SC',
            'typeDesc': 'Signed Contract',
            'person': {'id': 592450, 'fullName': 'Aaron Judge'},
        }
    ]
}


class TestConferences:
    def test_creates_from_data(self):
        c = Conferences(CONFERENCES_DATA)
        assert hasattr(c, 'conferences')

    def test_conferences_is_list(self):
        c = Conferences(CONFERENCES_DATA)
        assert isinstance(c.conferences, list)
        assert len(c.conferences) == 1

    def test_conference_has_name(self):
        c = Conferences(CONFERENCES_DATA)
        assert c.conferences[0].name == 'American League'

    def test_conference_has_id(self):
        c = Conferences(CONFERENCES_DATA)
        assert c.conferences[0].id == 203


class TestSeasons:
    def test_creates_from_data(self):
        s = Seasons(SEASONS_DATA)
        assert hasattr(s, 'seasons')

    def test_seasons_is_list(self):
        s = Seasons(SEASONS_DATA)
        assert isinstance(s.seasons, list)
        assert len(s.seasons) == 1

    def test_season_has_id(self):
        # The MLB API returns seasonId as a string; Pydantic stores it as-is.
        s = Seasons(SEASONS_DATA)
        assert s.seasons[0].season_id == '2023'

    def test_season_has_wildcard(self):
        s = Seasons(SEASONS_DATA)
        assert s.seasons[0].has_wildcard is True


class TestVenues:
    def test_creates_from_data(self):
        v = Venues(VENUES_DATA)
        assert hasattr(v, 'venues')

    def test_venues_is_list(self):
        v = Venues(VENUES_DATA)
        assert isinstance(v.venues, list)
        assert len(v.venues) == 1

    def test_venue_has_name(self):
        v = Venues(VENUES_DATA)
        assert v.venues[0].name == 'Yankee Stadium'

    def test_venue_has_id(self):
        v = Venues(VENUES_DATA)
        assert v.venues[0].id == 3313


class TestDraft:
    def test_creates_from_data(self):
        d = Draft(DRAFT_DATA)
        assert hasattr(d, 'drafts')

    def test_drafts_contains_data(self):
        d = Draft(DRAFT_DATA)
        assert d.drafts['draftYear'] == 2023


class TestStats:
    def test_creates_from_data(self):
        s = Stats(STATS_DATA)
        assert hasattr(s, 'stats')

    def test_stats_contains_data(self):
        s = Stats(STATS_DATA)
        assert isinstance(s.stats, list)
        assert len(s.stats) == 1


class TestStatsLeaders:
    def test_creates_from_data(self):
        sl = StatsLeaders(LEADERS_DATA)
        assert hasattr(sl, 'league_leaders')

    def test_league_leaders_contains_data(self):
        sl = StatsLeaders(LEADERS_DATA)
        assert isinstance(sl.league_leaders, list)
        assert len(sl.league_leaders) == 1


class TestHomeRunDerby:
    def test_creates_from_data(self):
        h = HomeRunDerby(HRD_DATA)
        assert hasattr(h, 'game_id')

    def test_game_id(self):
        h = HomeRunDerby(HRD_DATA)
        assert h.game_id == 12345

    def test_state(self):
        h = HomeRunDerby(HRD_DATA)
        assert h.state == 'final'


class TestAttendance:
    def test_creates_from_data(self):
        a = Attendance(ATTENDANCE_DATA)
        assert hasattr(a, 'records')

    def test_records_is_list(self):
        a = Attendance(ATTENDANCE_DATA)
        assert isinstance(a.records, list)

    def test_aggregate_totals(self):
        a = Attendance(ATTENDANCE_DATA)
        assert hasattr(a, 'aggregate_totals')


class TestAwards:
    def test_creates_from_data(self):
        a = Awards(AWARDS_DATA)
        assert hasattr(a, 'awards')

    def test_awards_is_list(self):
        a = Awards(AWARDS_DATA)
        assert isinstance(a.awards, list)
        assert len(a.awards) == 1

    def test_award_has_name(self):
        a = Awards(AWARDS_DATA)
        assert a.awards[0].name == 'Baseball Hall of Fame'

    def test_award_has_id(self):
        a = Awards(AWARDS_DATA)
        assert a.awards[0].id == 'MLBHOF'


class TestJobs:
    def test_creates_from_data(self):
        j = Jobs(JOBS_DATA)
        assert hasattr(j, 'roster')

    def test_roster_is_list(self):
        j = Jobs(JOBS_DATA)
        assert isinstance(j.roster, list)
        assert len(j.roster) == 1


class TestTransactions:
    def test_creates_from_data(self):
        t = Transactions(TRANSACTIONS_DATA)
        assert hasattr(t, 'transactions')

    def test_transactions_is_list(self):
        t = Transactions(TRANSACTIONS_DATA)
        assert isinstance(t.transactions, list)
        assert len(t.transactions) == 1

    def test_transaction_has_type(self):
        t = Transactions(TRANSACTIONS_DATA)
        assert t.transactions[0].type_code == 'SC'
