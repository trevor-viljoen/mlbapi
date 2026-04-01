# Teams

## `team_id()` — Quick Lookup (no API call)

The fastest way to get a team ID. Accepts an abbreviation, nickname, full name,
or city — case-insensitive, no network request:

```python
from mlbapi import team_id

team_id('NYY')               # 147
team_id('yankees')           # 147
team_id('New York Yankees')  # 147
team_id('new york')          # 147

team_id('LAD')               # 119
team_id('Dodgers')           # 119

team_id('unknown')           # None
```

## `TEAMS` — Full Static List

```python
from mlbapi import TEAMS

for team in TEAMS:
    print(f"{team['abbreviation']:4s}  {team['id']:3d}  {team['full_name']}")
```

---

## `client.teams(**kwargs)` → `Teams`

Fetches live team information from `/api/v1/teams`. Use this when you need
venue, division, league, or other metadata that `team_id()` doesn't provide.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `sport_id` | `int` | Sport ID (default: `1` for MLB) |
| `season` | `str` | Season year, e.g. `'2024'` |
| `team_ids` | `str \| list` | Comma-separated or list of team IDs |
| `league_ids` | `str \| list` | Filter by league(s) |
| `division_id` | `int` | Filter by division |
| `game_type` | `str` | Game type (`R`, `P`, `S`, etc.) |
| `hydrate` | `str` | Additional data to hydrate |
| `active_status` | `str` | `'Y'`, `'N'`, or `'B'` (both) |
| `fields` | `str` | Comma-separated fields to return |

### Examples

```python
from mlbapi import Client, team_id

client = Client()

# Look up a specific team's full metadata
tid = team_id('NYY')
teams = client.teams(team_ids=tid)
team = teams.teams[0]

print(team.name)              # 'New York Yankees'
print(team.venue.name)        # 'Yankee Stadium'
print(team.division.name)     # 'American League East'
print(team.league.name)       # 'American League'

# All MLB teams
for team in client.teams().teams:
    print(f'{team.abbreviation:4s}  {team.id:3d}  {team.name}')

# Teams in a division (AL East = 201)
teams = client.teams(division_id=201)
```

---

## Team IDs Quick Reference

| Abbr | ID | Team | Abbr | ID | Team |
|---|---|---|---|---|---|
| BAL | 110 | Baltimore Orioles | ATL | 144 | Atlanta Braves |
| BOS | 111 | Boston Red Sox | MIA | 146 | Miami Marlins |
| NYY | 147 | New York Yankees | NYM | 121 | New York Mets |
| TB | 139 | Tampa Bay Rays | PHI | 143 | Philadelphia Phillies |
| TOR | 141 | Toronto Blue Jays | WSH | 120 | Washington Nationals |
| CWS | 145 | Chicago White Sox | CHC | 112 | Chicago Cubs |
| CLE | 114 | Cleveland Guardians | CIN | 113 | Cincinnati Reds |
| DET | 116 | Detroit Tigers | MIL | 158 | Milwaukee Brewers |
| KC | 118 | Kansas City Royals | PIT | 134 | Pittsburgh Pirates |
| MIN | 142 | Minnesota Twins | STL | 138 | St. Louis Cardinals |
| HOU | 117 | Houston Astros | ARI | 109 | Arizona Diamondbacks |
| LAA | 108 | Los Angeles Angels | COL | 115 | Colorado Rockies |
| OAK | 133 | Oakland Athletics | LAD | 119 | Los Angeles Dodgers |
| SEA | 136 | Seattle Mariners | SD | 135 | San Diego Padres |
| TEX | 140 | Texas Rangers | SF | 137 | San Francisco Giants |
