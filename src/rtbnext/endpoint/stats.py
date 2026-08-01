"""
Stats Endpoint

Provides access to stats resources, scatter collections, historic
data, and grouped indices.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.schema.stats import DBStats, GlobalStats, ProfileStats, WealthStats


class StatsEndpoint( EndpointBase ):
    """
    Endpoint implementation for stats resources.

    Provides access to stats resources, scatter collections,
    historic data, and grouped indices.
    """

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
    def wealth( self ) -> Resource[ WealthStats ]:
        """Returns the wealth statistics resource."""

        return self._resource( "v2/stats/wealth.json" )
