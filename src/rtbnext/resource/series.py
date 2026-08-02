"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from __future__ import annotations

from typing import Generic, TypedDict, TypeVar

from rtbnext.resource.collection import DateCollectionBase


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""

    date: str


type TimeSeriesRow = list[ str | int | float ]

D = TypeVar( "D", bound= list[ TimeSeriesRow ] )
R = TypeVar( "R", bound= TimePoint )


class TimeSeriesCollection( DateCollectionBase[ R, R ], Generic[ R ] ):
    """
    Collection wrapper for time-series resources.

    This class is the base for CSV resource collections, providing methods
    to access dated data points, aggregate them and get statistical values
    like min, max, median etc.
    """
