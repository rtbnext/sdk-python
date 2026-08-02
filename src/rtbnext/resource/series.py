"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from __future__ import annotations

from typing import TypedDict, TypeVar


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""

    date: str


type TimeSeriesRow = list[ str | int | float ]

D = TypeVar( "D", bound= list[ TimeSeriesRow ] )
R = TypeVar( "R", bound= TimePoint )
