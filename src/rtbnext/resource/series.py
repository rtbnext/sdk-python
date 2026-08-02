"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date as date_type
from statistics import mean, median
from typing import Callable, Generic, Literal, TypedDict, TypeVar, cast
from rtbnext.core.loader import ResourceStateLoader
from rtbnext.core.parser import ParserFn
from rtbnext.resource.base import Resource
from rtbnext.resource.collection import DateCollectionBase

TimePoint = TypedDict( "TimePoint", { "date": str } )
type TimeSeriesRow = list[ str | int | float ]

D = TypeVar( "D", bound= list[ TimeSeriesRow ] )
R = TypeVar( "R", bound= TimePoint )

type AggregatePeriod = Literal[ "week", "month", "quarter", "year" ]
type NumberCallback[ R ] = Callable[ [ R ], int | float ]
type PointFn[ D, R ] = Callable[ [ D ], R ]
type AggregatedTimeSeries = TimeSeriesCollection[ AggregatePoint ]

AggregateValue = TypedDict( "AggregateValue", {
    "first": float,
    "last": float,
    "min": float,
    "max": float,
    "avg": float,
    "sum": float
} )

AggregateRange = TypedDict( "AggregateRange", {
    "from": str,
    "to": str
} )

AggregatePoint = TypedDict( "AggregatePoint", {
    "date": str,
    "label": str,
    "range": AggregateRange
} )


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

    def _aggregate( self, points: list[ R ], label: str | None = None ) -> AggregatePoint:
        """Aggregate a group of points."""

        sorted_points = sorted( points, key= lambda point: point[ "date" ] )

        result: dict[ str, object ] = {
            "date": sorted_points[ -1 ][ "date" ],
            "label": label or sorted_points[ -1 ][ "date" ],
            "range": {
                "from": sorted_points[ 0 ][ "date" ],
                "to": sorted_points[ -1 ][ "date" ]
            }
        }

        keys = sorted_points[ 0 ].keys()

        for key in keys:
            if key == "date":
                continue

            values = [
                float( point[ key ] ) for point in sorted_points
                if isinstance( point.get( key ), ( int, float ) )
            ]

            if not values:
                continue

            result[ key ] = {
                "first": values[ 0 ],
                "last": values[ -1 ],
                "min": min( values ),
                "max": max( values ),
                "avg": float( mean( values ) ),
                "sum": sum( values )
            }

        return cast( AggregatePoint, result )

    def _aggregated_series( self, points: list[ AggregatePoint ] ) -> AggregatedTimeSeries:
        """Returns a time series collection of aggregated points."""

        return TimeSeriesCollection(
            points,
            factory= lambda item: item,
            date= lambda item: item[ "date" ]
        )

    def min( self, callback: NumberCallback | None = None ) -> float:
        """Returns the minimum value."""

        return min( self._numbers( callback ) )

    def max( self, callback: NumberCallback | None = None ) -> float:
        """Returns the maximum value."""

        return max( self._numbers( callback ) )

    def sum( self, callback: NumberCallback | None = None ) -> float:
        """Returns the sum of values."""

        return sum( self._numbers( callback ) )

    def avg( self, callback: NumberCallback | None = None ) -> float:
        """Returns the average value."""

        return float( mean( self._numbers( callback ) ) )

    def median( self, callback: NumberCallback | None = None ) -> float:
        """Returns the median value."""

        return float( median( self._numbers( callback ) ) )

    @property
    def labels( self ) -> list[ str ]:
        """Returns the date labels."""

        return [ point[ "date" ] for point in self ]

    @property
    def columns( self ) -> dict[ str, list[ object ] ]:
        """Returns the values grouped by column."""

        result: dict[ str, list[ object ] ] = {}

        for point in self:
            for key, value in point.items():
                result.setdefault( key, [] ).append( value )

        return result

    def values( self, callback: NumberCallback ) -> list[ int | float ]:
        """Returns the mapped numeric values."""

        return [ callback( point ) for point in self ]

    def column( self, key: str ) -> list[ object ]:
        """Returns all values of a column."""

        return [ point[ key ] for point in self ]

    def aggregate( self, period: AggregatePeriod | Callable[ [ R ], str ] ) -> AggregatedTimeSeries:
        """Aggregates points by period."""

        groups: dict[ str, list[ R ] ] = defaultdict( list )

        for point in self:
            groups[ (
                period( point ) if callable( period )
                else self._period( point[ "date" ], period )
            ) ].append( point )

        return self._aggregated_series( [
            self._aggregate( group, label )
            for label, group in groups.items()
        ] )

    def buckets( self, count: int ) -> AggregatedTimeSeries:
        """Splits points into equally sized buckets."""

        if count >= self.count:
            return self._aggregated_series( [
                self._aggregate( [ point ], f"{ index + 1 }/{ self.count }" )
                for index, point in enumerate( self )
            ] )

        size, points = self.count / count, self.items
        result: list[ AggregatePoint ] = []

        for index in range( count ):
            start, end = int( index * size ), int( ( index + 1 ) * size )
            result.append( self._aggregate( points[ start : end ], f"{ index + 1 }/{ count }" ) )

        return self._aggregated_series( result )


class TimeSeriesResource( Resource[ D ], Generic[ D, R ] ):
    """
    Resource wrapper for time-series endpoints.

    This class converts raw CSV rows into typed time-series points and
    exposes them through a time-series collection.
    """

    def __init__(
        self, path: str, loader: ResourceStateLoader, parser: ParserFn[ D ], *,
        point: PointFn[ TimeSeriesRow, R ]
    ) -> None:
        super().__init__( path, loader, parser )
        self._point = point

    def _collect_points( self, rows: D ) -> TimeSeriesCollection[ R ]:
        """Create a time-series collection from raw rows."""

        return TimeSeriesCollection(
            [ self._point( row ) for row in reversed( rows ) ],
            factory= lambda item: item,
            date= lambda point: point[ "date" ]
        )

    async def series( self ) -> TimeSeriesCollection[ R ]:
        """Returns the parsed time-series data as a typed collection."""

        return await self._transform( self._collect_points )
