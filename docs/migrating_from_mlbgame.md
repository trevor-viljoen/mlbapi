# Migrating from mlbgame

[mlbgame](https://github.com/panzarino/mlbgame) parsed MLB's legacy XML GameDay
feed, which is no longer maintained. `mlbapi` wraps the current JSON StatsAPI
(`statsapi.mlb.com/api/v1`). The two libraries cover similar ground but the
underlying data sources and object shapes are different enough that there is no
mechanical shim — this guide walks you through the conceptual mapping.

---

## Installation

```bash
pip install mlbapi
```

---

## Key differences

| | mlbgame | mlbapi |
|---|---|---|
| Data source | Legacy XML GameDay feed | JSON StatsAPI (`statsapi.mlb.com`) |
| Entry point | Module-level functions (`mlbgame.day(...)`) | `Client` instance (`client.schedule(...)`) |
| Game identifier | String `game_id` (`gid_2024_06_01_...`) | Integer `game_pk` (e.g. `745453`) |
| Object model | Custom attribute objects | Pydantic v2 models |

### The game ID change

This is the most disruptive difference. mlbgame used string IDs derived from
the GameDay feed path (e.g. `gid_2015_04_12_kcamlb_anamlb_1`). mlbapi uses
the integer `game_pk` from the StatsAPI.

To find a `game_pk`, query the schedule and read it off the returned game object:

```python
from mlbapi import Client

client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)
for date in schedule.dates:
    for game in date.games:
        print(game.game_pk, game.teams.away.team.name, 'vs', game.teams.home.team.name)
```

---

## Function mapping

### Games for a day — `mlbgame.day()` / `mlbgame.games()`

```python
# mlbgame
import mlbgame
games = mlbgame.day(2024, 6, 1, home='Yankees')
all_june = mlbgame.combine_games(mlbgame.games(2024, 6, home='Yankees'))

# mlbapi — single day
client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)

# mlbapi — date range (replaces games() + combine_games())
schedule = client.schedule(start_date='2024-06-01', end_date='2024-06-30', team_id=147)
for date in schedule.dates:
    for game in date.games:
        print(game)
```

`combine_games()` is not needed — `schedule.dates` is a flat list of date
objects each containing a `games` list. Iterate both levels.

---

### Box score — `mlbgame.box_score()`

```python
# mlbgame
box = mlbgame.box_score(game_id)

# mlbapi
box = client.boxscore(game_pk)
```

---

### Game overview / linescore — `mlbgame.overview()`

```python
# mlbgame
overview = mlbgame.overview(game_id)

# mlbapi
linescore = client.linescore(game_pk)
```

---

### Play-by-play / game events — `mlbgame.game_events()`

```python
# mlbgame
events = mlbgame.game_events(game_id)

# mlbapi — structured play-by-play
pbp = client.play_by_play(game_pk)

# mlbapi — full live feed with richer context
feed = client.live_feed(game_pk)
```

---

### Player and team stats — `mlbgame.player_stats()` / `mlbgame.team_stats()`

```python
# mlbgame
stats = mlbgame.player_stats(game_id)
team  = mlbgame.team_stats(game_id)

# mlbapi — both are inside the box score
box = client.boxscore(game_pk)
# box.teams.home.players  — dict of player stat lines
# box.teams.home.teamStats — team-level totals

# or from the live feed
feed = client.live_feed(game_pk)
```

---

### Teams — `mlbgame.teams()`

```python
# mlbgame
teams = mlbgame.teams()

# mlbapi
teams = client.teams()
for team in teams.teams:
    print(team.id, team.name)
```

---

### Standings — `mlbgame.standings()`

```python
# mlbgame
standings = mlbgame.standings()

# mlbapi
standings = client.standings()
for record in standings.records:
    for entry in record.team_records:
        print(entry.team.name, entry.wins, entry.losses)
```

---

### Roster — `mlbgame.roster()`

There is no dedicated `client.roster()` method yet. Use `client.get()` directly:

```python
# mlbgame
roster = mlbgame.roster(team_id)

# mlbapi
data = client.get('/v1/teams/147/roster', season=2024)
for player in data['roster']:
    print(player['person']['fullName'], player['jerseyNumber'])

# Roster types: 'active', '40Man', 'fullRoster', 'depthChart', 'coach'
data = client.get('/v1/teams/147/roster/40Man', season=2024)
```

---

### Broadcast information — `mlbgame.broadcast_info()`

Broadcast data is available as a hydration on the schedule endpoint, returned
per game:

```python
# mlbgame
info = mlbgame.broadcast_info(team_id, date)

# mlbapi
schedule = client.schedule(date='2024-06-01', team_id=147, hydrate='broadcasts')
for date in schedule.dates:
    for game in date.games:
        for broadcast in getattr(game, 'broadcasts', []):
            print(broadcast.get('name'), broadcast.get('type'), broadcast.get('homeAway'))
```

---

### Important dates — `mlbgame.important_dates()`

Season key dates (opening day, all-star, postseason start, etc.) are available
from the seasons endpoint:

```python
# mlbgame
dates = mlbgame.important_dates(2024)

# mlbapi
seasons = client.seasons(season=2024, sport_id=1, with_game_type_dates=True)
s = seasons.seasons[0]
print('Opening day:      ', s.regular_season_start_date)
print('All-Star:         ', s.all_star_date)
print('Postseason start: ', s.post_season_start_date)
print('Season end:       ', s.season_end_date)
```

---

### Players — `mlbgame.players()`

```python
# mlbgame — players/coaches/umpires for a specific game
players = mlbgame.players(game_id)

# mlbapi — player lookup by ID
person = client.person(660271)
print(person.people[0].full_name)

# search by name
results = client.people_search('Ohtani')
for p in results.people:
    print(p.id, p.full_name)
```

Umpires for a specific game are included in the box score:

```python
box = client.boxscore(game_pk)
for umpire in box.officials:
    print(umpire.official.full_name, umpire.official_type)
```

---

### League info — `mlbgame.league()`

The StatsAPI exposes league information through the schedule, standings, and
teams endpoints via hydrations and filters. There is no direct `league()`
equivalent yet; use `client.get()` for raw access:

```python
data = client.get('/v1/league', leagueIds='103,104')
```

---

### Injuries — `mlbgame.injury()`

Injured list placements and returns are available through the transactions
endpoint. IL moves come through with type code `SC` (status change):

```python
# mlbgame
injuries = mlbgame.injury()

# mlbapi — filter transactions for IL-related status changes
from mlbapi import Client

client = Client()
txs = client.transactions(sport_id=1, start_date='2024-06-01', end_date='2024-06-30')
il_moves = [
    t for t in txs.transactions
    if t.type_code == 'SC' and 'injured list' in (t.description or '').lower()
]
for move in il_moves:
    print(move.description)
```

This covers placements, activations, and transfers between IL stints (10-day,
15-day, 60-day). mlbgame's `injury()` returned a snapshot of the current IL;
the transactions approach requires filtering a date range instead.

---

## Raw API access

For anything not yet wrapped by a dedicated method, use `client.get()`:

```python
client = Client()
data = client.get('/v1/teams/147/coaches', season=2024)
data = client.get('/v1/teams/147/alumni', season=2024, group='hitting')
data = client.get('/v1/league', leagueIds='103,104')
```
