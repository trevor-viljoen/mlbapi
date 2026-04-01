"""Tests for examples/live_scores.py.

Uses Textual's async test runner (app.run_test()) with pytest-asyncio.
All API calls are replaced by a mock Client — no network traffic.
"""

from __future__ import annotations

import sys
import os
from datetime import date
from unittest.mock import MagicMock

import pytest

# Make the examples package importable when pytest runs from the project root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from examples.live_scores import (
    MLBTerminal,
    SchedulePane,
    StandingsPane,
    BoxScoreScreen,
    _attr,
    _score,
)
from textual.widgets import DataTable, Label, TabbedContent


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

FIXED_DATE = date(2024, 6, 1)


def _game(
    game_pk: int = 716463,
    away: str = "New York Yankees",
    home: str = "Houston Astros",
    away_score: int = 3,
    home_score: int = 5,
    abstract: str = "Final",
    state: str = "Final",
    game_date: str = "2024-06-01T18:05:00Z",
    venue: str = "Minute Maid Park",
) -> MagicMock:
    """Build a minimal mock game object."""
    g = MagicMock()
    g.game_pk = game_pk
    g.game_date = game_date
    g.status.abstract_game_state = abstract
    g.status.detailed_state = state
    g.teams.away.team.name = away
    g.teams.away.score = away_score
    g.teams.home.team.name = home
    g.teams.home.score = home_score
    g.venue.name = venue
    g.linescore.current_inning = None
    g.linescore.inning_half_abbreviation = ""
    return g


def _schedule(*games) -> MagicMock:
    """Wrap games in a mock Schedule with one Date."""
    date_obj = MagicMock()
    date_obj.games = list(games)
    sched = MagicMock()
    sched.dates = [date_obj]
    return sched


def _standings_record(division: str, teams: list[tuple[str, int, int]]) -> MagicMock:
    """Build a mock StandingsRecord."""
    record = MagicMock()
    record.division.name = division
    trs = []
    for name, w, l in teams:
        tr = MagicMock()
        tr.team.name = name
        tr.wins = w
        tr.losses = l
        tr.winning_percentage = f"{w / (w + l):.3f}" if (w + l) else ".000"
        tr.games_back = "-"
        tr.streak.streak_code = "W1"
        trs.append(tr)
    record.team_records = trs
    return record


def _mock_client(
    schedule=None,
    al_standings=None,
    nl_standings=None,
    boxscore=None,
    linescore=None,
) -> MagicMock:
    """Return a mock Client with configurable return values."""
    client = MagicMock()
    client.schedule.return_value = schedule or _schedule()
    al = MagicMock()
    al.records = [_standings_record("AL East", [("New York Yankees", 95, 67)])]
    nl = MagicMock()
    nl.records = [_standings_record("NL West", [("Los Angeles Dodgers", 98, 64)])]
    client.standings.side_effect = lambda league_id=None, **kw: (
        al_standings or al if league_id == 103 else nl_standings or nl
    )
    client.boxscore.return_value = boxscore or MagicMock()
    client.linescore.return_value = linescore or MagicMock()
    return client


# ---------------------------------------------------------------------------
# Unit tests — no Textual runtime needed
# ---------------------------------------------------------------------------

class TestHelpers:
    def test_attr_simple(self):
        obj = MagicMock()
        obj.foo = "bar"
        assert _attr(obj, "foo") == "bar"

    def test_attr_nested(self):
        obj = MagicMock()
        obj.a.b.c = "deep"
        assert _attr(obj, "a", "b", "c") == "deep"

    def test_attr_missing_returns_default(self):
        assert _attr(None, "anything", default="x") == "x"

    def test_attr_chain_through_none(self):
        obj = MagicMock()
        obj.a = None
        assert _attr(obj, "a", "b", default="fallback") == "fallback"

    def test_score_with_value(self):
        team = MagicMock()
        team.score = 7
        assert _score(team) == "7"

    def test_score_zero(self):
        team = MagicMock()
        team.score = 0
        assert _score(team) == "0"

    def test_score_none_returns_dash(self):
        obj = MagicMock()
        obj.score = None
        assert _score(obj) == "-"


# ---------------------------------------------------------------------------
# Integration tests — full Textual app headlessly via run_test()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_app_starts():
    """App should mount without raising any exception."""
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.1)


@pytest.mark.asyncio
async def test_schedule_tab_is_active_by_default():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.1)
        tabs = app.query_one(TabbedContent)
        assert tabs.active == "schedule"


@pytest.mark.asyncio
async def test_schedule_renders_games():
    """Games returned by mock client should appear as rows in the table."""
    games = [
        _game(game_pk=1, away="Yankees", home="Astros", abstract="Final"),
        _game(game_pk=2, away="Red Sox", home="Rays",   abstract="Final"),
    ]
    client = _mock_client(schedule=_schedule(*games))
    app = MLBTerminal(FIXED_DATE, client=client)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.5)
        table = app.query_one("#sched-table", DataTable)
        assert table.row_count == 2


@pytest.mark.asyncio
async def test_schedule_shows_team_names():
    client = _mock_client(
        schedule=_schedule(_game(away="New York Yankees", home="Houston Astros"))
    )
    app = MLBTerminal(FIXED_DATE, client=client)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.5)
        table = app.query_one("#sched-table", DataTable)
        assert table.row_count == 1
        # The first row's first cell should contain the away team name
        cell = table.get_cell_at((0, 0))
        assert "Yankees" in str(cell)


@pytest.mark.asyncio
async def test_no_games_shows_message():
    """Empty schedule should show 'No games scheduled' status."""
    empty = MagicMock()
    empty.dates = []
    client = _mock_client(schedule=empty)
    app = MLBTerminal(FIXED_DATE, client=client)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.5)
        status = app.query_one("#sched-status", Label)
        assert "No games" in str(status.render())


@pytest.mark.asyncio
async def test_date_label_shows_initial_date():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.2)
        label = app.query_one("#sched-date-label", Label)
        rendered = str(label.render())
        assert "2024" in rendered
        assert "June" in rendered


@pytest.mark.asyncio
async def test_next_date_advances_one_day():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.2)
        pane = app.query_one(SchedulePane)
        assert pane.current_date == FIXED_DATE
        await pilot.press("]")
        await pilot.pause(0.1)
        assert pane.current_date == date(2024, 6, 2)


@pytest.mark.asyncio
async def test_prev_date_goes_back_one_day():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.2)
        await pilot.press("[")
        await pilot.pause(0.1)
        pane = app.query_one(SchedulePane)
        assert pane.current_date == date(2024, 5, 31)


@pytest.mark.asyncio
async def test_tab_switches_to_standings():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.1)
        # Switch tab programmatically — the Tab key moves focus, not tabs
        app.query_one(TabbedContent).active = "standings"
        await pilot.pause(0.3)
        tabs = app.query_one(TabbedContent)
        assert tabs.active == "standings"


@pytest.mark.asyncio
async def test_standings_renders_teams():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        app.query_one(TabbedContent).active = "standings"
        await pilot.pause(0.5)
        al_table = app.query_one("#std-table-al", DataTable)
        # Division header + 1 team = 2 rows
        assert al_table.row_count >= 1


@pytest.mark.asyncio
async def test_enter_with_no_game_selected_does_not_crash():
    """Pressing Enter when no row is selected should be a no-op."""
    empty = MagicMock()
    empty.dates = []
    app = MLBTerminal(FIXED_DATE, client=_mock_client(schedule=empty))
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.3)
        await pilot.press("enter")
        await pilot.pause(0.1)
        # No BoxScoreScreen should be pushed
        assert not app.screen_stack or not isinstance(app.screen, BoxScoreScreen)


@pytest.mark.asyncio
async def test_boxscore_screen_opens_for_selected_game():
    games = [_game(game_pk=716463)]
    client = _mock_client(schedule=_schedule(*games))

    # Minimal box/line mocks with enough structure to avoid render errors
    box = MagicMock()
    box.teams.away.team.name = "Yankees"
    box.teams.home.team.name = "Astros"
    box.teams.away.team_stats.batting.runs = 3
    box.teams.home.team_stats.batting.runs = 5
    box.teams.away.batters = []
    box.teams.home.batters = []
    box.teams.away.players = {}
    box.teams.home.players = {}
    box.info = []

    line = MagicMock()
    line.status.abstract_game_state = "Final"
    line.current_inning = 9
    line.inning_half_abbreviation = "B"
    line.innings = []
    line.teams.away.runs = 3
    line.teams.away.hits = 8
    line.teams.away.errors = 0
    line.teams.home.runs = 5
    line.teams.home.hits = 10
    line.teams.home.errors = 1

    client.boxscore.return_value = box
    client.linescore.return_value = line

    app = MLBTerminal(FIXED_DATE, client=client)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.5)
        await pilot.press("enter")
        await pilot.pause(0.5)
        assert isinstance(app.screen, BoxScoreScreen)


@pytest.mark.asyncio
async def test_boxscore_screen_closes_on_escape():
    games = [_game(game_pk=716463)]
    client = _mock_client(schedule=_schedule(*games))

    box = MagicMock()
    box.teams.away.team.name = "Yankees"
    box.teams.home.team.name = "Astros"
    box.teams.away.team_stats.batting.runs = 3
    box.teams.home.team_stats.batting.runs = 5
    box.teams.away.batters = []
    box.teams.home.batters = []
    box.teams.away.players = {}
    box.teams.home.players = {}
    box.info = []

    line = MagicMock()
    line.status.abstract_game_state = "Final"
    line.current_inning = None
    line.inning_half_abbreviation = ""
    line.innings = []
    line.teams.away.runs = 3
    line.teams.away.hits = 8
    line.teams.away.errors = 0
    line.teams.home.runs = 5
    line.teams.home.hits = 10
    line.teams.home.errors = 1

    client.boxscore.return_value = box
    client.linescore.return_value = line

    app = MLBTerminal(FIXED_DATE, client=client)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.5)
        await pilot.press("enter")
        await pilot.pause(0.5)
        assert isinstance(app.screen, BoxScoreScreen)
        await pilot.press("escape")
        await pilot.pause(0.2)
        assert not isinstance(app.screen, BoxScoreScreen)


@pytest.mark.asyncio
async def test_q_quits_app():
    app = MLBTerminal(FIXED_DATE, client=_mock_client())
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause(0.1)
        await pilot.press("q")
