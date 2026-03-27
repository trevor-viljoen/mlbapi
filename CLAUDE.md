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
| `mlbapi/data/gameday.py` | Schedule endpoints |
| `mlbapi/data/standings.py` | Standings endpoints |
| `mlbapi/data/team.py` | Team endpoints |
| `mlbapi/data/division.py` | Division endpoints |

## Code Standards

- [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)
- All new functions require tests in `tests/`
- Python snake_case kwargs are converted to/from camelCase API params via `mlbapi/utils.py`

## API Base URL

`https://statsapi.mlb.com/api/v1`

## Exception Hierarchy

```
MLBAPIException
├── RequestException       - HTTP/network failure (wraps requests.exceptions.RequestException)
├── ImplementationException - Unsupported endpoint
├── ObjectNotFoundException - API returned an error message
└── ParameterException     - Invalid kwargs passed to a data function
```

## Supported Endpoints

| Endpoint | Module | Description |
|---|---|---|
| `game` | `data/game.py` | Boxscore, linescore, play-by-play, live feed, win probability |
| `schedule` | `data/gameday.py` | Game schedules by date/team |
| `standings` | `data/standings.py` | League standings |
| `teams` | `data/team.py` | Team information |
| `divisions` | `data/division.py` | Division information |

## Stub Modules (Not Yet Implemented)

The following data modules are empty placeholders:
- `mlbapi/data/conference.py`
- `mlbapi/data/season.py`
- `mlbapi/data/venue.py`
- `mlbapi/data/draft.py`
- `mlbapi/data/stats.py`
- `mlbapi/data/homerunderby.py`
- `mlbapi/data/sport.py` (skeleton exists but untested)

## Adding a New Endpoint

1. Add the endpoint constant to `mlbapi/endpoint.py`
2. Add the endpoint string to `SUPPORTED_ENDPOINTS` in `mlbapi/data/__init__.py`
3. Create the data module in `mlbapi/data/<name>.py` with a `VALID_*_PARAMS` list and `get_*()` functions
4. Create the object class(es) in `mlbapi/object/<name>.py`
5. Export the public function from `mlbapi/__init__.py`
6. Write tests in `tests/`
