#!/usr/bin/env python3
"""Interactive MLB terminal — live scores, box scores, and standings.

Usage
-----
    python examples/live_scores.py
    python examples/live_scores.py --date 2024-06-01

Controls
--------
    Tab / Shift+Tab     Switch between Schedule and Standings
    Shift+← / Shift+→  Previous / next date  ([ / ] also work)
    ↑ / ↓              Navigate game rows
    Enter               Open live game view
    r                   Refresh data
    q                   Quit

    Inside game view:
    Esc / b             Return to schedule

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
from textual.screen import ModalScreen, Screen
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
    s = _attr(team_side, "score", default=None)
    return str(s) if s is not None else "-"


def _pips(filled: int, total: int, filled_char: str, empty_char: str,
          filled_style: str = "", empty_style: str = "dim") -> str:
    parts = []
    for i in range(total):
        ch = filled_char if i < filled else empty_char
        style = filled_style if i < filled else empty_style
        parts.append(f"[{style}]{ch}[/]" if style else ch)
    return " ".join(parts)


def _base_diamond(first: bool, second: bool, third: bool) -> str:
    """Return a 3-line Unicode base-path diamond."""
    on  = "[bold yellow]◆[/bold yellow]"
    off = "[dim]◇[/dim]"
    b1 = on if first  else off
    b2 = on if second else off
    b3 = on if third  else off
    return f"   {b2}\n{b3}   {b1}\n   [dim]◇[/dim]"


# ---------------------------------------------------------------------------
# Game Screen widgets
# ---------------------------------------------------------------------------

class ScoreBug(Static):
    """Top-of-screen score/inning display."""

    def update_state(self, line, away_name: str, home_name: str,
                     away_score: str, home_score: str) -> None:
        abstract = _attr(line, "status", "abstract_game_state", default="")
        inning   = _attr(line, "current_inning_ordinal", default="")
        half     = _attr(line, "inning_half", default="")
        is_top   = _attr(line, "is_top_inning", default=None)

        if abstract == "Final":
            middle = "[bold green] FINAL [/bold green]"
        elif abstract == "Live" and inning:
            abbr = "▲" if is_top else "▼"
            middle = f"[bold yellow] {abbr} {inning} [/bold yellow]"
        else:
            game_time = _attr(line, "game_date", default="")
            t = game_time.split("T")[1][:5] if "T" in game_time else "—"
            middle = f"[dim] {t} UTC [/dim]"

        away_str = f"[bold]{away_name}[/bold]  [bold cyan]{away_score}[/bold cyan]"
        home_str = f"[bold cyan]{home_score}[/bold cyan]  [bold]{home_name}[/bold]"
        self.update(f"{away_str}  {middle}  {home_str}")


class BasesCount(Static):
    """Combined base diamond + B/S/O count display."""

    def update_state(self, line) -> None:
        first  = _attr(line, "offense", "first",  default=None) is not None
        second = _attr(line, "offense", "second", default=None) is not None
        third  = _attr(line, "offense", "third",  default=None) is not None

        balls   = int(_attr(line, "balls",   default=0) or 0)
        strikes = int(_attr(line, "strikes", default=0) or 0)
        outs    = int(_attr(line, "outs",    default=0) or 0)

        abstract = _attr(line, "status", "abstract_game_state", default="")
        if abstract not in ("Live",):
            self.update("")
            return

        diamond = _base_diamond(first, second, third)
        b = _pips(balls,   4, "⬤", "○", "green",  "dim")
        s = _pips(strikes, 3, "⬤", "○", "red",    "dim")
        o = _pips(outs,    3, "⬤", "○", "yellow", "dim")

        count_line = f"B {b}   S {s}   O {o}"
        self.update(f"{diamond}\n\n{count_line}")


class MatchupDisplay(Static):
    """Current batter vs pitcher."""

    def update_state(self, line) -> None:
        abstract = _attr(line, "status", "abstract_game_state", default="")
        if abstract != "Live":
            self.update("")
            return
        batter  = _attr(line, "offense", "batter",   "full_name", default="—")
        pitcher = _attr(line, "defense", "pitcher",  "full_name", default="—")
        on_deck = _attr(line, "offense", "on_deck",  "full_name", default="")
        self.update(
            f"[bold]AB:[/bold] {batter}  [dim]vs[/dim]  {pitcher}\n"
            + (f"[dim]On deck: {on_deck}[/dim]" if on_deck else "")
        )


class PlayFeed(Widget):
    """Scrollable recent play-by-play feed."""

    DEFAULT_CSS = """
    PlayFeed { height: 1fr; border: solid $panel; }
    PlayFeed Label { padding: 0 1; }
    PlayFeed #pf-title { text-style: bold; background: $panel; }
    PlayFeed ScrollableContainer { height: 1fr; }
    """

    def compose(self) -> ComposeResult:
        yield Label("Recent Plays", id="pf-title")
        with ScrollableContainer(id="pf-scroll"):
            yield Static("", id="pf-content")

    def set_plays(self, plays: list[str], scoring_indices: set[int]) -> None:
        lines = []
        for i, desc in enumerate(plays):
            if i in scoring_indices:
                lines.append(f"[bold green]★ {desc}[/bold green]")
            else:
                lines.append(f"[dim]·[/dim] {desc}")
        self.query_one("#pf-content", Static).update("\n".join(lines) if lines else "[dim]No plays yet.[/dim]")
        # Auto-scroll to bottom (most recent play)
        self.query_one("#pf-scroll", ScrollableContainer).scroll_end(animate=False)


# ---------------------------------------------------------------------------
# Game Screen
# ---------------------------------------------------------------------------

class GameScreen(ModalScreen):
    """Full live-game view: score bug, bases/count, matchup, plays, linescore."""

    BINDINGS = [
        Binding("escape", "dismiss", "Back", show=False),
        Binding("b",      "dismiss", "Back"),
        Binding("r",      "refresh_game", "Refresh"),
    ]

    DEFAULT_CSS = """
    GameScreen { align: center middle; }

    #gs-outer {
        width: 95%;
        height: 95%;
        border: round $primary;
        background: $surface;
    }

    #gs-score-bug {
        text-align: center;
        padding: 1 2;
        background: $panel;
        text-style: bold;
    }

    #gs-live-badge {
        text-align: center;
        height: 1;
        padding: 0 1;
    }

    #gs-middle {
        height: 1fr;
    }

    #gs-left {
        width: 28;
        padding: 1 2;
        border-right: solid $panel;
    }

    #gs-right {
        width: 1fr;
    }

    BasesCount {
        height: auto;
        padding: 1 0;
    }

    MatchupDisplay {
        height: auto;
        padding: 1 0;
    }

    #gs-linescore-wrap {
        height: auto;
        padding: 1 2;
        border-top: solid $panel;
    }

    #gs-linescore {
        height: auto;
    }

    #gs-info {
        height: auto;
        padding: 0 2 1 2;
        color: $text-muted;
    }

    #gs-footer {
        text-align: center;
        height: 1;
        padding: 0 1;
        background: $panel;
        color: $text-muted;
    }

    .live-on  { color: red; }
    .live-off { color: $panel; }
    """

    def __init__(self, game_pk: int, client: Client) -> None:
        super().__init__()
        self._game_pk   = game_pk
        self._client    = client
        self._abstract  = ""
        self._prev_away = -1
        self._prev_home = -1
        self._blink_on  = True
        self._refresh_timer = None

    def compose(self) -> ComposeResult:
        with Vertical(id="gs-outer"):
            yield ScoreBug(id="gs-score-bug")
            yield Label("", id="gs-live-badge")
            with Horizontal(id="gs-middle"):
                with Vertical(id="gs-left"):
                    yield BasesCount(id="gs-bases")
                    yield MatchupDisplay(id="gs-matchup")
                yield PlayFeed(id="gs-playfeed")
            with Vertical(id="gs-linescore-wrap"):
                yield DataTable(id="gs-linescore", show_cursor=False)
                yield Static("", id="gs-info")
            yield Label("[b][Esc / B][/b] back  [b]R[/b] refresh", id="gs-footer")

    def on_mount(self) -> None:
        self._load()
        # Blinking ● LIVE indicator
        self.set_interval(0.8, self._blink_live)

    @work(thread=True)
    def _load(self) -> None:
        try:
            box  = self._client.boxscore(self._game_pk)
            line = self._client.linescore(self._game_pk)
            pbp  = self._client.play_by_play(self._game_pk)
        except MLBAPIException as exc:
            self.app.call_from_thread(lambda: self._show_error(str(exc)))
            return
        self.app.call_from_thread(lambda: self._populate(box, line, pbp))

    def _show_error(self, msg: str) -> None:
        self.query_one("#gs-score-bug", ScoreBug).update(f"[red]{msg}[/red]")

    def _populate(self, box, line, pbp) -> None:
        away_name = _attr(box, "teams", "away", "team", "name", default="Away")
        home_name = _attr(box, "teams", "home", "team", "name", default="Home")
        away_r    = _attr(box, "teams", "away", "team_stats", "batting", "runs", default="-")
        home_r    = _attr(box, "teams", "home", "team_stats", "batting", "runs", default="-")

        self._abstract = _attr(line, "status", "abstract_game_state", default="")

        # --- Score bug ---
        self.query_one("#gs-score-bug", ScoreBug).update_state(
            line, away_name, home_name, str(away_r), str(home_r)
        )

        # --- Scoring play flash ---
        try:
            away_now = int(away_r)
            home_now = int(home_r)
            if (self._prev_away >= 0 and
                    (away_now > self._prev_away or home_now > self._prev_home)):
                self._flash_score()
            self._prev_away = away_now
            self._prev_home = home_now
        except (TypeError, ValueError):
            pass

        # --- Bases + count ---
        self.query_one("#gs-bases", BasesCount).update_state(line)

        # --- Matchup ---
        self.query_one("#gs-matchup", MatchupDisplay).update_state(line)

        # --- Play feed ---
        all_plays = (pbp or {}).get("allPlays", []) if isinstance(pbp, dict) else []
        scoring_set = set((pbp or {}).get("scoringPlays", []) if isinstance(pbp, dict) else [])
        recent = all_plays[-20:]  # last 20 plays
        offset = max(0, len(all_plays) - 20)
        adjusted_scoring = {i - offset for i in scoring_set if i >= offset}

        descs = [
            p.get("result", {}).get("description", "")
            for p in recent
            if p.get("result", {}).get("description")
        ]
        self.query_one("#gs-playfeed", PlayFeed).set_plays(descs, adjusted_scoring)

        # --- Linescore by inning ---
        ls = self.query_one("#gs-linescore", DataTable)
        ls.clear(columns=True)
        innings = getattr(line, "innings", []) or []
        ls.add_columns("", *[str(inn.num) for inn in innings], "R", "H", "E")

        away_t = _attr(line, "teams", "away", default=None)
        home_t = _attr(line, "teams", "home", default=None)
        ls.add_row(
            away_name,
            *[str(_attr(inn, "away", "runs", default="x")) for inn in innings],
            str(_attr(away_t, "runs",   default=away_r)),
            str(_attr(away_t, "hits",   default="?")),
            str(_attr(away_t, "errors", default="?")),
        )
        ls.add_row(
            home_name,
            *[str(_attr(inn, "home", "runs", default="x")) for inn in innings],
            str(_attr(home_t, "runs",   default=home_r)),
            str(_attr(home_t, "hits",   default="?")),
            str(_attr(home_t, "errors", default="?")),
        )

        # --- Game info ---
        info_items = getattr(box, "info", []) or []
        info_lines = [
            f"[dim]{_attr(i, 'label')}:[/dim] {_attr(i, 'value')}"
            for i in info_items if _attr(i, "label")
        ]
        if info_lines:
            self.query_one("#gs-info", Static).update("  ".join(info_lines[:4]))

        # --- Schedule auto-refresh ---
        if self._refresh_timer is None:
            if self._abstract == "Live":
                self._refresh_timer = self.set_interval(10, self._auto_refresh)
            elif self._abstract == "Preview":
                self._refresh_timer = self.set_interval(30, self._auto_refresh)

    def _flash_score(self) -> None:
        """Briefly highlight the score bug to signal a scoring play."""
        bug = self.query_one("#gs-score-bug", ScoreBug)
        bug.add_class("scoring-flash")
        self.set_timer(1.5, lambda: bug.remove_class("scoring-flash"))

    def _blink_live(self) -> None:
        if self._abstract != "Live":
            return
        badge = self.query_one("#gs-live-badge", Label)
        if self._blink_on:
            badge.update("[bold red]● LIVE[/bold red]")
        else:
            badge.update("[dim]● LIVE[/dim]")
        self._blink_on = not self._blink_on

    def _auto_refresh(self) -> None:
        self._load()

    def action_refresh_game(self) -> None:
        self._load()


# ---------------------------------------------------------------------------
# Schedule Pane
# ---------------------------------------------------------------------------

class SchedulePane(Widget):
    """Schedule DataTable with date navigation."""

    current_date: reactive[date] = reactive(date.today, init=False)

    def __init__(self, client: Client, initial_date: date) -> None:
        super().__init__()
        self._client       = client
        self._games: list  = []
        self._initial_date = initial_date

    def compose(self) -> ComposeResult:
        yield Label("", id="sched-date-label")
        yield Label("", id="sched-status")
        yield DataTable(id="sched-table", cursor_type="row", zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#sched-table", DataTable).add_columns(
            "Away", "R", "Home", "R", "Status", "Inning", "Venue",
        )
        # call_after_refresh ensures the full widget tree is laid out before
        # we trigger the first network load.
        self.call_after_refresh(lambda: setattr(self, "current_date", self._initial_date))

    def watch_current_date(self, d: date) -> None:
        self.query_one("#sched-date-label", Label).update(
            f"[bold]{d.strftime('%A, %B %-d, %Y')}[/bold]"
        )
        self._load()

    @work(thread=True)
    def _load(self) -> None:
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
            away     = _attr(game, "teams", "away", default=None)
            home     = _attr(game, "teams", "home", default=None)
            abstract = _attr(game, "status", "abstract_game_state", default="")
            state    = _attr(game, "status", "detailed_state",       default="")
            inning   = _attr(game, "linescore", "current_inning",               default="")
            half     = _attr(game, "linescore", "inning_half_abbreviation",     default="")

            if abstract == "Final":
                status_str, inning_str = "[green]Final[/green]", ""
            elif abstract == "Live":
                status_str = "[bold yellow]Live[/bold yellow]"
                inning_str = f"{half} {inning}" if inning else ""
            elif abstract == "Preview":
                game_time = _attr(game, "game_date", default="")
                status_str = (
                    f"[dim]{game_time.split('T')[1][:5]} UTC[/dim]"
                    if "T" in game_time else f"[dim]{state}[/dim]"
                )
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

        # Ensure the table redraws after bulk row insertion
        table.refresh()

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
# Standings Pane
# ---------------------------------------------------------------------------

class StandingsPane(Widget):

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
                    str(_attr(tr, "wins",               default="")),
                    str(_attr(tr, "losses",             default="")),
                    str(_attr(tr, "winning_percentage", default="")),
                    str(_attr(tr, "games_back",         default="")),
                    _attr(tr, "streak", "streak_code",  default=""),
                )

    def refresh_data(self) -> None:
        self._load()


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------

class MLBTerminal(App):

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

    .scoring-flash { background: darkgreen; }
    """

    BINDINGS = [
        Binding("q",           "quit",         "Quit"),
        Binding("r",           "refresh",      "Refresh"),
        Binding("shift+left",  "prev_date",    "← Day"),
        Binding("shift+right", "next_date",    "Day →"),
        Binding("[",           "prev_date",    "← Day",  show=False),
        Binding("]",           "next_date",    "Day →",  show=False),
        Binding("enter",       "open_game",    "Game view"),
    ]

    def __init__(self, initial_date: date, client: Optional[Client] = None) -> None:
        super().__init__()
        self._initial_date = initial_date
        self._client       = client or Client()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial="schedule"):
            with TabPane("Schedule", id="schedule"):
                yield SchedulePane(self._client, self._initial_date)
            with TabPane("Standings", id="standings"):
                yield StandingsPane(self._client)
        yield Footer()

    def on_mount(self) -> None:
        self.title     = "mlbapi  —  MLB Live Scores"
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

    def action_open_game(self) -> None:
        if self.query_one(TabbedContent).active != "schedule":
            return
        game_pk = self.query_one(SchedulePane).selected_game_pk()
        if game_pk is not None:
            self.push_screen(GameScreen(game_pk, self._client))

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
