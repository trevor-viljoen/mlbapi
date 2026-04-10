# Client

`Client` is the sole public entry point for all MLB StatsAPI calls. Instantiate
once and reuse; it is thread-safe when an external session is injected.

---

## Constructor

```python
mlbapi.Client(
    base_url: str = 'https://statsapi.mlb.com/api',
    timeout: int | float | None = None,
    session: requests.Session | None = None,
)
```

| Parameter | Default | Description |
|---|---|---|
| `base_url` | `'https://statsapi.mlb.com/api'` | Override for proxies or local mirrors |
| `timeout` | `None` | HTTP timeout in seconds for every request |
| `session` | `None` | Inject a `requests.Session` (see below) |

---

## Basic Usage

```python
from mlbapi import Client

# Default — uses requests.get() for each call
client = Client()

# With timeout
client = Client(timeout=30)

# Custom base URL (proxy, local mock, etc.)
client = Client(base_url='https://my-proxy.example.com/api')
```

---

## Injecting a Session

Pass a `requests.Session` to add custom headers, authentication, retry
adapters, or to isolate tests without monkey-patching `requests.get`.

```python
import requests
from requests.adapters import HTTPAdapter, Retry
from mlbapi import Client

retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retry))

client = Client(session=session)
```

When you inject a session, `Client` will use it for all HTTP calls but will
**never close it** — lifetime management is your responsibility.

---

## Context Manager

Use the context manager when you want `Client` to manage its own session:

```python
from mlbapi import Client

with Client() as client:
    schedule = client.schedule(date='2024-06-01')
    box = client.boxscore(schedule.dates[0].games[0].game_pk)
# session is closed here
```

Rules:
- If you pass a `session=` at construction, the context manager will **not**
  close it on exit. Lifecycle is yours.
- If no session is passed, `__enter__` creates one and `__exit__` closes it.

---

## `__repr__`

```python
>>> Client()
Client(base_url='https://statsapi.mlb.com/api')

>>> Client(timeout=30)
Client(base_url='https://statsapi.mlb.com/api', timeout=30)

>>> Client(session=requests.Session())
Client(base_url='https://statsapi.mlb.com/api', session=<Session>)
```

---

## All Methods

| Method | Returns | Description |
|---|---|---|
| `client.schedule(**kwargs)` | `Schedule` | Game schedule |
| `client.boxscore(game_pk)` | `BoxScore` | Full box score |
| `client.linescore(game_pk)` | `LineScore` | Live linescore |
| `client.play_by_play(game_pk)` | `dict` | Play-by-play |
| `client.live_feed(game_pk)` | `dict` | Live feed (v1.1) |
| `client.live_diff(game_pk)` | `dict` | Live feed diff (v1.1) |
| `client.standings(**kwargs)` | `Standings` | League standings |
| `client.teams(**kwargs)` | `Teams` | Team information |
| `client.divisions(**kwargs)` | `Divisions` | Division information |
| `client.conferences(**kwargs)` | `dict` | Conference information |
| `client.seasons(**kwargs)` | `dict` | Season information |
| `client.venues(**kwargs)` | `dict` | Venue information |
| `client.draft(year)` | `dict` | Draft picks |
| `client.stats(**kwargs)` | `dict` | Player/team stats |
| `client.stats_leaders(**kwargs)` | `dict` | Stats leaders |
| `client.homerunderby(game_pk)` | `dict` | Home Run Derby |
| `client.attendance(**kwargs)` | `dict` | Attendance data |
| `client.awards(**kwargs)` | `dict` | Awards |
| `client.transactions(**kwargs)` | `dict` | Transactions |
| `client.get(path, **params)` | `dict` | Raw API access (any endpoint) |

See individual endpoint pages for full parameter lists.
