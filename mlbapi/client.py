"""MLB StatsAPI client.

This is the primary entry point for making API calls.  All network I/O flows
through :class:`Client`; the module-level convenience functions in
``mlbapi/__init__.py`` delegate to a shared default instance.

Usage::

    # Module-level convenience — zero configuration required
    import mlbapi
    schedule = mlbapi.schedule(date='2024-06-01')

    # Configured client
    client = mlbapi.Client(timeout=30)
    schedule = client.schedule(date='2024-06-01')

    # Inject a requests.Session (custom headers, retries, auth, …)
    import requests
    s = requests.Session()
    s.headers['X-Custom-Header'] = 'value'
    client = mlbapi.Client(session=s)
"""

from __future__ import annotations

import json
from typing import Optional

import requests

from mlbapi import endpoint, exceptions, version
from mlbapi.data import get_api_url
from mlbapi.utils import check_kwargs, to_api_keys, to_comma_delimited_string

# Valid-parameter lists from the data layer (single source of truth)
from mlbapi.data.game import (
    VALID_BOXSCORE_PARAMS,
    VALID_COLOR_DIFF_PARAMS,
    VALID_COLOR_PARAMS,
    VALID_COLOR_TIMESTAMPS_PARAMS,
    VALID_CONTENT_PARAMS,
    VALID_CONTEXT_METRICS_PARAMS,
    VALID_LINESCORE_PARAMS,
    VALID_LIVE_DIFF_PARAMS,
    VALID_LIVE_PARAMS,
    VALID_LIVE_TIMESTAMPS_PARAMS,
    VALID_PLAY_BY_PLAY_PARAMS,
    VALID_WIN_PROBABILITY_PARAMS,
)
from mlbapi.data.gameday import VALID_SCHEDULE_PARAMS
from mlbapi.data.standings import VALID_STANDINGS_PARAMS
from mlbapi.data.team import VALID_TEAMS_PARAMS
from mlbapi.data.division import VALID_DIVISION_PARAMS
from mlbapi.data.conference import VALID_CONFERENCE_PARAMS
from mlbapi.data.season import VALID_SEASON_PARAMS
from mlbapi.data.venue import VALID_VENUE_PARAMS
from mlbapi.data.draft import VALID_DRAFT_PARAMS
from mlbapi.data.stats import (
    VALID_STATS_LEADERS_PARAMS,
    VALID_STATS_PARAMS,
    VALID_STATS_STREAKS_PARAMS,
)
from mlbapi.data.homerunderby import VALID_HOMERUNDERBY_PARAMS
from mlbapi.data.attendance import VALID_ATTENDANCE_PARAMS
from mlbapi.data.awards import VALID_AWARDS_PARAMS
from mlbapi.data.jobs import VALID_JOBS_PARAMS
from mlbapi.data.transactions import VALID_TRANSACTIONS_PARAMS
from mlbapi.data.meta import get_meta

# Model classes
from mlbapi.object.attendance import Attendance
from mlbapi.object.awards import Awards
from mlbapi.object.conference import Conferences
from mlbapi.object.division import Divisions
from mlbapi.object.draft import Draft
from mlbapi.object.game import BoxScore, LineScore
from mlbapi.object.gameday import Schedule
from mlbapi.object.homerunderby import HomeRunDerby
from mlbapi.object.jobs import Jobs
from mlbapi.object.season import Seasons
from mlbapi.object.standings import Standings
from mlbapi.object.stats import Stats, StatsLeaders
from mlbapi.object.team import Teams
from mlbapi.object.transactions import Transactions
from mlbapi.object.venue import Venues

BASE_URL = 'https://statsapi.mlb.com/api'


class Client:
    """Configurable MLB StatsAPI client.

    The client is the sole entry point for all API calls.  Instantiate once,
    reuse everywhere.

    Args:
        base_url: Override the API base URL (default: ``https://statsapi.mlb.com/api``).
        timeout:  HTTP timeout in seconds applied to every request.
        session:  A :class:`requests.Session` to use for all HTTP calls.
                  Inject one to add custom headers, auth, retry adapters, or
                  for testing without patching ``requests.get``.

    Examples::

        # Basic usage
        from mlbapi import Client
        client = Client()
        schedule = client.schedule(date='2024-06-01')

        # Configured client
        client = Client(timeout=30)
        client = Client(base_url='https://my-proxy/api', timeout=10)

        # Inject a session for custom headers, retry logic, etc.
        import requests
        from requests.adapters import HTTPAdapter, Retry
        s = requests.Session()
        s.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1)))
        client = Client(session=s)

        # Context manager — session created/closed automatically
        with Client() as client:
            box = client.boxscore(716463)
    """
    """Configurable MLB StatsAPI client.

    Args:
        base_url: Override the default ``https://statsapi.mlb.com/api`` base.
        timeout: HTTP timeout in seconds passed to every request.
        session: A ``requests.Session`` to use for all HTTP calls.  Provide
            this to add custom headers, auth, retry adapters, etc.  When
            *None* (the default) the module-level :func:`requests.get` is
            used, which keeps backwards compatibility with tests that patch
            ``requests.get``.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: Optional[int] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._session = session
        self._owns_session = False  # True only when we created the session

    # ------------------------------------------------------------------
    # Context manager — auto-creates and closes a Session
    # ------------------------------------------------------------------

    def __enter__(self) -> 'Client':
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                'User-Agent': f'mlbapi/{version.__version__}',
                'Accept-encoding': 'gzip',
                'Connection': 'close',
            })
            self._owns_session = True
        return self

    def __exit__(self, *_) -> None:
        if self._owns_session and self._session is not None:
            self._session.close()
            self._session = None
            self._owns_session = False

    def __repr__(self) -> str:
        parts = [f'base_url={self._base_url!r}']
        if self._timeout is not None:
            parts.append(f'timeout={self._timeout!r}')
        if self._session is not None:
            parts.append('session=<Session>')
        return f'Client({", ".join(parts)})'

    # ------------------------------------------------------------------
    # Internal HTTP
    # ------------------------------------------------------------------

    def _get(self, url: str, params: Optional[dict] = None) -> dict:
        """Make a single GET request and return the parsed JSON dict."""
        headers = {
            'User-Agent': f'mlbapi/{version.__version__}',
            'Accept-encoding': 'gzip',
            'Connection': 'close',
        }
        kwargs: dict = {'headers': headers}
        if params:
            kwargs['params'] = params
        if self._timeout is not None:
            kwargs['timeout'] = self._timeout

        try:
            if self._session is not None:
                resp = self._session.get(url, **kwargs)
            else:
                resp = requests.get(url, **kwargs)

            try:
                data = resp.json()
            except json.JSONDecodeError as exc:
                raise exc

            if 'message' in data:
                error = 'msg number {}: {}'.format(
                    data.get('messageNumber', '?'), data['message']
                )
                raise exceptions.ObjectNotFoundException(error)

        except requests.exceptions.RequestException as exc:
            raise exceptions.RequestException(exc)

        return data

    def _request(
        self,
        ep: str,
        context: Optional[str] = None,
        primary_key=None,
        secondary_key=None,
        valid_params: Optional[list] = None,
        api_version: Optional[str] = None,
        **kwargs,
    ) -> dict:
        """Validate params, build URL, execute HTTP GET, return JSON dict."""
        check_kwargs(kwargs.keys(), valid_params, exceptions.ParameterException)
        url = get_api_url(ep, context, primary_key, secondary_key,
                          api_version=api_version)
        params = to_api_keys(kwargs) if kwargs else None
        return self._get(url, params=params)

    # ------------------------------------------------------------------
    # Game endpoints
    # ------------------------------------------------------------------

    def linescore(self, game_pk: int, **kwargs) -> LineScore:
        """Linescore for a game."""
        data = self._request(endpoint.GAME, 'linescore', primary_key=game_pk,
                             valid_params=VALID_LINESCORE_PARAMS, **kwargs)
        return LineScore.model_validate(data)

    def play_by_play(self, game_pk: int, **kwargs) -> dict:
        """Play-by-play data for a game (raw dict — no object wrapper yet)."""
        return self._request(endpoint.GAME, 'playByPlay', primary_key=game_pk,
                             valid_params=VALID_PLAY_BY_PLAY_PARAMS, **kwargs)

    def boxscore(self, game_pk: int, **kwargs) -> BoxScore:
        """Boxscore for a game."""
        data = self._request(endpoint.GAME, 'boxscore', primary_key=game_pk,
                             valid_params=VALID_BOXSCORE_PARAMS, **kwargs)
        return BoxScore.model_validate(data)

    def live_diff(self, game_pk: int, **kwargs) -> dict:
        """Live feed diff/patch (raw dict — no object wrapper yet)."""
        return self._request(endpoint.GAME, 'feed/live/diffPatch',
                             primary_key=game_pk,
                             valid_params=VALID_LIVE_DIFF_PARAMS,
                             api_version='v1.1', **kwargs)

    # ------------------------------------------------------------------
    # Schedule
    # ------------------------------------------------------------------

    def schedule(self, **kwargs) -> Schedule:
        """Game schedule, optionally filtered by date/team/sport."""
        if 'start_date' in kwargs and 'end_date' not in kwargs:
            raise exceptions.ParameterException('start_date requires end_date.')
        if 'end_date' in kwargs and 'start_date' not in kwargs:
            raise exceptions.ParameterException('end_date requires start_date.')
        if 'opponent_id' in kwargs and 'team_id' not in kwargs:
            raise exceptions.ParameterException('opponent_id requires team_id.')
        if 'seasons' in kwargs:
            kwargs['seasons'] = to_comma_delimited_string(kwargs['seasons'], int)
        elif 'sport_id' not in kwargs:
            kwargs['sport_id'] = 1
        data = self._request(endpoint.SCHEDULE,
                             valid_params=VALID_SCHEDULE_PARAMS, **kwargs)
        return Schedule.model_validate(data)

    # ------------------------------------------------------------------
    # Standings
    # ------------------------------------------------------------------

    def standings(self, standings_type=None, **kwargs) -> Standings:
        """League standings."""
        if 'league_id' in kwargs:
            kwargs['league_id'] = to_comma_delimited_string(
                kwargs['league_id'], int)
        data = self._request(endpoint.STANDINGS, primary_key=standings_type,
                             valid_params=VALID_STANDINGS_PARAMS, **kwargs)
        return Standings.model_validate(data)

    # ------------------------------------------------------------------
    # Teams
    # ------------------------------------------------------------------

    def teams(self, **kwargs) -> Teams:
        """Team information."""
        if 'league_ids' in kwargs:
            kwargs['league_ids'] = to_comma_delimited_string(
                kwargs['league_ids'], int)
        data = self._request(endpoint.TEAM, valid_params=VALID_TEAMS_PARAMS,
                             **kwargs)
        return Teams.model_validate(data)

    # ------------------------------------------------------------------
    # Divisions
    # ------------------------------------------------------------------

    def divisions(self, **kwargs) -> Divisions:
        """Division information."""
        data = self._request(endpoint.DIVISION,
                             valid_params=VALID_DIVISION_PARAMS, **kwargs)
        return Divisions.model_validate(data)

    # ------------------------------------------------------------------
    # Conferences
    # ------------------------------------------------------------------

    def conferences(self, **kwargs) -> Conferences:
        """Conference information."""
        data = self._request(endpoint.CONFERENCE,
                             valid_params=VALID_CONFERENCE_PARAMS, **kwargs)
        return Conferences.model_validate(data)

    # ------------------------------------------------------------------
    # Seasons
    # ------------------------------------------------------------------

    def seasons(self, **kwargs) -> Seasons:
        """Season information."""
        data = self._request(endpoint.SEASON,
                             valid_params=VALID_SEASON_PARAMS, **kwargs)
        return Seasons.model_validate(data)

    def all_seasons(self, **kwargs) -> Seasons:
        """All seasons."""
        data = self._request(endpoint.SEASON, 'all',
                             valid_params=VALID_SEASON_PARAMS, **kwargs)
        return Seasons.model_validate(data)

    # ------------------------------------------------------------------
    # Venues
    # ------------------------------------------------------------------

    def venues(self, **kwargs) -> Venues:
        """Venue information."""
        data = self._request(endpoint.VENUE, valid_params=VALID_VENUE_PARAMS,
                             **kwargs)
        return Venues.model_validate(data)

    # ------------------------------------------------------------------
    # Draft
    # ------------------------------------------------------------------

    def draft(self, year: int, **kwargs) -> Draft:
        """Draft information for a given year."""
        data = self._request(endpoint.DRAFT, primary_key=year,
                             valid_params=VALID_DRAFT_PARAMS, **kwargs)
        return Draft.model_validate(data)

    def draft_prospects(self, **kwargs) -> Draft:
        """Draft prospects."""
        data = self._request(endpoint.DRAFT, 'prospects',
                             valid_params=VALID_DRAFT_PARAMS, **kwargs)
        return Draft.model_validate(data)

    def draft_latest(self, year: int, **kwargs) -> Draft:
        """Latest draft picks for a given year."""
        data = self._request(endpoint.DRAFT, 'latest', primary_key=year,
                             valid_params=VALID_DRAFT_PARAMS, **kwargs)
        return Draft.model_validate(data)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self, **kwargs) -> Stats:
        """Player/team stats."""
        data = self._request(endpoint.STATS, valid_params=VALID_STATS_PARAMS,
                             **kwargs)
        return Stats.model_validate(data)

    def stats_leaders(self, **kwargs) -> StatsLeaders:
        """Stats leaders."""
        data = self._request(endpoint.STATS, 'leaders',
                             valid_params=VALID_STATS_LEADERS_PARAMS, **kwargs)
        return StatsLeaders.model_validate(data)

    def stats_streaks(self, **kwargs) -> Stats:
        """Stats streaks."""
        data = self._request(endpoint.STATS, 'streaks',
                             valid_params=VALID_STATS_STREAKS_PARAMS, **kwargs)
        return Stats.model_validate(data)

    # ------------------------------------------------------------------
    # Home Run Derby
    # ------------------------------------------------------------------

    def homerunderby(self, game_pk: int, **kwargs) -> HomeRunDerby:
        """Home Run Derby data for a game."""
        data = self._request(endpoint.HOMERUNDERBY, primary_key=game_pk,
                             valid_params=VALID_HOMERUNDERBY_PARAMS, **kwargs)
        return HomeRunDerby.model_validate(data)

    def homerunderby_bracket(self, game_pk: int, **kwargs) -> HomeRunDerby:
        """Home Run Derby bracket."""
        data = self._request(endpoint.HOMERUNDERBY, primary_key=game_pk,
                             context='bracket',
                             valid_params=VALID_HOMERUNDERBY_PARAMS, **kwargs)
        return HomeRunDerby.model_validate(data)

    def homerunderby_pool(self, game_pk: int, **kwargs) -> HomeRunDerby:
        """Home Run Derby pool."""
        data = self._request(endpoint.HOMERUNDERBY, primary_key=game_pk,
                             context='pool',
                             valid_params=VALID_HOMERUNDERBY_PARAMS, **kwargs)
        return HomeRunDerby.model_validate(data)

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def attendance(self, **kwargs) -> Attendance:
        """Attendance data."""
        data = self._request(endpoint.ATTENDANCE,
                             valid_params=VALID_ATTENDANCE_PARAMS, **kwargs)
        return Attendance.model_validate(data)

    # ------------------------------------------------------------------
    # Awards
    # ------------------------------------------------------------------

    def awards(self, **kwargs) -> Awards:
        """Awards list."""
        data = self._request(endpoint.AWARDS, valid_params=VALID_AWARDS_PARAMS,
                             **kwargs)
        return Awards.model_validate(data)

    def award_recipients(self, award_id: str, **kwargs) -> Awards:
        """Recipients for a specific award."""
        data = self._request(endpoint.AWARDS, primary_key=award_id,
                             context='recipients',
                             valid_params=VALID_AWARDS_PARAMS, **kwargs)
        return Awards.model_validate(data)

    # ------------------------------------------------------------------
    # Jobs
    # ------------------------------------------------------------------

    def jobs(self, **kwargs) -> Jobs:
        """Job listings."""
        data = self._request(endpoint.JOBS, valid_params=VALID_JOBS_PARAMS,
                             **kwargs)
        return Jobs.model_validate(data)

    def umpires(self, **kwargs) -> Jobs:
        """Umpire roster."""
        data = self._request(endpoint.JOBS, 'umpires',
                             valid_params=VALID_JOBS_PARAMS, **kwargs)
        return Jobs.model_validate(data)

    def datacasters(self, **kwargs) -> Jobs:
        """Datacaster roster."""
        data = self._request(endpoint.JOBS, 'datacasters',
                             valid_params=VALID_JOBS_PARAMS, **kwargs)
        return Jobs.model_validate(data)

    def official_scorers(self, **kwargs) -> Jobs:
        """Official scorer roster."""
        data = self._request(endpoint.JOBS, 'officialScorers',
                             valid_params=VALID_JOBS_PARAMS, **kwargs)
        return Jobs.model_validate(data)

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    def transactions(self, **kwargs) -> Transactions:
        """Transaction data."""
        data = self._request(endpoint.TRANSACTIONS,
                             valid_params=VALID_TRANSACTIONS_PARAMS, **kwargs)
        return Transactions.model_validate(data)

    # ------------------------------------------------------------------
    # Meta (lookup tables)
    # ------------------------------------------------------------------

    def meta(self, meta_type: str) -> dict:
        """Lookup table data for valid parameter values.

        ``meta_type`` is one of the values in
        ``mlbapi.data.meta.VALID_META_TYPES``.
        """
        return get_meta(meta_type)
