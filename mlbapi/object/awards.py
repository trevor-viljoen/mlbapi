"""Pydantic models for the awards object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.object import MLBModel


class Award(MLBModel):
    pass


class Awards(MLBModel):
    awards: Optional[List[Award]] = None
