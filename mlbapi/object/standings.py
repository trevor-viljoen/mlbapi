#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import jsons

import inflection

import mlbapi.object
from mlbapi.object.game import Team

class Standings:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'records':
                records = mlbapi.object.listofobjs(value, Record)
                setattr(self, inflection.underscore(key), records)
            else:
                mlbapi.object.setobjattr(self, key, value)
    def json(self):
        return jsons.dump(self)

class Record:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'standingsType':
                mlbapi.object.setobjattr(self, key, value)
            elif key == 'league':
                mlbapi.object.setobjattr(self, key, value, League)
            elif key == 'division':
                mlbapi.object.setobjattr(self, key, value, Division)
            elif key == 'sport':
                mlbapi.object.setobjattr(self, key, value, Sport)
            elif key == 'teamRecords':
                team_records = mlbapi.object.listofobjs(value, TeamRecord)
                setattr(self, inflection.underscore(key), team_records)
            else:
                mlbapi.object.setobjattr(self, key, value)

class StandingsType:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class League:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class Division:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class Sport:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class TeamRecord:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'team':
                mlbapi.object.setobjattr(self, key, value, Team)
            elif key == 'streak':
                mlbapi.object.setobjattr(self, key, value, Streak)
            elif key == 'leagueRecord':
                mlbapi.object.setobjattr(self, key, value, LeagueRecord)
            elif key == 'records':
                mlbapi.object.setobjattr(self, key, value, Records)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Streak:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class LeagueRecord:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'league':
                mlbapi.object.setobjattr(self, key, value, League)
            else:
                mlbapi.object.setobjattr(self, key, value)

class Records:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'splitRecords':
                split_records = mlbapi.object.listofobjs(value, SplitRecord)
                setattr(self, inflection.underscore(key), split_records)
            elif key == 'divisionRecords':
                division_records = mlbapi.object.listofobjs(value, DivisionRecord)
                setattr(self, inflection.underscore(key), division_records)
            elif key == 'overallRecords':
                overall_records = mlbapi.object.listofobjs(value, OverallRecord)
                setattr(self, inflection.underscore(key), overall_records)
            elif key == 'leagueRecords':
                league_records = mlbapi.object.listofobjs(value, LeagueRecord)
                setattr(self, inflection.underscore(key), league_records)
            elif key == 'expectedRecords':
                expected_records = mlbapi.object.listofobjs(value, ExpectedRecord)
                setattr(self, inflection.underscore(key), expected_records)
            else:
                mlbapi.object.setobjattr(self, key, value)

class SplitRecord:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class DivisionRecord:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'division':
                mlbapi.object.setobjattr(self, key, value, Division)
            else:
                mlbapi.object.setobjattr(self, key, value)

class OverallRecord:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)

class ExpectedRecord:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)
