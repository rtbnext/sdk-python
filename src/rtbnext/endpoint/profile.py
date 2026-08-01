"""
Profile Endpoint

Provides access to profile metadata, details, history, index,
and search index.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource, CollectItem
from rtbnext.schema.profile import ProfileData, ProfileHistory, ProfileMeta
from rtbnext.utils import sanitize


class ProfileEndpoint( EndpointBase ):
    """
    Endpoint implementation for profile resources.

    Provides access to profile metadata, details, history,
    index, and search index.
    """

    def _entity( self, item: CollectItem ):
        ...

    def _collect( self ):
        ...

    def meta( self, uri: str ) -> Resource[ ProfileMeta ]:
        """Returns profile metadata for the given URI."""

        return self._resource( f"v2/profile/{ sanitize( uri ) }/meta.json" )

    def data( self, uri: str ) -> Resource[ ProfileData ]:
        """Returns profile data for the given URI."""

        return self._resource( f"v2/profile/{ sanitize( uri ) }/profile.json" )

    def history( self, uri: str ):
        """Returns profile history time-series data for the given URI."""
        ...

    def get( self, uri: str ):
        """Returns the profile entity for a URI."""

        return self._entity( CollectItem( uri= uri ) )

    @property
    def index( self ):
        """Returns the profile index collection."""
        ...

    @property
    def search_index( self ):
        """Returns the profile search index collection."""
        ...
