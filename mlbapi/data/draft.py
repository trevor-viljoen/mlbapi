#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the draft API endpoints.

This module's functions get the JSON payloads for the mlb.com draft API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_DRAFT_PARAMS = ['limit', 'round', 'name', 'school', 'state', 'country',
                      'position', 'team_id', 'player_id', 'bis_player_id', 'fields']


def get_draft(year, **kwargs):
    """This endpoint allows you to pull draft information for a given year.

    Args:
        year (int): The draft year (e.g. 2024)

    params:
      limit <limit>
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
      round <round>
        Description: Draft round
        Parameter Type: query
        Data Type: string
      name <name>
        Description: Player name filter
        Parameter Type: query
        Data Type: string
      school <school>
        Description: School name filter
        Parameter Type: query
        Data Type: string
      state <state>
        Description: State filter
        Parameter Type: query
        Data Type: string
      country <country>
        Description: Country filter
        Parameter Type: query
        Data Type: string
      position <position>
        Description: Position filter
        Parameter Type: query
        Data Type: string
      teamId <team_id>
        Description: Unique team identifier
        Parameter Type: query
        Data Type: integer
      playerId <player_id>
        Description: Unique player identifier
        Parameter Type: query
        Data Type: integer
      bisPlayerId <bis_player_id>
        Description: BIS player identifier
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_DRAFT_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.DRAFT, primary_key=year, **kwargs)


def get_draft_prospects(**kwargs):
    """This endpoint allows you to pull draft prospect information.

    params:
      limit <limit>
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_DRAFT_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.DRAFT, context='prospects', **kwargs)


def get_draft_latest(year, **kwargs):
    """This endpoint allows you to pull the latest draft picks for a given year.

    Args:
        year (int): The draft year (e.g. 2024)

    params:
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_DRAFT_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.DRAFT, primary_key=year, context='latest', **kwargs)
