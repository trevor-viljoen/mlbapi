# Teams

`client.teams(**kwargs)` → `Teams`

Fetches team information from `/api/v1/teams`.

---

## Parameters

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

---

## Examples

```python
from mlbapi import Client

client = Client()

# All MLB teams
teams = client.teams()

# Teams for a specific season
teams = client.teams(season='2024')

# Specific team(s) by ID
teams = client.teams(team_ids=147)           # Yankees
teams = client.teams(team_ids=[147, 111])    # Yankees + Red Sox

# Teams in a division (AL East = 201)
teams = client.teams(division_id=201)
```

---

## Response Structure

```python
teams = client.teams()

for team in teams.teams:
    print(team.id)
    print(team.name)              # 'New York Yankees'
    print(team.abbreviation)      # 'NYY'
    print(team.team_name)         # 'Yankees'
    print(team.location_name)     # 'New York'
    print(team.venue.name)        # 'Yankee Stadium'
    print(team.division.name)     # 'American League East'
    print(team.league.name)       # 'American League'
```

---

## Common Team IDs

| Team | ID | Team | ID |
|---|---|---|---|
| Yankees | 147 | Dodgers | 119 |
| Red Sox | 111 | Giants | 137 |
| Astros | 117 | Cubs | 112 |
| Braves | 144 | Cardinals | 138 |
| Mets | 121 | Padres | 135 |
| Blue Jays | 141 | Phillies | 143 |
| Orioles | 110 | Nationals | 120 |
| Rays | 139 | Marlins | 146 |
| Rangers | 140 | Brewers | 158 |
| Angels | 108 | Pirates | 134 |
| Athletics | 133 | Reds | 113 |
| Mariners | 136 | Indians/Guardians | 114 |
| White Sox | 145 | Tigers | 116 |
| Twins | 142 | Royals | 118 |
| Rockies | 115 | Diamondbacks | 109 |

Get the full current list: `client.teams()`
