# -*- coding: utf-8 -*-
#
# mlbapi — Python 3 wrapper for the MLB StatsAPI at statsapi.mlb.com
#
# Trevor Viljoen <trevor.viljoen@gmail.com>
#

from mlbapi import exceptions
from mlbapi import version
from mlbapi.client import Client

# ---------------------------------------------------------------------------
# Default client — used by every module-level convenience function below.
# Replace or configure by instantiating your own: mlbapi.Client(timeout=30)
# ---------------------------------------------------------------------------
_default = Client()

# ---------------------------------------------------------------------------
# Public API — each function delegates to the default client.
# For full control (custom timeout, session, base URL) use Client directly.
# ---------------------------------------------------------------------------

def linescore(game_pk, **kwargs):       return _default.linescore(game_pk, **kwargs)
def play_by_play(game_pk, **kwargs):    return _default.play_by_play(game_pk, **kwargs)
def boxscore(game_pk, **kwargs):        return _default.boxscore(game_pk, **kwargs)
def live_diff(game_pk, **kwargs):       return _default.live_diff(game_pk, **kwargs)
def schedule(**kwargs):                 return _default.schedule(**kwargs)
def standings(**kwargs):                return _default.standings(**kwargs)
def teams(**kwargs):                    return _default.teams(**kwargs)
def divisions(**kwargs):                return _default.divisions(**kwargs)
def conferences(**kwargs):              return _default.conferences(**kwargs)
def seasons(**kwargs):                  return _default.seasons(**kwargs)
def all_seasons(**kwargs):              return _default.all_seasons(**kwargs)
def venues(**kwargs):                   return _default.venues(**kwargs)
def draft(year, **kwargs):              return _default.draft(year, **kwargs)
def draft_prospects(**kwargs):          return _default.draft_prospects(**kwargs)
def draft_latest(year, **kwargs):       return _default.draft_latest(year, **kwargs)
def stats(**kwargs):                    return _default.stats(**kwargs)
def stats_leaders(**kwargs):            return _default.stats_leaders(**kwargs)
def stats_streaks(**kwargs):            return _default.stats_streaks(**kwargs)
def homerunderby(game_pk, **kwargs):    return _default.homerunderby(game_pk, **kwargs)
def homerunderby_bracket(game_pk, **kwargs): return _default.homerunderby_bracket(game_pk, **kwargs)
def homerunderby_pool(game_pk, **kwargs):    return _default.homerunderby_pool(game_pk, **kwargs)
def attendance(**kwargs):               return _default.attendance(**kwargs)
def awards(**kwargs):                   return _default.awards(**kwargs)
def award_recipients(award_id, **kwargs): return _default.award_recipients(award_id, **kwargs)
def jobs(**kwargs):                     return _default.jobs(**kwargs)
def umpires(**kwargs):                  return _default.umpires(**kwargs)
def datacasters(**kwargs):              return _default.datacasters(**kwargs)
def official_scorers(**kwargs):         return _default.official_scorers(**kwargs)
def transactions(**kwargs):             return _default.transactions(**kwargs)
def meta(meta_type):                    return _default.meta(meta_type)


__title__   = 'mlbapi'
__license__ = 'MIT'
__author__  = 'Trevor Viljoen'
__contact__ = 'trevor.viljoen@gmail.com'
__url__     = 'https://github.com/trevor-viljoen/mlbapi'
__version__ = version.__version__
__all__ = [
    'Client',
    '__version__',
    'linescore', 'play_by_play', 'boxscore', 'live_diff',
    'schedule', 'standings', 'teams', 'divisions', 'conferences',
    'seasons', 'all_seasons', 'venues',
    'draft', 'draft_prospects', 'draft_latest',
    'stats', 'stats_leaders', 'stats_streaks',
    'homerunderby', 'homerunderby_bracket', 'homerunderby_pool',
    'attendance', 'awards', 'award_recipients',
    'jobs', 'umpires', 'datacasters', 'official_scorers',
    'transactions', 'meta',
]
