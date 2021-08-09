#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

import inflection

import mlbapi.object

class Umpire(object):
    def __init__(self, data):
        for ass, name in data.items():
            setattr(self, 'assignment', ass)
            setattr(self, 'name', name)

class Color(mlbapi.object.Object):
    pass

class ColorTimestamps(mlbapi.object.Object):
    pass

class ColorDiff(mlbapi.object.Object):
    pass

class Content(mlbapi.object.Object):
    def __init__(self, data):
        self.media = None
        self.highlights = None
        self.summary = None
        self.game_notes = None

class ContextMetrics(mlbapi.object.Object):
    pass

class LineScore(mlbapi.object.Object):
    def __init__(self, data):
        for key, value in data.items():
            if key == 'innings':
                innings = mlbapi.object.listofobjs(value, Inning)
                setattr(self, inflection.underscore(key), innings)
            elif key == 'teams':
                setattr(self, inflection.underscore(key), Teams(value))
            elif key == 'defense':
                setattr(self, inflection.underscore(key), Defense(value))
            elif key == 'offense':
                setattr(self, inflection.underscore(key), Offense(value))
            else:
                mlbapi.object.setobjattr(self, key, value)

class Inning(mlbapi.object.Object):
    def __init__(self, data):
        for key, value in data.items():
            if key == 'home':
                setattr(self, inflection.underscore(key), Home(value))
            elif key == 'away':
                setattr(self, inflection.underscore(key), Away(value))
            else:
                mlbapi.object.setobjattr(self, key, value)

class Home(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Away(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Defense:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'pitcher':
                setattr(self, inflection.underscore(key), Pitcher(value))
            elif key == 'catcher':
                setattr(self, inflection.underscore(key), Catcher(value))
            elif key == 'first':
                setattr(self, inflection.underscore(key), First(value))
            elif key == 'second':
                setattr(self, inflection.underscore(key), Second(value))
            elif key == 'third':
                setattr(self, inflection.underscore(key), Third(value))
            elif key == 'shortstop':
                setattr(self, inflection.underscore(key), Shortstop(value))
            elif key == 'left':
                setattr(self, inflection.underscore(key), Left(value))
            elif key == 'center':
                setattr(self, inflection.underscore(key), Center(value))
            elif key == 'right':
                setattr(self, inflection.underscore(key), Right(value))
            elif key == 'team':
                setattr(self, inflection.underscore(key), Team(value))
            elif key == 'batter':
                setattr(self, inflection.underscore(key), Batter(value))
            elif key == 'onDeck':
                setattr(self, inflection.underscore(key), OnDeck(value))
            elif key == 'inHole':
                setattr(self, inflection.underscore(key), InHole(value))
            else:
                mlbapi.object.setobjattr(self, key, value)

class Pitcher(Defense):
    def __init__(self, data):
        super().__init__(data)

class Catcher(Defense):
    def __init__(self, data):
        super().__init__(data)

class First(Defense):
    def __init__(self, data):
        super().__init__(data)

class Second(Defense):
    def __init__(self, data):
        super().__init__(data)

class Third(Defense):
    def __init__(self, data):
        super().__init__(data)

class Shortstop(Defense):
    def __init__(self, data):
        super().__init__(data)

class Left(Defense):
    def __init__(self, data):
        super().__init__(data)

class Center(Defense):
    def __init__(self, data):
        super().__init__(data)

class Right(Defense):
    def __init__(self, data):
        super().__init__(data)

class Team(Defense):
    def __init__(self, data):
        super().__init__(data)

class Offense(mlbapi.object.Object):
    def __init__(self, data):
        for key, value in data.items():
            if key == 'batter':
                setattr(self, inflection.underscore(key), Batter(value))
            elif key == 'onDeck':
                setattr(self, inflection.underscore(key), OnDeck(value))
            elif key == 'inHole':
                setattr(self, inflection.underscore(key), InHole(value))
            elif key == 'pitcher':
                setattr(self, inflection.underscore(key), Pitcher(value))
            elif key == 'first':
                if value:
                    setattr(self, inflection.underscore(key), First(value))
                else:
                    setattr(self, inflection.underscore(key), None)
            elif key == 'second':
                if value:
                    setattr(self, inflection.underscore(key), Second(value))
                else:
                    setattr(self, inflection.underscore(key), None)
            elif key == 'third':
                if value:
                    setattr(self, inflection.underscore(key), Third(value))
                else:
                    setattr(self, inflection.underscore(key), None)
            elif key == 'team':
                setattr(self, inflection.underscore(key), (value))
            else:
                mlbapi.object.setobjattr(self, key, value)

class Batter(Offense):
    def __init__(self, data):
        super().__init__(data)

class OnDeck(Offense):
    def __init__(self, data):
        super().__init__(data)

class InHole(Offense):
    def __init__(self, data):
        super().__init__(data)

class Pitcher(Offense):
    def __init__(self, data):
        super().__init__(data)

class First(Offense):
    def __init__(self, data):
        super().__init__(data)

class Second(Offense):
    def __init__(self, data):
        super().__init__(data)

class Third(Offense):
    def __init__(self, data):
        super().__init__(data)

class Team(Offense):
    def __init__(self, data):
        super().__init__(data)

class Live(mlbapi.object.Object):
    pass

class LiveDiff(mlbapi.object.Object):
    pass

class LiveTimestamps(mlbapi.object.Object):
    pass

class PlayByPlay(mlbapi.object.Object):
    pass

class WinProbability(mlbapi.object.Object):
    pass

class BoxScore(mlbapi.object.Object):
    def __init__(self, data):
        for key, value in data.items():
            if key == 'teams':
                mlbapi.object.setobjattr(self, key, value, Teams)
            elif key == 'officials':
                officials = mlbapi.object.listofobjs(value, Official)
                setattr(self, inflection.underscore(key), officials)
            elif key == 'info':
                info = mlbapi.object.listofobjs(value, Info)
                setattr(self, inflection.underscore(key), info)
            elif key == 'pitchingNotes':
                if value:
                    setattr(self, inflection.underscore(key), value)
                else:
                    setattr(self, inflection.underscore(key), None)

class Teams:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'away':
                mlbapi.object.setobjattr(self, key, value, AwayTeam)
            elif key == 'home':
                mlbapi.object.setobjattr(self, key, value, HomeTeam)


class Team:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'status':
                mlbapi.object.setobjattr(self, key, value, Status)
            elif key == 'teams':
                mlbapi.object.setobjattr(self, key, value, Teams)
            elif key == 'venue':
                mlbapi.object.setobjattr(self, key, value, Venue)
            elif key == 'springVenue':
                mlbapi.object.setobjattr(self, key, value, SpringVenue)
            elif key == 'content':
                mlbapi.object.setobjattr(self, key, value, Content)
            elif key == 'league':
                mlbapi.object.setobjattr(self, key, value, League)
            elif key == 'division':
                mlbapi.object.setobjattr(self, key, value, Division)
            elif key == 'sport':
                mlbapi.object.setobjattr(self, key, value, Sport)
            elif key == 'record':
                mlbapi.object.setobjattr(self, key, value, Record)
            elif key == 'springLeague':
                mlbapi.object.setobjattr(self, key, value, SpringLeague)
            elif key == 'conference':
                mlbapi.object.setobjattr(self, key, value, Conference)
            else:
                mlbapi.object.setobjattr(self, key, value)

class AwayTeam:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'team':
                mlbapi.object.setobjattr(self, key, value, Team)
            elif key == 'teamStats':
                mlbapi.object.setobjattr(self, key, value, TeamStats)
            elif key in ['batters', 'pitchers', 'bench', 'bullpen', 'battingOrder']:
                setattr(self, inflection.underscore(key), value)
            elif key == 'info': # FIX
                setattr(self, inflection.underscore(key), None)
            elif key == 'note': # FIX
                setattr(self, inflection.underscore(key), None)
            elif key == 'players':
                players = []
                for k, v in value.items():
                    players.append(Player(v))
                    setattr(self, 'players', players)
            else:
                mlbapi.object.setobjattr(self, key, value)

class HomeTeam:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'team':
                mlbapi.object.setobjattr(self, key, value, Team)
            elif key == 'teamStats':
                mlbapi.object.setobjattr(self, key, value, TeamStats)
            elif key in ['batters', 'pitchers', 'bench', 'bullpen', 'battingOrder']:
                setattr(self, inflection.underscore(key), value)
            elif key == 'info': # FIX
                setattr(self, inflection.underscore(key), None)
            elif key == 'note': # FIX
                setattr(self, inflection.underscore(key), None)
            elif key == 'players':
                players = []
                for k, v in value.items():
                    players.append(Player(v))
                    setattr(self, 'players', players)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Stats:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'batting':
                if value:
                    mlbapi.object.setobjattr(self, key, value, Batting)
                else:
                    setattr(self, 'batting', None)
            elif key == 'pitching':
                mlbapi.object.setobjattr(self, key, value, Pitching)
            elif key == 'fielding':
                mlbapi.object.setobjattr(self, key, value, Fielding)
            else:
                mlbapi.object.setobjattr(self, key, value)

class TeamStats(Stats):
    def __init__(self, data):
        super().__init__(data)

class SeasonStats(Stats):
    def __init__(self, data):
        super().__init__(data)

class Official:
    def __init__(self, data):
        for key, value in data['official'].items():
            mlbapi.object.setobjattr(self, key, value)

class Player:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'person':
                mlbapi.object.setobjattr(self, key, value, Person)
            elif key == 'position':
                mlbapi.object.setobjattr(self, key, value, Position)
            elif key == 'allPositions':
                all_positions = mlbapi.object.listofobjs(value, AllPositions)
                setattr(self, inflection.underscore(key), all_positions)
            elif key == 'stats':
                mlbapi.object.setobjattr(self, key, value, Stats)
            elif key == 'status':
                mlbapi.object.setobjattr(self, key, value, Status)
            elif key == 'seasonStats':
                mlbapi.object.setobjattr(self, key, value, SeasonStats)
            elif key == 'gameStatus':
                mlbapi.object.setobjattr(self, key, value, GameStatus)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Position(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class AllPositions(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class GameStatus(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Batting(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Pitching(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Fielding(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Person(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Status(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Venue(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class SpringVenue(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class League(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class SpringLeague(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class LeagueRecord(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Conference(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Records:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class Division:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'league':
                mlbapi.object.setobjattr(self, key, value, League)
            elif key == 'sport':
                mlbapi.object.setobjattr(self, key, value, Sport)
            else:
                mlbapi.object.setobjattr(self, key, value)


class Sport(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Record:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'leagueRecord':
                mlbapi.object.setobjattr(self, key, value, LeagueRecord)
            elif key == 'records':
                if value:
                    mlbapi.object.setobjattr(self, key, value, Records)
                else:
                    setattr(self, key, None)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Info(mlbapi.object.Object):
    def __init__(self, data):
        info = None
        k = None
        v = None
        for key, value in data.items():
            if key == 'label':
                k = value
            elif key == 'value':
                v = value
            if v:
                setattr(self, 'info', (k, v))
            else:
                setattr(self, 'info', (k))

