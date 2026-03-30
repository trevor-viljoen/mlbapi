#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the conferences API endpoints.

This module's functions get the JSON payloads for the mlb.com conferences API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_CONFERENCE_PARAMS = ['conference_id', 'season', 'fields']


def get_conferences(**kwargs):
    """This endpoint allows you to pull conferences.

    params:
      conferenceId <conference_id>
        Description: Unique conference identifier.
        Parameter Type: query
        Data Type: Optional integer
      season <season>
        Description: Season of play
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
    check_kwargs(kwargs.keys(), VALID_CONFERENCE_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.CONFERENCE, **kwargs)
