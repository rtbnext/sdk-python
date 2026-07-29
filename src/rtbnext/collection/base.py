"""
Base Collection

Implements the base collections shared by resource collections.
"""

from __future__ import annotations

from typing import Callable, Generic, Iterator, Self, TypeVar
from rtbnext.utils import ymd

R = TypeVar( "R" )
T = TypeVar( "T" )


class CollectionBase( Generic[ T, R ] ):
    """
    Provides common immutable collection operations.

    This class serves as a base for resource collections, providing methods to
    manipulate and access the underlying items while maintaining immutability.
    """

    def __init__(
        self, items: list[ T ], *,
        factory: Callable[ [ T ], R ] | None = None,
        total: int | None = None
    ) -> None:
        self._items, self._factory = items, factory
        self._total = len( items ) if total is None else total

    def __getitem__( self, index: int ) -> T | R:
        item = self._items[ index ]
        return self._factory( item ) if self._factory else item

    def __len__( self ) -> int:
        return self.count

    def __iter__( self ) -> Iterator[ T ] | map[ R ]:
        return iter( self._items ) if self._factory is None else map( self._factory, self._items )

    def __contains__( self, item: object ) -> bool:
        return item in self._items

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
    def first( self ) -> T | R | None:
        """Returns the first item."""

        return None if not self._items else (
            self._factory( self._items[ 0 ] ) if self._factory else self._items[ 0 ]
        )

    @property
    def last( self ) -> T | R | None:
        """Returns the last item."""

        return None if not self._items else (
            self._factory( self._items[ -1 ] ) if self._factory else self._items[ -1 ]
        )

    def to_array( self ) -> list[ T ] | list[ R ]:
        """Returns all items as list."""

        if self._factory is None:
            return list( self._items )
        else:
            return [ self._factory( i ) for i in self._items ]

    def map( self, callback: Callable[ [ T | R, int ], R ] ):
        """Map items."""

        if self._factory is None:
            return [ callback( i, idx ) for idx, i in enumerate( self._items ) ]
        else:
            return [ callback( self._factory( i ), idx ) for idx, i in enumerate( self._items ) ]

    def take( self, count: int ) -> Self:
        """Return a collection containing the first items."""

        return self._clone( self._items[ : count ] )

    def skip( self, count: int ) -> Self:
        """Return a collection without the first items."""

        return self._clone( self._items[ count : ] )

    def slice( self, start: int | None = None, end: int | None = None ) -> Self:
        """Return a collection containing a sliced range of items."""

        return self._clone( self._items[ start : end ] )

    def reversed( self ) -> Self:
        """Return a collection containing reversed items."""

        return self._clone( self._items[ ::-1 ] )


class DateCollectionBase( CollectionBase[ T ] ):
    """
    Provides date-related immutable collection operations.

    This class extends the base collection adding special methods dealing with
    dates, like `year`, `month`, or `between`.
    """

    def year( self, year: int ) -> Self:
        """Filters resources by year."""

        return self._clone( [ item for item in self._items if str( item ).startswith( f"{ year }-" ) ] )

    def month( self, year: int, month: int ) -> Self:
        """Filters resources by month."""

        return self._clone( [
            item for item in self._items
            if str( item ).startswith( f"{ year }-{ month:02d }-" )
        ] )
