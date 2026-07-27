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
