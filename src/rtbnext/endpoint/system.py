"""
System Endpoint

Provides access to system status information.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.schema.system import SystemStatus

type SystemStatusResource = Resource[ SystemStatus ]


class SystemEndpoint( EndpointBase ):
    """
    Endpoint implementation for system resources.

    Provides access to system status information.
    """

    @property
    def status( self ) -> SystemStatusResource:
        """Returns the current system status resource."""

        return self._resource( "v2/system/status.json" )
