"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypedDict, TypeVar

from rtbnext.resource.base import Resource
from rtbnext.utils import sanitize
from rtbnext.resource.collection import IndexCollectionBase, ItemFactory


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""

    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""

    items: list[ T ]


D = TypeVar( "D", bound= CollectData )
I = TypeVar( "I", bound= CollectItem )
E = TypeVar( "E" )

type EntityFn[ I, E ] = Callable[ [ I ], E ]
type FindFn[ I ] = Callable[ [ list[ I ], str ], I | None ]
type SearchFn[ I ] = Callable[ [ I, str, list[ str ] ], bool ]


class CollectCollection( IndexCollectionBase[ I, E ], Generic[ I, E ] ):
    """
    Collection wrapper for entity-based resources.

    This class extends the indexed collection with searching, filtering,
    grouping, sorting and set operations.
    """

    def __init__(
        self, items: list[ I ], *,
        factory: ItemFactory[ I, E ],
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


class CollectableResource( Resource[ D ], Generic[ D, I, E ] ):
    ...
