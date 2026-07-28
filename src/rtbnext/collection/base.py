"""
Base Collection

Implements the base collection shared by all resource collections.
"""

from __future__ import annotations

from typing import Generic, Self, TypeVar

T = TypeVar( "T" )


class CollectionBase( Generic[ T ] ):
    """
    Provides common immutable collection slicing operations.

    This class serves as a base for resource collections, providing methods to
    manipulate and access the underlying items while maintaining immutability.
    """

    def __init__( self, items: list[ T ], total: int | None = None ) -> None:
        self._items = items
        self._total = len( items ) if total is None else total

    def _clone( self, items: list[ T ] ) -> Self:
        """Create a new collection instance with replaced items."""

        return self.__class__( items, self._total )
