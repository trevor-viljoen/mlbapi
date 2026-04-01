"""Pydantic models for the conferences object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Conference(MLBModel):
    pass


class Conferences(MLBModel):
    conferences: Optional[List[Conference]] = None
