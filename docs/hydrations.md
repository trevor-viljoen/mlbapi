# Hydrations

The MLB StatsAPI supports a `hydrate` parameter on many endpoints. A hydration
instructs the API to embed additional sub-resources inline in the response,
saving round-trips you would otherwise need to make separately.

```python
# Without hydration — venue is just a reference {id, name, link}
schedule = client.schedule(date='2024-06-01', team_id=147)

# With hydration — venue object includes full address, coordinates, capacity
schedule = client.schedule(date='2024-06-01', team_id=147, hydrate='venue')
```

Hydrations are passed as a plain string. Multiple hydrations are
comma-separated. Some hydrations accept arguments in parentheses.

---

## Schedule

Endpoint: `client.schedule(**kwargs)`

### Broadcasts

Embed TV and radio broadcast information for each game.

```python
schedule = client.schedule(date='2024-06-01', team_id=147, hydrate='broadcasts')

for date in schedule.dates:
    for game in date.games:
        for broadcast in getattr(game, 'broadcasts', []):
            print(broadcast['name'], broadcast['type'], broadcast['homeAway'])
# WFAN 660/101.9 FM FM away
# YES TV home
# WADO 1280 AM away
```

### Linescore

Embed the current linescore (score by inning, count, outs) in the schedule
response — useful for building a scoreboard without a second request per game.

```python
schedule = client.schedule(date='2024-06-01', team_id=147, hydrate='linescore')

for date in schedule.dates:
    for game in date.games:
        ls = getattr(game, 'linescore', None)
        if ls:
            print(ls['currentInningOrdinal'], ls['inningState'])
```

### Probable Pitchers

```python
schedule = client.schedule(
    date='2024-06-01', team_id=147, hydrate='probablePitcher'
)

for date in schedule.dates:
    for game in date.games:
        home = game.teams.home
        away = game.teams.away
        home_sp = getattr(home, 'probable_pitcher', None)
        away_sp = getattr(away, 'probable_pitcher', None)
        print(
            f'{away.team.name}: {away_sp.full_name if away_sp else "TBD"}'
            f'  vs  '
            f'{home.team.name}: {home_sp.full_name if home_sp else "TBD"}'
        )
```

### Venue

```python
schedule = client.schedule(date='2024-06-01', team_id=147, hydrate='venue')

for date in schedule.dates:
    for game in date.games:
        print(getattr(game, 'venue', {}).get('name'))
# Oracle Park
```

### Team with nested league

Hydrations can be nested using parentheses to pull sub-resources into the
hydrated object.

```python
schedule = client.schedule(
    date='2024-06-01', team_id=147, hydrate='team(league)'
)

for date in schedule.dates:
    for game in date.games:
        team = game.teams.home.team
        print(team.name, getattr(team, 'league', {}).get('name'))
# San Francisco Giants  National League
```

### Combining hydrations

Pass a comma-separated string to request multiple hydrations at once.

```python
schedule = client.schedule(
    date='2024-06-01',
    team_id=147,
    hydrate='linescore,broadcasts,venue,probablePitcher',
)
```

---

## People / Person

Endpoint: `client.person(person_id)` · `client.people(person_ids)`

### Career stats

Stats hydrations use the format `stats(group=[…],type=[…])`.

```python
# Career regular season hitting stats
person = client.person(
    660271,
    hydrate='stats(group=[hitting],type=[careerRegularSeason])',
)
splits = person.people[0].stats[0]['splits']
career = splits[0]['stat']
print(career['homeRuns'], career['avg'], career['ops'])
# 407 .306 .997

# Single season pitching stats
person = client.person(
    592789,
    hydrate='stats(group=[pitching],type=[season],season=2024)',
)
```

Available `group` values: `hitting`, `pitching`, `fielding`

Common `type` values: `season`, `careerRegularSeason`, `careerStatSplits`,
`gameLog`, `lastXGames`, `byDateRange`

### Current team

```python
person = client.person(660271, hydrate='currentTeam')
print(person.people[0].current_team.name)
# Los Angeles Dodgers
```

### Awards

```python
person = client.person(660271, hydrate='awards')
for award in getattr(person.people[0], 'awards', []):
    print(award.get('award', {}).get('name'), award.get('season'))
```

### Draft info

```python
person = client.person(660271, hydrate='draft')
print(person.people[0].draft_year)
```

### Combining people hydrations

```python
person = client.person(
    660271,
    hydrate='currentTeam,awards,stats(group=[hitting],type=[careerRegularSeason])',
)
```

---

## Teams

Endpoint: `client.teams(**kwargs)`

### League and division

```python
teams = client.teams(team_id=147, hydrate='league,division,venue')
team = teams.teams[0]
print(team.league.name)     # American League
print(team.division.name)   # American League East
print(team.venue.name)      # Yankee Stadium
```

---

## Venues

Endpoint: `client.venues(**kwargs)`

### Location

Full address and GPS coordinates.

```python
venues = client.venues(venue_ids=3313, hydrate='location')
loc = venues.venues[0].location
print(loc.address1, loc.city, loc.state)
# One East 161st Street  Bronx  New York
print(loc.default_coordinates.latitude, loc.default_coordinates.longitude)
# 40.82919482  -73.9264977
```

### Field dimensions

```python
venues = client.venues(venue_ids=3313, hydrate='fieldInfo')
fi = venues.venues[0].field_info
print(fi.capacity, fi.turf_type, fi.roof_type)
print(f'LF: {fi.left_line}  CF: {fi.center}  RF: {fi.right_line}')
```

### Timezone

```python
venues = client.venues(venue_ids=3313, hydrate='timezone')
tz = venues.venues[0].time_zone
print(tz.id, tz.offset)
# America/New_York  -4
```

---

## Stats leaders

Endpoint: `client.stats_leaders(**kwargs)`

### Embed person and team

```python
leaders = client.stats_leaders(
    leader_categories='homeRuns',
    season=2024,
    sport_id=1,
    hydrate='person,team',
)
for leader in leaders.league_leaders[0].leaders[:5]:
    print(leader.person.full_name, leader.team.name, leader.value)
# Aaron Judge  New York Yankees  58
```

---

## Raw access

For endpoints or hydration values not yet modelled, access the raw dict
directly through `client.get()`:

```python
data = client.get(
    '/v1/schedule',
    sportId=1,
    date='2024-06-01',
    hydrate='decisions,weather,flags',
)
```

---

## Finding valid hydrations

The MLB StatsAPI does not publish a complete list of valid hydrations per
endpoint. The best discovery approaches are:

1. **Trial and error** — unsupported hydrations are silently ignored or return
   an error message in the response
2. **The meta endpoint** — `client.meta('hydrations')` may list known values
   depending on the API version
3. **Third-party swagger docs** —
   [joerex1418/mlb-statsapi-swagger-docs](https://github.com/joerex1418/mlb-statsapi-swagger-docs)
   documents many hydration options per endpoint
