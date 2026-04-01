# Migration from mlbgame

[mlbgame](https://github.com/panzarino/mlbgame) was a popular Python library
that parsed MLB's legacy XML Gameday feed. That feed was discontinued when MLB
moved to the JSON StatsAPI. This guide helps you migrate existing mlbgame code
to mlbapi.

---

## Key Differences

| | mlbgame | mlbapi |
|---|---|---|
| Data source | XML Gameday feed (discontinued) | JSON StatsAPI |
| Access pattern | Module-level functions | `Client` instance |
| Return types | Custom objects | Pydantic v2 models |
| Python version | 2.7/3.x | 3.10+ |

---

## Getting Games (Schedule)

**mlbgame:**
```python
import mlbgame

games = mlbgame.games(2023, 6, 1, home='Yankees')
day = mlbgame.combine(games, out_all=True)
```

**mlbapi:**
```python
from mlbapi import Client

client = Client()
schedule = client.schedule(date='2023-06-01', team_id=147)

for date in schedule.dates:
    for game in date.games:
        print(game.game_pk, game.status.detailed_state)
```

---

## Box Scores

**mlbgame:**
```python
import mlbgame

overview = mlbgame.overview(game_id)
```

**mlbapi:**
```python
from mlbapi import Client

client = Client()
box = client.boxscore(game_pk)

# Team names
print(box.teams.away.team.name)
print(box.teams.home.team.name)

# Stats
print(box.teams.away.team_stats.batting.runs)
print(box.teams.home.team_stats.batting.hits)
```

---

## Standings

**mlbgame:**
```python
import mlbgame

standings = mlbgame.standings()
```

**mlbapi:**
```python
from mlbapi import Client

client = Client()
standings = client.standings(league_id=[103, 104])

for record in standings.records:
    for tr in record.team_records:
        print(f'{tr.team.name}  {tr.wins}-{tr.losses}')
```

---

## Finding Team IDs

mlbgame used team nicknames as strings (`'Yankees'`). mlbapi uses numeric team
IDs. Get the full list:

```python
from mlbapi import Client

client = Client()
teams = client.teams()

for team in teams.teams:
    print(f'{team.name}: {team.id}')
```

Or see the [Teams endpoint reference](endpoints/teams.md) for common IDs.

---

## The "Gameday" Concept

In mlbgame, "gameday" referred to the structure of MLB's old XML feed (which
was served from `gd2.mlb.com/components/game/mlb/`). That feed is gone.

In mlbapi, the equivalent is the `/api/v1/schedule` endpoint. The module
`mlbapi.data.schedule` implements it.
