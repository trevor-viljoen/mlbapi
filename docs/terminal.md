# Interactive Terminal

`examples/live_scores.py` is a full interactive terminal for browsing live
scores, box scores, and standings, built with [Textual](https://textual.textualize.io/).

---

## Installation

```bash
pip install "mlbapi[examples]"
# or directly:
pip install textual
```

---

## Running

```bash
# Today's games
python examples/live_scores.py

# Start on a specific date
python examples/live_scores.py --date 2024-06-01
```

---

## Controls

| Key | Action |
|---|---|
| `Tab` / `Shift+Tab` | Switch between Schedule and Standings tabs |
| `↑` / `↓` | Navigate game rows |
| `Shift+←` / `Shift+→` | Previous / next date |
| `[` / `]` | Previous / next date (alternative) |
| `Enter` | Open box score for the selected game |
| `r` | Refresh data |
| `q` | Quit |
| `Esc` / `b` | Close box score (return to schedule) |

> **Note:** Plain `←`/`→` are consumed by the game table for cell navigation.
> Use `Shift+←`/`Shift+→` or `[`/`]` to change dates.

---

## Views

### Schedule

Shows all games for the current date with:
- Away and home team names
- Current score (or `-` if the game hasn't started)
- Game status: time, Live with inning, or Final
- Venue name

Auto-refreshes every 30 seconds so live scores stay current.

### Box Score (modal)

Press `Enter` on any game to open a full box score showing:
- Final / live score header
- Away batting lineup with AB / R / H / RBI / BB / SO / AVG
- Home batting lineup with totals
- Inning-by-inning linescore (R / H / E)
- Game info (weather, wind, attendance)

### Standings

Shows current AL and NL standings side-by-side, grouped by division:
- W / L / PCT / GB / Streak

---

## Screenshot

```
╔══════════════════ mlbapi — MLB Live Scores ══════════════════════════════════╗
║ Schedule [Tab]      Standings [Tab]                                  12:30  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Tuesday, June 1, 2024                                                        ║
║                                                                              ║
║  Away                  R   Home                  R   Status   Inn   Venue   ║
║  ──────────────────────────────────────────────────────────────────────────  ║
║  New York Yankees      3   Houston Astros         5   Final         ...     ║
║  Boston Red Sox        1   Tampa Bay Rays         0   Live    B 7th ...     ║
║  Los Angeles Dodgers   -   San Francisco Giants   -   07:15 UTC     ...     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ q Quit  r Refresh  [ ← Day  ] Day →  Enter Box score                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
