# mlbapi

[![PyPI version](https://img.shields.io/pypi/v/mlbapi.svg)](https://pypi.org/project/mlbapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/mlbapi.svg)](https://pypi.org/project/mlbapi/)
[![License](https://img.shields.io/github/license/trevor-viljoen/mlbapi.svg)](https://github.com/trevor-viljoen/mlbapi/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/trevor-viljoen/mlbapi?style=social)](https://github.com/trevor-viljoen/mlbapi/stargazers)

**mlbapi** is a Python 3 client for the [MLB StatsAPI](https://statsapi.mlb.com/) — the data source that powers MLB.com's live game data, box scores, standings, and more.

All responses are returned as validated Pydantic models, so you get attribute access, type safety, and IDE autocompletion with no JSON parsing required.

---

## Installation

```bash
pip install mlbapi
```

Requires Python 3.10+ and `pydantic >= 2.0`.

---

## Quick Start

Everything goes through a `Client` instance.

```python
from mlbapi import Client

client = Client()
```

### Schedule

```python
from mlbapi import Client

client = Client()

# Single date
schedule = client.schedule(date='2024-06-01', team_id=117)

# Date range
schedule = client.schedule(
    start_date='2024-04-01',
    end_date='2024-10-01',
    team_id=117,
)

for date in schedule.dates:
    for game in date.games:
        print(game.game_pk, game.status.detailed_state)
```

### Box Score

```python
from mlbapi import Client

client = Client()

schedule = client.schedule(date='2024-06-01', team_id=117)
game_pk = schedule.dates[0].games[0].game_pk

box = client.boxscore(game_pk)

# Team batting stats
print(box.teams.away.team.name)
print(box.teams.away.team_stats.batting.model_dump())

# Game info (weather, attendance, etc.)
for item in box.info:
    print(item.info)
```

### Linescore

```python
from mlbapi import Client

client = Client()

schedule = client.schedule(date='2024-06-01', team_id=117)
game_pk = schedule.dates[0].games[0].game_pk

line = client.linescore(game_pk)

print(
    f'{line.inning_half} of the {line.current_inning_ordinal} — '
    f'{line.offense.batter.full_name} facing {line.defense.pitcher.full_name}. '
    f'Count: {line.balls}-{line.strikes}, {line.outs} out(s).'
)
```

### Standings

```python
from mlbapi import Client

client = Client()

standings = client.standings(league_id=[103, 104])  # AL + NL

for record in standings.records:
    for tr in record.team_records:
        print(f'{tr.team.name:30s}  {tr.wins}-{tr.losses}  {tr.winning_percentage}')
```

---

## Configuration

### Timeout

```python
client = Client(timeout=30)
```

### Custom Session (retries, proxy, headers)

```python
import requests
from requests.adapters import HTTPAdapter, Retry

retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retry))

client = Client(session=session)
```

### Context Manager

Use the context manager when you want the client to manage its own session lifecycle:

```python
from mlbapi import Client

with Client() as client:
    schedule = client.schedule(date='2024-06-01')
    box = client.boxscore(schedule.dates[0].games[0].game_pk)
```

The session is opened on `__enter__` and closed on `__exit__`.

---

## Error Handling

All exceptions inherit from `mlbapi.MLBAPIException`.

```python
from mlbapi import Client, ParameterException, ObjectNotFoundException, RequestException

client = Client()

try:
    box = client.boxscore(716463)
except ParameterException as e:
    print(f'Bad parameter: {e}')
except ObjectNotFoundException as e:
    print(f'Not found: {e}')
except RequestException as e:
    print(f'Network error: {e}')
```

| Exception | Raised when |
|---|---|
| `ParameterException` | An invalid kwarg is passed to an endpoint method |
| `ObjectNotFoundException` | The API returned an error message (bad ID, etc.) |
| `RequestException` | An HTTP/network error occurred |
| `ImplementationException` | An unsupported endpoint was requested |

---

## Available Methods

| Method | Description |
|---|---|
| `client.schedule(**kwargs)` | Game schedule by date/team/sport |
| `client.boxscore(game_pk)` | Full box score for a game |
| `client.linescore(game_pk)` | Live linescore (count, bases, pitcher/batter) |
| `client.play_by_play(game_pk)` | Play-by-play data |
| `client.live_diff(game_pk)` | Live feed diff/patch (v1.1) |
| `client.standings(**kwargs)` | League standings |
| `client.teams(**kwargs)` | Team information |
| `client.divisions(**kwargs)` | Division information |
| `client.conferences(**kwargs)` | Conference information |
| `client.seasons(**kwargs)` | Season information |
| `client.all_seasons(**kwargs)` | All seasons |
| `client.venues(**kwargs)` | Venue information |
| `client.draft(year)` | Draft picks for a year |
| `client.draft_prospects(**kwargs)` | Draft prospects |
| `client.draft_latest(year)` | Latest draft picks |
| `client.stats(**kwargs)` | Player/team stats |
| `client.stats_leaders(**kwargs)` | Stats leaders |
| `client.stats_streaks(**kwargs)` | Stats streaks |
| `client.homerunderby(game_pk)` | Home Run Derby data |
| `client.attendance(**kwargs)` | Attendance data |
| `client.awards(**kwargs)` | Awards |
| `client.award_recipients(award_id)` | Recipients for an award |
| `client.jobs(**kwargs)` | Job listings |
| `client.umpires(**kwargs)` | Umpire roster |
| `client.transactions(**kwargs)` | Transaction data |
| `client.meta(meta_type)` | Lookup table values |

---

## Team IDs

| Team | ID | Team | ID |
|---|---|---|---|
| Yankees | 147 | Dodgers | 119 |
| Red Sox | 111 | Giants | 137 |
| Astros | 117 | Cubs | 112 |
| Braves | 144 | Cardinals | 138 |
| Mets | 121 | Padres | 135 |

Full list: `client.teams()`

---

## Migrating from mlbgame

Coming from [panzarino/mlbgame](https://github.com/panzarino/mlbgame)? See the [migration guide](docs/migrating_from_mlbgame.md) for a function-by-function mapping.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request. Bug reports and feature requests can be filed as [GitHub Issues](https://github.com/trevor-viljoen/mlbapi/issues).

---

## Support the Project

If `mlbapi` saves you time, consider supporting its development:

- ⭐ **Star this repo** — it helps others discover the project
- 💛 **[Sponsor on GitHub](https://github.com/sponsors/trevor-viljoen)**
- ☕ **[Donate via PayPal](https://paypal.me/trevorviljoen)**

---

## License

This project is licensed under the terms found in [LICENSE](LICENSE).

---

## Disclaimer

This library is not affiliated with or endorsed by Major League Baseball or MLB Advanced Media. Use of the MLB StatsAPI is subject to [MLB's terms of service](https://www.mlb.com/official-information/terms-of-use).
