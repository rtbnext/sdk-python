"""
System Endpoint

Provides access to system status information.
"""

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource


class System( EndpointBase ):
    """
    Endpoint implementation for system resources.

    Provides access to system status information.
    """

    @property
    def status( self ) -> Resource:
        """Returns the current system status resource."""

        return self._json( "v2/system/status.json" )
