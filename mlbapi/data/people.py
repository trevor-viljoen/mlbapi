#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the people API endpoints.

This module's functions gets the JSON payloads for the mlb.com games API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
from mlbapi.data import request


VALID_PERSON_PARAMS = ['person_id', 'person_ids', 'season', 'group', 'fields']
VALID_CURRENT_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']
VALID_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']

def get_person(person_id, **kwargs):
    """This endpoint allows you to pull the information for a player.
    Args:
        person_id (int): Unique Player Identifier
        params (dict): Contains the person_ids, season, group, and fields
            parameters described below.

    params:
      person_id (required)
        Description: Unique Player Identifier
        Parameter Type: path
        Data Type: integer
      person_ids
        Description: Comma delimited list of person ID.
        Format: 1234, 2345
        Parameter Type: query
        Data Type: array[integer]
      season
        Description: Season of play
        Parameter Type: query
        Data Type: string
      group *may not yet do anything
        Description: Category of statistics to return. 0: hitting, 1: pitching,
            2: fielding, 3: running
        Format: 0, 1, 2, 3
        Parameter Type: query
        Data Type: array[string]
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json
    """
    return request(endpoint.PEOPLE, primary_key=person_id,
                   valid_params=VALID_PERSON_PARAMS, **kwargs)

def get_current_game_stats(person_id, **kwargs):
    """This endpoint allows you to pull the current game status for a given
    player.
    Args:
        person_id (int): Unique Player Identifier
        params (dict): Contains the person_ids, season, group, and fields
            parameters described below.

    params:
      person_id (required)
        Description: Unique Player Identifier
        Parameter Type: path
        Data Type: integer
      group *may not yet do anything
        Description: Category of statistics to return. 0: hitting, 1: pitching,
            2: fielding, 3: running
        Format: 0, 1, 2, 3
        Parameter Type: query
        Data Type: array[string]
      timecode
        Description: Use this parameter to return a snapshot of the data at the
            specified time.
        Format: YYYYMMDD_HHMMSS
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json
    """
    return request(endpoint.PEOPLE, 'stats/game/current', primary_key=person_id,
                   valid_params=VALID_CURRENT_GAME_STATS_PARAMS, **kwargs)

def get_game_stats(person_id, game_pk, **kwargs):
    """This endpoint allows you to pull the game stats for a given player and
    game.
    Args:
        person_id (int): Unique Player Identifier
        game_pk (int): Unique Primary Key representing a game.
        params (dict): Contains the group, and fields parameters described
            below.

    params:
      person_id (required)
        Description: Unique Player Identifier
        Parameter Type: path
        Data Type: integer
      game_pk (required)
        Description: Unique Primary Key representing a game.
        Parameter Type: path
        Data Type: integer
      group *may not yet do anything
        Description: Category of statistics to return. 0: hitting, 1: pitching,
            2: fielding, 3: running
        Format: 0, 1, 2, 3
        Parameter Type: query
        Data Type: array[string]
      fields
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json
    """
    return request(endpoint.PEOPLE, 'stats/game', primary_key=person_id,
                   secondary_key=game_pk, valid_params=VALID_GAME_STATS_PARAMS,
                   **kwargs)
