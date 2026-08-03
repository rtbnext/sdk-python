"""
Stats Endpoint

Provides access to stats resources, scatter collections, historic
data, and grouped indices.
"""

from __future__ import annotations

from typing import TypedDict

from rtbnext.endpoint.base import EndpointBase
from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource
from rtbnext.schema.stats import (
    DBStats, GlobalStats, ProfileStats, Scatter, ScatterItem, Top10, WealthStats, HistoryItem, History
)

HistoryPoint = TypedDict( "HistoryPoint", {
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quote": float,
    "change": float,
    "percent": float
} )


class StatsEndpoint( EndpointBase ):
    """
    Endpoint implementation for stats resources.

    Provides access to stats resources, scatter collections,
    historic data, and grouped indices.
    """

    def _point( self, point: HistoryItem ) -> HistoryPoint:
        """Converts a raw history row into a typed history point."""
        
        date, count, total, woman, quote, change, percent = point

        return {
            "date": date, "count": count, "total": total, "woman": woman,
            "quote": quote, "change": change, "percent": percent
        }

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
    def top10( self ) -> Resource[ Top10 ]:
        """Returns the top 10 billionaires list resource."""

        return self._resource( "v2/stats/top10.json" )
