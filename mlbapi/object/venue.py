#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Venue:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Venues:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'venues':
                venues = mlbapi.object.listofobjs(value, Venue)
                setattr(self, inflection.underscore(key), venues)
            else:
                mlbapi.object.setobjattr(self, key, value)
