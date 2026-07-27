"""Implements the base resource wrapper for HTTP responses."""


from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generic, Self, TypeVar

from rtbnext.core.http_client import HttpResponse, RequestOptions
from rtbnext.core.resource import ResourceLoader, ResourceState


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
        """
        Parse the loaded HTTP response.

        Returns:
            The parsed resource value.

        Raises:
            RuntimeError:
                If the resource has not been loaded yet.
        """

        if self._state is None:
            raise RuntimeError( "Resource has not been loaded." )

        self._value = self._parser( self._state.response )
        self._parsed = True
        self._emit( "parse" )

        return self._value

    def _value_or_raise ( self ) -> D:
        """
        Return the parsed resource value or raise an error if unavailable.

        Returns:
            The parsed resource value.

        Raises:
            RuntimeError:
                If the resource value is unavailable.
        """

        if self._value is None:
            raise RuntimeError( "Resource value unavailable." )

        return self._value

    async def _transform ( self, fn: Callable[ [ D ], Awaitable[ Any ] | Any ] ) -> Any:
        """
        Transform parsed resource data and cache the result.

        The transformation is executed only once. Concurrent callers reuse
        the same pending task.

        Args:
            fn:
                Transformation function.

        Returns:
            The transformed value.
        """

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

    def _emit ( self, *events: str ) -> None:
        """
        Emit lifecycle events.

        Args:
            events:
                Event names to emit.
        """

        for event in events:
            for handler in self._hooks.get( event, set() ):
                handler( self )

    def on ( self, event: str, handler: Callable[ [ Self ], None ] ) -> Self:
        """
        Register an event handler.

        Args:
            event:
                Event name.
            handler:
                Callback invoked when the event occurs.

        Returns:
            The current resource instance.
        """

        self._hooks.setdefault( event, set() ).add( handler )
        return self

    def off ( self, event: str, handler: Callable[ [ Self ], None ] ) -> Self:
        """
        Remove an event handler.

        Args:
            event:
                Event name.
            handler:
                Handler to remove.

        Returns:
            The current resource instance.
        """

        self._hooks.get( event, set() ).discard( handler )
        return self

    @property
    def valid ( self ) -> bool:
        """
        Return whether the current resource state is still valid.

        Resources that have not been loaded yet are considered valid.
        """

        return (
            not self._loaded
            or self._state is None
            or self._loader.valid( self._state )
        )

    async def load ( self, options: RequestOptions | None = None ) -> None:
        """
        Load the resource if it has not already been loaded.

        Multiple concurrent calls share the same loading task.

        Args:
            options:
                Optional request options.
        """

        if self._loaded:
            return

        if self._loading is None:

            async def execute () -> None:
                self._state = await self._loader.load( self._path, options )
                self._loaded = True

                self._reset()
                self._emit( "load", "update" )

            self._loading = asyncio.create_task( execute() )

        try:
            await self._loading
        finally:
            self._loading = None

    async def refresh ( self, options: RequestOptions | None = None ) -> None:
        """
        Refresh the resource from the network.

        Args:
            options:
                Optional request options.
        """

        self._state = await self._loader.refresh( self._path, options )
        self._loaded = True

        self._reset()
        self._emit( "refresh", "update" )

    async def data ( self ) -> D:
        """
        Return parsed resource data.

        The resource is loaded lazily and parsed only once.

        Returns:
            Parsed resource value.
        """

        await self.load()

        if not self._parsed:
            return self._parse()

        return self._value_or_raise()
