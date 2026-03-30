#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the venues API endpoints.

This module's functions get the JSON payloads for the mlb.com venues API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_VENUE_PARAMS = ['venue_ids', 'season', 'hydrate', 'fields']


def get_venues(**kwargs):
    """This endpoint allows you to pull venue information.

    params:
      venueIds <venue_ids>
        Description: Comma delimited list of Unique venue identifiers.
        Parameter Type: query
        Data Type: array[integer]
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
    check_kwargs(kwargs.keys(), VALID_VENUE_PARAMS, mlbapi.exceptions.ParameterException)
    if 'venue_ids' in kwargs:
        if isinstance(kwargs['venue_ids'], list):
            try:
                kwargs['venue_ids'] = ','.join(str(int(v)) for v in kwargs['venue_ids'])
            except ValueError as error:
                raise mlbapi.exceptions.ParameterException(error)
        else:
            raise mlbapi.exceptions.ParameterException(
                'venue_ids must be a list of venue IDs as Integers or Strings.')
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.VENUE, **kwargs)
