#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mlbapi models for the people/person API endpoint.

Classes
-------
Position
    A player's fielding position (code, name, type, abbreviation).
Handedness
    Batting side or pitch hand (code, description).
Person
    Full player/person record as returned by ``/api/v1/people/{id}``.
People
    Container returned by ``/api/v1/people``; wraps a list of
    :class:`Person` objects.
"""

from mlbapi.models import MLBModel


def _int_or_none(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _float_or_none(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class Position(MLBModel):
    """A player's fielding position.

    Attributes
    ----------
    code : str or None
    name : str or None
    type : str or None
    abbreviation : str or None
    """

    FIELDS = {
        'code':         ('code',         str),
        'name':         ('name',         str),
        'type':         ('type',         str),
        'abbreviation': ('abbreviation', str),
    }


class Handedness(MLBModel):
    """Batting side or pitching hand.

    Attributes
    ----------
    code : str or None
        Single-letter code, e.g. ``'R'``, ``'L'``, ``'S'``.
    description : str or None
        Human-readable label, e.g. ``'Right'``, ``'Left'``, ``'Switch'``.
    """

    FIELDS = {
        'code':        ('code',        str),
        'description': ('description', str),
    }


class Person(MLBModel):
    """A full player/person record.

    Core identity attributes are always populated when the data is present.
    Nested sub-objects (``primary_position``, ``bat_side``, ``pitch_hand``)
    are only set when the API response includes them.

    Attributes
    ----------
    id : int or None
    full_name : str or None
    link : str or None
    first_name : str or None
    last_name : str or None
    primary_number : str or None
    birth_date : str or None
    current_age : int or None
    birth_city : str or None
    birth_state_province : str or None
    birth_country : str or None
    height : str or None
    weight : int or None
    active : bool or None
    use_name : str or None
    middle_name : str or None
    boxscore_name : str or None
    gender : str or None
    is_player : bool or None
    is_verified : bool or None
    draft_year : int or None
    mlb_debut_date : str or None
    name_first_last : str or None
    name_slug : str or None
    first_last_name : str or None
    last_first_name : str or None
    last_init_name : str or None
    init_last_name : str or None
    full_fml_name : str or None
    full_lfm_name : str or None
    strike_zone_top : float or None
    strike_zone_bottom : float or None
    primary_position : Position or None
    bat_side : Handedness or None
    pitch_hand : Handedness or None
    """

    FIELDS = {
        'id':                  ('id',                   _int_or_none),
        'fullName':            ('full_name',            str),
        'link':                ('link',                 str),
        'firstName':           ('first_name',           str),
        'lastName':            ('last_name',            str),
        'primaryNumber':       ('primary_number',       str),
        'birthDate':           ('birth_date',           str),
        'currentAge':          ('current_age',          _int_or_none),
        'birthCity':           ('birth_city',           str),
        'birthStateProvince':  ('birth_state_province', str),
        'birthCountry':        ('birth_country',        str),
        'height':              ('height',               str),
        'weight':              ('weight',               _int_or_none),
        'active':              ('active',               bool),
        'useName':             ('use_name',             str),
        'middleName':          ('middle_name',          str),
        'boxscoreName':        ('boxscore_name',        str),
        'gender':              ('gender',               str),
        'isPlayer':            ('is_player',            bool),
        'isVerified':          ('is_verified',          bool),
        'draftYear':           ('draft_year',           _int_or_none),
        'mlbDebutDate':        ('mlb_debut_date',       str),
        'nameFirstLast':       ('name_first_last',      str),
        'nameSlug':            ('name_slug',            str),
        'firstLastName':       ('first_last_name',      str),
        'lastFirstName':       ('last_first_name',      str),
        'lastInitName':        ('last_init_name',       str),
        'initLastName':        ('init_last_name',       str),
        'fullFMLName':         ('full_fml_name',        str),
        'fullLFMName':         ('full_lfm_name',        str),
        'strikeZoneTop':       ('strike_zone_top',      _float_or_none),
        'strikeZoneBottom':    ('strike_zone_bottom',   _float_or_none),
    }

    def __init__(self, data: dict):
        super().__init__(data)
        if not isinstance(data, dict):
            return
        pos = data.get('primaryPosition')
        self.primary_position = Position(pos) if isinstance(pos, dict) else None

        bat = data.get('batSide')
        self.bat_side = Handedness(bat) if isinstance(bat, dict) else None

        pitch = data.get('pitchHand')
        self.pitch_hand = Handedness(pitch) if isinstance(pitch, dict) else None


class People(MLBModel):
    """Container returned by ``GET /api/v1/people``.

    Attributes
    ----------
    people : list[Person]
    copyright : str or None
    """

    FIELDS = {
        'copyright': ('copyright', str),
    }

    def __init__(self, data: dict):
        super().__init__(data)
        raw = data.get('people', []) if isinstance(data, dict) else []
        self.people = [Person(p) for p in raw if isinstance(p, dict)]
