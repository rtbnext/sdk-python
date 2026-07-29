"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from collections import defaultdict
from typing import Callable, Generic, TypedDict, TypeVar

from rtbnext.resource.collection import IndexCollectionBase, ItemFactory
from rtbnext.utils import sanitize


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""

    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""

    items: list[ T ]

K = TypeVar( "K" )
T = TypeVar( "T", bound= CollectItem )
R = TypeVar( "R" )

type FindFn[ T ] = Callable[ [ list[ T ], str ], T | None ]
type SearchFn[ T ] = Callable[ [ T, str, list[ str ] ], bool ]


class CollectCollection( IndexCollectionBase[ T, R ], Generic[ T, R ] ):
    """
    Collection wrapper for entity-based resources.

    This class extends the indexed collection with searching, filtering,
    grouping, sorting and set operations.
    """

    def __init__(
        self, items: list[ T ], *,
        factory: ItemFactory[ T, R ] = None,
        total: int | None = None,
        find: FindFn[ T ] | None = None,
        search: SearchFn[ T ] | None = None
    ) -> None:
        super().__init__( items, factory= factory, total= total )

        self._find = find or self._default_find
        self._search = search or self._default_search

    @staticmethod
    def _default_find( items: list[ T ], uri_like: str ) -> T | None:
        """Return the first item matching a URI-like string."""

        uri = sanitize( uri_like )
        return next( ( item for item in items if item[ "uri" ] == uri ), None )

    @staticmethod
    def _default_search( item: T, query: str, terms: list[ str ] ) -> bool:
        """Return whether an item matches a search query."""

        name = item.get( "searchName" ) or sanitize( item.get( "name", "" ) )
        text = item.get( "text", "" )

        return (
            query in name or query in text
            or all( term in name or term in text for term in terms )
        )

    def _clone( self, items: list[ T ] ) -> CollectCollection[ T, R ]:
        """Create a new collection preserving configuration."""

        return CollectCollection(
            items, factory= self._factory, total= self._total,
            find= self._find, search= self._search
        )

    def get( self, uri: str ) -> T | R | None:
        """Return an item by its exact URI."""

        return next( (
            self._resolve( item ) for item in self._items if item[ "uri" ] == uri
        ), None )

    def filter( self, predicate: Callable[ [ T | R ], bool ] ) -> CollectCollection[ T, R ]:
        """Return items matching a predicate."""

        return self._clone( [ item for item in self._items if predicate( self._resolve( item ) ) ] )

    def find( self, uri_like: str ) -> T | R | None:
        """Return the first matching URI-like item."""

        item = self._find( self._items, uri_like )
        return None if item is None else self._resolve( item )

    def search( self, query: str ) -> CollectCollection[ T, R ]:
        """Return items matching a search query."""

        query, terms = sanitize( query ), query.split()
        return self._clone( [ item for item in self._items if self._search( item, query, terms ) ] )

    def intersect( self, other: CollectCollection[ T, R ] ) -> CollectCollection[ T, R ]:
        """Return items also contained in another collection."""

        uris = { item[ "uri" ] for item in other.items }
        return self._clone( [ item for item in self._items if item[ "uri" ] in uris ] )

    def exclude( self, other: CollectCollection[ T, R ] ) -> CollectCollection[ T, R ]:
        """Return items not contained in another collection."""

        uris = { item[ "uri" ] for item in other.items }
        return self._clone( [ item for item in self._items if item[ "uri" ] not in uris ] )

    def union( self, other: CollectCollection[ T, R ] ) -> CollectCollection[ T, R ]:
        """Return the union of two collections."""

        seen: set[ str ] = set()
        merged: list[ T ] = []

        for item in [ *self._items, *other.items ]:
            if item[ "uri" ] not in seen:
                seen.add( item[ "uri" ] )
                merged.append( item )

        return self._clone( merged )

    def group_by(
        self,
        callback: Callable[ [ T | R ], K ]
    ) -> dict[ K, CollectCollection[ T, R ] ]:
        """Group items using a callback."""

        groups: defaultdict[ K, list[ T ] ] = defaultdict( list )

        for item in self._items:
            groups[ callback( self._resolve( item ) ) ].append( item )

        return {
            key: self._clone( values )
            for key, values in groups.items()
        }

    def order_by( self, key: str, descending: bool = False ) -> CollectCollection[ T, R ]:
        """Return items ordered by a dictionary key."""

        return self._clone( sorted(
            self._items,
            key= lambda item: ( item.get( key ) is None, item.get( key ) ),
            reverse= descending
        ) )

    def sort(
        self, key: Callable[ [ T | R ], K ], *,
        reverse: bool = False
    ) -> CollectCollection[ T, R ]:
        """Return items sorted using a custom key."""

        return self._clone( sorted(
            self._items,
            key= lambda item: key( self._resolve( item ) ),
            reverse= reverse
        ) )
