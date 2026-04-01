# mlbapi Documentation

**mlbapi** is a Python 3 client for the [MLB StatsAPI](https://statsapi.mlb.com/) — the data source powering MLB.com's live game data, box scores, standings, and more.

All responses are Pydantic v2 models: attribute access, type safety, and IDE autocompletion with no JSON parsing required.

---

## Contents

- [Getting Started](getting-started.md) — installation, first request, common patterns
- [Client](client.md) — configuration, sessions, context manager, `__repr__`
- [Error Handling](error-handling.md) — exception hierarchy and examples
- [Raw Access](raw-access.md) — `client.get()`, `model_dump()`, working with untyped responses
- [Models](models.md) — how Pydantic models work, camelCase normalisation, extra fields
- **Endpoints**
  - [Schedule](endpoints/schedule.md)
  - [Box Score](endpoints/boxscore.md)
  - [Line Score](endpoints/linescore.md)
  - [Standings](endpoints/standings.md)
  - [Teams](endpoints/teams.md)
  - [Divisions](endpoints/divisions.md)
  - [Live Feed](endpoints/live.md)
- [Testing](testing.md) — writing tests, mocking the client
- [Migration from mlbgame](migration.md) — upgrading from the legacy library
- [Contributing](contributing.md) — adding endpoints, code standards

---

## Quick Example

```python
from mlbapi import Client

with Client() as client:
    schedule = client.schedule(date='2024-06-01', team_id=147)
    game_pk = schedule.dates[0].games[0].game_pk
    box = client.boxscore(game_pk)
    print(f'{box.teams.away.team.name} @ {box.teams.home.team.name}')
```
