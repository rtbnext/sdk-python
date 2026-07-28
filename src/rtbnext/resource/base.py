"""
Base Resource

Implements the base resource wrapper for HTTP responses.
"""

from __future__ import annotations

from typing import Generic, TypeVar

D = TypeVar( "D" )


class Resource ( Generic[ D ] ):
    """
    Base resource wrapper for lazy loading, parsing and cache state management.

    Resources are loaded only when data is requested. Loaded responses are kept
    as resource state while parsed values are cached separately.
    """

    @property
    def valid( self ) -> bool:
        return False
