# Raw Access

mlbapi's two-layer design means you always have access to the raw JSON data
alongside the Pydantic model wrapper.

---

## `client.get()` — Any Endpoint, Raw Dict

For endpoints without a dedicated method, or when you need the raw JSON:

```python
from mlbapi import Client

client = Client()

# Get sports list
data = client.get('/v1/sports')

# Person bio with hydration
data = client.get('/v1/people/660271', hydrate='stats(group=[hitting],type=[career])')

# Absolute URL also works
data = client.get('https://statsapi.mlb.com/api/v1/sports')
```

Parameters passed as keyword arguments are forwarded as query-string params
**without camelCase conversion** — use the API's native parameter names.

---

## `model.model_dump()` — Model → Dict

Every Pydantic model exposes `model_dump()`:

```python
client = Client()
box = client.boxscore(716463)

# Full dict
d = box.model_dump()

# Only specific fields
d = box.model_dump(include={'teams', 'info'})

# Reconstruct camelCase keys (as the API returns them)
d = box.model_dump(by_alias=True)
```

---

## Accessing Extra Fields

All models use `extra="allow"`, so unknown API keys are accessible as
attributes even if they have no declared field:

```python
box = client.boxscore(716463)

# If the API adds a new field 'newField', it becomes:
print(box.new_field)  # auto-normalised to snake_case
```

---

## When to Use Raw Access

- Calling an endpoint that doesn't have a dedicated `Client` method yet
- Accessing a field that is not mapped by any model
- Passing the data to another library that expects plain dicts
- Debugging: comparing the model's output against the actual API response

```python
client = Client()

# Raw API response
raw = client.get('/v1/game/716463/boxscore')

# Pydantic model
box = client.boxscore(716463)

# They represent the same data; raw gives you the camelCase original
assert raw['teams']['away']['team']['name'] == box.teams.away.team.name
```
