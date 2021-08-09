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

from .object.game import BoxScore
from .object.game import LineScore
from .object.team import Teams
from .object.division import Divisions
from .object.gameday import Schedule
from .object.standings import Standings

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

__title__ = 'mlbapi'
__license__ = 'MIT'
__author__ = 'Trevor Viljoen'
__contact__ = 'trevor.viljoen@gmail.com'
__url__ = 'https://github.com/trevor-viljoen/mlbapi'
__all__ = [
    '__version__', 'standings', 'schedule', 'boxscore', 'linescore',
    'teams', 'play_by_play', 'live_diff'
]
__version__ = version.__version__
