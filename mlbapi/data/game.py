#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the games API endpoints.

This module's functions gets the JSON payloads for the mlb.com games API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
from mlbapi.data import request
from mlbapi.utils import check_kwargs
from mlbapi.exceptions import ParameterException


VALID_BOXSCORE_PARAMS = ['game_pk', 'timecode', 'fields']
VALID_COLOR_PARAMS = ['game_pk', 'timecode', 'fields']
VALID_COLOR_DIFF_PARAMS = ['game_pk', 'start_timecode', 'end_timecode']
VALID_COLOR_TIMESTAMPS_PARAMS = ['game_pk']
VALID_CONTENT_PARAMS = ['game_pk', 'highlight_limit']
VALID_CONTEXT_METRICS_PARAMS = ['game_pk', 'timecode']
VALID_LINESCORE_PARAMS = ['game_pk', 'timecode', 'fields']
VALID_LIVE_PARAMS = ['game_pk', 'timecode', 'fields']
VALID_LIVE_DIFF_PARAMS = ['game_pk', 'start_timecode', 'end_timecode']
VALID_LIVE_TIMESTAMPS_PARAMS = ['game_pk']
VALID_PLAY_BY_PLAY_PARAMS = ['game_pk', 'timecode', 'fields']
VALID_WIN_PROBABILITY_PARAMS = ['game_pk', 'timecode', 'fields']


def get_boxscore(game_pk, **kwargs):
    """This endpoint allows you to pull the boxscore for a game.
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json
    """
    return request(endpoint.GAME, 'boxscore', primary_key=game_pk,
                   valid_params=VALID_BOXSCORE_PARAMS, **kwargs)

def get_color(game_pk, **kwargs):
    """
    This API can return very large payloads. It is STRONGLY recommended that
    clients ask for diffs and use "Accept-Encoding: gzip" header.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'feed/color', primary_key=game_pk,
                   valid_params=VALID_COLOR_PARAMS, **kwargs)

def get_color_diff(game_pk, **kwargs):
    """
    ?? Not Yet Implemented ??

    This API can return very large payloads. It is STRONGLY recommended that
    clients ask for diffs and use "Accept-Encoding: gzip" header.

    startTimecode and endTimecode can be used for getting diffs.

    Expected usage:
      1) Request full payload by not passing startTimecode or endTimecode. This
         will return the entire color feed up till the current time.
      2) Find the latest timecode in this response.
      3) Wait X seconds
      4) Use the timecode from 2 as the startTimecode. This will give you a
         diff of everything that has happened since startTimecode.
      5) If no data is returned, wait X seconds and do the same request.
      6) If data is returned, get a new timeStamp from the response, and use
         that for the next call as startTimecode.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
      startTimecode
        Description: Start time code will give you everything since that time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      endTimecode
        Description: End time code will give you a snapshot at that specific
            time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
    """
    return request(endpoint.GAME, 'feed/color/diffPatch', primary_key=game_pk,
                   valid_params=VALID_COLOR_DIFF_PARAMS, **kwargs)

def get_color_timestamps(game_pk, **kwargs):
    """
    This can be used for replaying games. endpoint returns all of the timecodes
    that can be used with diffs for mlbapi.data.get_color.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
    """
    return request(endpoint.GAME, 'feed/color/timestamps', primary_key=game_pk,
                   valid_params=VALID_COLOR_TIMESTAMPS_PARAMS, **kwargs)

def get_content(game_pk, **kwargs):
    """
    Retrieve game content such as highlights.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      highlightLimit:
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
    """
    return request(endpoint.GAME, 'content', primary_key=game_pk,
                   valid_params=VALID_CONTENT_PARAMS, **kwargs)

def get_context_metrics(game_pk, **kwargs):
    """
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'contextMetrics', primary_key=game_pk,
                   valid_params=VALID_CONTEXT_METRICS_PARAMS, **kwargs)

def get_linescore(game_pk, **kwargs):
    """
    This endpoint allows you to pull the linescore for a game.
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'linescore', primary_key=game_pk,
                   valid_params=VALID_LINESCORE_PARAMS, **kwargs)

def get_live(game_pk, **kwargs):
    """
    This API can return very large payloads. It is STRONGLY recommended that
    clients ask for diffs and use "Accept-Encoding: gzip" header.
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'feed/live', primary_key=game_pk,
                   valid_params=VALID_LIVE_PARAMS, **kwargs)

def get_live_diff(game_pk, **kwargs):
    """
    ?? Not Yet Implemented ??

    This endpoint allows comparison of game files and shows any differences or
    discrepancies between the two.

    Diff/Patch System: startTimecode and endTimecode can be used for getting diffs.

    Expected usage:
      1) Request full payload by not passing startTimecode or endTimecode. This
         will return the most recent game state.
      2) Find the latest timecode in this response.
      3) Wait X seconds
      4) Use the timecode from 2 as the startTimecode. This will give you a
         diff of everything that has happened since startTimecode.
      5) If no data is returned, wait X seconds and do the same request.
      6) If data is returned, get a new timeStamp from the response, and use
         that for the next call as startTimecode.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
      startTimecode
        Description: Start time code will give you everything since that time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      endTimecode
        Description: End time code will give you a snapshot at that specific
            time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
    """
    return request(endpoint.GAME, 'feed/live/diffPatch', primary_key=game_pk,
                   valid_params=VALID_LIVE_DIFF_PARAMS, **kwargs)

def get_live_timestamps(game_pk, **kwargs):
    """
    This can be used for replaying games. endpoint returns all of the timecodes
    that can be used with diffs for mlbapi.game.live_diff.

    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: string
    """
    return request(endpoint.GAME, 'feed/live/timestamps', primary_key=game_pk,
                   valid_params=VALID_LIVE_TIMESTAMPS_PARAMS, **kwargs)

def get_play_by_play(game_pk, **kwargs):
    """This endpoint allows you to pull the play by play for a game.
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      timecode
        Description: Use this parameter to return a snapshot of the data at
            the specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'playByPlay', primary_key=game_pk,
                   valid_params=VALID_PLAY_BY_PLAY_PARAMS, **kwargs)

def get_win_probability(game_pk, **kwargs):
    """
    params:
      game_pk (required)
        Description: Unique Primary Key Representing a Game
        Parameter Type: path
        Data Type: integer? #string elsewhere in documentation
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
        Parameter Type: query
        Data Type: string
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]
    """
    return request(endpoint.GAME, 'winProbability', primary_key=game_pk,
                   valid_params=VALID_WIN_PROBABILITY_PARAMS, **kwargs)
