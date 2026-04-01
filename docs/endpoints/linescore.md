# Line Score

`client.linescore(game_pk, **kwargs)` → `LineScore`

Fetches the live linescore for a game from `/api/v1/game/{game_pk}/linescore`.
Best used for in-progress games; works on completed games too.

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `game_pk` | `int` | The game's primary key (required) |
| `timecode` | `str` | Return state at a specific point in time |
| `fields` | `str` | Comma-separated list of fields to return |

---

## Examples

```python
from mlbapi import Client

client = Client()
line = client.linescore(716463)
```

---

## Response Structure

### Count and Outs

```python
print(line.current_inning)         # 9
print(line.current_inning_ordinal) # '9th'
print(line.inning_half)            # 'Bottom'
print(line.balls)                  # 2
print(line.strikes)                # 1
print(line.outs)                   # 2
```

### Current Players (in-progress games)

```python
# Batter and pitcher
print(line.offense.batter.full_name)   # current batter
print(line.defense.pitcher.full_name)  # current pitcher

# Baserunners
if line.offense.first:
    print(f'Runner on first: {line.offense.first.full_name}')
if line.offense.second:
    print(f'Runner on second: {line.offense.second.full_name}')
if line.offense.third:
    print(f'Runner on third: {line.offense.third.full_name}')
```

### By-Inning Breakdown

```python
for inning in line.innings:
    print(
        f'Inning {inning.num}: '
        f'Away {inning.away.runs} — Home {inning.home.runs}'
    )

# Totals
print(line.teams.away.runs, line.teams.away.hits, line.teams.away.errors)
print(line.teams.home.runs, line.teams.home.hits, line.teams.home.errors)
```

### Formatted Summary

```python
print(
    f'{line.inning_half} of the {line.current_inning_ordinal} — '
    f'{line.offense.batter.full_name} facing {line.defense.pitcher.full_name}. '
    f'Count: {line.balls}-{line.strikes}, {line.outs} out(s).'
)
```
