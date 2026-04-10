"""Pydantic models for the transactions API endpoint."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlbapi.models import MLBModel


class Transaction(MLBModel):
    """A single transaction record."""
    id: Optional[int] = None
    person: Optional[Dict[str, Any]] = None
    to_team: Optional[Dict[str, Any]] = None
    from_team: Optional[Dict[str, Any]] = None
    type_code: Optional[str] = None
    type_desc: Optional[str] = None
    effective_date: Optional[str] = None
    resolution_date: Optional[str] = None
    description: Optional[str] = None


class Transactions(MLBModel):
    """Container returned by ``GET /api/v1/transactions``."""
    transactions: Optional[List[Transaction]] = None
