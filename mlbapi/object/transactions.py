#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inflection

import mlbapi.object


class Transaction:
    def __init__(self, data):
        for key, value in data.items():
            mlbapi.object.setobjattr(self, key, value)


class Transactions:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'transactions':
                transactions = mlbapi.object.listofobjs(value, Transaction)
                setattr(self, inflection.underscore(key), transactions)
            else:
                mlbapi.object.setobjattr(self, key, value)
