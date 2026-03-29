#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the awards API endpoints.

This module's functions get the JSON payloads for the mlb.com awards API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_AWARDS_PARAMS = ['sport_id', 'league_id', 'season', 'hydrate', 'fields']


def get_awards(**kwargs):
    """This endpoint allows you to pull awards.

    params:
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
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
      hydrate <hydrate>
        Description: Insert name of sub-resource to hydrate the response.
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
    check_kwargs(kwargs.keys(), VALID_AWARDS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.AWARDS, **kwargs)


def get_award_recipients(award_id, **kwargs):
    """This endpoint allows you to pull award recipients for a specific award.

    Args:
        award_id (str): Unique award identifier (e.g. 'MLBHOF')

    params:
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
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
      hydrate <hydrate>
        Description: Insert name of sub-resource to hydrate the response.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_AWARDS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.AWARDS, primary_key=award_id, context='recipients', **kwargs)
