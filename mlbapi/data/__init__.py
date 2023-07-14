#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

import mlbapi.version
import mlbapi.exceptions
from mlbapi.utils import to_api_keys
from mlbapi.utils import check_kwargs

#TEST_URL = "https://statsapi.mlb.com/api/v1/game/447440/boxscore"
API_VERSION = "v1"
BASE_URL = 'https://statsapi.mlb.com/api'
SUPPORTED_ENDPOINTS = ['game', 'people', 'schedule', 'teams', 'standings', 'divisions']

def request(endpoint, context=None, primary_key=None, secondary_key=None,
            valid_params=None, **kwargs):
    """This method takes a primary_key, an API context, and optionally a
    dictionary of params passed as a query to the API context.

    Args:
        endpoint (string): The API endpoint
        context (string): The API endpoint context
        primary_key (int): The primary key, ex: game_pk, person_id
        secondary_key (int): The secondary key, ex: game_pk, person_id
        valid_params (list): A list of valid parameters for the endpoint

    Returns:
        dict: The returned object is the json payload from the API context.

    Raises:
        requests.exceptions.RequestException
    """

    check_kwargs(kwargs.keys(), valid_params, mlbapi.exceptions.ParameterException)

    api_url = get_api_url(endpoint, context, primary_key, secondary_key)
    headers = {
        'User-Agent': 'mlbapi/{0}'.format(mlbapi.version.__version__),
        'Accept-encoding': 'gzip',
        'Connection': 'close'
    }
    return get_json_data(headers, api_url, **kwargs)

def get_json_data(headers, api_url, **kwargs):
    """This method returns json data from a request

    Args:
        headers (dict): A dictionary of HTTP headers
        api_url (string): The API URL to request

    Returns:
        dict: The returned object is the json payload from the API context.

    Raises:
        requests.exceptions.RequestException
    """
    try:
        if kwargs:
            params = mlbapi.utils.to_api_keys(kwargs)
            #print(api_url, params)
            api_request = requests.get(api_url, headers=headers, params=params)
        else:
            api_request = requests.get(api_url, headers=headers)
        try:
            jdata = api_request.json()
            if 'message' in jdata:
                error = 'msg number {}: {}'.format(jdata['messageNumber'],
                                                   jdata['message'])
                raise mlbapi.exceptions.ObjectNotFoundException(error)
        except json.decoder.JSONDecodeError as error:
            print('{}'.format(api_request.url))
            raise error
    except requests.exceptions.RequestException as error:
        raise mlbapi.exceptions.RequestException(error)
    return jdata

def get_api_url(endpoint, context=None, primary_key=None, secondary_key=None):
    """ Return the API URL to retrieve """
    api_url = ''
    components = [arg for arg in [API_VERSION, endpoint, primary_key, context,
                                  secondary_key] if arg]
    if endpoint in SUPPORTED_ENDPOINTS:
        base_url = '{}{}'.format(BASE_URL, '/{}'*len(components))
        api_url = base_url.format(*components)
    else:
        error = 'The {} API is not yet implemented.'.format(endpoint)
        raise mlbapi.exceptions.ImplementationException(error)
    return api_url
