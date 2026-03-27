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

Two-layer design separating HTTP concerns from data modeling:

- **Data layer** (`mlbapi/data/`): Validates parameters and makes raw HTTP requests returning JSON dicts
- **Object layer** (`mlbapi/object/`): Python objects that wrap the JSON dicts for attribute-style access

### Request Flow

1. Public API function (e.g., `mlbapi.schedule()`) calls a data layer function
2. Data layer validates kwargs against a `VALID_*_PARAMS` list, then calls `mlbapi.data.request()`
3. `request()` builds the URL, sets headers, calls `requests.get()`, returns JSON
4. The public API function wraps the JSON in an object layer class and returns it

### Key Files

| File | Purpose |
|---|---|
| `mlbapi/__init__.py` | Public API entry point |
| `mlbapi/endpoint.py` | API endpoint string constants |
| `mlbapi/exceptions.py` | Custom exception classes |
| `mlbapi/utils.py` | Shared utility functions (case conversion, validation) |
| `mlbapi/data/__init__.py` | Core HTTP request logic and URL construction |
| `mlbapi/data/game.py` | Game endpoints (boxscore, linescore, play-by-play, live) |
| `mlbapi/data/schedule.py` | Schedule endpoint — primary implementation, class-based |
| `mlbapi/data/gameday.py` | Schedule endpoint — mlbgame migration compatibility wrapper |
| `mlbapi/data/standings.py` | Standings endpoints |
| `mlbapi/data/team.py` | Team endpoints |
| `mlbapi/data/division.py` | Division endpoints |

## Code Standards

- [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)
- All new functions require tests in `tests/`
- Python snake_case kwargs are converted to/from camelCase API params via `mlbapi/utils.py`

## API Base URL

`https://statsapi.mlb.com/api/v1`

Note: The live game feed endpoints (`feed/live`, `feed/live/diffPatch`,
`feed/live/timestamps`) use **v1.1** instead of v1. Pass `api_version='v1.1'`
to `mlbapi.data.request()` for these.

## Historical Context

### Origin of `VALID_*_PARAMS` lists

All parameter lists were transcribed directly from the MLB StatsAPI swagger
documentation at the time each endpoint was implemented. camelCase API params
were converted to snake_case Python kwargs. Some params (e.g.
`calendar_types`, `performer_ids`, `use_latest_games`) may no longer appear in
the current API — they were valid when originally documented.

### `data/schedule.py` vs `data/gameday.py`

Two modules wrap the same `/schedule` API endpoint:

- `data/schedule.py` — the primary implementation. Class-based interface
  (`Schedule.get_schedule()`), params taken directly from the swagger docs.
- `data/gameday.py` — a migration compatibility shim written to help users move
  from [panzarino/mlbgame](https://github.com/panzarino/mlbgame), a predecessor
  library that parsed MLB's legacy XML API. The "gameday" concept maps to the
  old XML feed's structure. Users migrating from mlbgame should be directed here.

## Exception Hierarchy

```
MLBAPIException
├── RequestException        - HTTP/network failure (wraps requests.exceptions.RequestException)
├── ImplementationException - Unsupported endpoint
├── ObjectNotFoundException - API returned an error message
└── ParameterException      - Invalid kwargs passed to a data function
```

## Supported Endpoints

| Endpoint | Module | Description |
|---|---|---|
| `game` | `data/game.py` | Boxscore, linescore, play-by-play, live feed (v1.1), win probability |
| `schedule` | `data/schedule.py` | Game schedules by date/team (primary) |
| `schedule` | `data/gameday.py` | Game schedules — mlbgame migration compat |
| `standings` | `data/standings.py` | League standings |
| `teams` | `data/team.py` | Team information |
| `divisions` | `data/division.py` | Division information |
| `sports` | `data/sport.py` | Sports information |

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

## Adding a New Endpoint

1. Add the endpoint constant to `mlbapi/endpoint.py`
2. Add the endpoint string to `SUPPORTED_ENDPOINTS` in `mlbapi/data/__init__.py`
3. Create the data module in `mlbapi/data/<name>.py` with a `VALID_*_PARAMS` list and `get_*()` functions
4. Create the object class(es) in `mlbapi/object/<name>.py`
5. Export the public function from `mlbapi/__init__.py`
6. Write tests in `tests/`
