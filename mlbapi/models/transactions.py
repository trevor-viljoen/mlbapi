"""Pydantic models for the transactions object layer."""

from __future__ import annotations

from typing import List, Optional

from mlbapi.models import MLBModel


class Transaction(MLBModel):
    pass


class Transactions(MLBModel):
    transactions: Optional[List[Transaction]] = None
