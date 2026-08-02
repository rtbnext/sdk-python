"""
Profile Endpoint

Provides access to profile metadata, details, history, index,
and search index.
"""

from __future__ import annotations

from functools import cached_property
from typing import Generic

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource, CollectItem, FindFn, I, SearchFn
from rtbnext.schema.profile import (
    ProfileData, ProfileIndex, ProfileIndexItem, ProfileMeta, SearchIndex, SearchIndexItem
)
from rtbnext.utils import sanitize


class ProfileEntity( Generic[ I ] ):
    """
    Lazy profile entity exposing related profile resources.

    Wraps a raw profile item and provides lazy access to its
    associated metadata, profile data, and history resources.
    """

    def __init__( self, endpoint: ProfileEndpoint, item: I ) -> None:
        self._endpoint, self._item = endpoint, item

    def __getattr__( self, name: str ) -> object:
        """Forward unknown attributes to the underlying profile item."""

        try:
            return self._item[ name ]
        except KeyError:
            raise AttributeError( name ) from None

    @property
    def uri( self ) -> str:
        """Return the profile URI."""

        return self._item[ "uri" ]

    @cached_property
    def meta( self ) -> Resource[ ProfileMeta ]:
        """Return the lazily loaded profile metadata resource."""

        return self._endpoint.meta( self.uri )

    @cached_property
    def data( self ) -> Resource[ ProfileData ]:
        """Return the lazily loaded profile data resource."""

        return self._endpoint.data( self.uri )

    @cached_property
    def history( self ):
        """Return the lazily loaded profile history resource."""
        ...


class ProfileEndpoint( EndpointBase ):
    """
    Endpoint implementation for profile resources.

    Provides access to profile metadata, details, history,
    index, and search index.
    """

    def _entity( self, item: I ) -> ProfileEntity[ I ]:
        """Creates a profile entity with lazy-loaded related resources."""

        return ProfileEntity( self, item )

    def _collect(
        self, path: str, *,
        find: FindFn[ I ] | None = None,
        search: SearchFn[ I ] | None = None
    ) -> CollectableResource:
        """Returns a profile collection resource from a JSON endpoint."""

        return self._collectable( path, entity= self._entity, find= find, search= search )

    def meta( self, uri: str ) -> Resource[ ProfileMeta ]:
        """Returns profile metadata for the given URI."""

        return self._resource( f"v2/profile/{ sanitize( uri ) }/meta.json" )

    def data( self, uri: str ) -> Resource[ ProfileData ]:
        """Returns profile data for the given URI."""

        return self._resource( f"v2/profile/{ sanitize( uri ) }/profile.json" )

    def history( self ):
        """Returns profile history time-series data for the given URI."""
        ...

    def get( self, uri: str ) -> ProfileEntity[ CollectItem ]:
        """Returns the profile entity for a URI."""

        return self._entity( CollectItem( uri= sanitize( uri ) ) )

    @property
    def index( self ) -> CollectableResource[
        ProfileIndex, ProfileIndexItem, ProfileEntity[ ProfileIndexItem ]
    ]:
        """Returns the profile index collection."""

        return self._collect( "v2/profile/index.json" )

    @property
    def search_index( self ) -> CollectableResource[
        SearchIndex, SearchIndexItem, ProfileEntity[ SearchIndexItem ]
    ]:
        """Returns the profile search index collection."""

        return self._collect( "v2/profile/search.json" )
