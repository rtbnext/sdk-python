"""
Mover Endpoint

Provides access to mover snapshots and mover index resources.
"""

from __future__ import annotations

from typing import cast

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.base import Resource
from rtbnext.resource.dateable import DateableResource
from rtbnext.utils import ymd


class MoverEndpoint( EndpointBase ):
    """
    Endpoint implementation for mover resources.

    Provides access to mover snapshots and mover index resources.
    """

    def snapshot( self, date: object ) -> Resource:
        """Returns a mover snapshot for a given date."""

        return self._json( f"v2/mover/{ ymd( date ) }.json" )

    @property
    def index( self ) -> DateableResource:
        """Returns the root mover index resource."""

        return cast( DateableResource, self._json( "v2/mover/index.json", date= self.snapshot ) )
