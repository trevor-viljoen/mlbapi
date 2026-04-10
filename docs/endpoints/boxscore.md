# Box Score

`client.boxscore(game_pk, **kwargs)` → `BoxScore`

Fetches the full box score for a game from `/api/v1/game/{game_pk}/boxscore`.

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `game_pk` | `int` | The game's primary key (required) |
| `fields` | `str` | Comma-separated list of fields to return |
| `timecode` | `str` | Return state at a specific point in time |

---

## Examples

```python
from mlbapi import Client

client = Client()
box = client.boxscore(716463)
```

---

## Response Structure

### Teams

```python
box.teams.away.team.name       # 'New York Yankees'
box.teams.home.team.name       # 'Houston Astros'

# Team batting stats
batting = box.teams.away.team_stats.batting
print(batting.runs)
print(batting.hits)
print(batting.home_runs)
print(batting.strike_outs)
print(batting.model_dump())    # full dict

# Team pitching stats
pitching = box.teams.home.team_stats.pitching
print(pitching.earned_runs)
print(pitching.strike_outs)
```

### Players (Batters and Pitchers)

```python
# Player batting order
for batter_id in box.teams.away.batters:
    player = box.teams.away.players[f'ID{batter_id}']
    print(player.person.full_name)
    print(player.stats.batting.hits, player.stats.batting.at_bats)

# Pitchers used
for pitcher_id in box.teams.away.pitchers:
    player = box.teams.away.players[f'ID{pitcher_id}']
    print(player.person.full_name)
    print(player.stats.pitching.innings_pitched)
```

### Game Info (Weather, Attendance, etc.)

```python
for item in box.info:
    print(item.label, '-', item.value)
# e.g. 'Weather - 72° F, Sunny'
#      'Wind - 12 mph, Out To CF'
#      'Att - 42,318'
```

### Officials (Umpires)

```python
for official in box.officials:
    print(official.official_type, official.official.full_name)
# e.g. 'Home Plate  John Doe'
```

---

## Getting `game_pk` from Schedule

```python
client = Client()
schedule = client.schedule(date='2024-06-01', team_id=147)
game_pk = schedule.dates[0].games[0].game_pk
box = client.boxscore(game_pk)
```
