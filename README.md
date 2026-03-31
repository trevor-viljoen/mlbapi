# mlbapi

[![PyPI version](https://img.shields.io/pypi/v/mlbapi.svg)](https://pypi.org/project/mlbapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/mlbapi.svg)](https://pypi.org/project/mlbapi/)
[![License](https://img.shields.io/github/license/trevor-viljoen/mlbapi.svg)](https://github.com/trevor-viljoen/mlbapi/blob/dev/LICENSE)
[![Stars](https://img.shields.io/github/stars/trevor-viljoen/mlbapi?style=social)](https://github.com/trevor-viljoen/mlbapi/stargazers)

**mlbapi** is a Python library that provides Pythonic bindings for [MLB Advanced Media's StatsAPI](https://statsapi.mlb.com/) — the same data source that powers MLB.com's live game data, box scores, standings, and more.

Unlike raw API calls, `mlbapi` returns structured Python objects so you can work with MLB data naturally in your code.

-----

## Features

- Schedule lookups by team and date range
- Box score data including batting and pitching stats
- Live linescore data (inning, batter, pitcher, count)
- Structured Python objects from every endpoint — no manual JSON parsing
- Lightweight: only requires `requests`

-----

## Installation

```bash
pip install mlbapi
```

-----

## Quick Start

### Get a team's schedule for a date range

```python
import mlbapi

# Houston Astros schedule for the 2024 season
schedule = mlbapi.schedule(start_date='04/01/2024', end_date='10/01/2024', team_id=117)
```

### Get a team's schedule for a single date

```python
import mlbapi

schedule = mlbapi.schedule(date='04/01/2024', team_id=117)
```

### Get box score data for a game

```python
import mlbapi

schedule = mlbapi.schedule(date='04/01/2024', team_id=117)
game_pk = schedule.dates[0].games[0].game_pk
boxscore = mlbapi.boxscore(game_pk)

# Print all game info (weather, attendance, venue, etc.)
for info in boxscore.info:
    print(info.info)

# Print batting stats for both teams
print(boxscore.teams.away.team_stats.batting.__dict__)
print(boxscore.teams.home.team_stats.batting.__dict__)
```

### Get live linescore data

```python
import mlbapi

schedule = mlbapi.schedule(date='04/01/2024', team_id=117)
game_pk = schedule.dates[0].games[0].game_pk
line = mlbapi.linescore(game_pk)

output = '{} of the {}, {} facing {}. {} ball(s), {} strike(s), {} out(s)'
print(output.format(
    line.inning_half,
    line.current_inning_ordinal,
    line.offense.batter.full_name,
    line.defense.pitcher.full_name,
    line.balls,
    line.strikes,
    line.outs
))
# Top of the 9th, Scott Van Slyke facing Framber Valdez. 0 ball(s), 3 strike(s), 3 out(s)
```

-----

## Team IDs

Common MLB team IDs for reference:

|Team   |ID |Team     |ID |
|-------|---|---------|---|
|Yankees|147|Dodgers  |119|
|Red Sox|111|Giants   |137|
|Astros |117|Cubs     |112|
|Braves |144|Cardinals|138|
|Mets   |121|Padres   |135|

A full list is available via `mlbapi.teams()`.

-----

## Documentation

Full documentation and endpoint reference coming soon. In the meantime, feel free to [open an issue](https://github.com/trevor-viljoen/mlbapi/issues) with questions.

-----

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request. Bug reports and feature requests can be filed as [GitHub Issues](https://github.com/trevor-viljoen/mlbapi/issues).

-----

## Support the Project

If `mlbapi` saves you time, consider supporting its development:

- ⭐ **Star this repo** — it helps others discover the project
- 💛 **[Sponsor on GitHub](https://github.com/sponsors/trevor-viljoen)**
- ☕ **[Donate via PayPal](https://paypal.me/trevorviljoen)**

-----

## License

This project is licensed under the terms found in [LICENSE](LICENSE).

-----

## Disclaimer

This library is not affiliated with or endorsed by Major League Baseball or MLB Advanced Media. Use of the MLB StatsAPI is subject to [MLB's terms of service](https://www.mlb.com/official-information/terms-of-use).
