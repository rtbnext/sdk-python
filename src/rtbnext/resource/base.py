"""
Base Resource

Implements the base resource wrapper for HTTP responses.
Resource pooling is intended to optimize memory allocation.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

D = TypeVar( "D" )
R = TypeVar( "R", bound= "Resource[ Any ]" )


class Resource( Generic[ D ] ):
    ...


class ResourcePool( Generic[ R ] ):
    ...
