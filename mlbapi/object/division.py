"""Pydantic models for the divisions object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.object import MLBModel
from mlbapi.object.game import Division


class Divisions(MLBModel):
    divisions: Optional[List[Division]] = None
