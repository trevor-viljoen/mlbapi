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
    if 'league_ids' in kwargs.keys(): # Make sure seasons is a comma delimited list
        if isinstance(kwargs['league_ids'], list):
            temp = []
            for league_id in kwargs['league_ids']:
                if not isinstance(league_id, int):
                    try:
                        temp.append(int(league_id))
                    except ValueError as error:
                        raise mlbapi.exceptions.ParameterException(error)
            if temp:
                kwargs['league_ids'] = ','.join(temp)
        else:
            error = 'seasons must be a list of years as Integers or Strings.'
            raise mlbapi.exceptions.ParameterException(error)
        kwargs['league_ids'] = ','.join([str(lid) for lid in kwargs['league_ids']])

    return request(endpoint.TEAM, **kwargs)

def get_teams_affiliates(**kwargs):
    """ """

def get_teams_history(**kwargs):
    """ """

def get_teams_stats(**kwargs):
    """ """

def get_team_affiliates(**kwargs):
    """ """

def get_team_alumni(**kwargs):
    """ """

def get_team_coaches(**kwargs):
    """ """

def get_team_history(**kwargs):
    """ """

def get_team_leaders(**kwargs):
    """ """

def get_team_roster(**kwargs):
    """ """

def get_team_roster_type(**kwargs):
    """ """

def get_team_stats(**kwargs):
    """ """


