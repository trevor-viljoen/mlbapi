""" Misclaneous utility functions """

import time
import inflection

import mlbapi.exceptions

def check_kwargs(keys, list_of_valid_params, exception):
    """ Make sure we have a valid set of keys for a given endpoint """
    for key in keys:
        if key not in list_of_valid_params:
            error = '{} is not a valid parameter.'.format(key)
            raise exception(error)
    return True

def to_python_var(api_key):
    """ API Key format to python variable format """
    return inflection.underscore(api_key)

def to_api_keys(python_vars):
    """ return a dictionary of api keys in correct format """
    api_dict = {}
    for key, value in python_vars.items():
        api_dict[inflection.camelize(key, False)] = value
    return api_dict

def valid_timecode(timecode):
    """ validate a timecode """
    try:
        time.strptime(timecode, '%Y%m%d_%H%M%S')
        return True
    except ValueError:
        return False

def to_comma_delimited_string(key, instype):
    """ Return a comma delimited string """
    temp = []
    if not isinstance(key, instype):
        try:
            temp.append(instype(key))
        except ValueError as error:
            raise mlbapi.exceptions.ParameterException(error)
    return ','.join(temp)
