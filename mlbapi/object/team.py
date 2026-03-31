"""Pydantic models for the teams object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.object import MLBModel
from mlbapi.object.game import Team


class Teams(MLBModel):
    teams: Optional[List[Team]] = None
