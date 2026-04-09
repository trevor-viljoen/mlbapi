#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi models for the venues API endpoint.

Classes
-------
VenueLocation
    Physical location details for a venue (city, state, coordinates).
TimeZone
    Time-zone information for a venue.
FieldInfo
    Ballpark dimensions and surface information.
Venue
    A single MLB venue, optionally hydrated with location/tz/field details.
Venues
    Container returned by the ``/api/v1/venues`` endpoint; wraps a list of
    :class:`Venue` objects.
"""

from mlbapi.models import MLBModel


def _float_or_none(v):
    """Convert to float, returning None on failure."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int_or_none(v):
    """Convert to int, returning None on failure."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


class VenueLocation(MLBModel):
    """Physical location details for a venue.

    Attributes
    ----------
    address1 : str or None
    city : str or None
    state : str or None
    state_abbrev : str or None
    postal_code : str or None
    country : str or None
    phone : str or None
    latitude : float or None
    longitude : float or None
    """

    FIELDS = {
        'address1':    ('address1',    str),
        'city':        ('city',        str),
        'state':       ('state',       str),
        'stateAbbrev': ('state_abbrev', str),
        'postalCode':  ('postal_code', str),
        'country':     ('country',     str),
        'phone':       ('phone',       str),
    }

    def __init__(self, data: dict):
        # Initialise declared FIELDS first
        super().__init__(data)
        # Handle nested defaultCoordinates
        coords = data.get('defaultCoordinates', {}) if isinstance(data, dict) else {}
        self.latitude = _float_or_none(coords.get('latitude'))
        self.longitude = _float_or_none(coords.get('longitude'))


class TimeZone(MLBModel):
    """Time-zone information for a venue.

    Attributes
    ----------
    id : str or None
        IANA time-zone string (e.g. ``'America/New_York'``).
    offset : int or None
        UTC offset in hours.
    tz : str or None
        Abbreviation (e.g. ``'ET'``).
    """

    FIELDS = {
        'id':     ('id',     str),
        'offset': ('offset', _int_or_none),
        'tz':     ('tz',     str),
    }


class FieldInfo(MLBModel):
    """Ballpark field dimensions and surface.

    Attributes
    ----------
    capacity : int or None
    turf_type : str or None
    roof_type : str or None
    left_line : int or None
    left : int or None
    left_center : int or None
    center : int or None
    right_center : int or None
    right_line : int or None
    right : int or None
    """

    FIELDS = {
        'capacity':    ('capacity',     _int_or_none),
        'turfType':    ('turf_type',    str),
        'roofType':    ('roof_type',    str),
        'leftLine':    ('left_line',    _int_or_none),
        'left':        ('left',         _int_or_none),
        'leftCenter':  ('left_center',  _int_or_none),
        'center':      ('center',       _int_or_none),
        'rightCenter': ('right_center', _int_or_none),
        'rightLine':   ('right_line',   _int_or_none),
        'right':       ('right',        _int_or_none),
    }


class Venue(MLBModel):
    """A single MLB venue.

    Attributes
    ----------
    id : int or None
    name : str or None
    link : str or None
    location : VenueLocation or None
        Populated when the API response is hydrated with ``location``.
    time_zone : TimeZone or None
        Populated when the API response is hydrated with ``timeZone``.
    field_info : FieldInfo or None
        Populated when the API response is hydrated with ``fieldInfo``.
    active : bool or None
    season : str or None
    """

    FIELDS = {
        'id':     ('id',     _int_or_none),
        'name':   ('name',   str),
        'link':   ('link',   str),
        'active': ('active', bool),
        'season': ('season', str),
    }

    def __init__(self, data: dict):
        super().__init__(data)
        if not isinstance(data, dict):
            return
        loc = data.get('location')
        self.location = VenueLocation(loc) if isinstance(loc, dict) else None

        tz = data.get('timeZone')
        self.time_zone = TimeZone(tz) if isinstance(tz, dict) else None

        fi = data.get('fieldInfo')
        self.field_info = FieldInfo(fi) if isinstance(fi, dict) else None


class Venues(MLBModel):
    """Container returned by ``GET /api/v1/venues``.

    Attributes
    ----------
    venues : list[Venue]
    copyright : str or None
    """

    FIELDS = {
        'copyright': ('copyright', str),
    }

    def __init__(self, data: dict):
        super().__init__(data)
        raw = data.get('venues', []) if isinstance(data, dict) else []
        self.venues = [Venue(v) for v in raw if isinstance(v, dict)]
