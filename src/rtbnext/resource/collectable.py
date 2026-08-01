"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypedDict, TypeVar

from rtbnext.resource.base import Resource
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


class CollectableResource( Resource[ D ], Generic[ D, I, E ] ):
    ...
