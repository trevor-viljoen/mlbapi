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

def _to_camel(snake: str) -> str:
    """Convert snake_case to camelCase for dict key fallback lookups."""
    parts = snake.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def _attr(obj, *keys, default=""):
    """Safely traverse a chain of attributes or dict keys.

    Handles Pydantic model attributes *and* raw API dicts (e.g. ``line.status``
    is stored as ``{"abstractGameState": "Live"}`` by Pydantic's extra="allow").
    For dicts, tries the snake_case key first, then the camelCase equivalent.
    """
    for key in keys:
        if obj is None:
            return default
        if isinstance(obj, dict):
            obj = obj.get(key, obj.get(_to_camel(key)))
        else:
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
    """Return a 2-line base diamond (no home plate — scoring = off bases).

    Layout:  col 2 = 2B  (2-space indent)
             col 0 = 3B, col 4 = 1B  (3 spaces between, midpoint = col 2) ✓
    """
    on  = "[bold yellow]◆[/bold yellow]"
    off = "[dim]◇[/dim]"
    return f"  {on if second else off}\n{on if third else off}   {on if first else off}"


# ---------------------------------------------------------------------------
# Game Screen widgets
# ---------------------------------------------------------------------------

class ScoreBug(Static):
    """Top-of-screen score/inning display."""

    def update_state(self, abstract: str, line, away_name: str, home_name: str,
                     away_score: str, home_score: str) -> None:
        inning = _attr(line, "current_inning_ordinal", default="")
        is_top = _attr(line, "is_top_inning", default=None)

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
    """Base diamond + B/S/O count display.

    Flashes a yellow border briefly whenever a new runner reaches base.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._prev_bases = (False, False, False)

    def update_state(self, abstract: str, line) -> None:
        if abstract not in ("Live",):
            self.update("")
            return

        first  = _attr(line, "offense", "first",  default=None) is not None
        second = _attr(line, "offense", "second", default=None) is not None
        third  = _attr(line, "offense", "third",  default=None) is not None
        balls   = int(_attr(line, "balls",   default=0) or 0)
        strikes = int(_attr(line, "strikes", default=0) or 0)
        outs    = int(_attr(line, "outs",    default=0) or 0)

        current = (first, second, third)
        if self._prev_bases != current:
            new_runner = any(c and not p for c, p in zip(current, self._prev_bases))
            if new_runner:
                self._flash_bases()
        self._prev_bases = current

        diamond = _base_diamond(first, second, third)
        # 3B / 2S / 2O: the 4th ball = walk, 3rd strike = K, 3rd out = end of inning —
        # all reset immediately, so we never need to show the final pip filled.
        b = _pips(min(balls,   3), 3, "●", "○", "green",  "dim")
        s = _pips(min(strikes, 2), 2, "●", "○", "red",    "dim")
        o = _pips(min(outs,    2), 2, "●", "○", "yellow", "dim")

        count_line = f"B {b}  S {s}  O {o}"
        self.update(f"{diamond}\n\n{count_line}")

    def _flash_bases(self) -> None:
        self.add_class("base-flash")
        self.set_timer(0.7, lambda: self.remove_class("base-flash"))


class MatchupDisplay(Static):
    """Current batter vs pitcher."""

    def update_state(self, abstract: str, line) -> None:
        if abstract != "Live":
            self.update("")
            return
        batter  = _attr(line, "offense", "batter",  "full_name", default="—")
        pitcher = _attr(line, "defense", "pitcher", "full_name", default="—")
        on_deck = _attr(line, "offense", "on_deck", "full_name", default="")
        self.update(
            f"[bold]AB:[/bold] {batter}  [dim]vs[/dim]  {pitcher}\n"
            + (f"[dim]On deck: {on_deck}[/dim]" if on_deck else "")
        )


class LastPlay(Static):
    """Most recent completed play — event type + short description."""

    _EVENT_STYLE = {
        "Home Run": "bold yellow",
        "Triple":   "bold green",
        "Double":   "bold green",
        "Single":   "green",
        "Walk":     "cyan",
        "Hit By Pitch": "cyan",
    }

    def set_play(self, event: str, desc: str, is_scoring: bool) -> None:
        if not event and not desc:
            self.update("")
            return
        icon  = "★" if is_scoring else "⚾"
        style = "bold green" if is_scoring else self._EVENT_STYLE.get(event, "dim")
        short = (desc[:54] + "…") if len(desc) > 54 else desc
        self.update(f"[{style}]{icon} {event}[/{style}]\n[dim]{short}[/dim]")


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


class BoxScoreTable(Widget):
    """Batting lineup with stats for one team."""

    DEFAULT_CSS = """
    BoxScoreTable { height: auto; }
    BoxScoreTable #bs-title { padding: 0 1; text-style: bold; background: $panel; }
    BoxScoreTable DataTable { height: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Label("BATTING", id="bs-title")
        yield DataTable(id="bs-table", show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#bs-table", DataTable).add_columns(
            "Player", "Pos", "AB", "R", "H", "RBI", "BB", "K", "AVG"
        )

    def populate(self, box, side: str) -> None:
        """Fill batting rows from a BoxScore model and team side ('away'/'home')."""
        team_obj = _attr(box, "teams", side, default=None)
        if team_obj is None:
            return
        team_name = _attr(team_obj, "team", "name", default=side.upper())
        self.query_one("#bs-title", Label).update(f"[bold]{team_name} BATTING[/bold]")

        players_list = getattr(team_obj, "players", None) or []
        player_map: dict = {}
        for p in players_list:
            pid = _attr(p, "person", "id", default=None)
            if pid is not None:
                player_map[pid] = p

        batters = getattr(team_obj, "batters", None) or []
        if not isinstance(batters, list):
            return

        table = self.query_one("#bs-table", DataTable)
        table.clear()
        for pid in batters:
            player = player_map.get(pid)
            if not player:
                continue
            name = _attr(player, "person", "full_name", default="—")
            pos  = _attr(player, "position", "abbreviation", default="")
            bat  = _attr(player, "stats", "batting", default=None)
            ab   = _attr(bat, "at_bats",      default="-")
            r    = _attr(bat, "runs",          default="-")
            h    = _attr(bat, "hits",          default="-")
            rbi  = _attr(bat, "rbi",           default="-")
            bb   = _attr(bat, "base_on_balls", default="-")
            k    = _attr(bat, "strike_outs",   default="-")
            avg  = _attr(bat, "avg",           default=".---")
            # Shorten "Firstname Lastname" → "F. Lastname" for narrow display
            parts = name.rsplit(" ", 1)
            short = f"{parts[0][0]}. {parts[1]}" if len(parts) == 2 else name
            table.add_row(
                short[:18], pos[:3],
                str(ab), str(r), str(h), str(rbi), str(bb), str(k), str(avg),
            )


class PitchingTable(Widget):
    """Pitching line for one team."""

    DEFAULT_CSS = """
    PitchingTable { height: auto; }
    PitchingTable #pt-title { padding: 0 1; text-style: bold; background: $panel; }
    PitchingTable DataTable { height: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Label("PITCHING", id="pt-title")
        yield DataTable(id="pt-table", show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#pt-table", DataTable).add_columns(
            "Pitcher", "IP", "H", "R", "ER", "BB", "K", "ERA"
        )

    def populate(self, box, side: str) -> None:
        team_obj = _attr(box, "teams", side, default=None)
        if team_obj is None:
            return
        team_name = _attr(team_obj, "team", "name", default=side.upper())
        self.query_one("#pt-title", Label).update(f"[bold]{team_name} PITCHING[/bold]")

        players_list = getattr(team_obj, "players", None) or []
        player_map: dict = {}
        for p in players_list:
            pid = _attr(p, "person", "id", default=None)
            if pid is not None:
                player_map[pid] = p

        pitchers = getattr(team_obj, "pitchers", None) or []
        if not isinstance(pitchers, list):
            return

        table = self.query_one("#pt-table", DataTable)
        table.clear()
        for pid in pitchers:
            player = player_map.get(pid)
            if not player:
                continue
            name = _attr(player, "person", "full_name", default="—")
            pit  = _attr(player, "stats", "pitching", default=None)
            ip   = _attr(pit, "innings_pitched", default="-")
            h    = _attr(pit, "hits",             default="-")
            r    = _attr(pit, "runs",             default="-")
            er   = _attr(pit, "earned_runs",      default="-")
            bb   = _attr(pit, "base_on_balls",    default="-")
            k    = _attr(pit, "strike_outs",      default="-")
            era  = _attr(pit, "era",              default="-")
            parts = name.rsplit(" ", 1)
            short = f"{parts[0][0]}. {parts[1]}" if len(parts) == 2 else name
            table.add_row(short[:18], str(ip), str(h), str(r), str(er), str(bb), str(k), str(era))


class BoxScorePane(Widget):
    """Away and home batting + pitching stats, scrollable."""

    DEFAULT_CSS = "BoxScorePane { height: 1fr; }"

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield BoxScoreTable(id="bs-away")
            yield PitchingTable(id="bp-away")
            yield BoxScoreTable(id="bs-home")
            yield PitchingTable(id="bp-home")

    def populate(self, box) -> None:
        self.query_one("#bs-away", BoxScoreTable).populate(box, "away")
        self.query_one("#bp-away", PitchingTable).populate(box, "away")
        self.query_one("#bs-home", BoxScoreTable).populate(box, "home")
        self.query_one("#bp-home", PitchingTable).populate(box, "home")


# ---------------------------------------------------------------------------
# Pitch F/X widgets
# ---------------------------------------------------------------------------

_PITCH_CALL_STYLE: dict[str, str] = {
    "B": "green",        # Ball
    "C": "red",          # Called Strike
    "S": "bold red",     # Swinging Strike
    "F": "yellow",       # Foul
    "T": "yellow",       # Foul Tip
    "X": "dim",          # In Play (out recorded)
    "D": "bold yellow",  # In Play (no out)
    "E": "bold yellow",  # In Play (run scored)
}

_PITCH_CALL_CHAR: dict[str, str] = {
    "B": "B",  "C": "K",  "S": "S",  "F": "F",
    "T": "T",  "X": "X",  "D": "H",  "E": "R",
}

_PITCH_TYPE_SHORT: dict[str, str] = {
    "Four-Seam Fastball": "FF",
    "Two-Seam Fastball":  "FT",
    "Sinker":             "SI",
    "Cutter":             "FC",
    "Curveball":          "CU",
    "Slider":             "SL",
    "Sweeper":            "SW",
    "Changeup":           "CH",
    "Split-Finger":       "FS",
    "Knuckleball":        "KN",
    "Fastball":           "FA",
}


class StrikeZonePlot(Static):
    """3×3 MLB strike zone grid (catcher's view).

    Zone layout:
        1 | 2 | 3   (top)
        4 | 5 | 6   (middle)
        7 | 8 | 9   (bottom)
    Shows the most-recent pitch call per zone cell.
    Pitches with zone 11–14 land outside the box (not plotted).
    """

    DEFAULT_CSS = "StrikeZonePlot { height: auto; padding: 0 0; }"

    def set_pitches(self, pitches: list[dict]) -> None:
        zone_map: dict[int, str] = {}
        for p in pitches:
            pd   = p.get("pitchData") or {}
            zone = pd.get("zone")
            code = (p.get("details") or {}).get("call", {}).get("code", "")
            if zone is not None:
                try:
                    zone_map[int(zone)] = code
                except (ValueError, TypeError):
                    pass

        def cell(z: int) -> str:
            code = zone_map.get(z)
            if code is None:
                return "[dim] · [/dim]"
            ch    = _PITCH_CALL_CHAR.get(code, code or "?")
            style = _PITCH_CALL_STYLE.get(code, "")
            return f"[{style}] {ch} [/{style}]" if style else f" {ch} "

        rows = [
            "┌───┬───┬───┐",
            f"│{cell(1)}│{cell(2)}│{cell(3)}│",
            "├───┼───┼───┤",
            f"│{cell(4)}│{cell(5)}│{cell(6)}│",
            "├───┼───┼───┤",
            f"│{cell(7)}│{cell(8)}│{cell(9)}│",
            "└───┴───┴───┘",
        ]
        self.update("\n".join(rows))


class PitchSequence(Widget):
    """Current at-bat pitch sequence — number, type, velocity, call."""

    DEFAULT_CSS = """
    PitchSequence { height: auto; }
    PitchSequence #ps-title { padding: 0 1; text-style: bold; background: $panel; }
    PitchSequence DataTable  { height: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Label("At-Bat Pitches", id="ps-title")
        yield DataTable(id="ps-table", show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#ps-table", DataTable).add_columns("#", "Type", "MPH", "Call")

    def populate(self, pitches: list[dict]) -> None:
        table = self.query_one("#ps-table", DataTable)
        table.clear()
        for i, p in enumerate(pitches, 1):
            details    = p.get("details") or {}
            pitch_type = (details.get("type") or {}).get("description", "")
            short_type = _PITCH_TYPE_SHORT.get(pitch_type, pitch_type[:4] if pitch_type else "?")
            pd         = p.get("pitchData") or {}
            speed_raw  = pd.get("startSpeed")
            speed      = f"{speed_raw:.1f}" if speed_raw is not None else "—"
            call_info  = details.get("call") or {}
            call_code  = call_info.get("code", "")
            call_desc  = call_info.get("description", call_code)
            call_ch    = _PITCH_CALL_CHAR.get(call_code, call_code or "?")
            call_style = _PITCH_CALL_STYLE.get(call_code, "")
            call_markup = (
                f"[{call_style}]{call_ch} {call_desc}[/{call_style}]"
                if call_style else f"{call_ch} {call_desc}"
            )
            # Include spin rate if available
            spin = (pd.get("breaks") or {}).get("spinRate")
            spin_str = f"  [dim]{spin:.0f}rpm[/dim]" if spin else ""
            table.add_row(str(i), short_type, speed + spin_str, call_markup)


class PitchFXPane(Widget):
    """Strike zone plot + pitch sequence for the current at-bat."""

    DEFAULT_CSS = "PitchFXPane { height: 1fr; }"

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label(
                "[bold]Strike Zone[/bold]  [dim](catcher's view · last pitch/zone)[/dim]",
                id="pfx-zone-title",
            )
            yield StrikeZonePlot(id="pfx-zone")
            yield PitchSequence(id="pfx-seq")

    def update_pitches(self, pitches: list[dict]) -> None:
        self.query_one("#pfx-zone", StrikeZonePlot).set_pitches(pitches)
        self.query_one("#pfx-seq", PitchSequence).populate(pitches)


# ---------------------------------------------------------------------------
# Game Screen
# ---------------------------------------------------------------------------

class GameScreen(ModalScreen):
    """Full live-game view: score bug, bases/count, matchup, plays, linescore."""

    BINDINGS = [
        Binding("escape", "dismiss",      "Back",      show=False),
        Binding("b",      "dismiss",      "Back"),
        Binding("r",      "refresh_game", "Refresh"),
        Binding("1",      "show_plays",   "Half Inn.", show=False),
        Binding("2",      "show_box",     "Box Score", show=False),
        Binding("3",      "show_full",    "Full PBP",  show=False),
        Binding("4",      "show_pitches", "Pitches",   show=False),
    ]

    DEFAULT_CSS = """
    GameScreen { align: center middle; }

    #gs-outer {
        width: 98%;
        height: 98%;
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
    }

    #gs-middle { height: 1fr; }

    #gs-left {
        width: 30;
        padding: 1 1;
        border-right: solid $panel;
    }

    #gs-right { width: 1fr; }

    BasesCount {
        height: auto;
        padding: 1 0;
    }

    BasesCount.base-flash { border: solid $warning; }

    MatchupDisplay {
        height: auto;
        padding: 1 0;
        border-top: dashed $panel;
    }

    LastPlay {
        height: auto;
        padding: 1 0;
        border-top: dashed $panel;
    }

    #gs-tabs { height: 1fr; }

    #gs-linescore-wrap {
        height: auto;
        padding: 0 1;
        border-top: solid $panel;
    }

    #gs-linescore { height: auto; max-height: 5; }

    #gs-info {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }

    #gs-footer {
        text-align: center;
        height: 1;
        padding: 0 1;
        background: $panel;
        color: $text-muted;
    }

    .scoring-flash { background: darkgreen; }
    """

    def __init__(self, game_pk: int, client: Client,
                 abstract_state: str = "") -> None:
        super().__init__()
        self._game_pk       = game_pk
        self._client        = client
        self._abstract      = abstract_state  # seeded from schedule; refreshed on each load
        self._prev_away     = -1
        self._prev_home     = -1
        self._blink_on      = True
        self._refresh_timer = None

    def compose(self) -> ComposeResult:
        with Vertical(id="gs-outer"):
            yield Label("", id="gs-live-badge")
            yield ScoreBug(id="gs-score-bug")
            with Horizontal(id="gs-middle"):
                with Vertical(id="gs-left"):
                    yield BasesCount(id="gs-bases")
                    yield MatchupDisplay(id="gs-matchup")
                    yield LastPlay(id="gs-lastplay")
                with Vertical(id="gs-right"):
                    with TabbedContent(id="gs-tabs", initial="gs-tab-plays"):
                        with TabPane("▶ Half Inn.", id="gs-tab-plays"):
                            yield PlayFeed(id="gs-playfeed")
                        with TabPane("📋 Box", id="gs-tab-box"):
                            yield BoxScorePane(id="gs-boxscore")
                        with TabPane("📜 Full PBP", id="gs-tab-full"):
                            yield PlayFeed(id="gs-fullpbp")
                        with TabPane("⚾ Pitches", id="gs-tab-pitches"):
                            yield PitchFXPane(id="gs-pitchfx")
            with Vertical(id="gs-linescore-wrap"):
                yield DataTable(id="gs-linescore", show_cursor=False)
                yield Static("", id="gs-info")
            yield Label(
                "[b][Esc/B][/b] back  [b]R[/b] refresh  "
                "[b]1[/b] half inn.  [b]2[/b] box  [b]3[/b] full pbp  [b]4[/b] pitches",
                id="gs-footer",
            )

    def on_mount(self) -> None:
        self._load()
        self.set_interval(0.8, self._blink_live)
        # Start auto-refresh immediately using the state seeded from the schedule.
        # _populate will stop the timer if the game reaches Final.
        if self._abstract != "Final":
            interval = 5 if self._abstract == "Live" else 30
            self._refresh_timer = self.set_interval(interval, self._auto_refresh)

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

        # abstract_game_state: try linescore first (dict traversal), fall back to
        # the value seeded from the schedule when this screen was opened.
        ls_abstract = _attr(line, "status", "abstract_game_state", default="")
        if ls_abstract:
            self._abstract = ls_abstract

        # --- Score bug ---
        self.query_one("#gs-score-bug", ScoreBug).update_state(
            self._abstract, line, away_name, home_name, str(away_r), str(home_r)
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
        self.query_one("#gs-bases", BasesCount).update_state(self._abstract, line)

        # --- Matchup ---
        self.query_one("#gs-matchup", MatchupDisplay).update_state(self._abstract, line)

        # --- Play feed + last play banner ---
        all_plays   = (pbp or {}).get("allPlays",    []) if isinstance(pbp, dict) else []
        scoring_set = set((pbp or {}).get("scoringPlays", []) if isinstance(pbp, dict) else [])

        # Last play banner
        if all_plays:
            last     = all_plays[-1]
            last_idx = len(all_plays) - 1
            self.query_one("#gs-lastplay", LastPlay).set_play(
                last.get("result", {}).get("event",       ""),
                last.get("result", {}).get("description", ""),
                last_idx in scoring_set,
            )

        # Current half-inning filter for the "Half Inn." tab
        curr_inning = _attr(line, "current_inning", default=None)
        is_top      = _attr(line, "is_top_inning",  default=None)
        curr_half   = "top" if is_top else "bottom"

        if self._abstract == "Live" and curr_inning is not None:
            half_indexed = [
                (i, p) for i, p in enumerate(all_plays)
                if (p.get("about", {}).get("inning") == curr_inning
                    and p.get("about", {}).get("halfInning", "").lower() == curr_half)
            ]
        else:
            # Final / Preview: show last 15 plays
            offset = max(0, len(all_plays) - 15)
            half_indexed = list(enumerate(all_plays))[offset:]

        half_descs: list[str] = []
        half_scoring: set[int] = set()
        for orig_idx, play in half_indexed:
            desc = play.get("result", {}).get("description", "")
            if desc:
                if orig_idx in scoring_set:
                    half_scoring.add(len(half_descs))
                half_descs.append(desc)
        self.query_one("#gs-playfeed", PlayFeed).set_plays(half_descs, half_scoring)

        # Full PBP tab — all plays
        all_descs: list[str] = []
        all_scoring: set[int] = set()
        for i, play in enumerate(all_plays):
            desc = play.get("result", {}).get("description", "")
            if desc:
                if i in scoring_set:
                    all_scoring.add(len(all_descs))
                all_descs.append(desc)
        self.query_one("#gs-fullpbp", PlayFeed).set_plays(all_descs, all_scoring)

        # --- Box score (batting lineup) ---
        try:
            self.query_one("#gs-boxscore", BoxScorePane).populate(box)
        except Exception:
            pass  # gracefully skip if box data is unavailable

        # --- Pitch F/X (current at-bat) ---
        curr_play = pbp.get("currentPlay", {}) if isinstance(pbp, dict) else {}
        pitches = [
            e for e in (curr_play.get("playEvents") or [])
            if e.get("type") == "pitch"
        ]
        try:
            self.query_one("#gs-pitchfx", PitchFXPane).update_pitches(pitches)
        except Exception:
            pass

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

        # --- Auto-refresh timer: manage state transitions ---
        if self._abstract == "Final":
            # Game over — stop polling
            if self._refresh_timer is not None:
                self._refresh_timer.stop()
                self._refresh_timer = None
        elif self._refresh_timer is None:
            # Game went Live after we opened it in Preview (or state was unknown)
            interval = 5 if self._abstract == "Live" else 30
            self._refresh_timer = self.set_interval(interval, self._auto_refresh)

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

    def action_show_plays(self) -> None:
        self.query_one("#gs-tabs", TabbedContent).active = "gs-tab-plays"

    def action_show_box(self) -> None:
        self.query_one("#gs-tabs", TabbedContent).active = "gs-tab-box"

    def action_show_full(self) -> None:
        self.query_one("#gs-tabs", TabbedContent).active = "gs-tab-full"

    def action_show_pitches(self) -> None:
        self.query_one("#gs-tabs", TabbedContent).active = "gs-tab-pitches"


# ---------------------------------------------------------------------------
# Schedule Pane
# ---------------------------------------------------------------------------

class SchedulePane(Widget):
    """Schedule DataTable with date navigation."""

    def __init__(self, client: Client, initial_date: date) -> None:
        super().__init__()
        self._client       = client
        self._games: list  = []
        self.current_date  = initial_date  # plain attribute — no reactive timing issues

    def compose(self) -> ComposeResult:
        yield Label("", id="sched-date-label")
        yield Label("", id="sched-status")
        yield DataTable(id="sched-table", cursor_type="row", zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one("#sched-table", DataTable).add_columns(
            "Away", "R", "Home", "R", "Status", "Inning", "Venue",
        )
        self._update_date_label()
        self._load()

    def _update_date_label(self) -> None:
        self.query_one("#sched-date-label", Label).update(
            f"[bold]{self.current_date.strftime('%A, %B %-d, %Y')}[/bold]"
        )

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
            inning   = _attr(game, "linescore", "current_inning",           default="")
            half     = _attr(game, "linescore", "inning_half_abbreviation", default="")

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

        table.refresh()

    def selected_game_pk(self) -> Optional[int]:
        pk, _ = self.selected_game_info()
        return pk

    def selected_game_info(self) -> tuple:
        """Return (game_pk, abstract_game_state) for the currently highlighted row."""
        table = self.query_one("#sched-table", DataTable)
        idx = table.cursor_row
        if not self._games or idx < 0 or idx >= len(self._games):
            return None, ""
        game = self._games[idx]
        abstract = _attr(game, "status", "abstract_game_state", default="")
        return getattr(game, "game_pk", None), abstract

    def prev_date(self) -> None:
        self.current_date = self.current_date - timedelta(days=1)
        self._update_date_label()
        self._load()

    def next_date(self) -> None:
        self.current_date = self.current_date + timedelta(days=1)
        self._update_date_label()
        self._load()

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
        pk, abstract = self.query_one(SchedulePane).selected_game_info()
        if pk is not None:
            self.push_screen(GameScreen(pk, self._client, abstract_state=abstract))

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
