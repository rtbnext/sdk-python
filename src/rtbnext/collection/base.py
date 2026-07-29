"""
Base Collection

Implements the base collections shared by resource collections.
"""

from __future__ import annotations

from typing import Callable, Generic, Iterator, Self, TypeVar

from rtbnext.defaults import DEFAULT_PER_PAGE
from rtbnext.utils import ymd

R = TypeVar( "R" )
T = TypeVar( "T" )
U = TypeVar( "U" )


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

    def _resolve( self, item: T ) -> T | R:
        """Resolve an item using the configured factory."""

        return self._factory( item ) if self._factory else item

    def _clone( self, items: list[ T ] ) -> Self:
        """Create a new collection instance with replaced items."""

        return self.__class__( items, factory= self._factory, total= self._total )

    def __getitem__( self, index: int ) -> Self | T | R:
        return (
            self._clone( self._items[ index ] )
            if isinstance( index, slice )
            else self._resolve( self._items[ index ] )
        )

    def __len__( self ) -> int:
        return self.count

    def __iter__( self ) -> Iterator[ T | R ]:
        return map( self._resolve, self._items )

    def __contains__( self, item: object ) -> bool:
        return item in self._items

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
    def first( self ) -> T | R | None:
        """Returns the first item."""

        return None if not self._items else self._resolve( self._items[ 0 ] )

    @property
    def last( self ) -> T | R | None:
        """Returns the last item."""

        return None if not self._items else self._resolve( self._items[ -1 ] )

    def to_array( self ) -> list[ T | R ]:
        """Returns all items as list."""

        return [ self._resolve( item ) for item in self._items ]

    def map( self, callback: Callable[ [ T | R, int ], U ] ) -> list[ U ]:
        """Map items."""

        return [ callback( item, index ) for index, item in enumerate( self ) ]

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


class DateCollectionBase( CollectionBase[ str, R ], Generic[ R ] ):
    """
    Provides date-related immutable collection operations.

    This class extends the base collection adding special methods dealing with
    dates, like `year`, `month`, or `between`.
    """

    @property
    def dates( self ) -> list[ str ]:
        """Returns the underlying date values."""

        return self._items.copy()

    def year( self, year: int ) -> Self:
        """Filters resources by year."""

        return self._clone( [ item for item in self._items if item.startswith( f"{ year }-" ) ] )

    def month( self, year: int, month: int ) -> Self:
        """Filters resources by month."""

        return self._clone( [
            item for item in self._items
            if item.startswith( f"{ year }-{ month:02d }-" )
        ] )

    def before( self, date: str ) -> Self:
        """Returns resources before a date."""

        target = ymd( date )
        return self._clone( [ item for item in self._items if item < target ] )

    def after( self, date: str ) -> Self:
        """Returns resources after a date."""

        target = ymd( date )
        return self._clone( [ item for item in self._items if item > target ] )

    def since( self, date: str ) -> Self:
        """Returns resources from a date onward."""

        target = ymd( date )
        return self._clone( [ item for item in self._items if item >= target ] )

    def until( self, date: str ) -> Self:
        """Returns resources up to a date."""

        target = ymd( date )
        return self._clone( [ item for item in self._items if item <= target ] )

    def between( self, start: str, end: str ) -> Self:
        """Returns resources inside a date range."""

        s, e = ymd( start ), ymd( end )
        return self._clone( [ item for item in self._items if s <= item <= e ] )


class IndexCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    """
    Provides cursor-related immutable collection operations.

    This class extends the base collection adding methods to handle cursor
    operations for items.
    """

    def __init__(
        self,
        items: list[ T ], *,
        factory: Callable[ [ T ], R ] | None = None,
        total: int | None = None
    ) -> None:
        super().__init__( items, factory= factory, total= total )
        self._cursor: int = -1

    @property
    def position( self ) -> int:
        return self._cursor

    @property
    def current( self ) -> T | R | None:
        """Return the current item."""

        return self.at( self._cursor )

    @property
    def next( self ) -> T | R | None:
        """Advance to the next item."""

        if self.hasNext:
            self._cursor += 1
            return self.current

    @property
    def prev( self ) -> T | R | None:
        """Move to the previous item."""

        if self.hasPrev:
            self._cursor -= 1
            return self.current

    @property
    def hasNext( self ) -> bool:
        """Return whether a next item exists."""

        return self._cursor + 1 < self.count

    @property
    def hasPrev( self ) -> bool:
        """Return whether a previous item exists."""

        return self._cursor > 0

    def at( self, index: int ) -> T | R | None:
        """Return the item at the given index."""

        return self._resolve( self._items[ index ] ) if 0 <= index < self.count else None

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
