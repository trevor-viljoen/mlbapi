"""Pydantic models for the jobs object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.object import MLBModel


class Job(MLBModel):
    pass


class Jobs(MLBModel):
    roster: Optional[List[Job]] = None
    job_list: Optional[List[Job]] = None
