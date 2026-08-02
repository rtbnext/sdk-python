"""
List Endpoint

Provides access to item snapshots, date-indexed list resources,
and the index listing all available lists.
"""

from __future__ import annotations

from functools import cached_property

from rtbnext.endpoint.base import EndpointBase
from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.dateable import DateableResource
from rtbnext.schema.generic import DateIndex
from rtbnext.schema.list import List, ListIndex, ListIndexItem, ListItem
from rtbnext.utils import sanitize, ymd

type ListSnapshot = CollectableResource[ List, ListItem, ProfileEntity[ ListItem ] ]
type ListDateIndex = DateableResource[ DateIndex, ListSnapshot ]
type ListEntity = _ListEntity


class _ListEntity:
    """Lazy entity for list index items."""

    def __init__( self, list: ListEndpoint, item: ListIndexItem ) -> None:
        self._list, self._item = list, item

    def __getattr__( self, name: str ) -> object:
        """Forward unknown attributes to the underlying profile item."""

        try:
            return self._item[ name ]
        except KeyError:
            raise AttributeError( name ) from None

    @property
    def uri( self ) -> str:
        """Returns the list URI."""

        return self._item[ "uri" ]

    @cached_property
    def dates( self ) -> ListDateIndex:
        """Returns the lazily loaded list date index resource."""

        return self._list.get( self.uri )


class ListEndpoint( EndpointBase ):
    """
    Endpoint implementation for list resources.

    Provides access to item snapshots, date-indexed list resources,
    and the index listing all available lists.
    """

    def snapshot( self, uri: str, date: str ) -> ListSnapshot:
        """Returns a snapshot collection for a list URI at a specific date."""

        return self._endpoints.profile.collect(
            f"v2/list/{ sanitize( uri ) }/{ ymd( date ) }.json"
        )

    def get( self, uri: str ) -> ListDateIndex:
        """Returns a date-indexed list resource for a list URI."""

        return self._dateable( f"v2/list/{ sanitize( uri ) }/index.json",
            date= lambda date: self.snapshot( uri, date )
        )

    @property
    def index( self ) -> CollectableResource[ ListIndex, ListIndexItem, ListEntity ]:
        """Returns the root list index resource."""

        return self._collectable( "v2/list/index.json",
            entity= lambda item: _ListEntity( self, item )
        )
