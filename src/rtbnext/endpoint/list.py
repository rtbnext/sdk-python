"""
List Endpoint

Provides access to item snapshots, date-indexed list resources,
and the index listing all available lists.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.utils import sanitize, ymd


class ListEndpoint( EndpointBase ):
    """
    Endpoint implementation for list resources.

    Provides access to item snapshots, date-indexed list resources,
    and the index listing all available lists.
    """

    def snapshot( self, uri: str, date: str ):
        """Returns a snapshot collection for a list URI at a specific date."""

        return self._endpoints.profile.collect(
            f"v2/list/{ sanitize( uri ) }/{ ymd( date ) }.json"
        )

    def get( self, uri: str ):
        """Returns a date-indexed list resource for a list URI."""

        return self._dateable( f"v2/list/{ sanitize( uri ) }/index.json",
            date= lambda date: self.snapshot( uri, date )
        )

    @property
    def index( self ):
        """Returns the root list index resource."""

        return self._collectable( "v2/list/index.json", entity= self.get )
