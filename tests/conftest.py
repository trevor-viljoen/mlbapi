"""Shared pytest fixtures and sample JSON data for mlbapi tests."""
import pytest
from unittest.mock import MagicMock


def make_mock_response(data):
    """Return a mock requests.Response that returns `data` from .json()."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    mock_resp.url = 'https://statsapi.mlb.com/api/v1/test'
    return mock_resp


# ---------------------------------------------------------------------------
# Sample API JSON responses
# ---------------------------------------------------------------------------

BOXSCORE_DATA = {
    'teams': {
        'away': {
            'team': {
                'id': 147,
                'name': 'New York Yankees',
                'link': '/api/v1/teams/147',
            },
            'teamStats': {
                'batting': {
                    'atBats': 33,
                    'runs': 5,
                    'hits': 9,
                },
                'pitching': {
                    'inningsPitched': '9.0',
                    'strikeOuts': 8,
                },
                'fielding': {
                    'errors': 0,
                },
            },
            'players': {
                'ID592450': {
                    'person': {'id': 592450, 'fullName': 'Aaron Judge', 'link': '/api/v1/people/592450'},
                    'jerseyNumber': '99',
                    'position': {'code': '9', 'name': 'Outfielder', 'type': 'Outfielder', 'abbreviation': 'RF'},
                    'status': {'code': 'A', 'description': 'Active'},
                    'stats': {
                        'batting': {'atBats': 4, 'runs': 1, 'hits': 2},
                        'pitching': {},
                        'fielding': {},
                    },
                    'seasonStats': {
                        'batting': {'atBats': 100, 'runs': 30, 'hits': 35},
                        'pitching': {},
                        'fielding': {},
                    },
                    'gameStatus': {'isCurrentBatter': False, 'isCurrentPitcher': False,
                                   'isOnBench': False, 'isSubstitute': False},
                }
            },
            'batters': [592450],
            'pitchers': [],
            'bench': [],
            'bullpen': [],
            'battingOrder': [592450],
            'info': [],
            'note': [],
        },
        'home': {
            'team': {
                'id': 111,
                'name': 'Boston Red Sox',
                'link': '/api/v1/teams/111',
            },
            'teamStats': {
                'batting': {'atBats': 30, 'runs': 3, 'hits': 7},
                'pitching': {'inningsPitched': '9.0', 'strikeOuts': 6},
                'fielding': {'errors': 1},
            },
            'players': {},
            'batters': [],
            'pitchers': [],
            'bench': [],
            'bullpen': [],
            'battingOrder': [],
            'info': [],
            'note': [],
        },
    },
    'officials': [
        {
            'official': {'id': 427151, 'fullName': 'John Umpire', 'link': '/api/v1/people/427151'},
            'officialType': 'Home Plate',
        }
    ],
    'info': [
        {'label': 'Weather', 'value': 'Sunny, 72F'},
    ],
    'pitchingNotes': [],
}

LINESCORE_DATA = {
    'currentInning': 9,
    'currentInningOrdinal': '9th',
    'inningState': 'Bottom',
    'innings': [
        {'num': 1, 'ordinalNum': '1st',
         'home': {'runs': 0, 'hits': 1, 'errors': 0, 'leftOnBase': 1},
         'away': {'runs': 1, 'hits': 2, 'errors': 0, 'leftOnBase': 0}},
        {'num': 2, 'ordinalNum': '2nd',
         'home': {'runs': 2, 'hits': 3, 'errors': 0, 'leftOnBase': 2},
         'away': {'runs': 0, 'hits': 0, 'errors': 0, 'leftOnBase': 0}},
    ],
    'teams': {
        'home': {'runs': 3, 'hits': 7, 'errors': 0, 'leftOnBase': 5},
        'away': {'runs': 5, 'hits': 9, 'errors': 1, 'leftOnBase': 7},
    },
    'defense': {
        'pitcher': {'id': 111, 'fullName': 'Pitcher One'},
        'catcher': {'id': 222, 'fullName': 'Catcher One'},
        'team': {'id': 111, 'name': 'Boston Red Sox'},
    },
    'offense': {
        'batter': {'id': 592450, 'fullName': 'Aaron Judge'},
        'onDeck': {'id': 333, 'fullName': 'On Deck Guy'},
        'inHole': {'id': 444, 'fullName': 'In Hole Guy'},
        'pitcher': {'id': 111, 'fullName': 'Pitcher One'},
        'first': None,
        'second': None,
        'third': None,
        'team': {'id': 147, 'name': 'New York Yankees'},
    },
    'balls': 2,
    'strikes': 1,
    'outs': 2,
}

SCHEDULE_DATA = {
    'copyright': 'Copyright 2023 MLB Advanced Media',
    'totalItems': 1,
    'totalEvents': 0,
    'totalGames': 1,
    'totalGamesInProgress': 0,
    'dates': [
        {
            'date': '2023-06-01',
            'totalItems': 1,
            'totalEvents': 0,
            'totalGames': 1,
            'totalGamesInProgress': 0,
            'games': [
                {
                    'gamePk': 716463,
                    'link': '/api/v1.1/game/716463/feed/live',
                    'gameType': 'R',
                    'season': '2023',
                    'gameDate': '2023-06-01T17:10:00Z',
                    'status': {
                        'abstractGameState': 'Final',
                        'codedGameState': 'F',
                        'detailedState': 'Final',
                        'statusCode': 'F',
                        'startTimeTBD': False,
                        'abstractGameCode': 'F',
                    },
                    'teams': {
                        'away': {
                            'leagueRecord': {'wins': 30, 'losses': 22, 'pct': '.577'},
                            'score': 5,
                            'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'},
                            'isWinner': True,
                            'splitSquad': False,
                            'seriesNumber': 1,
                        },
                        'home': {
                            'leagueRecord': {'wins': 25, 'losses': 27, 'pct': '.481'},
                            'score': 3,
                            'team': {'id': 111, 'name': 'Boston Red Sox', 'link': '/api/v1/teams/111'},
                            'isWinner': False,
                            'splitSquad': False,
                            'seriesNumber': 1,
                        },
                    },
                    'venue': {'id': 3, 'name': 'Fenway Park', 'link': '/api/v1/venues/3'},
                    'content': {'link': '/api/v1/game/716463/content'},
                }
            ],
            'events': [],
        }
    ],
}

STANDINGS_DATA = {
    'records': [
        {
            'standingsType': 'regularSeason',
            'league': {'id': 103, 'name': 'American League', 'link': '/api/v1/league/103'},
            'division': {'id': 201, 'name': 'American League East', 'link': '/api/v1/divisions/201'},
            'sport': {'id': 1, 'link': '/api/v1/sports/1', 'abbreviation': 'MLB'},
            'lastUpdated': '2023-06-01T00:00:00Z',
            'teamRecords': [
                {
                    'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'},
                    'season': '2023',
                    'streak': {'streakType': 'wins', 'streakNumber': 3, 'streakCode': 'W3'},
                    'divisionRank': '1',
                    'leagueRank': '2',
                    'sportRank': '3',
                    'gamesBack': '-',
                    'wildCardGamesBack': '-',
                    'leagueGamesBack': '-',
                    'springLeagueGamesBack': '-',
                    'sportGamesBack': '-',
                    'divisionGamesBack': '-',
                    'conferenceGamesBack': '-',
                    'leagueRecord': {'wins': 30, 'losses': 22, 'ties': 0, 'pct': '.577'},
                    'lastUpdated': '2023-06-01T00:00:00Z',
                    'records': {
                        'splitRecords': [
                            {'wins': 15, 'losses': 11, 'type': 'home', 'pct': '.577'},
                            {'wins': 15, 'losses': 11, 'type': 'away', 'pct': '.577'},
                        ],
                        'divisionRecords': [
                            {
                                'wins': 10, 'losses': 5, 'pct': '.667',
                                'division': {'id': 201, 'name': 'AL East', 'link': '/api/v1/divisions/201'},
                            }
                        ],
                        'overallRecords': [
                            {'wins': 30, 'losses': 22, 'type': 'regularSeason', 'pct': '.577'},
                        ],
                        'leagueRecords': [
                            {'wins': 20, 'losses': 15, 'pct': '.571',
                             'league': {'id': 103, 'name': 'AL', 'link': '/api/v1/league/103'}},
                        ],
                        'expectedRecords': [
                            {'wins': 29, 'losses': 23, 'type': 'xWinLoss', 'pct': '.558'},
                        ],
                    },
                    'runsAllowed': 220,
                    'runsScored': 260,
                    'divisionChamp': False,
                    'divisionLeader': True,
                    'hasWildcard': True,
                    'clinched': False,
                    'eliminationNumber': 'E',
                    'wins': 30,
                    'losses': 22,
                    'runDifferential': 40,
                    'winningPercentage': '.577',
                }
            ],
        }
    ]
}

TEAMS_DATA = {
    'teams': [
        {
            'id': 147,
            'name': 'New York Yankees',
            'link': '/api/v1/teams/147',
            'season': 2023,
            'venue': {'id': 3313, 'name': 'Yankee Stadium', 'link': '/api/v1/venues/3313'},
            'springVenue': {'id': 4214, 'link': '/api/v1/venues/4214'},
            'teamCode': 'nya',
            'fileCode': 'nyy',
            'abbreviation': 'NYY',
            'teamName': 'Yankees',
            'locationName': 'Bronx',
            'firstYearOfPlay': '1903',
            'league': {'id': 103, 'name': 'American League', 'link': '/api/v1/league/103'},
            'division': {'id': 201, 'name': 'American League East', 'link': '/api/v1/divisions/201'},
            'sport': {'id': 1, 'link': '/api/v1/sports/1', 'name': 'Major League Baseball'},
            'shortName': 'NY Yankees',
            'record': {
                'gamesPlayed': 52,
                'wildCardGamesBack': '-',
                'leagueGamesBack': '-',
                'springLeagueGamesBack': '-',
                'sportGamesBack': '-',
                'divisionGamesBack': '-',
                'conferenceGamesBack': '-',
                'leagueRecord': {'wins': 30, 'losses': 22, 'ties': 0, 'pct': '.577'},
                'records': {},
                'divisionLeader': True,
                'wins': 30,
                'losses': 22,
                'winningPercentage': '.577',
            },
            'springLeague': {'id': 114, 'name': 'Grapefruit League', 'link': '/api/v1/league/114',
                             'abbreviation': 'GL'},
            'allStarStatus': 'N',
            'active': True,
        }
    ]
}

DIVISIONS_DATA = {
    'divisions': [
        {
            'id': 201,
            'name': 'American League East',
            'season': '2023',
            'nameShort': 'AL East',
            'link': '/api/v1/divisions/201',
            'abbreviation': 'ALE',
            'league': {'id': 103, 'link': '/api/v1/league/103'},
            'sport': {'id': 1, 'link': '/api/v1/sports/1', 'abbreviation': 'MLB'},
            'hasWildcard': True,
            'sortOrder': 1,
            'numPlayoffTeams': 2,
            'active': True,
        }
    ]
}

CONFERENCES_DATA = {
    'conferences': [
        {'id': 203, 'name': 'American League', 'link': '/api/v1/conferences/203',
         'abbreviation': 'AL', 'shortName': 'AL', 'nameShort': 'AL',
         'league': {'id': 103}, 'sport': {'id': 1}, 'active': True},
    ]
}

SEASONS_DATA = {
    'seasons': [
        {'seasonId': '2024', 'hasWildcard': True, 'preSeasonStartDate': '2024-02-01',
         'seasonStartDate': '2024-03-28', 'regularSeasonStartDate': '2024-03-28',
         'regularSeasonEndDate': '2024-09-29', 'seasonEndDate': '2024-11-05',
         'offseasonStartDate': '2024-11-06', 'offSeasonEndDate': '2025-01-01',
         'seasonLevelGamedayType': 'P', 'gameType': 'R', 'active': True},
    ]
}

VENUES_DATA = {
    'venues': [
        {'id': 3313, 'name': 'Yankee Stadium', 'link': '/api/v1/venues/3313',
         'location': {'address1': '1 E 161st St', 'city': 'Bronx', 'state': 'New York',
                      'stateAbbrev': 'NY', 'postalCode': '10451',
                      'defaultCoordinates': {'latitude': 40.829659, 'longitude': -73.926186},
                      'country': 'USA', 'phone': '(718) 293-6000'},
         'timezone': {'id': 'America/New_York', 'offset': -5, 'tz': 'EST'},
         'fieldInfo': {'capacity': 47309, 'turfType': 'Grass', 'roofType': 'Open',
                       'leftLine': 318, 'left': 318, 'leftCenter': 399,
                       'center': 408, 'rightCenter': 385, 'rightLine': 314},
         'active': True},
    ]
}

DRAFT_DATA = {
    'drafts': {
        'rounds': [
            {'roundNumber': 1, 'round': '1',
             'picks': [
                 {'bisPlayerId': 933733, 'pickRound': '1', 'pickNumber': 1, 'roundPickNumber': 1,
                  'rank': 1, 'pickValue': '9234300', 'signingBonus': '9234300',
                  'home': {'city': 'Mableton', 'state': 'Georgia', 'country': 'USA'},
                  'scoutingReport': 'Top overall prospect.',
                  'person': {'id': 933733, 'fullName': 'Paul Skenes', 'link': '/api/v1/people/933733'},
                  'team': {'id': 134, 'name': 'Pittsburgh Pirates', 'link': '/api/v1/teams/134'},
                  'year': '2023', 'isPass': False, 'isDraft': True},
             ]},
        ]
    }
}

STATS_DATA = {
    'stats': [
        {'type': {'displayName': 'season'}, 'group': {'displayName': 'hitting'},
         'splits': [
             {'season': '2024',
              'stat': {'gamesPlayed': 130, 'atBats': 450, 'hits': 135,
                       'homeRuns': 28, 'rbi': 90, 'avg': '.300', 'ops': '.920'},
              'player': {'id': 660271, 'fullName': 'Juan Soto', 'link': '/api/v1/people/660271'},
              'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'}}
         ]}
    ]
}

STATS_LEADERS_DATA = {
    'leagueLeaders': [
        {'leaderCategory': 'homeRuns', 'season': '2024',
         'gameType': {'id': 'R', 'description': 'Regular Season'},
         'leaders': [
             {'rank': 1, 'value': '58', 'person': {'id': 592450, 'fullName': 'Aaron Judge'},
              'team': {'id': 147, 'name': 'New York Yankees'}, 'season': '2024'},
         ]}
    ]
}

HOMERUNDERBY_DATA = {
    'id': 716463,
    'bracket': {'rounds': []},
    'pool': {'players': []},
}

ATTENDANCE_DATA = {
    'records': [
        {'openingDay': '2024-03-28', 'attendanceRecords': [
            {'gameType': {'id': 'R', 'description': 'Regular Season'},
             'totalAway': 3000000, 'totalHome': 3200000, 'totalOpeningDay': 42000,
             'openingDayTotal': 42000, 'gamesTotal': 162, 'gamesAwayTotal': 81,
             'gamesHomeTotal': 81, 'year': '2024',
             'team': {'id': 147, 'name': 'New York Yankees', 'link': '/api/v1/teams/147'}},
        ]}
    ]
}

AWARDS_DATA = {
    'awards': [
        {'id': 'MLBHOF', 'name': 'Baseball Hall of Fame', 'description': 'Hall of Fame inductee',
         'link': '/api/v1/awards/MLBHOF', 'sport': {'id': 1}, 'league': {}},
    ]
}

JOBS_DATA = {
    'roster': [
        {'id': 427151, 'fullName': 'Joe West', 'link': '/api/v1/people/427151',
         'jobId': 'UMP', 'title': 'Home Plate', 'jerseyNumber': '22'},
    ]
}

TRANSACTIONS_DATA = {
    'transactions': [
        {'id': 1234, 'person': {'id': 660271, 'fullName': 'Juan Soto'},
         'toTeam': {'id': 147, 'name': 'New York Yankees'},
         'fromTeam': {'id': 135, 'name': 'San Diego Padres'},
         'date': '2024-01-01', 'effectiveDate': '2024-01-01',
         'resolutionDate': '2024-01-01', 'typeCode': 'TR', 'typeDesc': 'Trade',
         'description': 'Traded Juan Soto to New York Yankees'},
    ]
}

META_DATA = {
    'leagueLeaderTypes': [
        {'lookupName': 'homeRuns', 'description': 'Home Runs'},
        {'lookupName': 'battingAverage', 'description': 'Batting Average'},
    ]
}

SPORT_DATA = {
    'sports': [
        {'id': 1, 'code': 'mlb', 'link': '/api/v1/sports/1',
         'name': 'Major League Baseball', 'abbreviation': 'MLB',
         'sortOrder': 11, 'activeStatus': True},
    ]
}
