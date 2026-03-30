#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Stats:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'stats':
                setattr(self, inflection.underscore(key), value)
            else:
                mlbapi.object.setobjattr(self, key, value)


class StatsLeaders:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'leagueLeaders':
                setattr(self, inflection.underscore(key), value)
            else:
                mlbapi.object.setobjattr(self, key, value)
