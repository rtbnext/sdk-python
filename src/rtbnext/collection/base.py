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
