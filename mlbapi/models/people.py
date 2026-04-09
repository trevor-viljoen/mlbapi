"""Pydantic models for the people/person API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Handedness(MLBModel):
    """Batting side or pitching hand."""
    code: Optional[str] = None
    description: Optional[str] = None


class Position(MLBModel):
    """A player's primary fielding position."""
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    abbreviation: Optional[str] = None


class Person(MLBModel):
    """A full player/person record from ``/api/v1/people/{id}``."""
    id: Optional[int] = None
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    primary_number: Optional[str] = None
    birth_date: Optional[str] = None
    birth_city: Optional[str] = None
    birth_state_province: Optional[str] = None
    birth_country: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    primary_position: Optional[Position] = None
    use_name: Optional[str] = None
    middle_name: Optional[str] = None
    boxscore_name: Optional[str] = None
    gender: Optional[str] = None
    is_player: Optional[bool] = None
    is_verified: Optional[bool] = None
    mlb_debut_date: Optional[str] = None
    bat_side: Optional[Handedness] = None
    pitch_hand: Optional[Handedness] = None
    name_first_last: Optional[str] = None
    name_slug: Optional[str] = None
    strike_zone_top: Optional[float] = None
    strike_zone_bottom: Optional[float] = None
    link: Optional[str] = None


class People(MLBModel):
    """Container returned by ``GET /api/v1/people``."""
    people: Optional[List[Person]] = None
