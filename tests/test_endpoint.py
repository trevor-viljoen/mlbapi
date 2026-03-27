"""Tests for mlbapi.endpoint constants."""
import mlbapi.endpoint


def test_game_endpoint():
    assert mlbapi.endpoint.GAME == 'game'


def test_schedule_endpoint():
    assert mlbapi.endpoint.SCHEDULE == 'schedule'


def test_standings_endpoint():
    assert mlbapi.endpoint.STANDINGS == 'standings'


def test_team_endpoint():
    assert mlbapi.endpoint.TEAM == 'teams'


def test_division_endpoint():
    assert mlbapi.endpoint.DIVISION == 'divisions'


def test_people_endpoint():
    assert mlbapi.endpoint.PEOPLE == 'people'


def test_sports_endpoint():
    assert mlbapi.endpoint.SPORTS == 'sports'


def test_league_endpoint():
    assert mlbapi.endpoint.LEAGUE == 'league'


# Corrected endpoint paths (previously wrong)
def test_conference_endpoint_is_plural():
    assert mlbapi.endpoint.CONFERENCE == 'conferences'


def test_homerunderby_endpoint_is_camel_case():
    assert mlbapi.endpoint.HOMERUNDERBY == 'homeRunDerby'


def test_venue_endpoint_is_plural():
    assert mlbapi.endpoint.VENUE == 'venues'


def test_season_endpoint_path():
    assert mlbapi.endpoint.SEASON == 'seasons'


# New endpoints
def test_attendance_endpoint():
    assert mlbapi.endpoint.ATTENDANCE == 'attendance'


def test_awards_endpoint():
    assert mlbapi.endpoint.AWARDS == 'awards'


def test_jobs_endpoint():
    assert mlbapi.endpoint.JOBS == 'jobs'


def test_meta_endpoint():
    assert mlbapi.endpoint.META == 'meta'


def test_transactions_endpoint():
    assert mlbapi.endpoint.TRANSACTIONS == 'transactions'


def test_all_endpoints_are_strings():
    attrs = ['ATTENDANCE', 'AWARDS', 'CONFERENCE', 'CONFIG', 'DIVISION',
             'DRAFT', 'GAME', 'GAME_PACE', 'HIGH_LOW', 'HOMERUNDERBY',
             'JOBS', 'LEAGUE', 'META', 'PEOPLE', 'SCHEDULE', 'SEASON',
             'SPORTS', 'STANDINGS', 'STATS', 'TEAM', 'TRANSACTIONS', 'VENUE']
    for attr in attrs:
        assert isinstance(getattr(mlbapi.endpoint, attr), str), \
            f'{attr} should be a string'
