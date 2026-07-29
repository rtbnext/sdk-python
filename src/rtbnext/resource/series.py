"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from typing import Callable, Literal, TypedDict, TypeVar


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str


type AggregatePeriod = Literal[ "week", "month", "quarter", "year" ]

D = TypeVar( "D" )
R = TypeVar( "R", bound= TimePoint )

type PointFn[ D, R ] = Callable[ [ D ], R ]
