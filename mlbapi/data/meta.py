#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the meta/lookup API endpoints.

These endpoints return valid values for parameters used in other API calls.
Each meta_type maps to ``GET /api/v1/{meta_type}``.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import requests

import mlbapi.exceptions

BASE_URL = 'https://statsapi.mlb.com/api/v1'
_HEADERS = {'User-Agent': 'mlbapi', 'Accept-encoding': 'gzip'}

VALID_META_TYPES = [
    'awards',
    'baseballStats',
    'eventTypes',
    'fielderStatuses',
    'gameStatus',
    'gameTypes',
    'hitTrajectories',
    'jobTypes',
    'languages',
    'leagueLeaderTypes',
    'logicalEvents',
    'metrics',
    'pitchCodes',
    'pitchTypes',
    'platforms',
    'positions',
    'reviewReasons',
    'rosterTypes',
    'scheduleEventTypes',
    'sitCodes',
    'situationCodes',
    'sky',
    'standingsTypes',
    'statGroups',
    'statTypes',
    'transactionTypes',
    'windDirection',
]


def get_meta(meta_type: str) -> dict:
    """Return lookup-table data for *meta_type* (``GET /api/v1/{meta_type}``).

    Args:
        meta_type (str): One of the strings in ``VALID_META_TYPES``,
            e.g. ``'gameTypes'``, ``'statGroups'``.

    Returns:
        dict or list — the raw parsed JSON response.

    Raises:
        mlbapi.exceptions.ParameterException: if meta_type is not recognised.
    """
    if meta_type not in VALID_META_TYPES:
        raise mlbapi.exceptions.ParameterException(
            f'Invalid meta_type {meta_type!r}. '
            f'Valid types: {VALID_META_TYPES}'
        )
    resp = requests.get(
        f'{BASE_URL}/{meta_type}',
        headers=_HEADERS,
        timeout=10,
    )
    return resp.json()
