#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
import inflection
import mlbapi.object

class Schedule:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'dates':
                dates = mlbapi.object.listofobjs(value, Date)
                setattr(self, inflection.underscore(key), dates)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Date:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'games':
                games = mlbapi.object.listofobjs(value, Game)
                setattr(self, inflection.underscore(key), games)
            elif key == 'events':
                events = mlbapi.object.listofobjs(value, Event)
                setattr(self, inflection.underscore(key), events)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Event(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Game:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'status':
                mlbapi.object.setobjattr(self, key, value, Status)
            elif key == 'teams':
                mlbapi.object.setobjattr(self, key, value, Teams)
            elif key == 'venue':
                mlbapi.object.setobjattr(self, key, value, Venue)
            elif key == 'content':
                mlbapi.object.setobjattr(self, key, value, Content)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Teams:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'home':
                mlbapi.object.setobjattr(self, key, value, HomeTeam)
            elif key == 'away':
                mlbapi.object.setobjattr(self, key, value, AwayTeam)
            else:
                mlbapi.object.setobjattr(self, key, value)

class HomeTeam:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'leagueRecord':
                mlbapi.object.setobjattr(self, key, value, LeagueRecord)
            elif key == 'team':
                mlbapi.object.setobjattr(self, key, value, Team)
            else:
                mlbapi.object.setobjattr(self, key, value)

class AwayTeam(mlbapi.object.Object):
    def __init__(self, data):
        for key, value in data.items():
            if key == 'leagueRecord':
                mlbapi.object.setobjattr(self, key, value, LeagueRecord)
            elif key == 'team':
                mlbapi.object.setobjattr(self, key, value, Team)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Team(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Status(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class LeagueRecord(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Venue(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)

class Content(mlbapi.object.Object):
    def __init__(self, data):
        super().__init__(data)
