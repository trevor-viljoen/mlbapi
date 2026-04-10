"""mlbapi functions for the gamePace API endpoint."""

from mlbapi import endpoint, exceptions
from mlbapi.data import request
from mlbapi.utils import check_kwargs


VALID_GAME_PACE_PARAMS = [
    'season', 'team_id', 'league_id', 'league_list_id', 'sport_id',
    'game_type', 'start_date', 'end_date', 'venue_id', 'fields',
]


def get_game_pace(**kwargs):
    """Pace-of-game statistics for teams, leagues, and sports.

    params:
      season <season>
        Description: Season of play
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
      leagueListId <league_list_id>
        Description: Unique league list identifier
        Parameter Type: query
        Data Type: string
      sportId <sport_id>
        Description: Top level organization of a sport (MLB is 1)
        Parameter Type: query
        Data Type: integer
      gameType <game_type>
        Description: Type of Game. Available types in /api/v1/gameTypes
        Parameter Type: query
        Data Type: string
      startDate <start_date>
        Description: Start date for range of data. Format: MM/DD/YYYY
        Parameter Type: query
        Data Type: string
      endDate <end_date>
        Description: End date for range of data. Format: MM/DD/YYYY
        Parameter Type: query
        Data Type: string
      venueId <venue_id>
        Description: Unique venue identifier
        Parameter Type: query
        Data Type: integer
      fields <fields>
        Description: Comma delimited list of specific fields to be returned.
        Format: topLevelNode, childNode, attribute
        Parameter Type: query
        Data Type: array[string]

    Returns:
        json dict
    """
    check_kwargs(kwargs.keys(), VALID_GAME_PACE_PARAMS, exceptions.ParameterException)
    return request(endpoint.GAME_PACE, **kwargs)
