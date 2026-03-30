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
from mlbapi.utils import check_kwargs


VALID_DIVISION_PARAMS = ['division_id', 'league_id', 'sport_id']


def get_divisions(**kwargs):
    """This endpoint allows you to pull divisions.
    params:
      divisionId <division_id>
        Description: Unique division ID.
        Parameter Type: query
        Data Type: Optional integer
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: Optional integer
      leagueId <league_id>
        Description: Unique league id
        Parameter Type: query
        Data Type: Optional integer

    Returns:
        json array
    """
    check_kwargs(kwargs.keys(), VALID_DIVISION_PARAMS, mlbapi.exceptions.ParameterException)
    for kw_id in kwargs.keys():
        if not isinstance(kwargs[kw_id], int) and not isinstance(kwargs[kw_id], str):
            error = '{} must be an Integer or a String.'.format(kw_id)
            raise mlbapi.exceptions.ParameterException(error)

    return request(endpoint.DIVISION, **kwargs)


