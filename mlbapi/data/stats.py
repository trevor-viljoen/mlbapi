#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the stats API endpoints.

This module's functions get the JSON payloads for the mlb.com stats API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_STATS_PARAMS = [
    'stats', 'player_pool', 'position', 'team_id', 'league_id', 'league_list_id',
    'limit', 'offset', 'group', 'game_type', 'season', 'seasons', 'sport_ids',
    'pitching_team_id', 'opponent_id', 'metric_ids', 'game_pks', 'sitting_split_id',
    'sort_stat', 'order', 'hydrate', 'fields', 'person_id', 'player_id', 'metrics',
    'start_date', 'end_date',
]

VALID_STATS_LEADERS_PARAMS = [
    'leader_categories', 'player_pool', 'leader_game_types', 'stat_group',
    'season', 'league_id', 'sport_id', 'sports_id', 'hydrate', 'limit', 'offset',
    'expand', 'team_id', 'position', 'game_type', 'fields', 'stat_type',
]

VALID_STATS_STREAKS_PARAMS = [
    'streak_type', 'streak_span', 'game_type', 'season', 'sport_id',
    'limit', 'hydrate', 'fields', 'team_id', 'player_pool', 'position', 'stat_group',
]


def get_stats(**kwargs):
    """This endpoint allows you to pull player stats.

    params:
      stats <stats>
        Description: Type of statistics. Available types in /api/v1/statTypes
        Parameter Type: query
        Data Type: array[string]
      playerPool <player_pool>
        Description: Return pro, prospect, or all players
        Parameter Type: query
        Data Type: string
      position <position>
        Description: Position filter
        Parameter Type: query
        Data Type: string
      teamId <team_id>
        Description: Unique team identifier
        Parameter Type: query
        Data Type: integer
      leagueId <league_id>
        Description: Unique league identifier
        Parameter Type: query
        Data Type: integer
      limit <limit>
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
      offset <offset>
        Description: The pointer to start for a return set; used for pagination
        Parameter Type: query
        Data Type: integer
      group <group>
        Description: Category of statistic to return.
        Parameter Type: query
        Data Type: array[string]
      gameType <game_type>
        Description: Type of Game. Available types in /api/v1/gameTypes
        Parameter Type: query
        Data Type: string
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      sportIds <sport_ids>
        Description: Comma delimited list of top level organizations of a sport
        Parameter Type: query
        Data Type: array[integer]
      sortStat <sort_stat>
        Description: Stat to sort results by
        Parameter Type: query
        Data Type: string
      order <order>
        Description: The order of the results (asc or desc)
        Parameter Type: query
        Data Type: string
      hydrate <hydrate>
        Description: Insert name of sub-resource to hydrate the response.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]
      personId <person_id>
        Description: Unique player identifier
        Parameter Type: query
        Data Type: integer
      metrics <metrics>
        Description: Name of metric(s) to return
        Parameter Type: query
        Data Type: array[string]
      startDate <start_date>
        Description: Start date for date range (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string
      endDate <end_date>
        Description: End date for date range (format: MM/DD/YYYY)
        Parameter Type: query
        Data Type: string

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_STATS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.STATS, **kwargs)


def get_stats_leaders(**kwargs):
    """This endpoint allows you to pull stat leaders.

    params:
      leaderCategories <leader_categories>
        Description: Statistic categories to return (required)
        Parameter Type: query
        Data Type: array[string]
      playerPool <player_pool>
        Description: Return pro, prospect, or all players
        Parameter Type: query
        Data Type: string
      leaderGameTypes <leader_game_types>
        Description: Game types to filter by
        Parameter Type: query
        Data Type: array[string]
      statGroup <stat_group>
        Description: Category of statistic to return
        Parameter Type: query
        Data Type: string
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      leagueId <league_id>
        Description: Unique league identifier
        Parameter Type: query
        Data Type: integer
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      hydrate <hydrate>
        Description: Insert name of sub-resource to hydrate the response.
        Parameter Type: query
        Data Type: string
      limit <limit>
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]
      statType <stat_type>
        Description: Type of statistic to return
        Parameter Type: query
        Data Type: string

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_STATS_LEADERS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.STATS, context='leaders', **kwargs)


def get_stats_streaks(**kwargs):
    """This endpoint allows you to pull stat streaks.

    params:
      streakType <streak_type>
        Description: Type of streak to return
        Parameter Type: query
        Data Type: string
      streakSpan <streak_span>
        Description: Span of the streak (season, career, etc.)
        Parameter Type: query
        Data Type: string
      gameType <game_type>
        Description: Type of Game. Available types in /api/v1/gameTypes
        Parameter Type: query
        Data Type: string
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      limit <limit>
        Description: Number of results to return
        Parameter Type: query
        Data Type: integer
      hydrate <hydrate>
        Description: Insert name of sub-resource to hydrate the response.
        Parameter Type: query
        Data Type: string
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_STATS_STREAKS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'fields' in kwargs:
        if not isinstance(kwargs['fields'], list):
            raise mlbapi.exceptions.ParameterException('fields must be a list of strings.')
        kwargs['fields'] = ','.join(kwargs['fields'])
    return request(endpoint.STATS, context='streaks', **kwargs)
