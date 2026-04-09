#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the people API endpoints.

This module's functions get the JSON payloads for the mlb.com people API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


# ---------------------------------------------------------------------------
# Canonical parameter lists for all people/person endpoints
# ---------------------------------------------------------------------------

VALID_PEOPLE_PARAMS = [
    'person_ids', 'season', 'sport_id', 'group', 'hydrate', 'fields',
]
"""Parameters accepted by :func:`get_people` (``GET /api/v1/people``)."""

VALID_PERSON_PARAMS = [
    'person_id', 'person_ids', 'season', 'group', 'fields',
]
"""Parameters accepted by :func:`get_person` (``GET /api/v1/people/{id}``)."""

VALID_PEOPLE_SEARCH_PARAMS = [
    'names', 'sport_id', 'active_status', 'license_type', 'fields',
]
"""Parameters accepted by :func:`search_people`
(``GET /api/v1/people/search``)."""

VALID_PERSON_STATS_PARAMS = [
    'person_id', 'stats', 'group', 'season', 'sport_id',
    'game_type', 'start_date', 'end_date', 'hydrate', 'fields',
]
"""Parameters accepted by person-stats sub-endpoints."""

# Legacy aliases kept for backwards compatibility
VALID_CURRENT_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']
VALID_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _join_fields(kwargs):
    """Convert kwargs['fields'] list to comma-delimited string in-place."""
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def get_people(**kwargs):
    """Return information for one or more players (``GET /api/v1/people``).

    params:
      personIds <person_ids>
        Description: Comma-delimited list of person IDs.
        Parameter Type: query
        Data Type: array[integer]
      season <season>
        Description: Season of play.
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top-level organisation of a sport (MLB is 1).
        Parameter Type: query
        Data Type: integer
      group <group>
        Description: Stat group category.
        Parameter Type: query
        Data Type: string
      hydrate <hydrate>
        Description: Sub-resource name to hydrate the response.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma-delimited list of specific fields to return.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_PEOPLE_PARAMS, mlbapi.exceptions.ParameterException)
    if 'person_ids' in kwargs:
        if isinstance(kwargs['person_ids'], list):
            try:
                kwargs['person_ids'] = ','.join(str(int(p)) for p in kwargs['person_ids'])
            except ValueError as exc:
                raise mlbapi.exceptions.ParameterException(exc)
        # scalar values pass through as-is
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, **kwargs)


def get_person(person_id, **kwargs):
    """Return information for a single player (``GET /api/v1/people/{id}``).

    Args:
        person_id (int): Unique Player Identifier.

    params:
      person_ids <person_ids>
        Description: Comma-delimited list of person IDs.
        Parameter Type: query
        Data Type: array[integer]
      season <season>
        Description: Season of play.
        Parameter Type: query
        Data Type: string
      group <group>
        Description: Stat group category.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma-delimited list of specific fields to return.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_PERSON_PARAMS, mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, primary_key=person_id,
                   valid_params=VALID_PERSON_PARAMS, **kwargs)


def search_people(**kwargs):
    """Search for players by name (``GET /api/v1/people/search``).

    params:
      names <names>
        Description: Player name search string.
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top-level organisation of a sport (MLB is 1).
        Parameter Type: query
        Data Type: integer
      activeStatus <active_status>
        Description: Whether to return active, inactive, or all players.
          Valid values: ``Y``, ``N``, ``B`` (both).
        Parameter Type: query
        Data Type: string
      licenseType <license_type>
        Description: License type filter.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma-delimited list of specific fields to return.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_PEOPLE_SEARCH_PARAMS, mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, context='search', **kwargs)


def get_current_game_stats(person_id, **kwargs):
    """Return current-game stats for a player.

    Args:
        person_id (int): Unique Player Identifier.

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_CURRENT_GAME_STATS_PARAMS,
                 mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, 'stats/game/current', primary_key=person_id,
                   valid_params=VALID_CURRENT_GAME_STATS_PARAMS, **kwargs)


def get_game_stats(person_id, game_pk, **kwargs):
    """Return game stats for a specific player and game.

    Args:
        person_id (int): Unique Player Identifier.
        game_pk (int): Unique Primary Key representing a game.

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_GAME_STATS_PARAMS,
                 mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, 'stats/game', primary_key=person_id,
                   secondary_key=game_pk, valid_params=VALID_GAME_STATS_PARAMS,
                   **kwargs)
