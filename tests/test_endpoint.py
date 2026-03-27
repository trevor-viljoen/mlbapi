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


def test_all_endpoints_are_strings():
    attrs = ['CONFERENCE', 'CONFIG', 'DIVISION', 'DRAFT', 'GAME',
             'HOMERUNDERBY', 'LEAGUE', 'PEOPLE', 'SCHEDULE', 'SEASON',
             'SPORTS', 'STANDINGS', 'STATS', 'TEAM', 'VENUE']
    for attr in attrs:
        assert isinstance(getattr(mlbapi.endpoint, attr), str), \
            f'{attr} should be a string'
