#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

import inflection

import mlbapi.object
from mlbapi.object.game import Division

class Divisions:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'divisions':
                divisions = mlbapi.object.listofobjs(value, Division)
                setattr(self, inflection.underscore(key), divisions)
            else:
                mlbapi.object.setobjattr(self, key, value)

