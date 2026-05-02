#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the games API endpoints.

This module's functions gets the JSON payloads for the mlb.com games API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs, to_comma_delimited_string


VALID_STANDINGS_PARAMS = ['league_id', 'season', 'standings_types', 'date',
                          'team_id', 'include_mlb', 'expand', 'fields']


def get_standings(standings_type=None, **kwargs):
    """This endpoint allows you to pull standings.
    params:
      standingsType (required) <standings_type>
        Description: Type of season. Available types in /api/v1/standingsTypes
        Parameter Type: path
        Data Type: Optional string
      leagueId <league_id>
        Description: Unique League Identifier
        Parameter Type: query
        Data Type: integer
      season <season>
        Description: Season of play.
        Parameter Type: query
        Data Type: string
      standingsTypes <standings_types>
        Description: Type of season. Available types in /api/v1/standingsTypes
        Parameter Type: query
        Data Type: array[string]
      date <date>
        Description: Date of Game.
        Format: MM/DD/YYYY
        Parameter Type: query
        Data Type: LocalDate/string
      teamId <team_id>
        Description: Unique Team Identifier.
        Format: 141, 147, etc
        Parameter Type: query
        Data Type: integer
      includeMLB <include_mlb>
        Description: Determines whether to include major league teams when using the
          'BY_ORGANIZATION' standings type
        Parameter Type: query
        Data Type: boolean
      expand <expand>
        Description: expand
        Parameter Type: query
        Data Type: array[string]
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns json
    """
    check_kwargs(kwargs.keys(), VALID_STANDINGS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'league_id' in kwargs.keys():
        kwargs['league_id'] = to_comma_delimited_string(kwargs['league_id'], int)
    return request(endpoint.STANDINGS, primary_key=standings_type, **kwargs)
