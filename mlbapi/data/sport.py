#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the sports API endpoints.

This module's functions gets the JSON payloads for the mlb.com sports API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_SPORTS_PARAMS = ['sport_id', 'fields']


def get_sports(**kwargs):
    """This endpoint allows you to pull sports.
    params:
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: path
        Data Type: Optional integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json array
    """
    check_kwargs(kwargs.keys(), VALID_SPORTS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'sport_id' in kwargs:
        if not isinstance(kwargs['sport_id'], int) and not isinstance(kwargs['sport_id'], str):
            error = 'sport_id must be an Integer or a String.'
            raise mlbapi.exceptions.ParameterException(error)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            error = 'fields must be a list of strings.'
            raise mlbapi.exceptions.ParameterException(error)
        kwargs['fields'] = ','.join(kwargs['fields'])

    return request(endpoint.SPORTS, **kwargs)
