# Divisions

`client.divisions(**kwargs)` → `Divisions`

Fetches division information from `/api/v1/divisions`.

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `division_id` | `int` | A specific division ID |
| `league_id` | `int` | Filter by league (`103` AL, `104` NL) |
| `sport_id` | `int` | Sport ID (default: `1` for MLB) |
| `fields` | `str` | Comma-separated fields to return |

---

## Examples

```python
from mlbapi import Client

client = Client()

# All MLB divisions
divisions = client.divisions()

# AL divisions only
divisions = client.divisions(league_id=103)

# Specific division
divisions = client.divisions(division_id=201)  # AL East
```

---

## Response Structure

```python
divisions = client.divisions()

for div in divisions.divisions:
    print(div.id)
    print(div.name)         # 'American League East'
    print(div.abbreviation) # 'ALE'
    print(div.league.id)    # 103
    print(div.sport.id)     # 1
```

---

## Division IDs

| Division | ID |
|---|---|
| AL East | 201 |
| AL Central | 202 |
| AL West | 200 |
| NL East | 204 |
| NL Central | 205 |
| NL West | 203 |
