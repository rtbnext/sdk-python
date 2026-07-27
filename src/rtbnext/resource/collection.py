"""Base collection implementation used by all resource collections."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, Self, TypeVar

T = TypeVar( "T" )


class CollectionBase ( Generic[ T ] ):
    """Base class for immutable SDK collections."""

    def __init__ ( self, items: list[ T ], total: int | None = None ) -> None:
        self._items = items
        self._total = len( items ) if total is None else total

    def _clone ( self, items: list[ T ] ) -> Self:
        """Return a new collection instance with the given items."""
        return self.__class__ ( items, self._total )

    @property
    def items ( self ) -> list[ T ]:
        """Return the collection items."""
        return self._items

    @property
    def total ( self ) -> int:
        """Return the total number of available items."""
        return self._total

    @property
    def count ( self ) -> int:
        """Return the number of items in this collection."""
        return len( self._items )

    @property
    def first ( self ) -> T | None:
        """Return the first item."""
        return self._items[ 0 ] if self._items else None

    @property
    def last ( self ) -> T | None:
        """Return the last item."""
        return self._items[ -1 ] if self._items else None

    def at ( self, index: int ) -> T | None:
        """Return the item at the given index."""

        try:
            return self._items[ index ]
        except IndexError:
            return None

    def to_list ( self ) -> list[ T ]:
        """Return a shallow copy of the collection."""
        return list( self._items )

    def map ( self, callback: Callable[ [ T, int ], object ] ) -> list[ object ]:
        """Map all items to a new list."""
        return [ callback( item, index ) for index, item in enumerate( self._items ) ]

    def for_each ( self, callback: Callable[ [ T, int ], None ] ) -> None:
        """Call a function for every item."""

        for index, item in enumerate( self._items ):
            callback( item, index )

    def __iter__ ( self ) -> Iterator[ T ]:
        """Iterate over all items."""
        return iter( self._items )

    def __len__ ( self ) -> int:
        """Return the number of items."""
        return len( self._items )

    def __getitem__ ( self, index: int ) -> T:
        """Return an item by index."""
        return self._items[ index ]

    def take ( self, count: int ) -> Self:
        """Return a new collection with the first `count` items."""
        return self._clone( self._items[ : count ] )

    def skip ( self, count: int ) -> Self:
        """Return a new collection without the first `count` items."""
        return self._clone( self._items[ count : ] )

    def slice ( self, start: int | None = None, end: int | None = None ) -> Self:
        """Return a new collection with the items from `start` to `end`."""
        return self._clone( self._items[ start : end ] )
