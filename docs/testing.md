# Testing

mlbapi's `Client` is designed for testability: inject a mock `requests.Session`
to avoid real network calls.

---

## Injecting a Mock Session

```python
import pytest
from unittest.mock import MagicMock
import requests
from mlbapi import Client

def make_client(data: dict) -> Client:
    """Return a Client backed by a mock session returning *data*."""
    session = MagicMock(spec=requests.Session)
    response = MagicMock()
    response.json.return_value = data
    session.get.return_value = response
    return Client(session=session)


def test_schedule_returns_dates():
    data = {
        'dates': [{
            'date': '2024-06-01',
            'games': [{
                'gamePk': 716463,
                'gameDate': '2024-06-01T18:05:00Z',
                'status': {'detailedState': 'Final'},
                'teams': {
                    'away': {'team': {'id': 147, 'name': 'New York Yankees'}},
                    'home': {'team': {'id': 117, 'name': 'Houston Astros'}},
                },
                'venue': {'id': 239, 'name': 'Minute Maid Park'},
                'content': {'link': '/api/v1/game/716463/content'},
            }],
        }],
    }
    client = make_client(data)
    schedule = client.schedule(date='2024-06-01')
    assert len(schedule.dates) == 1
    assert schedule.dates[0].games[0].game_pk == 716463
```

---

## Testing with `patch('requests.get')`

When no session is injected, `Client` falls back to `requests.get`, so you can
patch it globally:

```python
from unittest.mock import patch, MagicMock
from mlbapi import Client

def test_boxscore_calls_requests_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {'teams': {}, 'officials': [], 'info': []}

    with patch('requests.get', return_value=mock_response) as mock_get:
        Client().boxscore(716463)

    mock_get.assert_called_once()
```

---

## Testing the Context Manager

```python
from unittest.mock import patch, MagicMock
from mlbapi import Client

def test_context_manager_closes_session():
    with patch('requests.Session') as MockSession:
        mock_session = MockSession.return_value
        mock_session.headers = {}
        mock_session.get.return_value = MagicMock()
        mock_session.get.return_value.json.return_value = {}

        c = Client()
        with c:
            pass

        mock_session.close.assert_called_once()
    assert c._session is None
```

---

## `conftest.py` Pattern

For larger test suites, define fixtures in `conftest.py`:

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock
import requests
from mlbapi import Client

SCHEDULE_DATA = {
    'dates': [{'date': '2024-06-01', 'games': [...]}],
}

BOXSCORE_DATA = {
    'teams': {'away': {...}, 'home': {...}},
    'officials': [],
    'info': [],
}

@pytest.fixture
def mock_client(request):
    """Fixture that returns a Client pre-loaded with test data."""
    data = request.param if hasattr(request, 'param') else {}
    session = MagicMock(spec=requests.Session)
    response = MagicMock()
    response.json.return_value = data
    session.get.return_value = response
    return Client(session=session)
```

---

## Asserting URL and Params

```python
def test_schedule_sends_sport_id():
    session = MagicMock(spec=requests.Session)
    response = MagicMock()
    response.json.return_value = {'dates': []}
    session.get.return_value = response

    Client(session=session).schedule(date='2024-06-01')

    _, kwargs = session.get.call_args
    assert kwargs['params']['sportId'] == 1
```
