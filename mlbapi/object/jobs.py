#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Job:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Jobs:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'roster':
                jobs = mlbapi.object.listofobjs(value, Job)
                setattr(self, inflection.underscore(key), jobs)
            elif key == 'jobList':
                jobs = mlbapi.object.listofobjs(value, Job)
                setattr(self, inflection.underscore(key), jobs)
            else:
                mlbapi.object.setobjattr(self, key, value)
