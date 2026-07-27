"""
RESOURCE

Implements the resource loader and pooling of resource states.
"""


from __future__ import annotations

from dataclasses import dataclass

from .http_client import HttpResponse


@dataclass ( slots= True )
class ResourceState:
    """
    Represents the state of a cached resource.
    """

    response: HttpResponse
    created: float
    expires: float | None = None
    etag: str | None = None
    last_modified: str | None = None
