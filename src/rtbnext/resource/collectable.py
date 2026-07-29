"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from collections import defaultdict
from typing import Callable, Generic, Self, TypedDict, TypeVar

from rtbnext.core.parser import ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.base import Resource
from rtbnext.resource.collection import IndexCollectionBase, ItemFactory
from rtbnext.utils import sanitize


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""
    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""
    items: list[ T ]

D = TypeVar( "D", bound= CollectData )
I = TypeVar( "I", bound= CollectItem )
E = TypeVar( "E" )
K = TypeVar( "K" )

type EntityFn[ I, E ] = Callable[ [ I ], E ]
type FindFn[ T ] = Callable[ [ list[ T ], str ], T | None ]
type SearchFn[ T ] = Callable[ [ T, str, list[ str ] ], bool ]


class CollectCollection( IndexCollectionBase[ I, E ], Generic[ I, E ] ):
    """
    Collection wrapper for entity-based resources.

    This class extends the indexed collection with searching, filtering,
    grouping, sorting and set operations.
    """

    def __init__(
        self, items: list[ I ], *,
        factory: ItemFactory[ I, E ] = None,
        total: int | None = None,
        find: FindFn[ I ] | None = None,
        search: SearchFn[ I ] | None = None
    ) -> None:
        super().__init__( items, factory= factory, total= total )

        self._find = find or self._default_find
        self._search = search or self._default_search

    @staticmethod
    def _default_find( items: list[ I ], uri_like: str ) -> I | None:
        """Return the first item matching a URI-like string."""

        uri = sanitize( uri_like )
        return next( ( item for item in items if item[ "uri" ] == uri ), None )

    @staticmethod
    def _default_search( item: I, query: str, terms: list[ str ] ) -> bool:
        """Return whether an item matches a search query."""

        name = item.get( "searchName" ) or sanitize( item.get( "name", "" ) )
        text = item.get( "text", "" )

        return (
            query in name or query in text
            or all( term in name or term in text for term in terms )
        )

    def _clone( self, items: list[ I ] ) -> Self:
        """Create a new collection preserving configuration."""

        return self.__class__(
            items, factory= self._factory, total= self._total,
            find= self._find, search= self._search
        )

    def get( self, uri: str ) -> I | E | None:
        """Return an item by its exact URI."""

        return next( (
            self._resolve( item ) for item in self._items if item[ "uri" ] == uri
        ), None )

    def filter( self, predicate: Callable[ [ I | E ], bool ] ) -> Self:
        """Return items matching a predicate."""

        return self._clone( [ item for item in self._items if predicate( self._resolve( item ) ) ] )

    def find( self, uri_like: str ) -> I | E | None:
        """Return the first matching URI-like item."""

        item = self._find( self._items, uri_like )
        return None if item is None else self._resolve( item )

    def search( self, query: str ) -> Self:
        """Return items matching a search query."""

        query, terms = sanitize( query ), query.split()
        return self._clone( [ item for item in self._items if self._search( item, query, terms ) ] )

    def intersect( self, other: Self ) -> Self:
        """Return items also contained in another collection."""

        uris = { item[ "uri" ] for item in other.items }
        return self._clone( [ item for item in self._items if item[ "uri" ] in uris ] )

    def exclude( self, other: Self ) -> Self:
        """Return items not contained in another collection."""

        uris = { item[ "uri" ] for item in other.items }
        return self._clone( [ item for item in self._items if item[ "uri" ] not in uris ] )

    def union( self, other: Self ) -> Self:
        """Return the union of two collections."""

        seen: set[ str ] = set()
        merged: list[ I ] = []

        for item in [ *self._items, *other.items ]:
            if item[ "uri" ] not in seen:
                seen.add( item[ "uri" ] )
                merged.append( item )

        return self._clone( merged )

    def group_by( self, callback: Callable[ [ I | E ], K ] ) -> dict[ K, Self ]:
        """Group items using a callback."""

        groups: defaultdict[ K, list[ I ] ] = defaultdict( list )

        for item in self._items:
            groups[ callback( self._resolve( item ) ) ].append( item )

        return {
            key: self._clone( values )
            for key, values in groups.items()
        }

    def order_by( self, key: str, descending: bool = False ) -> Self:
        """Return items ordered by a dictionary key."""

        return self._clone( sorted(
            self._items,
            key= lambda item: ( item.get( key ) is None, item.get( key ) ),
            reverse= descending
        ) )

    def sort(
        self, *,
        key: Callable[ [ I | E ], str | int | float | bool ],
        reverse: bool = False
    ) -> Self:
        """Return items sorted using a custom key."""

        return self._clone( sorted(
            self._items,
            key= lambda item: key( self._resolve( item ) ),
            reverse= reverse
        ) )


class CollectableResource( Resource[ D ], Generic[ D, I, E ] ):
    """
    Resource wrapper for collection-oriented endpoints.

    This class converts raw API items into entity objects and exposes them
    through a lazily created collection supporting filtering, searching,
    sorting and paging operations.
    """

    def __init__(
        self, path: str, loader: ResourceLoader, parser: ParserFn[ D ], *,
        entity: EntityFn[ I, E ],
        find: FindFn[ I ] | None = None,
        search: SearchFn[ I ] | None = None
    ) -> None:
        super().__init__( path, loader, parser )

        self._entity = entity
        self._find = find
        self._search = search

    def _collect( self, items: list[ I ] ) -> CollectCollection[ I, E ]:
        """Create a collection from resolved entities."""

        return CollectCollection( items, find= self._find, search= self._search )
