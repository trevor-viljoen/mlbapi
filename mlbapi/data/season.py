#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the seasons API endpoints.

This module's functions get the JSON payloads for the mlb.com seasons API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_SEASON_PARAMS = ['season', 'sport_id', 'division_id', 'league_id', 'fields']


def get_seasons(**kwargs):
    """This endpoint allows you to pull season information.

    params:
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      divisionId <division_id>
        Description: Unique division identifier
        Parameter Type: query
        Data Type: integer
      leagueId <league_id>
        Description: Unique league identifier
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_SEASON_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.SEASON, **kwargs)


def get_all_seasons(**kwargs):
    """This endpoint allows you to pull all season information.

    params:
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_SEASON_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.SEASON, context='all', **kwargs)
