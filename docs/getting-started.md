# Getting Started

## Installation

```bash
pip install mlbapi
```

Requires Python 3.10+ and `pydantic >= 2.0`.

---

## Your First Request

Everything goes through a `Client` instance:

```python
from mlbapi import Client

client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)

for date in schedule.dates:
    for game in date.games:
        print(game.game_pk, game.status.detailed_state)
```

---

## Common Patterns

### Get today's Yankees schedule

```python
from datetime import date
from mlbapi import Client

client = Client()
today = date.today().isoformat()
schedule = client.schedule(date=today, team_id=147)
```

### Pull a box score from the schedule

```python
client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)

if schedule.dates:
    game_pk = schedule.dates[0].games[0].game_pk
    box = client.boxscore(game_pk)
    print(box.teams.away.team.name, 'vs', box.teams.home.team.name)
```

### Get standings for both leagues

```python
client = Client()
standings = client.standings(league_id=[103, 104])  # AL + NL

for record in standings.records:
    print(f'\n--- Division: {record.division.name} ---')
    for tr in record.team_records:
        print(f'  {tr.team.name:30s}  {tr.wins}-{tr.losses}  {tr.winning_percentage}')
```

### Use a context manager for automatic session cleanup

```python
from mlbapi import Client

with Client() as client:
    schedule = client.schedule(date='2024-06-01')
    box = client.boxscore(schedule.dates[0].games[0].game_pk)
    line = client.linescore(schedule.dates[0].games[0].game_pk)
```

The session is opened on `__enter__` and closed on `__exit__`.

---

## Next Steps

- [Client configuration](client.md) — timeout, custom sessions, retries
- [Error handling](error-handling.md) — catching exceptions
- [Raw access](raw-access.md) — getting JSON dicts instead of models
