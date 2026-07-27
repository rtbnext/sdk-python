"""Implements the resource wrapper for date-indexed endpoints"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeVar

from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.collection import CollectionBase
from rtbnext.resource.resource import Resource

R = TypeVar( "R" )
T = TypeVar( "T" )


class DateCollection ( CollectionBase[ str ], Generic[ T ] ):
    """Collection wrapper for date-indexed resources."""

    def __init__ (
        self,
        items: list[ str ],
        factory: Callable[ [ str ], T ],
        total: int | None = None
    ):
        super().__init__( items, total if total is not None else len( items ) )
        self._factory = factory

    def _clone ( self, items: list[ str ] ) -> DateCollection[ T ]:
        """Creates a new collection from date values."""
        return DateCollection( items, self._factory, self.total )

    def __iter__ ( self ) -> Iterator[ T ]:
        """Iterates over resolved resources."""

        for date in self._items:
            yield self._factory( date )

    @property
    def dates ( self ) -> list[ str ]:
        """Returns the underlying date values."""
        return self._items

    @property
    def first ( self ) -> T | None:
        """Returns the first resource."""
        return self._factory( self._items[ 0 ] ) if self._items else None

    @property
    def last ( self ) -> T | None:
        """Returns the last resource."""
        return self._factory( self._items[ -1 ] ) if self._items else None

    def find ( self, date: str ) -> T | None:
        """Finds a resource by exact date."""
        return self._factory( date ) if date in self._items else None

    def to_array ( self ) -> list[ T ]:
        """Returns all resolved resources."""
        return [ self._factory( date ) for date in self._items ]

    def map ( self, callback: Callable[ [ T, int ], Any ] ) -> list[ Any ]:
        """Maps resolved resources."""

        return [
            callback( self._factory( date ), index )
            for index, date in enumerate( self._items )
        ]

    def for_each ( self, callback: Callable[ [ T, int ], None ] ) -> None:
        """Executes a callback for each resolved resource."""

        for index, date in enumerate( self._items ):
            callback( self._factory( date ), index )

    def year ( self, year: int ) -> DateCollection[ T ]:
        """Filters resources by year."""
        return self._clone( [ date for date in self._items if date.startswith( f"{ year }-" ) ] )

    def month ( self, year: int, month: int ) -> DateCollection[ T ]:
        """Filters resources by month."""

        return self._clone( [
            date for date in self._items
            if date.startswith( f"{ year }-{ month:02d }-" )
        ] )

    def before ( self, date: str ) -> DateCollection[ T ]:
        """Returns resources before a date."""
        return self._clone( [ item for item in self._items if item < date ] )

    def after ( self, date: str ) -> DateCollection[ T ]:
        """Returns resources after a date."""
        return self._clone( [ item for item in self._items if item > date ] )

    def since ( self, date: str ) -> DateCollection[ T ]:
        """Returns resources from a date onward."""
        return self._clone( [ item for item in self._items if item >= date ] )

    def until ( self, date: str ) -> DateCollection[ T ]:
        """Returns resources up to a date."""
        return self._clone( [ item for item in self._items if item <= date ] )

    def between ( self, start: str, end: str ) -> DateCollection[ T ]:
        """Returns resources inside a date range."""
        return self._clone( [ item for item in self._items if start <= item <= end ] )


class DateableResource ( Resource[ D ], Generic[ D, R ] ):
    """Resource wrapper for date-indexed endpoints."""

    def __init__ (
        self,
        path: str,
        loader: ResourceLoader,
        parser: ParserFn[ D ],
        date: Callable[ [ str ], R ]
    ):
        super().__init__( path, loader, parser )
        self._factory = date
