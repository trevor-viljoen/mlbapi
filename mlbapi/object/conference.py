#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Conference:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Conferences:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'conferences':
                conferences = mlbapi.object.listofobjs(value, Conference)
                setattr(self, inflection.underscore(key), conferences)
            else:
                mlbapi.object.setobjattr(self, key, value)
