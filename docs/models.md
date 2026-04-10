# Models

All mlbapi response objects are Pydantic v2 models that inherit from `MLBModel`.

---

## MLBModel

Defined in `mlbapi/models/__init__.py`. Every response model inherits from it.

```python
from mlbapi.models import MLBModel
```

### camelCase Normalisation

The MLB StatsAPI returns camelCase keys (`gamePk`, `teamName`, `currentInning`).
`MLBModel` automatically converts all keys to snake_case before validation:

```python
box = client.boxscore(716463)
print(box.teams.away.team.name)    # works — 'name' from API's 'name'
print(box.teams.home.team_stats)   # works — 'teamStats' → 'team_stats'
```

This is done via a `model_validator(mode="before")` that runs
`inflection.underscore()` on every key in the incoming dict.

### Extra Fields

`extra="allow"` means the models accept and store any API key that isn't
explicitly declared as a field. New API keys never cause validation errors:

```python
box = client.boxscore(716463)
print(box.model_extra)  # dict of any fields not declared on BoxScore
```

### Serialisation

```python
model.model_dump()              # snake_case keys
model.model_dump(by_alias=True) # camelCase keys (as the API returns)
model.json()                    # alias for model_dump() — legacy compat
```

---

## Initialisation Styles

All models can be initialised two ways:

```python
from mlbapi.models.game import BoxScore

# Keyword arguments (standard Pydantic v2)
box = BoxScore(**api_response_dict)

# Positional dict (legacy pattern — still supported)
box = BoxScore(api_response_dict)
```

In practice you will almost always use `Model.model_validate(data)` which is
the idiomatic Pydantic v2 approach and handles nested models correctly.

---

## Model Reference

| Model | Module | Description |
|---|---|---|
| `BoxScore` | `models/game.py` | Full game box score |
| `LineScore` | `models/game.py` | Live linescore with count/bases/pitcher |
| `Schedule` | `models/schedule.py` | Schedule response (contains `dates`) |
| `Date` | `models/schedule.py` | One calendar date with a list of games |
| `Game` | `models/schedule.py` | Single scheduled game |
| `Standings` | `models/standings.py` | Full standings response |
| `StandingsRecord` | `models/standings.py` | One division's standing records |
| `Teams` | `models/team.py` | Teams list response |
| `Team` | `models/team.py` | Single team |
| `Divisions` | `models/division.py` | Divisions list response |
| `Division` | `models/division.py` | Single division |
| `PersonRef` | `models/common.py` | Lightweight person reference (id + fullName) |
| `TeamRef` | `models/common.py` | Lightweight team reference |
| `LeagueRef` | `models/common.py` | Lightweight league reference |
| `VenueRef` | `models/common.py` | Lightweight venue reference |
