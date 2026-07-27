"""Base collection implementation used by all resource collections."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

T = TypeVar( "T" )


class CollectionBase( Generic[ T ] ):
    """Base class for immutable SDK collections."""
