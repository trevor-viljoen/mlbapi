# -*- coding: utf-8 -*-


#
# mlbapi - A python3 wrapper for the MLB API at statsapi.mlb.com
#
# Trevor Viljoen
# trevor.viljoen@gmail.com
#

from mlbapi import exceptions
from mlbapi import version

from .data.game import get_linescore
from .data.game import get_play_by_play
from .data.game import get_boxscore
from .data.game import get_live_diff
from .data.team import get_teams
from .data.division import get_divisions
from .data.gameday import get_schedule
from .data.standings import get_standings
from .data.conference import get_conferences
from .data.season import get_seasons, get_all_seasons
from .data.venue import get_venues
from .data.draft import get_draft, get_draft_prospects, get_draft_latest
from .data.stats import get_stats, get_stats_leaders, get_stats_streaks
from .data.homerunderby import (get_homerunderby, get_homerunderby_bracket,
                                 get_homerunderby_pool)
from .data.attendance import get_attendance
from .data.awards import get_awards, get_award_recipients
from .data.jobs import get_jobs, get_umpires, get_datacasters, get_official_scorers
from .data.transactions import get_transactions
from .data.meta import get_meta

from .object.game import BoxScore
from .object.game import LineScore
from .object.team import Teams
from .object.division import Divisions
from .object.gameday import Schedule
from .object.standings import Standings
from .object.conference import Conferences
from .object.season import Seasons
from .object.venue import Venues
from .object.draft import Draft
from .object.stats import Stats, StatsLeaders
from .object.homerunderby import HomeRunDerby
from .object.attendance import Attendance
from .object.awards import Awards
from .object.jobs import Jobs
from .object.transactions import Transactions


def linescore(game_pk, **kwargs):
    data = get_linescore(game_pk, **kwargs)
    return LineScore(data)

def play_by_play(game_pk, **kwargs):
    data = get_play_by_play(game_pk, **kwargs)
    return data
    #return mlbapi.game.PlayByPlay(data) # @todo: add objects for PlayByPlay

def schedule(**kwargs):
    data = get_schedule(**kwargs)
    return Schedule(data)

def boxscore(game_pk, **kwargs):
    data = get_boxscore(game_pk, **kwargs)
    return BoxScore(data)

def live_diff(game_pk, **kwargs):
    data = get_live_diff(game_pk, **kwargs)
    return data

def teams(**kwargs):
    data = get_teams(**kwargs)
    return Teams(data)

def divisions(**kwargs):
    data = get_divisions(**kwargs)
    return Divisions(data)

def standings(**kwargs):
    data = get_standings(**kwargs)
    return Standings(data)

def conferences(**kwargs):
    data = get_conferences(**kwargs)
    return Conferences(data)

def seasons(**kwargs):
    data = get_seasons(**kwargs)
    return Seasons(data)

def all_seasons(**kwargs):
    data = get_all_seasons(**kwargs)
    return Seasons(data)

def venues(**kwargs):
    data = get_venues(**kwargs)
    return Venues(data)

def draft(year, **kwargs):
    data = get_draft(year, **kwargs)
    return Draft(data)

def draft_prospects(**kwargs):
    data = get_draft_prospects(**kwargs)
    return Draft(data)

def draft_latest(year, **kwargs):
    data = get_draft_latest(year, **kwargs)
    return Draft(data)

def stats(**kwargs):
    data = get_stats(**kwargs)
    return Stats(data)

def stats_leaders(**kwargs):
    data = get_stats_leaders(**kwargs)
    return StatsLeaders(data)

def stats_streaks(**kwargs):
    data = get_stats_streaks(**kwargs)
    return Stats(data)

def homerunderby(game_pk, **kwargs):
    data = get_homerunderby(game_pk, **kwargs)
    return HomeRunDerby(data)

def homerunderby_bracket(game_pk, **kwargs):
    data = get_homerunderby_bracket(game_pk, **kwargs)
    return HomeRunDerby(data)

def homerunderby_pool(game_pk, **kwargs):
    data = get_homerunderby_pool(game_pk, **kwargs)
    return HomeRunDerby(data)

def attendance(**kwargs):
    data = get_attendance(**kwargs)
    return Attendance(data)

def awards(**kwargs):
    data = get_awards(**kwargs)
    return Awards(data)

def award_recipients(award_id, **kwargs):
    data = get_award_recipients(award_id, **kwargs)
    return Awards(data)

def jobs(**kwargs):
    data = get_jobs(**kwargs)
    return Jobs(data)

def umpires(**kwargs):
    data = get_umpires(**kwargs)
    return Jobs(data)

def datacasters(**kwargs):
    data = get_datacasters(**kwargs)
    return Jobs(data)

def official_scorers(**kwargs):
    data = get_official_scorers(**kwargs)
    return Jobs(data)

def transactions(**kwargs):
    data = get_transactions(**kwargs)
    return Transactions(data)

def meta(meta_type):
    return get_meta(meta_type)


__title__ = 'mlbapi'
__license__ = 'MIT'
__author__ = 'Trevor Viljoen'
__contact__ = 'trevor.viljoen@gmail.com'
__url__ = 'https://github.com/trevor-viljoen/mlbapi'
__all__ = [
    '__version__',
    'standings', 'schedule', 'boxscore', 'linescore', 'teams', 'play_by_play',
    'live_diff', 'divisions', 'conferences', 'seasons', 'all_seasons', 'venues',
    'draft', 'draft_prospects', 'draft_latest', 'stats', 'stats_leaders',
    'stats_streaks', 'homerunderby', 'homerunderby_bracket', 'homerunderby_pool',
    'attendance', 'awards', 'award_recipients', 'jobs', 'umpires', 'datacasters',
    'official_scorers', 'transactions', 'meta',
]
__version__ = version.__version__
