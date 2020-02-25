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
import mlbapi.exceptions

VALID_SCHEDULE_PARAMS = ['calendar_types', 'team_id', 'league_id', 'sport_id',
                         'game_pk', 'game_pks', 'event_ids', 'venue_ids',
                         'performer_ids', 'game_type', 'game_types', 'season',
                         'seasons', 'date', 'start_date', 'end_date', 'timecode',
                         'use_latest_games', 'opponent_id', 'fields']

def get_schedule(**kwargs): # pylint: disable=too-many-branches
    """This endpoint allows you to pull shedules. The API parameter is camel cased. The
    python equivalent is passed in as a python variable, identified in the < >.

    Args:
        calendar_types (list[int]): Comma delimitd list of type of events
        team_id (list[int]): Unique Team Identifier. Format: 141, 147, etc.
        league_id (list[int]): Unique League Identifier
        sport_id (list[int]): Top level organization of a sport.
                              Format: SportId is 1 for MLB
        game_pk (int): Unique Primary Key representing a game
        game_pks (list[int]): List of unique primary keys
        event_ids (list[int]): A unique identifier for non-game event
        venue_ids (list[int]): Unique Venue Identifier
        performer_ids (list[int]): A unique identifier for non-team event
                                   performers
        game_type (str): Type of Game. Available types in api/v1/gameTypes
        game_types (list[str]): List of type of Game.
        season (str): Season of play
        seasons (list[str]): List of seasons of play
        date (str): Date of Game. Format: MM/DD/YYYY
        start_date (str): Start date for range of data. Must be used with
                          end date. Format: MM/DD/YYYY
        end_date (str): End date for range of data. Must be used with start
                        date. Format: MM/DD/YYYY
        timecode (str): Use this parameter to return a snapshot of the data at
                        the specified time. Format: YYYYMMDD_HHMMSS
        use_latest_games (bool): No description provided
        opponent_id (int): A unique identifier for the opposing team. Must be
                           used with teamId.
        fields (list[str]): List of specific fields to be returned.
                            Format: topLevelNode, childNode, attribute
    """
    if 'start_date' in kwargs.keys():
        if 'end_date' not in kwargs.keys():
            error = 'Query contains start_date with no end_date.'
            raise mlbapi.exceptions.ParameterException(error)
    elif 'end_date' in kwargs.keys():
        if 'start_date' not in kwargs.keys():
            error = 'Query contains end_date with no start_date.'
            raise mlbapi.exceptions.ParameterException(error)
    elif 'opponent_id' in kwargs.keys():
        if 'team_id' not in kwargs.keys():
            error = 'Query contains opponentId with no teamId.'
            raise mlbapi.exceptions.ParameterException(error)
    elif 'seasons' in kwargs.keys(): # Make sure seasons is a comma delimited list
        if isinstance(kwargs['seasons'], list):
            temp = []
            for season in kwargs['seasons']:
                if not isinstance(season, int):
                    try:
                        temp.append(int(season))
                    except ValueError as error:
                        raise mlbapi.exceptions.ParameterException(error)
            if temp:
                kwargs['seasons'] = ','.join(temp)
            else:
                kwargs['seasons'] = ','.join(kwargs['seasons'])
        else:
            error = 'seasons must be a list of years as Integers or Strings.'
            raise mlbapi.exceptions.ParameterException(error)
    elif 'sport_id' not in kwargs.keys():
        kwargs['sport_id'] = 1
    return request(endpoint.SCHEDULE, valid_params=VALID_SCHEDULE_PARAMS, **kwargs)
