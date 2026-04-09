"""Tests for Venues Pydantic model."""
import pytest

from mlbapi.models.venue import Venue, Venues

VENUES_FIXTURE = {
    'venues': [
        {
            'id': 31,
            'name': 'Fenway Park',
            'active': True,
            'location': {
                'city': 'Boston',
                'stateAbbrev': 'MA',
            },
            'timeZone': {
                'tz': 'EDT',
            },
            'fieldInfo': {
                'capacity': 37755,
                'turfType': 'Grass',
            },
        }
    ]
}


class TestVenuesModel:
    def test_isinstance_venues(self):
        result = Venues(VENUES_FIXTURE)
        assert isinstance(result, Venues)

    def test_venues_list_length(self):
        result = Venues(VENUES_FIXTURE)
        assert isinstance(result.venues, list)
        assert len(result.venues) == 1

    def test_venue_id(self):
        result = Venues(VENUES_FIXTURE)
        assert result.venues[0].id == 31

    def test_venue_name(self):
        result = Venues(VENUES_FIXTURE)
        assert result.venues[0].name == 'Fenway Park'

    def test_venue_active(self):
        result = Venues(VENUES_FIXTURE)
        assert result.venues[0].active is True

    def test_venue_nested_location(self):
        result = Venues(VENUES_FIXTURE)
        location = result.venues[0].location
        assert location is not None
        assert location.city == 'Boston'
        assert location.state_abbrev == 'MA'

    def test_venue_nested_timezone(self):
        result = Venues(VENUES_FIXTURE)
        tz = result.venues[0].time_zone
        assert tz is not None
        assert tz.tz == 'EDT'

    def test_venue_nested_field_info(self):
        result = Venues(VENUES_FIXTURE)
        fi = result.venues[0].field_info
        assert fi is not None
        assert fi.capacity == 37755
        assert fi.turf_type == 'Grass'

    def test_empty_venues(self):
        result = Venues({'venues': []})
        assert result.venues == []

    def test_venue_model_instance(self):
        result = Venues(VENUES_FIXTURE)
        assert isinstance(result.venues[0], Venue)
