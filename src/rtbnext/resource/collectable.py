"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from typing import Callable, TypedDict, TypeVar, Generic
from rtbnext.resource.collection import IndexCollectionBase, ItemFactory
from rtbnext.utils import sanitize


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""

    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""

    items: list[ T ]

K = TypeVar( "K" )
T = TypeVar( "T", bound= dict )
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

        self._find = find
        self._search = search

    def _clone( self, items: list[ T ] ) -> CollectCollection[ T, R ]:
        """Create a new collection preserving configuration."""

        return CollectCollection(
            items, factory= self._factory, total= self._total,
            find= self._find, search= self._search
        )

    def get( self, uri: str ) -> T | R | None:
        """Return an item by its exact URI."""

        for item in self._items:
            if item[ "uri" ] == uri:
                return self._resolve( item )

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
