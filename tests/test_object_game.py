"""Tests for mlbapi.object.game classes."""
import pytest

from mlbapi.object.game import (
    BoxScore, LineScore, Inning, Home, Away, Teams, AwayTeam, HomeTeam,
    Defense, Offense, Player, Person, Position, Status, Venue, League,
    Division, Sport, Official, Info, Record, TeamStats, Stats,
    Batting, Pitching, Fielding, Team,
)
from tests.conftest import BOXSCORE_DATA, LINESCORE_DATA


class TestBoxScore:
    def test_creates_from_data(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert hasattr(bs, 'teams')

    def test_teams_has_away_and_home(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert hasattr(bs.teams, 'away')
        assert hasattr(bs.teams, 'home')

    def test_away_team_name(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert bs.teams.away.team.name == 'New York Yankees'

    def test_home_team_name(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert bs.teams.home.team.name == 'Boston Red Sox'

    def test_officials_is_list(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert isinstance(bs.officials, list)
        assert len(bs.officials) == 1

    def test_info_is_list(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert isinstance(bs.info, list)

    def test_pitching_notes_none_when_empty(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert bs.pitching_notes is None

    def test_away_players_list(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert isinstance(bs.teams.away.players, list)
        assert len(bs.teams.away.players) == 1

    def test_away_team_stats(self):
        bs = BoxScore(BOXSCORE_DATA)
        assert hasattr(bs.teams.away, 'team_stats')
        assert hasattr(bs.teams.away.team_stats, 'batting')


class TestLineScore:
    def test_creates_from_data(self):
        ls = LineScore(LINESCORE_DATA)
        assert hasattr(ls, 'innings')

    def test_innings_is_list(self):
        ls = LineScore(LINESCORE_DATA)
        assert isinstance(ls.innings, list)
        assert len(ls.innings) == 2

    def test_inning_has_home_and_away(self):
        ls = LineScore(LINESCORE_DATA)
        inning = ls.innings[0]
        assert hasattr(inning, 'home')
        assert hasattr(inning, 'away')

    def test_teams_has_home_and_away(self):
        ls = LineScore(LINESCORE_DATA)
        assert hasattr(ls.teams, 'home')
        assert hasattr(ls.teams, 'away')

    def test_defense_has_pitcher(self):
        ls = LineScore(LINESCORE_DATA)
        assert hasattr(ls.defense, 'pitcher')

    def test_offense_has_batter(self):
        ls = LineScore(LINESCORE_DATA)
        assert hasattr(ls.offense, 'batter')

    def test_current_inning(self):
        ls = LineScore(LINESCORE_DATA)
        assert ls.current_inning == 9

    def test_balls_strikes_outs(self):
        ls = LineScore(LINESCORE_DATA)
        assert ls.balls == 2
        assert ls.strikes == 1
        assert ls.outs == 2

    def test_offense_base_runners_none(self):
        ls = LineScore(LINESCORE_DATA)
        assert ls.offense.first is None
        assert ls.offense.second is None
        assert ls.offense.third is None


class TestTeams:
    def test_creates_from_dict(self):
        data = {
            'away': {'id': 147, 'name': 'New York Yankees'},
            'home': {'id': 111, 'name': 'Boston Red Sox'},
        }
        t = Teams(data)
        assert hasattr(t, 'away')
        assert hasattr(t, 'home')


class TestDefense:
    def test_creates_pitcher(self):
        data = {'pitcher': {'id': 111, 'fullName': 'Test Pitcher'}}
        d = Defense(data)
        assert hasattr(d, 'pitcher')

    def test_creates_all_positions(self):
        data = {
            'pitcher': {'id': 1},
            'catcher': {'id': 2},
            'first': {'id': 3},
            'second': {'id': 4},
            'third': {'id': 5},
            'shortstop': {'id': 6},
            'left': {'id': 7},
            'center': {'id': 8},
            'right': {'id': 9},
            'team': {'id': 111},
        }
        d = Defense(data)
        for pos in ['pitcher', 'catcher', 'first', 'second', 'third',
                    'shortstop', 'left', 'center', 'right', 'team']:
            assert hasattr(d, pos), f'Defense missing attribute: {pos}'


class TestOffense:
    def test_creates_batter(self):
        data = {
            'batter': {'id': 592450, 'fullName': 'Aaron Judge'},
            'onDeck': {'id': 333},
            'inHole': {'id': 444},
            'pitcher': {'id': 111},
            'first': None,
            'second': None,
            'third': None,
            'team': {'id': 147},
        }
        o = Offense(data)
        assert hasattr(o, 'batter')
        assert o.first is None

    def test_base_runner_set_when_not_none(self):
        data = {
            'batter': {'id': 1},
            'first': {'id': 592450, 'fullName': 'Aaron Judge'},
        }
        o = Offense(data)
        assert o.first is not None


class TestInfo:
    def test_label_and_value(self):
        data = {'label': 'Weather', 'value': 'Sunny'}
        info = Info(data)
        assert info.info == ('Weather', 'Sunny')

    def test_label_only(self):
        data = {'label': 'Weather'}
        info = Info(data)
        assert info.info == 'Weather'


class TestRecord:
    def test_with_league_record(self):
        data = {
            'leagueRecord': {'wins': 30, 'losses': 22, 'ties': 0, 'pct': '.577'},
            'records': {},
        }
        r = Record(data)
        assert hasattr(r, 'league_record')

    def test_records_none_when_empty(self):
        data = {'records': {}}
        r = Record(data)
        # Empty dict is falsy, so records should be None
        assert r.records is None
