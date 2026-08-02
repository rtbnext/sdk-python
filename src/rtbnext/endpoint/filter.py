"""
Filter Endpoint

Provides access to filter collections for special categories,
demographics, and indices.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.collectable import CollectableResource
from rtbnext.schema.filter import Filter, FilterIndex, FilterItem

type FilterCollection = CollectableResource[ Filter, FilterItem, ProfileEntity[ FilterItem ] ]


class FilterEndpoint( EndpointBase ):
    """
    Endpoint implementation for filter resources.

    Provides access to filter collections for special categories,
    demographics, and indices.
    """

    def _filter( self, path: str ) -> FilterCollection:
        """Creates a filter collection using the profile endpoint's collection builder."""

        return self._endpoints.profile.collect( path )

    @property
    def deceased( self ) -> FilterCollection:
        """Returns the deceased profiles filter collection."""

        return self._filter( "v2/filter/special/deceased.json" )
