"""Base collection implementation used by all resource collections."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

T = TypeVar( "T" )


class CollectionBase( Generic[ T ] ):
    """Base class for immutable SDK collections."""

    def __init__ ( self, items: list[ T ], total: int | None = None ) -> None:
        self._items = items
        self._total = len( items ) if total is None else total

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
