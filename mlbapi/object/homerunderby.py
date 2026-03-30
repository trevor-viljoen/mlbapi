#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class HomeRunDerby:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)
