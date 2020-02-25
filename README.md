[![Join Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://pymlbapi-slack-invite.herokuapp.com/)

mlbapi v0.0.1 - python bindings for MLBAM's StatsAPI-based JSON API endpoints
mlbapi's data classes will return raw json data from the MLBAM's statsapi.
mlbapi's in `__init__.py` will return python objects from this data.

Examples
--------
Get the schedule for a given team during a given timeframe:

```python
import mlbapi

astros_schedule = mlbapi.schedule(start_date='04/01/2018', end_date='11/01/2018', team_id=117)
```

Get the schedule for a given team for a given date:

```python
import mlbapi

astros_schedule = mlbapi.schedule(date='03/05/2018', team_id=117)
```

Get the game info such as attendance, weather, wind, and venue for a given game:

```python
import mlbapi

astros_schedule = mlbapi.schedule(date='03/05/2018', team_id=117)

game_pk = astros_schedule.dates[0].games[0].game_pk
boxscore = mlbapi.boxscore(game_pk)

for info in boxscore.info:
    print(info.info)

print(boxscore.teams.away.team_stats.batting.__dict__)
print(boxscore.teams.home.team_stats.batting.__dict__)

```

```python
import mlbapi

astros_schedule = mlbapi.schedule(date='03/05/2018', team_id=117)

game_pk = astros_schedule.dates[0].games[0].game_pk
line = mlbapi.linescore(game_pk)

output = '{} of the {}, {} facing {}. {} ball(s), {} strike(s), {} out(s)'
print(output.format(line.inning_half, line.current_inning_ordinal, line.offense.batter.full_name,
                    line.defense.pitcher.full_name, line.balls, line.strikes, line.outs))

# Top of the 9th, Scott Van Slyke facing Framber Valdez. 0 ball(s), 3 strike(s), 3 out(s)
```
