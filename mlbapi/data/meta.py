#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the meta/lookup API endpoints.

This module's functions get the JSON payloads for the mlb.com meta (lookup
table) API endpoints. These endpoints return valid values for parameters used
in other API calls.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import mlbapi.exceptions
from mlbapi.data import request


VALID_META_TYPES = [
    'gameTypes',
    'gameStatus',
    'standingsTypes',
    'statGroups',
    'statTypes',
    'pitchTypes',
    'hitTrajectories',
    'fielderStatuses',
    'positions',
    'eventTypes',
    'metrics',
    'windDirection',
    'sky',
    'pitchCodes',
    'languages',
    'leagueLeaderTypes',
    'rosterTypes',
    'scheduleEventTypes',
    'situationCodes',
    'transactionTypes',
]


def get_meta(meta_type):
    """This endpoint allows you to pull lookup table data (meta) for
    valid parameter values used in other API calls.

    The meta_type IS the endpoint path segment, so the URL produced is
    ``/api/v1/{meta_type}``.

    Args:
        meta_type (str): The lookup table type.  Must be one of the strings in
            ``VALID_META_TYPES`` (e.g. ``'gameTypes'``, ``'statGroups'``).

    Returns:
        json (list or dict)

    Raises:
        mlbapi.exceptions.ParameterException: if meta_type is not recognised.
    """
    if meta_type not in VALID_META_TYPES:
        raise mlbapi.exceptions.ParameterException(
            '{} is not a valid meta type. Valid types: {}'.format(
                meta_type, ', '.join(VALID_META_TYPES)
            )
        )
    return request(meta_type)
