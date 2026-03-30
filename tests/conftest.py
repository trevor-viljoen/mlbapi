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
