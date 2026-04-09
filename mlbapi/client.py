#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""High-level Client for the MLB Stats API.

Provides a single :class:`Client` object that exposes every supported
endpoint as a typed method, returning model objects from
:mod:`mlbapi.models` or object wrappers from :mod:`mlbapi.object`.

Example usage::

    from mlbapi.client import Client

    client = Client()
    venues = client.venues(venue_ids=[3313, 4])
    for v in venues.venues:
        print(v.name)

    person = client.person(592450)
    print(person.full_name)

    results = client.people_search(names='Judge')
    for p in results.people:
        print(p.full_name)
"""

from mlbapi.data.game import (
    get_boxscore, get_linescore, get_play_by_play, get_live, get_live_diff,
    get_win_probability,
)
from mlbapi.data.schedule import Schedule as _Schedule
from mlbapi.data.gameday import get_schedule
from mlbapi.data.team import get_teams
from mlbapi.data.division import get_divisions
from mlbapi.data.standings import get_standings
from mlbapi.data.conference import get_conferences
from mlbapi.data.season import get_seasons, get_all_seasons
from mlbapi.data.venue import get_venues
from mlbapi.data.people import get_people, get_person, search_people
from mlbapi.data.draft import get_draft, get_draft_prospects, get_draft_latest
from mlbapi.data.stats import get_stats, get_stats_leaders, get_stats_streaks
from mlbapi.data.homerunderby import (
    get_homerunderby, get_homerunderby_bracket, get_homerunderby_pool,
)
from mlbapi.data.attendance import get_attendance
from mlbapi.data.awards import get_awards, get_award_recipients
from mlbapi.data.jobs import get_jobs, get_umpires, get_datacasters, get_official_scorers
from mlbapi.data.transactions import get_transactions
from mlbapi.data.meta import get_meta

from mlbapi.models.venue import Venues as VenuesModel
from mlbapi.models.people import People as PeopleModel, Person as PersonModel

from mlbapi.object.game import BoxScore, LineScore
from mlbapi.object.team import Teams
from mlbapi.object.division import Divisions
from mlbapi.object.gameday import Schedule
from mlbapi.object.standings import Standings
from mlbapi.object.conference import Conferences
from mlbapi.object.season import Seasons
from mlbapi.object.venue import Venues
from mlbapi.object.draft import Draft
from mlbapi.object.stats import Stats, StatsLeaders
from mlbapi.object.homerunderby import HomeRunDerby
from mlbapi.object.attendance import Attendance
from mlbapi.object.awards import Awards
from mlbapi.object.jobs import Jobs
from mlbapi.object.transactions import Transactions


class Client:
    """Facade over the full MLB Stats API.

    All methods accept the same keyword arguments as the underlying
    ``get_*`` data functions.  Model-layer methods (``people``, ``person``,
    ``people_search``, ``venues_model``) return :class:`mlbapi.models` objects;
    all other methods return :class:`mlbapi.object` wrappers.
    """

    # ------------------------------------------------------------------
    # People / Person  (models layer)
    # ------------------------------------------------------------------

    def people(self, **kwargs) -> PeopleModel:
        """Return a :class:`~mlbapi.models.people.People` model.

        Calls ``GET /api/v1/people``.
        """
        return PeopleModel(get_people(**kwargs))

    def person(self, person_id: int, **kwargs) -> PersonModel:
        """Return a :class:`~mlbapi.models.people.Person` model for *person_id*.

        Calls ``GET /api/v1/people/{person_id}``.
        """
        data = get_person(person_id, **kwargs)
        people_list = data.get('people', [])
        if people_list:
            return PersonModel(people_list[0])
        return PersonModel(data)

    def people_search(self, **kwargs) -> PeopleModel:
        """Search for players by name.

        Calls ``GET /api/v1/people/search``.
        Returns a :class:`~mlbapi.models.people.People` model.
        """
        return PeopleModel(search_people(**kwargs))

    # ------------------------------------------------------------------
    # Venues  (models layer)
    # ------------------------------------------------------------------

    def venues_model(self, **kwargs) -> VenuesModel:
        """Return a :class:`~mlbapi.models.venue.Venues` model.

        Calls ``GET /api/v1/venues``.
        """
        return VenuesModel(get_venues(**kwargs))

    # ------------------------------------------------------------------
    # Remaining endpoints  (object layer — unchanged behaviour)
    # ------------------------------------------------------------------

    def schedule(self, **kwargs) -> Schedule:
        return Schedule(get_schedule(**kwargs))

    def boxscore(self, game_pk: int, **kwargs) -> BoxScore:
        return BoxScore(get_boxscore(game_pk, **kwargs))

    def linescore(self, game_pk: int, **kwargs) -> LineScore:
        return LineScore(get_linescore(game_pk, **kwargs))

    def play_by_play(self, game_pk: int, **kwargs):
        return get_play_by_play(game_pk, **kwargs)

    def live(self, game_pk: int, **kwargs):
        return get_live(game_pk, **kwargs)

    def live_diff(self, game_pk: int, **kwargs):
        return get_live_diff(game_pk, **kwargs)

    def win_probability(self, game_pk: int, **kwargs):
        return get_win_probability(game_pk, **kwargs)

    def teams(self, **kwargs) -> Teams:
        return Teams(get_teams(**kwargs))

    def divisions(self, **kwargs) -> Divisions:
        return Divisions(get_divisions(**kwargs))

    def standings(self, **kwargs) -> Standings:
        return Standings(get_standings(**kwargs))

    def conferences(self, **kwargs) -> Conferences:
        return Conferences(get_conferences(**kwargs))

    def seasons(self, **kwargs) -> Seasons:
        return Seasons(get_seasons(**kwargs))

    def all_seasons(self, **kwargs) -> Seasons:
        return Seasons(get_all_seasons(**kwargs))

    def venues(self, **kwargs) -> Venues:
        """Return a legacy :class:`~mlbapi.object.venue.Venues` object layer."""
        return Venues(get_venues(**kwargs))

    def draft(self, year: int, **kwargs) -> Draft:
        return Draft(get_draft(year, **kwargs))

    def draft_prospects(self, **kwargs) -> Draft:
        return Draft(get_draft_prospects(**kwargs))

    def draft_latest(self, year: int, **kwargs) -> Draft:
        return Draft(get_draft_latest(year, **kwargs))

    def stats(self, **kwargs) -> Stats:
        return Stats(get_stats(**kwargs))

    def stats_leaders(self, **kwargs) -> StatsLeaders:
        return StatsLeaders(get_stats_leaders(**kwargs))

    def stats_streaks(self, **kwargs) -> Stats:
        return Stats(get_stats_streaks(**kwargs))

    def homerunderby(self, game_pk: int, **kwargs) -> HomeRunDerby:
        return HomeRunDerby(get_homerunderby(game_pk, **kwargs))

    def homerunderby_bracket(self, game_pk: int, **kwargs) -> HomeRunDerby:
        return HomeRunDerby(get_homerunderby_bracket(game_pk, **kwargs))

    def homerunderby_pool(self, game_pk: int, **kwargs) -> HomeRunDerby:
        return HomeRunDerby(get_homerunderby_pool(game_pk, **kwargs))

    def attendance(self, **kwargs) -> Attendance:
        return Attendance(get_attendance(**kwargs))

    def awards(self, **kwargs) -> Awards:
        return Awards(get_awards(**kwargs))

    def award_recipients(self, award_id: str, **kwargs) -> Awards:
        return Awards(get_award_recipients(award_id, **kwargs))

    def jobs(self, **kwargs) -> Jobs:
        return Jobs(get_jobs(**kwargs))

    def umpires(self, **kwargs) -> Jobs:
        return Jobs(get_umpires(**kwargs))

    def datacasters(self, **kwargs) -> Jobs:
        return Jobs(get_datacasters(**kwargs))

    def official_scorers(self, **kwargs) -> Jobs:
        return Jobs(get_official_scorers(**kwargs))

    def transactions(self, **kwargs) -> Transactions:
        return Transactions(get_transactions(**kwargs))

    def meta(self, meta_type: str):
        """Return lookup-table data for *meta_type*."""
        return get_meta(meta_type)
