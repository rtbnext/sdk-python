"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from statistics import median
from typing import Callable, Generic, Literal, TypedDict, TypeVar

from rtbnext.resource.collection import DateCollectionBase


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str


D = TypeVar( "D", bound= list[ TimePoint ] )
R = TypeVar( "R", bound= TimePoint )

type AggregatePeriod = Literal[ "week", "month", "quarter", "year" ]
type NumberCallback[ R ] = Callable[ [ R ], int | float ] | None


class TimeSeriesCollection( DateCollectionBase[ R, R ], Generic[ R ] ):
    """
    Collection wrapper for time-series resources.

    This class is the base for CSV resource collections, providing methods
    to access dated data points, aggregate them and get statistical values
    like min, max, median etc.
    """

    def _numbers( self, callback: NumberCallback = None ) -> list[ float ]:
        """Return numeric values from points."""

        return (
            [ float( callback( point ) ) for point in self ]
            if callback is not None else
            [
                float( value ) for point in self for key, value in point.items()
                if key != "date" and isinstance( value, ( int, float ) )
            ]
        )

    def min( self, callback: NumberCallback = None ) -> float:
        """Return minimum value."""

        return min( self._numbers( callback ) )

    def max( self, callback: NumberCallback = None ) -> float:
        """Return maximum value."""

        return max( self._numbers( callback ) )

    def sum( self, callback: NumberCallback = None ) -> float:
        """Return sum of values."""

        return sum( self._numbers( callback ) )

    def avg( self, callback: NumberCallback = None ) -> float:
        """Return average value."""

        values = self._numbers( callback )
        return sum( values ) / len( values )

    def median( self, callback: NumberCallback = None ) -> float:
        """Return median value."""

        return float( median( self._numbers( callback ) ) )

    @property
    def labels( self ) -> list[ str ]:
        """Return date labels."""

        return [ point[ "date" ] for point in self ]

    @property
    def columns( self ) -> dict[ str, list[ object ] ]:
        """Return values grouped by column."""

        result: dict[ str, list[ object ] ] = {}

        for point in self:
            for key, value in point.items():
                result.setdefault( key, [] ).append( value )

        return result
