"""Static MLB team lookup data.

Provides :data:`TEAMS` — a list of dicts, one per franchise — and
:func:`team_id` — a helper that resolves a name or abbreviation to a team ID.

Data is static (no API call required) and covers all 30 current MLB franchises.
"""

from __future__ import annotations

from typing import Optional

# Each entry: id, name, full_name, abbreviation, city (location_name)
# Sorted by division (AL East, AL Central, AL West, NL East, NL Central, NL West)
TEAMS: list[dict] = [
    # AL East
    {"id": 110, "name": "Orioles",        "full_name": "Baltimore Orioles",       "abbreviation": "BAL", "city": "Baltimore"},
    {"id": 111, "name": "Red Sox",         "full_name": "Boston Red Sox",          "abbreviation": "BOS", "city": "Boston"},
    {"id": 147, "name": "Yankees",         "full_name": "New York Yankees",        "abbreviation": "NYY", "city": "New York"},
    {"id": 139, "name": "Rays",            "full_name": "Tampa Bay Rays",          "abbreviation": "TB",  "city": "Tampa Bay"},
    {"id": 141, "name": "Blue Jays",       "full_name": "Toronto Blue Jays",       "abbreviation": "TOR", "city": "Toronto"},
    # AL Central
    {"id": 145, "name": "White Sox",       "full_name": "Chicago White Sox",       "abbreviation": "CWS", "city": "Chicago"},
    {"id": 114, "name": "Guardians",       "full_name": "Cleveland Guardians",     "abbreviation": "CLE", "city": "Cleveland"},
    {"id": 116, "name": "Tigers",          "full_name": "Detroit Tigers",          "abbreviation": "DET", "city": "Detroit"},
    {"id": 118, "name": "Royals",          "full_name": "Kansas City Royals",      "abbreviation": "KC",  "city": "Kansas City"},
    {"id": 142, "name": "Twins",           "full_name": "Minnesota Twins",         "abbreviation": "MIN", "city": "Minnesota"},
    # AL West
    {"id": 117, "name": "Astros",          "full_name": "Houston Astros",          "abbreviation": "HOU", "city": "Houston"},
    {"id": 108, "name": "Angels",          "full_name": "Los Angeles Angels",      "abbreviation": "LAA", "city": "Los Angeles"},
    {"id": 133, "name": "Athletics",       "full_name": "Oakland Athletics",       "abbreviation": "OAK", "city": "Oakland"},
    {"id": 136, "name": "Mariners",        "full_name": "Seattle Mariners",        "abbreviation": "SEA", "city": "Seattle"},
    {"id": 140, "name": "Rangers",         "full_name": "Texas Rangers",           "abbreviation": "TEX", "city": "Texas"},
    # NL East
    {"id": 144, "name": "Braves",          "full_name": "Atlanta Braves",          "abbreviation": "ATL", "city": "Atlanta"},
    {"id": 146, "name": "Marlins",         "full_name": "Miami Marlins",           "abbreviation": "MIA", "city": "Miami"},
    {"id": 121, "name": "Mets",            "full_name": "New York Mets",           "abbreviation": "NYM", "city": "New York"},
    {"id": 143, "name": "Phillies",        "full_name": "Philadelphia Phillies",   "abbreviation": "PHI", "city": "Philadelphia"},
    {"id": 120, "name": "Nationals",       "full_name": "Washington Nationals",    "abbreviation": "WSH", "city": "Washington"},
    # NL Central
    {"id": 112, "name": "Cubs",            "full_name": "Chicago Cubs",            "abbreviation": "CHC", "city": "Chicago"},
    {"id": 113, "name": "Reds",            "full_name": "Cincinnati Reds",         "abbreviation": "CIN", "city": "Cincinnati"},
    {"id": 158, "name": "Brewers",         "full_name": "Milwaukee Brewers",       "abbreviation": "MIL", "city": "Milwaukee"},
    {"id": 134, "name": "Pirates",         "full_name": "Pittsburgh Pirates",       "abbreviation": "PIT", "city": "Pittsburgh"},
    {"id": 138, "name": "Cardinals",       "full_name": "St. Louis Cardinals",     "abbreviation": "STL", "city": "St. Louis"},
    # NL West
    {"id": 109, "name": "Diamondbacks",    "full_name": "Arizona Diamondbacks",    "abbreviation": "ARI", "city": "Arizona"},
    {"id": 115, "name": "Rockies",         "full_name": "Colorado Rockies",        "abbreviation": "COL", "city": "Colorado"},
    {"id": 119, "name": "Dodgers",         "full_name": "Los Angeles Dodgers",     "abbreviation": "LAD", "city": "Los Angeles"},
    {"id": 135, "name": "Padres",          "full_name": "San Diego Padres",        "abbreviation": "SD",  "city": "San Diego"},
    {"id": 137, "name": "Giants",          "full_name": "San Francisco Giants",    "abbreviation": "SF",  "city": "San Francisco"},
]

# Build lookup index: every variant of a team's name/abbr → team ID
_LOOKUP: dict[str, int] = {}
for _t in TEAMS:
    _LOOKUP[_t["abbreviation"].upper()] = _t["id"]
    _LOOKUP[_t["name"].lower()] = _t["id"]
    _LOOKUP[_t["full_name"].lower()] = _t["id"]
    _LOOKUP[_t["city"].lower()] = _t["id"]


def team_id(query: str) -> Optional[int]:
    """Resolve a team name, nickname, city, or abbreviation to a team ID.

    The lookup is case-insensitive. Abbreviations are matched exactly
    (``'NYY'``, ``'nyy'``); names and cities use a lowercase comparison.

    Args:
        query: Any of: abbreviation (``'NYY'``), nickname (``'Yankees'``),
               full name (``'New York Yankees'``), or city (``'New York'``).

    Returns:
        The integer team ID, or ``None`` if no match is found.

    Examples::

        from mlbapi import team_id

        team_id('NYY')               # 147
        team_id('yankees')           # 147
        team_id('New York Yankees')  # 147
        team_id('BAL')               # 110
        team_id('unknown')           # None
    """
    return _LOOKUP.get(query.strip().lower()) or _LOOKUP.get(query.strip().upper())
