"""
Base Collections

Implements the base collections shared by resource collections.
"""

from __future__ import annotations

from typing import Callable, Generic, Self, TypeVar, cast

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


class DateCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    ...


class IndexCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    ...
