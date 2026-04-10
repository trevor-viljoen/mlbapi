#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the people/person API endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs

# ---------------------------------------------------------------------------
# Parameter lists
# ---------------------------------------------------------------------------

VALID_PEOPLE_PARAMS = [
    'person_ids', 'season', 'sport_id', 'hydrate', 'fields', 'accent',
]
"""Accepted by :func:`get_people` (``GET /api/v1/people``)."""

VALID_PERSON_PARAMS = [
    'person_id', 'person_ids', 'season', 'group', 'hydrate', 'fields',
]
"""Accepted by :func:`get_person` (``GET /api/v1/people/{id}``)."""

VALID_PEOPLE_SEARCH_PARAMS = [
    'names', 'sport_id', 'league_id', 'team_id', 'position',
    'active', 'verified', 'accent', 'hydrate', 'fields', 'limit', 'offset',
]
"""Accepted by :func:`search_people` (``GET /api/v1/people/search``)."""

VALID_PERSON_STATS_PARAMS = [
    'person_id', 'stats', 'group', 'season', 'sport_id',
    'game_type', 'start_date', 'end_date', 'hydrate', 'fields',
]
"""Accepted by person-stats sub-endpoints."""

# Legacy aliases
VALID_CURRENT_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']
VALID_GAME_STATS_PARAMS = ['person_id', 'group', 'timecode', 'fields']


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _join_fields(kwargs):
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def get_people(**kwargs):
    """Return one or more players (``GET /api/v1/people``).

    Args:
        person_ids: Comma-delimited list of person IDs (list[int] or str).
        season: Season of play.
        sport_id: Top-level sport organisation (MLB = 1).
        hydrate: Sub-resource name to hydrate.
        fields: List of fields to include in the response.
        accent: Whether to return accented characters (bool).

    Returns:
        dict — raw JSON response.
    """
    check_kwargs(kwargs.keys(), VALID_PEOPLE_PARAMS, mlbapi.exceptions.ParameterException)
    if 'person_ids' in kwargs and isinstance(kwargs['person_ids'], list):
        try:
            kwargs['person_ids'] = ','.join(str(int(p)) for p in kwargs['person_ids'])
        except (ValueError, TypeError) as exc:
            raise mlbapi.exceptions.ParameterException(exc)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, **kwargs)


def get_person(person_id, **kwargs):
    """Return a single player (``GET /api/v1/people/{person_id}``).

    Args:
        person_id (int): Unique player identifier.

    Returns:
        dict — raw JSON response.
    """
    check_kwargs(kwargs.keys(), VALID_PERSON_PARAMS, mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, primary_key=person_id,
                   valid_params=VALID_PERSON_PARAMS, **kwargs)


def search_people(**kwargs):
    """Search for players (``GET /api/v1/people/search``).

    Args:
        names: Player name search string.
        sport_id: Top-level sport organisation (MLB = 1).
        active: Filter by active status.
        fields: List of fields to include.

    Returns:
        dict — raw JSON response.
    """
    check_kwargs(kwargs.keys(), VALID_PEOPLE_SEARCH_PARAMS, mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, context='search', **kwargs)


def get_current_game_stats(person_id, **kwargs):
    """Return current-game stats for a player."""
    check_kwargs(kwargs.keys(), VALID_CURRENT_GAME_STATS_PARAMS,
                 mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, 'stats/game/current', primary_key=person_id,
                   valid_params=VALID_CURRENT_GAME_STATS_PARAMS, **kwargs)


def get_game_stats(person_id, game_pk, **kwargs):
    """Return game stats for a specific player and game."""
    check_kwargs(kwargs.keys(), VALID_GAME_STATS_PARAMS,
                 mlbapi.exceptions.ParameterException)
    _join_fields(kwargs)
    return request(endpoint.PEOPLE, 'stats/game', primary_key=person_id,
                   secondary_key=game_pk, valid_params=VALID_GAME_STATS_PARAMS,
                   **kwargs)
