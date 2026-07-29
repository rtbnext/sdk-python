"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from typing import Callable, TypedDict, TypeVar, Generic
from rtbnext.resource.collection import IndexCollectionBase, ItemFactory


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
