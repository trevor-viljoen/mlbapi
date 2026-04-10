"""Pydantic models for the divisions object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel
from mlbapi.models.game import Division


class Divisions(MLBModel):
    divisions: Optional[List[Division]] = None
