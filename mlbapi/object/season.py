#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Season:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Seasons:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'seasons':
                seasons = mlbapi.object.listofobjs(value, Season)
                setattr(self, inflection.underscore(key), seasons)
            else:
                mlbapi.object.setobjattr(self, key, value)
