#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inflection
from dateutil import parser

"""Module that is used for holding basic objects"""

def listofobjs(values, obj):
    """ Create a list of objects """
    temp = []
    for key in values:
        temp.append(obj(key))
    return temp

def setobjattr(obj, key, value, set_obj=None):
    """Sets an object attribute with the correct data type."""
    key = inflection.underscore(key)
    if set_obj:
        setattr(obj, key, set_obj(value))
    else:
        if isinstance(value, bool):
            setattr(obj, key, bool(value))
        else:
            try:
                setattr(obj, key, int(value))
            except ValueError:
                try:
                    setattr(obj, key, float(value))
                except ValueError:
                    try:
                        if 'ordinal' not in key:
                            setattr(obj, key, parser.parse(value))
                        else:
                            try:
                                setattr(obj, key, str(value))
                            except UnicodeEncodeError:
                                setattr(obj, key, value)
                    except (TypeError, ValueError):
                        try:
                            setattr(obj, key, str(value))
                        except UnicodeEncodeError:
                            setattr(obj, key, value)

class Object:
    """Basic class"""
    def __init__(self, data):
        """Creates an object that matches the corresponding values in `data`.
        `data` should be a dictionary of values.
        """
        # loop through data
        for key, value  in data.items():
            setobjattr(self, inflection.underscore(key), value)
