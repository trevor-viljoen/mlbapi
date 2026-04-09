#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live MLB scores TUI — terminal dashboard using only the stdlib curses module.

Run with::

    python examples/live_scores.py

Press ``q`` to quit, ``Left``/``Right`` arrow keys to move between dates,
and ``r`` to force a refresh.

Requires the mlbapi package to be installed (``pip install -e ".[dev]"``).
"""

import curses
import datetime
import time

import mlbapi


# ---------------------------------------------------------------------------
# Portable day-without-leading-zero helper
# ---------------------------------------------------------------------------

def _day_no_pad(dt: datetime.date) -> str:
    """Return the day-of-month as a string with no leading zero.

    Uses ``strftime('%d').lstrip('0') or '0'`` which works on every platform
    (``'%-d'`` is Linux-only and raises ``ValueError`` on Windows/macOS).
    """
    return dt.strftime('%d').lstrip('0') or '0'


# ---------------------------------------------------------------------------
# UI Panes
# ---------------------------------------------------------------------------

class SchedulePane:
    """Renders the schedule for a single date inside a curses window."""

    DATE_FMT = '%A, %B {day}, %Y'   # {day} is replaced by _day_no_pad()

    def __init__(self, window):
        self._win = window
        self._date = datetime.date.today()
        self._games = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def refresh_data(self):
        """Fetch today's schedule from the API."""
        date_str = self._date.strftime('%Y-%m-%d')
        try:
            sched = mlbapi.schedule(date=date_str)
            self._games = []
            for day in (sched.dates or []):
                for game in (day.games or []):
                    self._games.append(game)
        except Exception:  # noqa: BLE001 — show empty list on any API error
            self._games = []

    def move_date(self, delta_days: int):
        """Shift the displayed date by *delta_days* days."""
        self._date += datetime.timedelta(days=delta_days)
        self.refresh_data()

    def draw(self):
        """Render the pane into its curses window."""
        self._win.erase()
        self._update_date_label()
        self._draw_games()
        self._win.refresh()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _update_date_label(self):
        """Write the formatted date into row 0 of the window.

        Uses a portable day formatter — avoids the Linux-only ``'%-d'``
        strftime directive.
        """
        label = self.DATE_FMT.replace('{day}', _day_no_pad(self._date))
        formatted = self._date.strftime(label)
        try:
            self._win.addstr(0, 0, formatted, curses.A_BOLD)
        except curses.error:
            pass  # window too narrow — skip gracefully

    def _draw_games(self):
        """Write one line per game starting at row 2."""
        if not self._games:
            try:
                self._win.addstr(2, 2, 'No games scheduled.')
            except curses.error:
                pass
            return

        for idx, game in enumerate(self._games, start=2):
            try:
                away = getattr(getattr(getattr(game, 'teams', None), 'away', None),
                               'team', None)
                home = getattr(getattr(getattr(game, 'teams', None), 'home', None),
                               'team', None)
                away_name = getattr(away, 'name', '???') if away else '???'
                home_name = getattr(home, 'name', '???') if home else '???'

                away_score = getattr(
                    getattr(game.teams, 'away', None), 'score', None)
                home_score = getattr(
                    getattr(game.teams, 'home', None), 'score', None)

                state = getattr(
                    getattr(game, 'status', None), 'abstract_game_state', '')

                if away_score is not None and home_score is not None:
                    line = f'  {away_name:25s} {away_score:>2}  @  {home_name:25s} {home_score:>2}  [{state}]'
                else:
                    game_time = getattr(game, 'game_date', '')
                    line = f'  {away_name:25s}  @  {home_name:25s}  [{game_time}]'

                self._win.addstr(idx, 0, line[:curses.COLS - 1])
            except curses.error:
                break


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def _main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(30_000)  # refresh every 30 s

    pane = SchedulePane(stdscr)
    pane.refresh_data()
    pane.draw()

    while True:
        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key == curses.KEY_LEFT:
            pane.move_date(-1)
        elif key == curses.KEY_RIGHT:
            pane.move_date(1)
        elif key in (ord('r'), ord('R'), curses.ERR):
            # ERR means timeout — auto-refresh
            if key != curses.ERR:
                pane.refresh_data()

        pane.draw()


def main():
    curses.wrapper(_main)


if __name__ == '__main__':
    main()
