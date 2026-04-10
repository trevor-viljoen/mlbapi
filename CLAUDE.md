# mlbapi

Python 3 wrapper for the MLB StatsAPI at `statsapi.mlb.com`.

## Development Setup

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
pytest --cov=mlbapi --cov-report=term-missing
```

## Architecture

Two-layer design separating HTTP concerns from data modelling:

- **Data layer** (`mlbapi/data/`): Validates parameters and makes raw HTTP requests returning JSON dicts
- **Models layer** (`mlbapi/models/`): Pydantic v2 models that wrap the JSON dicts for attribute-style access and type safety

All public access goes through the `Client` class in `mlbapi/client.py`. There are no module-level convenience functions.

### Request Flow

1. Caller instantiates `Client` and calls an endpoint method (e.g., `client.schedule(date='2024-06-01')`)
2. `Client._request()` validates kwargs against the endpoint's `VALID_*_PARAMS` list, builds the URL, and calls `Client._get()`
3. `Client._get()` executes the HTTP GET (using an injected `requests.Session` or bare `requests.get`) and returns a JSON dict
4. The endpoint method wraps the dict in a Pydantic model and returns it

For unsupported or not-yet-wrapped endpoints use `client.get(path, **params)` to get the raw JSON dict.

### Key Files

| File | Purpose |
|---|---|
| `mlbapi/__init__.py` | Public re-exports (`Client`, exceptions, `__version__`) |
| `mlbapi/client.py` | Sole public entry point — all 25+ endpoint methods live here |
| `mlbapi/endpoint.py` | API endpoint string constants |
| `mlbapi/exceptions.py` | Custom exception classes |
| `mlbapi/utils.py` | Shared utility functions (case conversion, param validation) |
| `mlbapi/data/__init__.py` | URL construction (`get_api_url`) |
| `mlbapi/data/game.py` | `VALID_*_PARAMS` lists for game endpoints |
| `mlbapi/data/schedule.py` | `VALID_SCHEDULE_PARAMS` and `get_schedule()` |
| `mlbapi/data/standings.py` | `VALID_STANDINGS_PARAMS` and `get_standings()` |
| `mlbapi/data/team.py` | `VALID_TEAMS_PARAMS` and `get_teams()` |
| `mlbapi/data/division.py` | `VALID_DIVISION_PARAMS` and `get_divisions()` |
| `mlbapi/models/__init__.py` | `MLBModel` base class (Pydantic v2, camelCase normalisation) |
| `mlbapi/models/game.py` | `BoxScore`, `LineScore` models |
| `mlbapi/models/schedule.py` | `Schedule`, `Date`, `Game` models |
| `mlbapi/models/standings.py` | `Standings`, `StandingsRecord` models |
| `mlbapi/models/team.py` | `Teams`, `Team` models |
| `mlbapi/models/division.py` | `Divisions`, `Division` models |
| `mlbapi/models/common.py` | Shared reference types (`PersonRef`, `TeamRef`, etc.) |

## Code Standards

- [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)
- All new endpoint methods require tests in `tests/`
- Python snake_case kwargs are converted to camelCase API params via `mlbapi/utils.py`
- Models inherit from `MLBModel` (Pydantic v2 `BaseModel`)

## API Base URL

`https://statsapi.mlb.com/api/v1`

Note: The live game feed endpoints (`feed/live`, `feed/live/diffPatch`,
`feed/live/timestamps`) use **v1.1** instead of v1. Pass `api_version='v1.1'`
to `Client._request()` for these.

## Models Layer

All models inherit from `MLBModel` (`mlbapi/models/__init__.py`):

- **camelCase normalisation**: a `model_validator(mode="before")` converts every
  incoming key with `inflection.underscore()`, so `gamePk` becomes `game_pk`
  automatically — no field aliases needed in subclasses.
- **Extra fields allowed**: `extra="allow"` means unknown API keys are stored as
  attributes, so new API fields never break existing code.
- **Positional dict init**: `MLBModel(data_dict)` is accepted for legacy
  call-sites; internally this calls `super().__init__(**data_dict)` which still
  runs all validators.
- **Serialisation**: `model.model_dump()` (preferred) or the legacy `model.json()`
  both return a plain Python dict.

## Exception Hierarchy

```
MLBAPIException
├── RequestException        - HTTP/network failure (wraps requests.exceptions.RequestException)
├── ImplementationException - Unsupported endpoint
├── ObjectNotFoundException - API returned an error message (bad ID, etc.)
└── ParameterException      - Invalid kwargs passed to an endpoint method
```

## Supported Endpoints

| Endpoint | Data module | Model | Description |
|---|---|---|---|
| `game/{pk}/boxscore` | `data/game.py` | `models/game.py` | Full box score |
| `game/{pk}/linescore` | `data/game.py` | `models/game.py` | Live linescore |
| `game/{pk}/playByPlay` | `data/game.py` | raw dict | Play-by-play |
| `game/{pk}/feed/live` | `data/game.py` | raw dict | Live feed (v1.1) |
| `schedule` | `data/schedule.py` | `models/schedule.py` | Game schedule |
| `standings` | `data/standings.py` | `models/standings.py` | League standings |
| `teams` | `data/team.py` | `models/team.py` | Team information |
| `divisions` | `data/division.py` | `models/division.py` | Division information |
| `sports` | `data/sport.py` | raw dict | Sports information |

## Stub Modules (Not Yet Implemented)

The following data modules are empty placeholders:
- `mlbapi/data/conference.py` → `/api/v1/conferences`
- `mlbapi/data/season.py` → `/api/v1/seasons`
- `mlbapi/data/venue.py` → `/api/v1/venues`
- `mlbapi/data/draft.py` → `/api/v1/draft`
- `mlbapi/data/stats.py` → `/api/v1/stats`, `/api/v1/stats/leaders`, `/api/v1/stats/streaks`
- `mlbapi/data/homerunderby.py` → `/api/v1/homeRunDerby`

Additionally, the following endpoints have constants defined but no module yet:
- `ATTENDANCE` → `/api/v1/attendance`
- `AWARDS` → `/api/v1/awards`
- `JOBS` → `/api/v1/jobs`
- `META` → `/api/v1/{type}` (lookup tables for valid param values)
- `TRANSACTIONS` → `/api/v1/transactions`
- `GAME_PACE` → `/api/v1/gamePace`
- `HIGH_LOW` → `/api/v1/highLow/{orgType}`

Use `client.get('/v1/<endpoint>', **params)` to access any of these until they get a dedicated method.

## Adding a New Endpoint

1. Add the endpoint constant to `mlbapi/endpoint.py`
2. Create the data module `mlbapi/data/<name>.py` with a `VALID_*_PARAMS` list
3. Create the Pydantic model in `mlbapi/models/<name>.py` inheriting from `MLBModel`
4. Add a method to `Client` in `mlbapi/client.py` that calls `self._request(...)` and wraps the result
5. Write tests in `tests/`

## Origin of `VALID_*_PARAMS` Lists

All parameter lists were transcribed from the MLB StatsAPI swagger documentation
at the time each endpoint was implemented. camelCase API params were converted to
snake_case Python kwargs. Some params (e.g. `calendar_types`, `performer_ids`,
`use_latest_games`) may no longer appear in the current API — they were valid
when originally documented.
