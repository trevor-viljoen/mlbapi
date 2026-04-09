"""Pydantic models for the draft API endpoint.

The MLB API returns::

    {"drafts": {"rounds": [{"round": "1", "picks": [...]}]}}

so the nesting is: Draft → DraftsPayload → DraftRound → DraftPick.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class DraftPick(MLBModel):
    """A single draft selection."""
    pick_round: Optional[str] = None
    pick_number: Optional[int] = None
    round_pick_number: Optional[int] = None
    rank: Optional[int] = None
    bis_player_id: Optional[int] = None
    pick_value: Optional[str] = None
    signing_bonus: Optional[str] = None
    home: Optional[Dict[str, Any]] = None
    school: Optional[Dict[str, Any]] = None
    blurb: Optional[str] = None
    head_shot_link: Optional[str] = None
    person: Optional[Dict[str, Any]] = None
    team: Optional[Dict[str, Any]] = None


class DraftRound(MLBModel):
    """A round within a draft year."""
    round: Optional[str] = None
    round_text: Optional[str] = None
    picks: Optional[List[DraftPick]] = None


class DraftsPayload(MLBModel):
    """The ``drafts`` sub-object returned by the API."""
    draft_year: Optional[int] = None
    rounds: Optional[List[DraftRound]] = None


class Draft(MLBModel):
    """Top-level container returned by ``GET /api/v1/draft/{year}``."""
    drafts: Optional[DraftsPayload] = None
