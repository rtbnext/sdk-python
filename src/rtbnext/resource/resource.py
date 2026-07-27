"""
RESOURCE

Implements the base resource wrapper for HTTP responses.
"""


from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generic, Self, TypeVar

from rtbnext.core.resource import ResourceLoader, ResourceState
from rtbnext.core.http_client import RequestOptions, HttpResponse


D = TypeVar( "D" )
ParserFn = Callable[ [ HttpResponse ], D ]


class Resource ( Generic[ D ] ):
    """
    Base resource wrapper for lazy loading, parsing and cache state management.

    Resources are loaded only when data is requested. Loaded responses are kept
    as resource state while parsed values are cached separately.
    """

    def __init__ ( self, path: str, loader: ResourceLoader, parser: ParserFn[ D ] ) -> None:
        """
        Create a new resource wrapper.

        Args:
            path:
                API resource path.

            loader:
                Resource loader used for fetching and caching.

            parser:
                Function used to parse HTTP responses.
        """

        self._path = path
        self._loader = loader
        self._parser = parser

        self._hooks: dict[ str, set[ Callable[ [ Self ], None ] ] ] = {}

        self._loaded = False
        self._loading: asyncio.Task[ None ] | None = None

        self._state: ResourceState | None = None

        self._parsed = False
        self._value: D | None = None

        self._transformed: Any | Awaitable[ Any ] | None = None

    def _reset ( self ) -> None:
        """Reset parsed values after loading or refreshing."""

        self._parsed = False
        self._value = None
        self._transformed = None

    def _parse ( self ) -> D:
        """Parse the current response body."""

        if self._state is None:
            raise RuntimeError( "Resource has not been loaded." )

        self._value = self._parser( self._state.response )
        self._parsed = True
        self._emit( "parse" )

        return self._value

    async def _transform ( self, fn: Callable[ [ D ], Awaitable[ Any ] | Any ] ) -> Any:
        """Transform parsed resource data and cache the result."""

        if self._transformed is None:
            async def execute() -> Any:
                result = await self.data()
                value = fn( result )

                if asyncio.iscoroutine( value ):
                    value = await value

                self._transformed = value
                self._emit( "transform" )

                return value

            self._transformed = asyncio.create_task( execute() )

        return await self._transformed
