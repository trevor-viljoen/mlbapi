#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the Home Run Derby API endpoints.

This module's functions get the JSON payloads for the mlb.com Home Run Derby
API endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_HOMERUNDERBY_PARAMS = ['fields']


def get_homerunderby(game_pk, **kwargs):
    """This endpoint allows you to pull Home Run Derby data for a game.

    Args:
        game_pk (int): Unique primary key for the Home Run Derby game.

    params:
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_HOMERUNDERBY_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.HOMERUNDERBY, primary_key=game_pk, **kwargs)


def get_homerunderby_bracket(game_pk, **kwargs):
    """This endpoint allows you to pull Home Run Derby bracket data.

    Args:
        game_pk (int): Unique primary key for the Home Run Derby game.

    params:
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_HOMERUNDERBY_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.HOMERUNDERBY, primary_key=game_pk, context='bracket', **kwargs)


def get_homerunderby_pool(game_pk, **kwargs):
    """This endpoint allows you to pull Home Run Derby pool data.

    Args:
        game_pk (int): Unique primary key for the Home Run Derby game.

    params:
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_HOMERUNDERBY_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.HOMERUNDERBY, primary_key=game_pk, context='pool', **kwargs)
