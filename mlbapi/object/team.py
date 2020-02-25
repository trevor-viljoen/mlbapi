#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

import inflection

import mlbapi.object
from mlbapi.object.game import Team

class Teams:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'teams':
                teams = mlbapi.object.listofobjs(value, Team)
                setattr(self, inflection.underscore(key), teams)
            else:
                mlbapi.object.setobjattr(self, key, value)

