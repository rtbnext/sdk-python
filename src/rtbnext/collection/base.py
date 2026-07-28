"""
Base Collection

Implements the base collection shared by all resource collections.
"""

from __future__ import annotations

from typing import Any, Callable, Generic, Self, TypeVar

T = TypeVar( "T" )


class CollectionBase( Generic[ T ] ):
    """
    Provides common immutable collection slicing operations.

    This class serves as a base for resource collections, providing methods to
    manipulate and access the underlying items while maintaining immutability.
    """

    def __init__(
        self, items: list[ T ], *,
        factory: Callable[ [ T ], Any ] | None = None,
        total: int | None = None
    ) -> None:
        self._items, self._factory = items, factory
        self._total = len( items ) if total is None else total

    def _clone( self, items: list[ T ] ) -> Self:
        """Create a new collection instance with replaced items."""

        return self.__class__( items, factory= self._factory, total= self._total )

    @property
    def total( self ) -> int:
        """Return the total number of available items."""

        return self._total

    @property
    def count( self ) -> int:
        """Return the number of items currently contained."""

        return len( self._items )

    @property
    def first( self ) -> T | Any | None:
        """Returns the first item."""

        return None if not self._items else (
            self._factory( self._items[ 0 ] ) if self._factory else self._items[ 0 ]
        )

    @property
    def last( self ) -> T | Any | None:
        """Returns the last item."""

        return None if not self._items else (
            self._factory( self._items[ -1 ] ) if self._factory else self._items[ -1 ]
        )

    def to_array( self ) -> list[ T ] | list[ Any ]:
        """Returns all items as list."""

        return [ ( self._factory( i ) if self._factory else i ) for i in self._items ]

    def map( self, callback: Callable[ [ T, int ], Any ] ):
        """Map items."""

        return [
            callback( self._factory( i ) if self._factory else i, idx )
            for idx, i in enumerate( self._items )
        ]

    def take( self, count: int ) -> Self:
        """Return a collection containing the first items."""

        return self._clone( self._items[ : count ] )

    def skip( self, count: int ) -> Self:
        """Return a collection without the first items."""

        return self._clone( self._items[ count : ] )

    def slice( self, start: int | None = None, end: int | None = None ) -> Self:
        """Return a collection containing a sliced range of items."""

        return self._clone( self._items[ start : end ] )
