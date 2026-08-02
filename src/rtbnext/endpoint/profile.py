"""
Profile Endpoint

Provides access to profile metadata, details, history, index,
and search index.
"""

from __future__ import annotations

from functools import cached_property
from typing import Generic, TypedDict

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource, CollectItem, FindFn, I, SearchFn
from rtbnext.resource.series import TimeSeriesResource
from rtbnext.schema.profile import (
    ProfileData, ProfileHistory, ProfileHistoryItem, ProfileIndex, ProfileIndexItem, ProfileMeta,
    SearchIndex, SearchIndexItem
)
from rtbnext.utils import sanitize

ProfileHistoryPoint = TypedDict( "ProfileHistoryPoint", {
    "date": str,
    "rank": int,
    "networth": float,
    "change": float,
    "percent": float
} )


class ProfileEntity( Generic[ I ] ):
    """
    Lazy profile entity exposing related profile resources.

    Wraps a raw profile item and provides lazy access to its
    associated metadata, profile data, and history resources.
    """

    def __init__( self, endpoint: ProfileEndpoint, item: I ) -> None:
        self._endpoint, self._item = endpoint, item

    def __getattr__( self, name: str ) -> object:
        """Forwards unknown attributes to the underlying profile item."""

        try:
            return self._item[ name ]
        except KeyError:
            raise AttributeError( name ) from None

    @property
    def uri( self ) -> str:
        """Returns the profile URI."""

        return self._item[ "uri" ]

    @cached_property
    def meta( self ) -> Resource[ ProfileMeta ]:
        """Returns the lazily loaded profile metadata resource."""

        return self._endpoint.meta( self.uri )

    @cached_property
    def data( self ) -> Resource[ ProfileData ]:
        """Returns the lazily loaded profile data resource."""

        return self._endpoint.data( self.uri )

    @cached_property
    def history( self ) -> TimeSeriesResource[ ProfileHistory, ProfileHistoryPoint ]:
        """Returns the lazily loaded profile history resource."""

        return self._endpoint.history( self.uri )


class ProfileEndpoint( EndpointBase ):
    """
    Endpoint implementation for profile resources.

    Provides access to profile metadata, details, history,
    index, and search index.
    """

    def _point( self, point: ProfileHistoryItem ) -> ProfileHistoryPoint:
        """Converts a raw profile history row into a typed history point."""

        date, rank, ntw, change, pct = point
        return { "date": date, "rank": rank, "networth": ntw, "change": change, "percent": pct }

    def _entity( self, item: I ) -> ProfileEntity[ I ]:
        """Creates a profile entity with lazy-loaded related resources."""

        return ProfileEntity( self, item )

    def collect(
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

    def history( self, uri: str ) -> TimeSeriesResource[ ProfileHistory, ProfileHistoryPoint ]:
        """Returns profile history time-series data for the given URI."""

        return self._series( f"v2/profile/{ sanitize( uri ) }/history.csv", point= self._point )

    def get( self, uri: str ) -> ProfileEntity[ CollectItem ]:
        """Returns the profile entity for a URI."""

        return self._entity( CollectItem( uri= sanitize( uri ) ) )

    @property
    def index( self ) -> CollectableResource[
        ProfileIndex, ProfileIndexItem, ProfileEntity[ ProfileIndexItem ]
    ]:
        """Returns the profile index collection."""

        return self.collect( "v2/profile/index.json" )

    @property
    def search_index( self ) -> CollectableResource[
        SearchIndex, SearchIndexItem, ProfileEntity[ SearchIndexItem ]
    ]:
        """Returns the profile search index collection."""

        return self.collect( "v2/profile/search.json" )
