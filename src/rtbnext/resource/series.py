"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypedDict, TypeVar
from statistics import mean, median
from rtbnext.resource.collection import DateCollectionBase


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""

    date: str


type TimeSeriesRow = list[ str | int | float ]

D = TypeVar( "D", bound= list[ TimeSeriesRow ] )
R = TypeVar( "R", bound= TimePoint )

type NumberCallback[ R ] = Callable[ [ R ], int | float ]


class TimeSeriesCollection( DateCollectionBase[ R, R ], Generic[ R ] ):
    """
    Collection wrapper for time-series resources.

    This class is the base for CSV resource collections, providing methods
    to access dated data points, aggregate them and get statistical values
    like min, max, median etc.
    """

    def _numbers( self, callback: NumberCallback | None = None ) -> list[ float ]:
        """Return numeric values from points."""

        return (
            [ float( callback( point ) ) for point in self ]
            if callback is not None else
            [
                float( value ) for point in self for key, value in point.items()
                if key != "date" and isinstance( value, ( int, float ) )
            ]
        )

    def min( self, callback: NumberCallback | None = None ) -> float:
        """Return minimum value."""

        return min( self._numbers( callback ) )

    def max( self, callback: NumberCallback | None = None ) -> float:
        """Return maximum value."""

        return max( self._numbers( callback ) )

    def sum( self, callback: NumberCallback | None = None ) -> float:
        """Return sum of values."""

        return sum( self._numbers( callback ) )

    def avg( self, callback: NumberCallback | None = None ) -> float:
        """Return average value."""

        return float( mean( self._numbers( callback ) ) )

    def median( self, callback: NumberCallback | None = None ) -> float:
        """Return median value."""

        return float( median( self._numbers( callback ) ) )
