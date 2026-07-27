"""Base collection implementation shared by all resource collections."""


from __future__ import annotations

from typing import Generic, Self, TypeVar

T = TypeVar( "T" )


class CollectionBase ( Generic[ T ] ):
    """
    Provides common immutable collection slicing operations.
    
    This class serves as a base for resource collections, providing methods to
    manipulate and access the underlying items while maintaining immutability.
    """

    def __init__ ( self, items: list[ T ], total: int | None = None ) -> None:
        self._items = items
        self._total = len( items ) if total is None else total

    def _clone ( self, items: list[ T ] ) -> Self:
        """Create a new collection instance with replaced items."""
        return self.__class__( items, self._total )

    @property
    def total ( self ) -> int:
        """Return the total number of available items."""
        return self._total

    @property
    def count ( self ) -> int:
        """Return the number of items currently contained."""
        return len( self._items )

    def take ( self, count: int ) -> Self:
        """Return a collection containing the first items."""
        return self._clone( self._items[ : count ] )

    def skip ( self, count: int ) -> Self:
        """Return a collection without the first items."""
        return self._clone( self._items[ count : ] )

    def slice ( self, start: int | None = None, end: int | None = None ) -> Self:
        """Return a collection containing a sliced range of items."""
        return self._clone( self._items[ start : end ] )
