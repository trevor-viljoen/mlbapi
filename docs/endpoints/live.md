# Live Feed

The live feed endpoints return real-time game state from the MLB StatsAPI's
v1.1 feed. Responses are raw dicts — no Pydantic wrapper — because the payload
is extremely large and the schema changes frequently.

---

## `client.live_feed(game_pk)`

Full live game feed from `/api/v1.1/game/{game_pk}/feed/live`.

```python
from mlbapi import Client

client = Client()
feed = client.live_feed(716463)

# Game data
print(feed['gameData']['status']['detailedState'])
print(feed['gameData']['teams']['away']['name'])

# Live play data
plays = feed['liveData']['plays']
current_play = plays.get('currentPlay', {})
print(current_play.get('result', {}).get('description'))

# All plays
for play in plays.get('allPlays', []):
    result = play.get('result', {})
    if result.get('eventType') == 'home_run':
        print(result.get('description'))
```

---

## `client.live_diff(game_pk, start_timecode, end_timecode)`

Diff patch between two timepoints from `/api/v1.1/game/{game_pk}/feed/live/diffPatch`.

Use this to efficiently poll for changes during a live game rather than
refetching the full feed:

```python
client = Client()

# Initial fetch
feed = client.live_feed(game_pk)
last_timecode = feed['metaData']['timeStamp']

# Poll for changes
import time
while True:
    time.sleep(5)
    new_feed = client.live_feed(game_pk)
    new_timecode = new_feed['metaData']['timeStamp']

    if new_timecode != last_timecode:
        diff = client.live_diff(game_pk, last_timecode, new_timecode)
        # apply diff to your local state
        last_timecode = new_timecode
```

---

## `client.play_by_play(game_pk)`

Play-by-play from `/api/v1/game/{game_pk}/playByPlay`. Returns all plays in
a structured format:

```python
client = Client()
pbp = client.play_by_play(716463)

for play in pbp.get('allPlays', []):
    result = play.get('result', {})
    about = play.get('about', {})
    print(
        f'Inning {about.get("inning")} '
        f'({about.get("halfInning")}): '
        f'{result.get("description")}'
    )
```
