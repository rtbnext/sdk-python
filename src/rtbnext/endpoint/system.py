"""
System Endpoint

Provides access to system status information.
"""

from __future__ import annotations

from typing import cast

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource


class SystemEndpoint( EndpointBase ):
    """
    Endpoint implementation for system resources.

    Provides access to system status information.
    """

    @property
    def status( self ):
        """Returns the current system status resource."""

        return cast(
            Resource,
            self._json( "v2/system/status.json" )
        )
