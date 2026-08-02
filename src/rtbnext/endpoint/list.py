"""
List Endpoint

Provides access to item snapshots, date-indexed list resources,
and the index listing all available lists.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase


class ListEndpoint( EndpointBase ):
    """
    Endpoint implementation for list resources.

    Provides access to item snapshots, date-indexed list resources,
    and the index listing all available lists.
    """

    def snapshot( self, uri: str, date: str ):
        """Returns a snapshot collection for a list URI at a specific date."""
        ...

    def get( self, uri: str ):
        """Returns a date-indexed list resource for a list URI."""
        ...

    @property
    def index( self ):
        """Returns the root list index resource."""
        ...
