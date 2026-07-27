"""
CACHE

Implements ...
"""


from __future__ import annotations

from typing import Protocol

from .resource import ResourceState


class Cache( Protocol ):
    """
    Interface for cache implementations.

    A cache stores and retrieves resource states using string keys.
    Implementations may choose any storage backend, such as memory,
    the filesystem or an external database.
    """

    @property
    def size ( self ) -> int:
        """
        Return the number of cached resource states.
        """
        ...

    async def get ( self, key: str ) -> ResourceState | None:
        """
        Retrieve a cached resource state.

        Args:
          key:
            The cache key associated with the resource.

        Returns:
          The cached resource state if present, otherwise ``None``.
        """
        ...

    async def set ( self, key: str, value: ResourceState ) -> None:
        """
        Store a resource state.

        If the key already exists, the previous value is replaced.

        Args:
          key:
            The cache key.

          value:
            The resource state to store.
        """
        ...

    async def delete ( self, key: str ) -> None:
        """
        Remove a resource state from the cache.

        Args:
          key:
            The cache key.
        """
        ...

    async def clear ( self ) -> None:
        """
        Remove all resource states from the cache.
        """
        ...
