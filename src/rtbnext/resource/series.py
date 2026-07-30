"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from collections import defaultdict
from datetime import date as date_type
from statistics import mean, median
from typing import Callable, Generic, Literal, TypedDict, TypeVar, cast

from rtbnext.resource.collection import DateCollectionBase


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str


D = TypeVar( "D", bound= list[ TimePoint ] )
R = TypeVar( "R", bound= TimePoint )

type AggregatePeriod = Literal[ "week", "month", "quarter", "year" ]
type NumberCallback[ R ] = Callable[ [ R ], int | float ]


class AggregateValue( TypedDict ):
    """Numeric aggregate values."""
    first: float
    last: float
    min: float
    max: float
    avg: float
    sum: float


class AggregateRange( TypedDict ):
    """Date range of an aggregate."""
    from_: str
    to: str


class AggregatePoint( TypedDict, Generic[ R ] ):
    """Aggregated time-series point."""

    date: str
    label: str
    range: AggregateRange


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

    def _period( self, date: str, period: AggregatePeriod ) -> str:
        """Create an aggregation key from a date."""

        year, month, day = map( int, date.split( "-" ) )

        if period == "year":
            return str( year )

        if period == "quarter":
            return f"{ year }-Q{ ( month - 1 ) // 3 + 1 }"

        if period == "month":
            return f"{ year }-{ month:02d }"

        if period == "week":
            current, first = date_type( year, month, day ), date_type( year, 1, 1 )
            return f"{ year }-W{ ( ( current - first ).days // 7 + 1 ):02d }"

        raise ValueError( f"Invalid aggregate period: { period }" )

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

    def values( self, callback: NumberCallback ) -> list[ int | float ]:
        """Return mapped numeric values."""

        return [ callback( point ) for point in self ]

    def column( self, key: str ) -> list[ object ]:
        """Return all values of a column."""

        return [ point[ key ] for point in self ]
