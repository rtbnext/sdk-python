"""
Base Resource

Implements the base resource wrapper for HTTP responses.
"""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generic, Self

from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader, ResourceState

type TransformFn[ D ] = Callable[ [ D ], Awaitable[ Any ] | Any ]


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

    def _emit( self, *events: str ) -> None:
        """Emit lifecycle events."""

        for event in events:
            for handler in self._hooks.get( event, set() ):
                handler( self )

    def _reset( self ) -> None:
        """Reset parsed values after loading or refreshing."""

        self._parsed = False
        self._value = None
        self._transformed = None

    def _parse( self ) -> D:
        """Parse the loaded HTTP response."""

        if self._state is None:
            raise RuntimeError( "Resource has not been loaded." )

        self._value = self._parser( self._state.response )
        self._parsed = True
        self._emit( "parse" )

        return self._value

    async def _transform( self, fn: TransformFn[ D ] ) -> Any:
        """Transform parsed resource data and cache the result."""

        if self._transformed is None:

            async def execute () -> Any:
                value = fn( await self.data() )

                if asyncio.iscoroutine( value ):
                    value = await value

                self._transformed = value
                self._emit( "transform" )

                return value

            self._transformed = asyncio.create_task( execute() )

        return await self._transformed

    def _value_or_raise( self ) -> D:
        """Return the parsed resource value or raise an error if unavailable."""

        if self._value is None:
            raise RuntimeError( "Resource value unavailable." )

        return self._value

    def on( self, event: str, handler: Callable[ [ Self ], None ] ) -> Self:
        """Register an event handler."""

        self._hooks.setdefault( event, set() ).add( handler )
        return self

    def off( self, event: str, handler: Callable[ [ Self ], None ] ) -> Self:
        """Remove an event handler."""

        self._hooks.get( event, set() ).discard( handler )
        return self

    @property
    def valid( self ) -> bool:
        return False
