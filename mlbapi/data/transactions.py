#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the transactions API endpoints.

This module's functions get the JSON payloads for the mlb.com transactions API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_TRANSACTIONS_PARAMS = ['team_id', 'player_id', 'date', 'start_date',
                               'end_date', 'sport_id', 'fields']


def get_transactions(**kwargs):
    """This endpoint allows you to pull transaction data.

    params:
      teamId <team_id>
        Description: Unique team identifier
        Parameter Type: query
        Data Type: integer
      playerId <player_id>
        Description: Unique player identifier
        Parameter Type: query
        Data Type: integer
      date <date>
        Description: Date of transaction (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      startDate <start_date>
        Description: Start date for date range (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      endDate <end_date>
        Description: End date for date range (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
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
    check_kwargs(kwargs.keys(), VALID_TRANSACTIONS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.TRANSACTIONS, **kwargs)
