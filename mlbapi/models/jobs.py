"""Pydantic models for the jobs API endpoint.

The jobs API returns ``{"roster": [...]}`` (not ``{"jobs": [...]}``)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class Job(MLBModel):
    """A single job entry (umpire, datacaster, official scorer, etc.)."""
    id: Optional[int] = None
    title: Optional[str] = None
    person: Optional[Dict[str, Any]] = None


class Jobs(MLBModel):
    """Container returned by the jobs endpoint.

    The API uses ``roster`` as the key, not ``jobs``.
    """
    roster: Optional[List[Job]] = None
    job_list: Optional[List[Job]] = None
