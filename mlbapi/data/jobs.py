#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the jobs API endpoints.

This module's functions get the JSON payloads for the mlb.com jobs API
endpoints. This includes umpires, datacasters, and official scorers.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_JOBS_PARAMS = ['job_type', 'sport_id', 'date', 'fields']


def get_jobs(**kwargs):
    """This endpoint allows you to pull job information.

    params:
      jobType <job_type>
        Description: Type of job
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      date <date>
        Description: Date (format: MM/DD/YYYY)
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
    check_kwargs(kwargs.keys(), VALID_JOBS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.JOBS, **kwargs)


def get_umpires(**kwargs):
    """This endpoint allows you to pull umpire information.

    params:
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      date <date>
        Description: Date (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_JOBS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.JOBS, context='umpires', **kwargs)


def get_datacasters(**kwargs):
    """This endpoint allows you to pull datacaster information.

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
    check_kwargs(kwargs.keys(), VALID_JOBS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.JOBS, context='datacasters', **kwargs)


def get_official_scorers(**kwargs):
    """This endpoint allows you to pull official scorer information.

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
    check_kwargs(kwargs.keys(), VALID_JOBS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.JOBS, context='officialScorers', **kwargs)
