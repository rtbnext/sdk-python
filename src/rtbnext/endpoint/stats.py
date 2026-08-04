"""
Stats Endpoint

Provides access to stats resources, scatter collections, historic
data, and grouped indices.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from rtbnext.endpoint.base import EndpointBase
from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.indexable import IndexableResource
from rtbnext.resource.series import AggregateRange, AggregateValue, TimeSeriesResource
from rtbnext.schema.generic import Industry
from rtbnext.schema.stats import (
    CitizenshipStatsIndex, DBStats, GlobalStats, History, HistoryItem, IndustryStatsIndex,
    ProfileStats, Scatter, ScatterItem, Top10, WealthStats
)
from rtbnext.utils import sanitize

HistoryPoint = TypedDict( "HistoryPoint", {
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quota": float,
    "change": float,
    "percent": float
} )

HistoryAggregatePoint = TypedDict( "HistoryAggregatePoint", {
    "date": str,
    "label": str,
    "range": AggregateRange,
    "count": AggregateValue,
    "total": AggregateValue,
    "woman": AggregateValue,
    "quota": AggregateValue,
    "change": AggregateValue,
    "percent": AggregateValue
} )

type HistorySeries = TimeSeriesResource[ History, HistoryPoint, HistoryAggregatePoint ]
type CitizenshipIndexTree = dict[ str, HistorySeries ]
type IndustryIndexTree = dict[ Industry, HistorySeries ]


class StatsEndpoint( EndpointBase ):
    """
    Endpoint implementation for stats resources.

    Provides access to stats resources, scatter collections,
    historic data, and grouped indices.
    """

    def _point( self, point: HistoryItem ) -> HistoryPoint:
        """Converts a raw history row into a typed history point."""

        date, count, total, woman, quota, change, percent = point

        return {
            "date": date, "count": count, "total": total, "woman": woman,
            "quota": quota, "change": change, "percent": percent
        }

    def _keys( self, value: object ) -> list[ str ] | None:
        """Returns available index keys."""

        if not isinstance( value, dict ):
            return None

        if isinstance( items := value.get( "items" ), dict ):
            value.clear()
            value.update( items )

        return [] if "date" in value else list( value.keys() )

    def _group( self, group: Literal[ "industry", "citizenship" ] ) -> IndexableResource:
        """Builds an industry or citizenship index."""

        return self._indexable( f"v2/stats/{ group }/index.json",
            index= lambda path: getattr( self, group )( path[ -1 ] ),
            keys= self._keys
        )

    @property
    def db( self ) -> Resource[ DBStats ]:
        """Returns the database statistics resource."""

        return self._resource( "v2/stats/db.json" )

    @property
    def global_( self ) -> Resource[ GlobalStats ]:
        """Returns the global statistics resource."""

        return self._resource( "v2/stats/global.json" )

    @property
    def profile( self ) -> Resource[ ProfileStats ]:
        """Returns the profile statistics resource."""

        return self._resource( "v2/stats/profile.json" )

    @property
    def scatter( self ) -> CollectableResource[
        Scatter, ScatterItem, ProfileEntity[ ScatterItem ]
    ]:
        """Returns the profile scatter stats collection resource."""

        return self._endpoints.profile.collect( "v2/stats/scatter.json" )

    @property
    def wealth( self ) -> Resource[ WealthStats ]:
        """Returns the wealth statistics resource."""

        return self._resource( "v2/stats/wealth.json" )

    @property
    def history( self ) -> HistorySeries:
        """Returns the historical stats time series resource."""

        return self._series( "v2/stats/history.csv", point= self._point )

    @property
    def top_10( self ) -> Resource[ Top10 ]:
        """Returns the top 10 billionaires list resource."""

        return self._resource( "v2/stats/top10.json" )

    def industry( self, key: Industry ) -> HistorySeries:
        """Returns time series for a specific industry."""

        return self._series( f"v2/stats/industry/{ sanitize( key ) }.csv", point= self._point )

    def citizenship( self, key: str ) -> HistorySeries:
        """Returns time series for a specific citizenship, indexed by ISO code."""

        return self._series( f"v2/stats/citizenship/{ key.upper() }.csv", point= self._point )

    @property
    def industry_index( self ) -> IndexableResource[ IndustryStatsIndex, IndustryIndexTree ]:
        """Returns the industry stats index."""

        return self._group( "industry" )

    @property
    def citizenship_index( self ) -> IndexableResource[
        CitizenshipStatsIndex, CitizenshipIndexTree
    ]:
        """Returns the citizenship stats index."""

        return self._group( "citizenship" )
