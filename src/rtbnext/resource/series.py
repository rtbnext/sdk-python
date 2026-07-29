"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from typing import TypedDict


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str


class AggregateRange( TypedDict ):
    """The date range covered by this aggregate point."""

    from_: str
    to: str


class AggregateValue( TypedDict ):
    """Aggregated numeric summary values."""

    first: float
    last: float
    min: float
    max: float
    avg: float
    sum: float
