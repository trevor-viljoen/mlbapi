# Standings

`client.standings(**kwargs)` → `Standings`

Fetches standings from `/api/v1/standings`.

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `standings_type` | `str` | Type of standings: `regularSeason`, `wildCard`, `divisionLeaders`, etc. |
| `league_id` | `int \| list[int]` | League(s) to fetch — `103` (AL), `104` (NL), or `[103, 104]` |
| `season` | `str` | Season year, e.g. `'2024'` |
| `date` | `str` | Standings as of a specific date `YYYY-MM-DD` |
| `hydrate` | `str` | Additional data (e.g. `'team'`, `'division'`) |
| `fields` | `str` | Comma-separated fields to return |

---

## Examples

```python
from mlbapi import Client

client = Client()

# Current AL + NL standings
standings = client.standings(league_id=[103, 104])

# AL only, specific season
standings = client.standings(league_id=103, season='2023')

# Standings on a specific date
standings = client.standings(league_id=[103, 104], date='2024-08-01')

# Wild card standings
standings = client.standings(standings_type='wildCard', league_id=103)
```

---

## Response Structure

```python
standings = client.standings(league_id=[103, 104])

for record in standings.records:
    print(f'\n{record.division.name}')
    print(f'{"Team":30s}  W    L    PCT')
    print('-' * 50)

    for tr in record.team_records:
        print(
            f'{tr.team.name:30s}  '
            f'{tr.wins:<4} {tr.losses:<4} {tr.winning_percentage}'
        )
```

### Team Record Fields

```python
tr = standings.records[0].team_records[0]

tr.team.name           # 'New York Yankees'
tr.wins                # 95
tr.losses              # 67
tr.winning_percentage  # '.586'
tr.games_back          # '-'  or  '3.0'
tr.wild_card_gb        # wild card games behind
tr.streak.streak_code  # 'W3'  (three-game winning streak)
tr.league_record.wins
tr.league_record.losses
tr.league_record.pct
```
