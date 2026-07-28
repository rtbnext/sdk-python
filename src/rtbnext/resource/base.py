"""
Base Resource

Implements the base resource wrapper for HTTP responses.
"""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generic, Self

from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader, ResourceState


class Resource( Generic[ D ] ):
    """
    Base resource wrapper for lazy loading, parsing and cache state management.

    Resources are loaded only when data is requested. Loaded responses are kept
    as resource state while parsed values are cached separately.
    """

    def __init__( self, path: str, loader: ResourceLoader, parser: ParserFn[ D ] ) -> None:
        self._path, self._loader, self._parser = path, loader, parser

        self._hooks: dict[ str, set[ Callable[ [ Self ], None ] ] ] = {}

        self._state: ResourceState | None = None
        self._loaded = False
        self._loading: asyncio.Task[ None ] | None = None

        self._parsed = False
        self._value: D | None = None

        self._transformed: Any | Awaitable[ Any ] | None = None

    @property
    def valid( self ) -> bool:
        return False
