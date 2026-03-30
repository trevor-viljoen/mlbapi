#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Attendance:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'records':
                setattr(self, inflection.underscore(key), value)
            elif key == 'aggregateTotals':
                setattr(self, inflection.underscore(key), value)
            else:
                mlbapi.object.setobjattr(self, key, value)
