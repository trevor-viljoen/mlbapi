#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi functions for the games API endpoints.

This module's functions gets the JSON payloads for the mlb.com games API
endpoints.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from mlbapi import endpoint
import mlbapi.exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_TEAMS_PARAMS = ['team_id', 'season', 'division_id', 'game_type', 'league_ids',
                      'active_status', 'league_list_id', 'all_star_statuses', 'fields']

VALID_ROSTER_PARAMS = ['season', 'date', 'game_type', 'fields']

VALID_COACHES_PARAMS = ['season', 'date', 'fields']

VALID_TEAM_AFFILIATES_PARAMS = ['season', 'sport_id', 'fields']

VALID_TEAM_ALUMNI_PARAMS = ['season', 'group', 'fields']

VALID_TEAM_HISTORY_PARAMS = ['start_season', 'end_season', 'fields']

VALID_TEAM_LEADERS_PARAMS = ['leader_categories', 'season', 'leader_game_type',
                              'limit', 'stat_group', 'fields']

VALID_TEAM_STATS_PARAMS = ['stats', 'group', 'season', 'game_type',
                           'start_date', 'end_date', 'fields']

VALID_TEAMS_AFFILIATES_PARAMS = ['team_ids', 'season', 'sport_id', 'fields']

VALID_TEAMS_HISTORY_PARAMS = ['team_ids', 'start_season', 'end_season', 'fields']

VALID_TEAMS_STATS_PARAMS = ['stats', 'group', 'season', 'sport_id',
                            'game_type', 'fields']


def get_teams(**kwargs):
    """This endpoint allows you to pull teams.
    params:
      teamId (required) <team_id>
        Description: Unique Team Identifier
        Parameter Type: path
        Data Type: Optional integer
      season <season>
        Description: Season of play
        Parameter Type: query
        Data Type: string
      sportId <sport_id> #Not Implemented: "Object not found"
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      divisionId <division_id>
        Description: Unique division ID.
        Parameter Type: query
        Data Type: integer
      gameType <game_type>
        Description: Type of Game. Available types in /api/v1/gameTypes
        Parameter Type: query
        Data Type: string
      leagueIds <league_ids>
        Description: Comma delimited list of Unique league identifiers.
        Parameter Type: query
        Data Type: array[integer]
      sportIds <sport_ids> #Not Implemented: "Object not found"
        Description: Comma delimited list of top level organizations of a sport.
        Parameter Type: query
        Data Type: array[integer]
      activeStatus <active_status>
        Description: Flag for fetching teams that are currently active (Y), inactive (N),
          pending (P), or all teams (B).
        Parameter Type: query
        Data Type: string
        Options: ['ACTIVE', 'INACTIVE', 'PENDING', 'BOTH']
      leagueListId <league_list_id>
        Description: Unique league list identifier
        Parameter Type: query
        Data Type: string
        Options: ['MILB_FULL', 'MILB_SHORT', 'MILB_COMPLEX', 'MILB_ALL', 'MILB_ALL_NOMEX',
                  'MILB_ALL_DOMESTIC', 'MILB_NONCOMP', 'MILB_NONCOMP_NOMEX', 'MILB_DOMCOMP',
                  'MILB_INTCOMP', 'WIN_NOABL', 'WIN_CARIBBEAN', 'WIN_ALL', 'ABL', 'MLB',
                  'MLB_HIST', 'MLB_MILB', 'MLB_MILB_HIST', 'MLB_MILB_WIN', 'BASEBALL_ALL',
                  'MLB_SPRING']
      allStarStatuses <all_star_status>
        Description: allStarStatuses
        Parameter Type: query
        Data Type: array[string]
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json
    """
    check_kwargs(kwargs.keys(), VALID_TEAMS_PARAMS, mlbapi.exceptions.ParameterException)
    if 'league_ids' in kwargs.keys():
        if isinstance(kwargs['league_ids'], list):
            try:
                kwargs['league_ids'] = ','.join(str(int(lid)) for lid in kwargs['league_ids'])
            except ValueError as error:
                raise mlbapi.exceptions.ParameterException(error)
        else:
            error = 'league_ids must be a list of league IDs as Integers or Strings.'
            raise mlbapi.exceptions.ParameterException(error)

    return request(endpoint.TEAM, **kwargs)

def get_teams_affiliates(**kwargs):
    """Affiliates for multiple teams. Pass ``team_ids`` as a comma-delimited
    string or list of ints."""
    check_kwargs(kwargs.keys(), VALID_TEAMS_AFFILIATES_PARAMS, mlbapi.exceptions.ParameterException)
    if 'team_ids' in kwargs and isinstance(kwargs['team_ids'], list):
        kwargs['team_ids'] = ','.join(str(int(t)) for t in kwargs['team_ids'])
    return request(endpoint.TEAM, 'affiliates', **kwargs)

def get_teams_history(**kwargs):
    """Historical franchise records for multiple teams. Pass ``team_ids`` as a
    comma-delimited string or list of ints."""
    check_kwargs(kwargs.keys(), VALID_TEAMS_HISTORY_PARAMS, mlbapi.exceptions.ParameterException)
    if 'team_ids' in kwargs and isinstance(kwargs['team_ids'], list):
        kwargs['team_ids'] = ','.join(str(int(t)) for t in kwargs['team_ids'])
    return request(endpoint.TEAM, 'history', **kwargs)

def get_teams_stats(**kwargs):
    """Aggregated stats across all teams for a season."""
    check_kwargs(kwargs.keys(), VALID_TEAMS_STATS_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'stats', **kwargs)

def get_team_affiliates(team_id, **kwargs):
    """Minor-league and partner affiliates for a single team."""
    check_kwargs(kwargs.keys(), VALID_TEAM_AFFILIATES_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'affiliates', primary_key=team_id, **kwargs)

def get_team_alumni(team_id, **kwargs):
    """Alumni (former players) for a team in a given season."""
    check_kwargs(kwargs.keys(), VALID_TEAM_ALUMNI_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'alumni', primary_key=team_id, **kwargs)

def get_team_coaches(team_id, **kwargs):
    """Coaching staff for a team.

    params:
      team_id (required): Unique team identifier
      season: Season of play
      date: Date (format: MM/DD/YYYY)
      fields: Comma delimited list of specific fields to be returned
    """
    check_kwargs(kwargs.keys(), VALID_COACHES_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'coaches', primary_key=team_id, **kwargs)

def get_team_history(team_id, **kwargs):
    """Historical franchise records for a single team."""
    check_kwargs(kwargs.keys(), VALID_TEAM_HISTORY_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'history', primary_key=team_id, **kwargs)

def get_team_leaders(team_id, **kwargs):
    """Statistical leaders for a team in a given season."""
    check_kwargs(kwargs.keys(), VALID_TEAM_LEADERS_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'leaders', primary_key=team_id, **kwargs)

def get_team_roster(team_id, roster_type=None, **kwargs):
    """Roster for a team.

    params:
      team_id (required): Unique team identifier
      roster_type: One of 'active', '40Man', 'fullSeason', 'fullRoster',
                   'nonRosterInvitees', 'coach', 'depthChart'
      season: Season of play
      date: Date (format: MM/DD/YYYY)
      game_type: Type of game
      fields: Comma delimited list of specific fields to be returned
    """
    check_kwargs(kwargs.keys(), VALID_ROSTER_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'roster', primary_key=team_id,
                   secondary_key=roster_type, **kwargs)

def get_team_stats(team_id, **kwargs):
    """Stats for a single team."""
    check_kwargs(kwargs.keys(), VALID_TEAM_STATS_PARAMS, mlbapi.exceptions.ParameterException)
    return request(endpoint.TEAM, 'stats', primary_key=team_id, **kwargs)


