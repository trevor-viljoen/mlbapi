#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Award:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Awards:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'awards':
                awards = mlbapi.object.listofobjs(value, Award)
                setattr(self, inflection.underscore(key), awards)
            else:
                mlbapi.object.setobjattr(self, key, value)
