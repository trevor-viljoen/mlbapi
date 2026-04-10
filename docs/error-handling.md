# Error Handling

All exceptions inherit from `mlbapi.MLBAPIException`.

## Exception Hierarchy

```
MLBAPIException
├── RequestException        — HTTP/network failure
├── ImplementationException — Unsupported endpoint requested
├── ObjectNotFoundException — API returned an error message (bad game_pk, etc.)
└── ParameterException      — Invalid kwargs passed to an endpoint method
```

---

## Importing Exceptions

```python
from mlbapi import (
    MLBAPIException,
    ParameterException,
    ObjectNotFoundException,
    RequestException,
    ImplementationException,
)
```

---

## `ParameterException`

Raised when you pass a kwarg that isn't in the endpoint's valid-params list.

```python
from mlbapi import Client, ParameterException

client = Client()

try:
    schedule = client.schedule(typo_param='2024-06-01')
except ParameterException as e:
    print(f'Bad parameter: {e}')
```

This catches typos early — before any network request is made.

---

## `ObjectNotFoundException`

Raised when the API returns an error message, typically for a bad ID.

```python
from mlbapi import Client, ObjectNotFoundException

client = Client()

try:
    box = client.boxscore(999999999)  # bad game_pk
except ObjectNotFoundException as e:
    print(f'Not found: {e}')
```

---

## `RequestException`

Raised on any network or HTTP error (wraps `requests.exceptions.RequestException`).

```python
from mlbapi import Client, RequestException

client = Client(timeout=5)

try:
    schedule = client.schedule(date='2024-06-01')
except RequestException as e:
    print(f'Network error: {e}')
```

---

## Catching All mlbapi Errors

```python
from mlbapi import Client, MLBAPIException

client = Client()

try:
    box = client.boxscore(716463)
except MLBAPIException as e:
    print(f'mlbapi error ({type(e).__name__}): {e}')
```

---

## Schedule Validation Errors

The `schedule()` method validates parameter combinations before making a
network call:

```python
# These all raise ParameterException immediately:

# start_date without end_date
client.schedule(start_date='2024-04-01')

# end_date without start_date
client.schedule(end_date='2024-10-01')

# opponent_id without team_id (no meaning without a home team)
client.schedule(opponent_id=147)
```
