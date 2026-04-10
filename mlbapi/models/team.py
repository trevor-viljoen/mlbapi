"""Pydantic models for the teams object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel
from mlbapi.models.game import Team


class Teams(MLBModel):
    teams: Optional[List[Team]] = None
