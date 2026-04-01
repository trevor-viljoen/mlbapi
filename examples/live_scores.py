#!/usr/bin/env python3
"""Interactive MLB terminal — live scores, box scores, and standings.

Usage
-----
    python examples/live_scores.py
    python examples/live_scores.py --date 2024-06-01

Controls
--------
    Tab / Shift+Tab   Switch between Schedule and Standings
    ← / →             Previous / next date (Schedule)
    ↑ / ↓             Navigate game rows
    Enter             Open box score for selected game
    r                 Refresh data
    q                 Quit

Requirements
------------
    pip install "mlbapi[examples]"
    # or: pip install textual
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from typing import Optional

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Label,
    Static,
    TabbedContent,
    TabPane,
)

from mlbapi import Client
from mlbapi.exceptions import MLBAPIException


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _attr(obj, *keys, default=""):
    """Safely traverse a chain of attributes, returning *default* on any miss."""
    for key in keys:
        if obj is None:
            return default
        obj = getattr(obj, key, None)
    return obj if obj is not None else default


def _score(team_side) -> str:
    """Return score as string, or '-' if the game hasn't started."""
    s = _attr(team_side, "score", default=None)
    return str(s) if s is not None else "-"


# ---------------------------------------------------------------------------
# Box Score Modal
# ---------------------------------------------------------------------------

class BoxScoreScreen(ModalScreen):
    """Full-screen modal showing a game's box score."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("b", "dismiss", "Close"),
    ]

    def __init__(self, game_pk: int, client: Client) -> None:
        super().__init__()
        self._game_pk = game_pk
        self._client = client

    def compose(self) -> ComposeResult:
        with Vertical(id="bs-outer"):
            yield Label("Loading box score…", id="bs-title")
            yield Static("", id="bs-error")
            with ScrollableContainer(id="bs-scroll"):
                yield DataTable(id="bs-batting-away", show_cursor=False)
                yield Static(" ", id="bs-spacer1")
                yield DataTable(id="bs-batting-home", show_cursor=False)
                yield Static(" ", id="bs-spacer2")
                yield DataTable(id="bs-linescore", show_cursor=False)
                yield Static("", id="bs-info")
            yield Label("[b][Esc / B][/b] close", id="bs-footer")

    def on_mount(self) -> None:
        self._load()

    @work(thread=True)
    def _load(self) -> None:
        try:
            box = self._client.boxscore(self._game_pk)
            line = self._client.linescore(self._game_pk)
        except MLBAPIException as exc:
            self.app.call_from_thread(lambda: self._show_error(str(exc)))
            return
        self.app.call_from_thread(lambda: self._populate(box, line))

    def _show_error(self, msg: str) -> None:
        self.query_one("#bs-error", Static).update(f"[red]{msg}[/red]")
        self.query_one("#bs-title", Label).update("[red]Error loading box score[/red]")

    def _populate(self, box, line) -> None:
        away_name = _attr(box, "teams", "away", "team", "name", default="Away")
        home_name = _attr(box, "teams", "home", "team", "name", default="Home")
        away_r = _attr(box, "teams", "away", "team_stats", "batting", "runs", default="?")
        home_r = _attr(box, "teams", "home", "team_stats", "batting", "runs", default="?")

        abstract = _attr(line, "status", "abstract_game_state", default="")
        inning = _attr(line, "current_inning", default="")
        half = _attr(line, "inning_half_abbreviation", default="")
        if abstract == "Live" and inning:
            status_str = f"  [yellow]{half} {inning}[/yellow]"
        elif abstract == "Final":
            status_str = "  [green]Final[/green]"
        else:
            status_str = ""

        self.query_one("#bs-title", Label).update(
            f"[bold]{away_name}  {away_r}  —  {home_r}  {home_name}[/bold]{status_str}"
        )

        def build_batting(table: DataTable, team_data, team_name: str) -> None:
            table.clear(columns=True)
            table.add_columns(team_name, "AB", "R", "H", "RBI", "BB", "SO", "AVG")
            # players is a List[Player] (the model converts the API dict to a list)
            players_list = getattr(team_data, "players", []) or []
            players_by_id = {
                _attr(p, "person", "id", default=None): p
                for p in players_list
                if _attr(p, "person", "id", default=None) is not None
            }
            batter_ids = getattr(team_data, "batters", []) or []
            for pid in batter_ids:
                p = players_by_id.get(pid)
                if p is None:
                    continue
                name = _attr(p, "person", "full_name", default=str(pid))
                pos = _attr(p, "position", "abbreviation", default="")
                b = _attr(p, "stats", "batting", default=None)
                if b is None:
                    continue
                table.add_row(
                    f"{name} {pos}",
                    str(_attr(b, "at_bats", default=0)),
                    str(_attr(b, "runs", default=0)),
                    str(_attr(b, "hits", default=0)),
                    str(_attr(b, "rbi", default=0)),
                    str(_attr(b, "base_on_balls", default=0)),
                    str(_attr(b, "strike_outs", default=0)),
                    str(_attr(b, "avg", default=".---")),
                )
            bs = _attr(team_data, "team_stats", "batting", default=None)
            if bs:
                table.add_row(
                    "[bold]Totals[/bold]",
                    str(_attr(bs, "at_bats", default="")),
                    str(_attr(bs, "runs", default="")),
                    str(_attr(bs, "hits", default="")),
                    str(_attr(bs, "rbi", default="")),
                    str(_attr(bs, "base_on_balls", default="")),
                    str(_attr(bs, "strike_outs", default="")),
                    "",
                )

        build_batting(
            self.query_one("#bs-batting-away", DataTable),
            _attr(box, "teams", "away", default=None),
            away_name,
        )
        build_batting(
            self.query_one("#bs-batting-home", DataTable),
            _attr(box, "teams", "home", default=None),
            home_name,
        )

        ls_table = self.query_one("#bs-linescore", DataTable)
        ls_table.clear(columns=True)
        innings = getattr(line, "innings", []) or []
        ls_table.add_columns("", *[str(i.num) for i in innings], "R", "H", "E")

        away_t = _attr(line, "teams", "away", default=None)
        home_t = _attr(line, "teams", "home", default=None)
        ls_table.add_row(
            away_name,
            *[str(_attr(inn, "away", "runs", default="x")) for inn in innings],
            str(_attr(away_t, "runs", default=away_r)),
            str(_attr(away_t, "hits", default="?")),
            str(_attr(away_t, "errors", default="?")),
        )
        ls_table.add_row(
            home_name,
            *[str(_attr(inn, "home", "runs", default="x")) for inn in innings],
            str(_attr(home_t, "runs", default=home_r)),
            str(_attr(home_t, "hits", default="?")),
            str(_attr(home_t, "errors", default="?")),
        )

        info_items = getattr(box, "info", []) or []
        info_lines = [
            f"[dim]{_attr(i, 'label', default='')}:[/dim] {_attr(i, 'value', default='')}"
            for i in info_items
            if _attr(i, "label")
        ]
        if info_lines:
            self.query_one("#bs-info", Static).update("\n".join(info_lines))


# ---------------------------------------------------------------------------
# Schedule Tab Content
# ---------------------------------------------------------------------------

class SchedulePane(Widget):
    """Manages the schedule DataTable and date navigation."""

    # init=False prevents the watcher from firing before on_mount()
    current_date: reactive[date] = reactive(date.today, init=False)

    def __init__(self, client: Client, initial_date: date) -> None:
        super().__init__()
        self._client = client
        self._games: list = []
        self._initial_date = initial_date

    def compose(self) -> ComposeResult:
        yield Label("", id="sched-date-label")
        yield Label("", id="sched-status")
        yield DataTable(id="sched-table", cursor_type="row", zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#sched-table", DataTable).add_columns(
            "Away", "R", "Home", "R", "Status", "Inning", "Venue",
        )
        # Assign after DOM is ready; triggers watch_current_date
        self.current_date = self._initial_date

    def watch_current_date(self, d: date) -> None:
        self.query_one("#sched-date-label", Label).update(
            f"[bold]{d.strftime('%A, %B %-d, %Y')}[/bold]"
        )
        self._load()

    @work(thread=True)
    def _load(self) -> None:
        # Capture date before entering thread — reactive reads from threads
        # can race with main-thread writes.
        target_date = self.current_date
        self.app.call_from_thread(
            lambda: self.query_one("#sched-status", Label).update("[dim]Loading…[/dim]")
        )
        try:
            schedule = self._client.schedule(
                date=target_date.strftime("%Y-%m-%d"),
                sport_id=1,
                hydrate="linescore",
            )
        except MLBAPIException as exc:
            self.app.call_from_thread(
                lambda: self.query_one("#sched-status", Label).update(
                    f"[red]Error: {exc}[/red]"
                )
            )
            return
        self.app.call_from_thread(lambda: self._populate(schedule))

    def _populate(self, schedule) -> None:
        table = self.query_one("#sched-table", DataTable)
        table.clear()
        self._games = []

        games = [
            g
            for d in (getattr(schedule, "dates", []) or [])
            for g in (getattr(d, "games", []) or [])
        ]

        if not games:
            self.query_one("#sched-status", Label).update("[dim]No games scheduled.[/dim]")
            return

        self.query_one("#sched-status", Label).update("")

        for game in games:
            self._games.append(game)
            away = _attr(game, "teams", "away", default=None)
            home = _attr(game, "teams", "home", default=None)
            abstract = _attr(game, "status", "abstract_game_state", default="")
            state = _attr(game, "status", "detailed_state", default="")
            inning = _attr(game, "linescore", "current_inning", default="")
            half = _attr(game, "linescore", "inning_half_abbreviation", default="")

            if abstract == "Final":
                status_str, inning_str = "[green]Final[/green]", ""
            elif abstract == "Live":
                status_str = "[yellow]Live[/yellow]"
                inning_str = f"{half} {inning}" if inning else ""
            elif abstract == "Preview":
                game_time = _attr(game, "game_date", default="")
                if "T" in game_time:
                    status_str = f"[dim]{game_time.split('T')[1][:5]} UTC[/dim]"
                else:
                    status_str = f"[dim]{state}[/dim]"
                inning_str = ""
            else:
                status_str, inning_str = f"[dim]{state}[/dim]", ""

            table.add_row(
                _attr(away, "team", "name", default="—"),
                _score(away),
                _attr(home, "team", "name", default="—"),
                _score(home),
                status_str,
                inning_str,
                _attr(game, "venue", "name", default=""),
            )

    def selected_game_pk(self) -> Optional[int]:
        table = self.query_one("#sched-table", DataTable)
        idx = table.cursor_row
        if not self._games or idx < 0 or idx >= len(self._games):
            return None
        return getattr(self._games[idx], "game_pk", None)

    def prev_date(self) -> None:
        self.current_date = self.current_date - timedelta(days=1)

    def next_date(self) -> None:
        self.current_date = self.current_date + timedelta(days=1)

    def refresh_data(self) -> None:
        self._load()


# ---------------------------------------------------------------------------
# Standings Tab Content
# ---------------------------------------------------------------------------

class StandingsPane(Widget):
    """Manages the standings DataTables."""

    def __init__(self, client: Client) -> None:
        super().__init__()
        self._client = client

    def compose(self) -> ComposeResult:
        yield Label("", id="std-status")
        with Horizontal():
            with Vertical(id="std-al"):
                yield Label("[bold cyan]American League[/bold cyan]")
                yield DataTable(id="std-table-al", show_cursor=False, zebra_stripes=True)
            with Vertical(id="std-nl"):
                yield Label("[bold cyan]National League[/bold cyan]")
                yield DataTable(id="std-table-nl", show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        for tid in ("std-table-al", "std-table-nl"):
            self.query_one(f"#{tid}", DataTable).add_columns(
                "Division / Team", "W", "L", "PCT", "GB", "Strk"
            )
        self._load()

    @work(thread=True)
    def _load(self) -> None:
        self.app.call_from_thread(
            lambda: self.query_one("#std-status", Label).update("[dim]Loading…[/dim]")
        )
        try:
            al = self._client.standings(league_id=103)
            nl = self._client.standings(league_id=104)
        except MLBAPIException as exc:
            self.app.call_from_thread(
                lambda: self.query_one("#std-status", Label).update(
                    f"[red]Error: {exc}[/red]"
                )
            )
            return
        self.app.call_from_thread(lambda: self._populate(al, nl))

    def _populate(self, al, nl) -> None:
        self.query_one("#std-status", Label).update("")
        self._fill_table(
            self.query_one("#std-table-al", DataTable),
            getattr(al, "records", []) or [],
        )
        self._fill_table(
            self.query_one("#std-table-nl", DataTable),
            getattr(nl, "records", []) or [],
        )

    def _fill_table(self, table: DataTable, records: list) -> None:
        table.clear()
        for record in records:
            div_name = _attr(record, "division", "name", default="")
            table.add_row(f"[bold]{div_name}[/bold]", "", "", "", "", "")
            for tr in getattr(record, "team_records", []) or []:
                table.add_row(
                    f"  {_attr(tr, 'team', 'name', default='—')}",
                    str(_attr(tr, "wins", default="")),
                    str(_attr(tr, "losses", default="")),
                    str(_attr(tr, "winning_percentage", default="")),
                    str(_attr(tr, "games_back", default="")),
                    _attr(tr, "streak", "streak_code", default=""),
                )

    def refresh_data(self) -> None:
        self._load()


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------

class MLBTerminal(App):
    """Interactive MLB scores, box scores, and standings."""

    CSS = """
    Screen { background: $surface; }

    SchedulePane, StandingsPane { height: 1fr; }

    #sched-date-label { padding: 0 1; text-style: bold; }
    #sched-status     { padding: 0 1; height: 1; }
    #sched-table      { height: 1fr; }

    #std-status         { height: 1; padding: 0 1; }
    #std-al, #std-nl    { width: 1fr; padding: 0 1; }
    #std-table-al,
    #std-table-nl       { height: 1fr; }

    BoxScoreScreen { align: center middle; }

    #bs-outer {
        width: 90%;
        height: 90%;
        border: round $primary;
        background: $surface;
        padding: 1 2;
    }
    #bs-title  { text-align: center; padding-bottom: 1; text-style: bold; }
    #bs-error  { height: auto; }
    #bs-scroll { height: 1fr; }
    #bs-footer { text-align: center; padding-top: 1; color: $text-muted; }

    #bs-batting-away,
    #bs-batting-home,
    #bs-linescore { height: auto; margin-bottom: 1; }

    #bs-info { height: auto; padding-top: 1; color: $text-muted; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("left",  "prev_date", "Prev day", show=False),
        Binding("right", "next_date", "Next day", show=False),
        Binding("[", "prev_date", "← Day"),
        Binding("]", "next_date", "Day →"),
        Binding("enter", "open_boxscore", "Box score"),
    ]

    def __init__(self, initial_date: date, client: Optional[Client] = None) -> None:
        super().__init__()
        self._initial_date = initial_date
        self._client = client or Client()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial="schedule"):
            with TabPane("Schedule", id="schedule"):
                yield SchedulePane(self._client, self._initial_date)
            with TabPane("Standings", id="standings"):
                yield StandingsPane(self._client)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "mlbapi  —  MLB Live Scores"
        self.sub_title = "Interactive Terminal"
        self.set_interval(30, self._auto_refresh)

    def _auto_refresh(self) -> None:
        self.query_one(SchedulePane).refresh_data()

    def action_refresh(self) -> None:
        tab = self.query_one(TabbedContent).active
        if tab == "schedule":
            self.query_one(SchedulePane).refresh_data()
        else:
            self.query_one(StandingsPane).refresh_data()

    def action_prev_date(self) -> None:
        self.query_one(SchedulePane).prev_date()

    def action_next_date(self) -> None:
        self.query_one(SchedulePane).next_date()

    def action_open_boxscore(self) -> None:
        if self.query_one(TabbedContent).active != "schedule":
            return
        game_pk = self.query_one(SchedulePane).selected_game_pk()
        if game_pk is not None:
            self.push_screen(BoxScoreScreen(game_pk, self._client))

    def action_quit(self) -> None:
        self.exit()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive MLB terminal — live scores, box scores, standings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        metavar="YYYY-MM-DD",
        help="Starting date (default: today)",
    )
    args = parser.parse_args()

    try:
        initial_date = date.fromisoformat(args.date)
    except ValueError:
        parser.error(f"Invalid date: {args.date!r} — use YYYY-MM-DD format")

    MLBTerminal(initial_date).run()


if __name__ == "__main__":
    main()
