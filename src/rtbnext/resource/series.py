"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from typing import Callable, Literal, TypedDict, TypeVar, Generic
from rtbnext.resource.collection import DateCollectionBase


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str


D = TypeVar( "D", bound= list[ TimePoint ] )
R = TypeVar( "R", bound= TimePoint )

type AggregatePeriod = Literal[ "week", "month", "quarter", "year" ]
type Callback[ R ] = Callable[ [ R ], int | float ] | None


class TimeSeriesCollection( DateCollectionBase[ R, R ], Generic[ R ] ):
    """
    Collection wrapper for time-series resources.

    This class is the base for CSV resource collections, providing methods
    to access dated data points, aggregate them and get statistical values
    like min, max, median etc.
    """

    def _numbers( self, callback: Callback = None ) -> list[ float ]:
        """Return numeric values from points."""

        return (
            [ float( callback( point ) ) for point in self ]
            if callback is not None else
            [
                float( value ) for point in self for key, value in point.items()
                if key != "date" and isinstance( value, ( int, float ) )
            ]
        )
