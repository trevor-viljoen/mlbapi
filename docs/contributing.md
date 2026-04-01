# Contributing

Contributions are welcome. Please open an issue before submitting a large pull
request, so the change can be discussed first.

---

## Development Setup

```bash
git clone https://github.com/trevor-viljoen/mlbapi
cd mlbapi
pip install -e ".[dev]"
```

---

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=mlbapi --cov-report=term-missing

# Specific file
pytest tests/test_client.py -v
```

All tests must pass before submitting a pull request.

---

## Adding a New Endpoint

Follow these steps in order:

### 1. Add the endpoint constant

In `mlbapi/endpoint.py`:

```python
CONFERENCES = 'conferences'
```

### 2. Create the data module

In `mlbapi/data/conference.py`:

```python
VALID_CONFERENCE_PARAMS = [
    'conference_id',
    'league_id',
    'season',
    'fields',
]
```

The `VALID_*_PARAMS` list is the source of truth for parameter validation.
Copy parameter names from the MLB StatsAPI swagger docs, then convert
camelCase to snake_case.

### 3. Create the Pydantic model

In `mlbapi/models/conference.py`:

```python
from __future__ import annotations
from typing import List, Optional
from mlbapi.models import MLBModel
from mlbapi.models.common import LeagueRef, SportRef


class Conference(MLBModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    league: Optional[LeagueRef] = None
    sport: Optional[SportRef] = None


class Conferences(MLBModel):
    conferences: List[Conference] = []
```

Key rules:
- Inherit from `MLBModel`
- Use `Optional[T] = None` for all fields — API responses are inconsistent
- Use `List[T] = []` for list fields
- No need for camelCase aliases — `MLBModel._normalise_keys` handles the conversion
- For nested objects, use another `MLBModel` subclass

### 4. Add the method to `Client`

In `mlbapi/client.py`:

```python
# In the imports section:
from mlbapi.data.conference import VALID_CONFERENCE_PARAMS
from mlbapi.models.conference import Conferences

# In the Client class:
def conferences(self, **kwargs) -> Conferences:
    """Conference information."""
    data = self._request(endpoint.CONFERENCES, valid_params=VALID_CONFERENCE_PARAMS,
                         **kwargs)
    return Conferences.model_validate(data)
```

### 5. Write tests

In `tests/test_client.py` (add a `TestConferences` class):

```python
CONFERENCES_DATA = {
    'conferences': [{
        'id': 203,
        'name': 'American League',
        'abbreviation': 'AL',
    }],
}

class TestConferences:
    def test_returns_conferences(self):
        assert isinstance(_client(CONFERENCES_DATA).conferences(), Conferences)

    def test_conference_count(self):
        assert len(_client(CONFERENCES_DATA).conferences().conferences) == 1

    def test_conference_name(self):
        assert _client(CONFERENCES_DATA).conferences().conferences[0].name == 'American League'

    def test_invalid_param_raises(self):
        with pytest.raises(ParameterException):
            _client(CONFERENCES_DATA).conferences(not_valid='x')
```

Also add `CONFERENCES_DATA` to `tests/conftest.py` and import it in `test_client.py`.

---

## Code Standards

- Follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- snake_case for all Python identifiers; camelCase conversion is automatic
- `Optional[T] = None` for all model fields
- No bare `except:` — catch specific exceptions
- No module-level state or side effects on import
