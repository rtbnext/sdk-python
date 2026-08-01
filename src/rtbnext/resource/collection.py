"""
Base Collections

Implements the base collections shared by resource collections.
"""

from __future__ import annotations

from typing import Callable, Generic, Iterator, Self, TypeVar, cast

from rtbnext.defaults import DEFAULT_PER_PAGE

R = TypeVar( "R" )
T = TypeVar( "T" )
U = TypeVar( "U" )

type ItemFactory[ T, R ] = Callable[ [ T ], R ]


class CollectionBase( Generic[ T, R ] ):
    """
    Provides common immutable collection operations.

    This class serves as a base for resource collections, providing methods to
    manipulate and access the underlying items while maintaining immutability.
    """

    def __init__(
        self, items: list[ T ], *,
        factory: ItemFactory[ T, R ] = lambda item: cast( R, item ),
        total: int | None = None
    ) -> None:
        self._items, self._factory = items, factory
        self._total = len( items ) if total is None else total

    def _clone( self, items: list[ T ] ) -> Self:
        """Create a new collection instance with replaced items."""

        return self.__class__( items, factory= self._factory, total= self._total )

    def __getitem__( self, index: int ) -> Self | R:
        return (
            self._clone( self._items[ index ] )
            if isinstance( index, slice )
            else self._factory( self._items[ index ] )
        )

    def __contains__( self, item: object ) -> bool:
        return item in self._items

    def __len__( self ) -> int:
        return self.count

    def __iter__( self ) -> Iterator[ R ]:
        return map( self._factory, self._items )

    def __reversed__( self ) -> Iterator[ R ]:
        return map( self._factory, self._items[ ::-1 ] )

    @property
    def items( self ) -> list[ T ]:
        """Returns the raw items."""

        return self._items.copy()

    @property
    def total( self ) -> int:
        """Return the total number of available items."""

        return self._total

    @property
    def count( self ) -> int:
        """Return the number of items currently contained."""

        return len( self._items )

    @property
    def first( self ) -> R | None:
        """Returns the first item."""

        return None if not self._items else self._factory( self._items[ 0 ] )

    @property
    def last( self ) -> R | None:
        """Returns the last item."""

        return None if not self._items else self._factory( self._items[ -1 ] )

    def to_array( self ) -> list[ R ]:
        """Returns all resolved items as list."""

        return [ self._factory( item ) for item in self._items ]

    def map( self, callback: Callable[ [ R, int ], U ] ) -> list[ U ]:
        """Map resolved items."""

        return [ callback( item, index ) for index, item in enumerate( self ) ]

    def reversed( self ) -> Self:
        """Return a collection containing reversed items."""

        return self._clone( self._items[ ::-1 ] )

    def take( self, count: int ) -> Self:
        """Return a collection containing the first items."""

        return self._clone( self._items[ : count ] )

    def skip( self, count: int ) -> Self:
        """Return a collection without the first items."""

        return self._clone( self._items[ count : ] )

    def slice( self, start: int | None = None, end: int | None = None ) -> Self:
        """Return a collection containing a sliced range of items."""

        return self._clone( self._items[ start : end ] )


class DateCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    """
    Provides date-related immutable collection operations.

    This class extends the base collection adding special methods dealing with
    dates, like `year`, `month`, or `between`.
    """
    ...


class IndexCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    """
    Provides cursor-related immutable collection operations.

    This class extends the base collection adding methods to handle cursor
    operations for items.
    """

    def __init__(
        self, items: list[ T ], *,
        factory: ItemFactory[ T, R ] = lambda item: cast( R, item ),
        total: int | None = None
    ) -> None:
        super().__init__( items, factory= factory, total= total )
        self._cursor: int = -1

    @property
    def position( self ) -> int:
        """Return the current cursor position."""

        return self._cursor

    @property
    def current( self ) -> R | None:
        """Return the current resolved item."""

        return self.at( self._cursor )

    @property
    def next( self ) -> R | None:
        """Return the next resolved item."""

        self._cursor += 1
        return self.at( self._cursor )

    @property
    def prev( self ) -> R | None:
        """Return the previous resolved item."""

        self._cursor -= 1
        return self.at( self._cursor )

    @property
    def has_next( self ) -> bool:
        """Return whether a next item exists."""

        return self._cursor + 1 < self.count

    @property
    def has_prev( self ) -> bool:
        """Return whether a previous item exists."""

        return self._cursor > 0

    def reset( self ) -> Self:
        """Reset the cursor."""

        self._cursor = -1
        return self

    def at( self, index: int ) -> R | None:
        """Return the resolved item at the given index."""

        return self._factory( self._items[ index ] ) if 0 <= index < self.count else None

    def page( self, page: int, per_page: int = DEFAULT_PER_PAGE ) -> Self:
        """Return a collection containing one page."""

        start = max( page - 1, 0 ) * per_page
        return self._clone( self._items[ start : start + per_page ] )

    def pages( self, per_page: int = DEFAULT_PER_PAGE ) -> list[ Self ]:
        """Return all pages."""

        return [
            self._clone( self._items[ i : i + per_page ] )
            for i in range( 0, self.count, per_page )
        ]
