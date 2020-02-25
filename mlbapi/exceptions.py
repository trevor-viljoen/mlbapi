#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""MLBAPI Exceptions"""

class MLBAPIException(Exception):
    """
    Common exception class. More specific exceptions are
    subclasses of MLBAPIException.
    """

class RequestException(MLBAPIException):
    """
    Wrapper for requests.exceptions.RequestException
    """

class ImplementationException(MLBAPIException):
    """
    Catches erroneous API endpoints passed to requests
    """

class ObjectNotFoundException(MLBAPIException):
    """
    Catches bad data from a request
    """

class ParameterException(MLBAPIException):
    """
    Incorrect Parameters passed to "get_" methods
    """
