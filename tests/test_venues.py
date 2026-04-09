"""Tests for mlbapi.models.venue — Venue, VenueLocation, TimeZone,
FieldInfo, and Venues model classes."""
import pytest

from mlbapi.models.venue import FieldInfo, TimeZone, Venue, VenueLocation, Venues


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

VENUE_MINIMAL = {'id': 3313, 'name': 'Yankee Stadium', 'link': '/api/v1/venues/3313'}

VENUE_HYDRATED = {
    'id': 3313,
    'name': 'Yankee Stadium',
    'link': '/api/v1/venues/3313',
    'active': True,
    'season': '2023',
    'location': {
        'address1': '1 East 161st Street',
        'city': 'Bronx',
        'state': 'New York',
        'stateAbbrev': 'NY',
        'postalCode': '10451',
        'country': 'USA',
        'phone': '(718) 293-4300',
        'defaultCoordinates': {
            'latitude': 40.829659,
            'longitude': -73.926186,
        },
    },
    'timeZone': {
        'id': 'America/New_York',
        'offset': -4,
        'tz': 'EDT',
    },
    'fieldInfo': {
        'capacity': 47309,
        'turfType': 'Grass',
        'roofType': 'Open',
        'leftLine': 318,
        'left': 318,
        'leftCenter': 399,
        'center': 408,
        'rightCenter': 385,
        'rightLine': 314,
        'right': 314,
    },
}

VENUES_DATA = {
    'copyright': 'Copyright 2023 MLB',
    'venues': [VENUE_MINIMAL, VENUE_HYDRATED],
}


# ---------------------------------------------------------------------------
# VenueLocation
# ---------------------------------------------------------------------------

class TestVenueLocation:
    def test_city(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.city == 'Bronx'

    def test_state(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.state == 'New York'

    def test_state_abbrev(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.state_abbrev == 'NY'

    def test_postal_code(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.postal_code == '10451'

    def test_country(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.country == 'USA'

    def test_phone(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert loc.phone == '(718) 293-4300'

    def test_latitude(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert abs(loc.latitude - 40.829659) < 1e-5

    def test_longitude(self):
        loc = VenueLocation(VENUE_HYDRATED['location'])
        assert abs(loc.longitude - (-73.926186)) < 1e-5

    def test_empty_coords(self):
        loc = VenueLocation({'city': 'Boston'})
        assert loc.latitude is None
        assert loc.longitude is None


# ---------------------------------------------------------------------------
# TimeZone
# ---------------------------------------------------------------------------

class TestTimeZone:
    def test_id(self):
        tz = TimeZone(VENUE_HYDRATED['timeZone'])
        assert tz.id == 'America/New_York'

    def test_offset(self):
        tz = TimeZone(VENUE_HYDRATED['timeZone'])
        assert tz.offset == -4

    def test_tz_abbrev(self):
        tz = TimeZone(VENUE_HYDRATED['timeZone'])
        assert tz.tz == 'EDT'


# ---------------------------------------------------------------------------
# FieldInfo
# ---------------------------------------------------------------------------

class TestFieldInfo:
    def test_capacity(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.capacity == 47309

    def test_turf_type(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.turf_type == 'Grass'

    def test_roof_type(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.roof_type == 'Open'

    def test_center(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.center == 408

    def test_left_line(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.left_line == 318

    def test_right_line(self):
        fi = FieldInfo(VENUE_HYDRATED['fieldInfo'])
        assert fi.right_line == 314


# ---------------------------------------------------------------------------
# Venue — minimal (no hydration)
# ---------------------------------------------------------------------------

class TestVenueMinimal:
    def test_id(self):
        v = Venue(VENUE_MINIMAL)
        assert v.id == 3313

    def test_name(self):
        v = Venue(VENUE_MINIMAL)
        assert v.name == 'Yankee Stadium'

    def test_link(self):
        v = Venue(VENUE_MINIMAL)
        assert v.link == '/api/v1/venues/3313'

    def test_no_location(self):
        v = Venue(VENUE_MINIMAL)
        assert v.location is None

    def test_no_time_zone(self):
        v = Venue(VENUE_MINIMAL)
        assert v.time_zone is None

    def test_no_field_info(self):
        v = Venue(VENUE_MINIMAL)
        assert v.field_info is None


# ---------------------------------------------------------------------------
# Venue — hydrated
# ---------------------------------------------------------------------------

class TestVenueHydrated:
    def test_id(self):
        v = Venue(VENUE_HYDRATED)
        assert v.id == 3313

    def test_active(self):
        v = Venue(VENUE_HYDRATED)
        assert v.active is True

    def test_season(self):
        v = Venue(VENUE_HYDRATED)
        assert v.season == '2023'

    def test_location_is_venue_location(self):
        v = Venue(VENUE_HYDRATED)
        assert isinstance(v.location, VenueLocation)

    def test_location_city(self):
        v = Venue(VENUE_HYDRATED)
        assert v.location.city == 'Bronx'

    def test_time_zone_is_timezone(self):
        v = Venue(VENUE_HYDRATED)
        assert isinstance(v.time_zone, TimeZone)

    def test_time_zone_id(self):
        v = Venue(VENUE_HYDRATED)
        assert v.time_zone.id == 'America/New_York'

    def test_field_info_is_fieldinfo(self):
        v = Venue(VENUE_HYDRATED)
        assert isinstance(v.field_info, FieldInfo)

    def test_field_info_capacity(self):
        v = Venue(VENUE_HYDRATED)
        assert v.field_info.capacity == 47309


# ---------------------------------------------------------------------------
# Venues container
# ---------------------------------------------------------------------------

class TestVenues:
    def test_venues_list(self):
        vs = Venues(VENUES_DATA)
        assert isinstance(vs.venues, list)
        assert len(vs.venues) == 2

    def test_copyright(self):
        vs = Venues(VENUES_DATA)
        assert vs.copyright == 'Copyright 2023 MLB'

    def test_first_venue_id(self):
        vs = Venues(VENUES_DATA)
        assert vs.venues[0].id == 3313

    def test_second_venue_hydrated(self):
        vs = Venues(VENUES_DATA)
        assert vs.venues[1].location is not None

    def test_empty_venues(self):
        vs = Venues({'venues': []})
        assert vs.venues == []

    def test_missing_venues_key(self):
        vs = Venues({})
        assert vs.venues == []

    def test_repr_contains_class_name(self):
        vs = Venues(VENUES_DATA)
        assert 'Venues' in repr(vs)
