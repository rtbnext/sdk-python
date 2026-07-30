"""
HTTP Client

Implements an HTTP client with built-in rate limiting, request deduplication
and proper client identification.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass( slots= True, frozen= True )
class ClientIdentity:
    """Information used to identify the client making API requests."""

    name: str
    version: str
    contact: str | None = None
    email: str | None = None

    def __post_init__( self ) -> None:
        if not self.name.strip():
            raise ValueError( "Client name is required." )

        if not self.version.strip():
            raise ValueError( "Client version is required." )
