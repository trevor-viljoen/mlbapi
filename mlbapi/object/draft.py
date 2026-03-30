#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class DraftPick:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Draft:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'drafts':
                setattr(self, inflection.underscore(key), value)
            elif key == 'rounds':
                setattr(self, inflection.underscore(key), value)
            else:
                mlbapi.object.setobjattr(self, key, value)
