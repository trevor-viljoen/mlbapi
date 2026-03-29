#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the attendance API endpoints.

This module's functions get the JSON payloads for the mlb.com attendance API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_ATTENDANCE_PARAMS = ['team_id', 'league_id', 'season', 'date',
                            'league_list_id', 'game_type', 'fields']


def get_attendance(**kwargs):
    """This endpoint allows you to pull attendance data.

    params:
      teamId <team_id>
        Description: Unique team identifier
        Parameter Type: query
        Data Type: integer
      leagueId <league_id>
        Description: Unique league identifier
        Parameter Type: query
        Data Type: integer
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      date <date>
        Description: Date of attendance (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      leagueListId <league_list_id>
        Description: Unique league list identifier
        Parameter Type: query
        Data Type: string
      gameType <game_type>
        Description: Type of Game. Available types in /api/v1/gameTypes
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_ATTENDANCE_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.ATTENDANCE, **kwargs)
