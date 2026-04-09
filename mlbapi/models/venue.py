"""Pydantic models for the venues API endpoint."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class VenueLocation(MLBModel):
    """Physical location details for a venue."""
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    state_abbrev: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TimeZone(MLBModel):
    """Time-zone information for a venue."""
    id: Optional[str] = None
    offset: Optional[int] = None
    offset_at_game_time: Optional[int] = None
    tz: Optional[str] = None


class FieldInfo(MLBModel):
    """Ballpark dimensions and surface."""
    capacity: Optional[int] = None
    turf_type: Optional[str] = None
    roof_type: Optional[str] = None
    left_line: Optional[int] = None
    left: Optional[int] = None
    left_center: Optional[int] = None
    center: Optional[int] = None
    right_center: Optional[int] = None
    right_line: Optional[int] = None


class Venue(MLBModel):
    """A single MLB venue."""
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    active: Optional[bool] = None
    location: Optional[VenueLocation] = None
    time_zone: Optional[TimeZone] = None
    field_info: Optional[FieldInfo] = None


class Venues(MLBModel):
    """Container returned by ``GET /api/v1/venues``."""
    venues: Optional[List[Venue]] = None
