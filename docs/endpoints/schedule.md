# Schedule

`client.schedule(**kwargs)` → `Schedule`

Fetches game schedule data from `/api/v1/schedule`.

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `date` | `str` | Single date, `YYYY-MM-DD` |
| `start_date` | `str` | Start of a date range (requires `end_date`) |
| `end_date` | `str` | End of a date range (requires `start_date`) |
| `team_id` | `int` | Filter to a specific team |
| `opponent_id` | `int` | Filter to games against a specific opponent (requires `team_id`) |
| `sport_id` | `int` | Sport ID (default: `1` for MLB) |
| `league_id` | `int` | Filter by league |
| `game_type` | `str` | Game type: `R` regular, `P` postseason, `S` spring training, etc. |
| `hydrate` | `str` | Additional data to hydrate (e.g. `'team'`, `'venue'`) |
| `fields` | `str` | Comma-separated list of fields to return |

---

## Validation Rules

- `start_date` requires `end_date` (and vice versa) — raises `ParameterException` otherwise
- `opponent_id` requires `team_id` — raises `ParameterException` otherwise
- `sport_id` defaults to `1` (MLB) if not provided

---

## Examples

```python
from mlbapi import Client

client = Client()

# Single date
schedule = client.schedule(date='2024-06-01')

# Single date for one team
schedule = client.schedule(date='2024-06-01', team_id=147)  # Yankees

# Date range
schedule = client.schedule(
    start_date='2024-04-01',
    end_date='2024-09-30',
    team_id=147,
)

# Yankees vs Red Sox games only
schedule = client.schedule(
    start_date='2024-04-01',
    end_date='2024-09-30',
    team_id=147,
    opponent_id=111,
)

# Postseason only
schedule = client.schedule(
    start_date='2024-10-01',
    end_date='2024-11-05',
    game_type='P',
)
```

---

## Response Structure

```python
schedule = client.schedule(date='2024-06-01', team_id=147)

# Iterate dates (usually one per calendar day)
for date in schedule.dates:
    print(date.date)        # '2024-06-01'

    for game in date.games:
        print(game.game_pk)
        print(game.game_date)
        print(game.status.detailed_state)  # 'Final', 'In Progress', etc.
        print(game.teams.away.team.name)
        print(game.teams.home.team.name)
        print(game.venue.name)
```

---

## Getting a `game_pk` for Box Score / Linescore

```python
client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)
game_pk = schedule.dates[0].games[0].game_pk

box = client.boxscore(game_pk)
line = client.linescore(game_pk)
```
