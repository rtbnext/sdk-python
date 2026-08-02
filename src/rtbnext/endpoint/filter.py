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
from rtbnext.schema.generic import AgeGroup, Gender, Industry

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

    @property
    def drop_off( self ) -> FilterCollection:
        """Returns the drop-off profiles filter collection."""

        return self._filter( "v2/filter/special/dropOff.json" )

    @property
    def family( self ) -> FilterCollection:
        """Returns the family profiles filter collection."""

        return self._filter( "v2/filter/special/family.json" )

    @property
    def self_made( self ) -> FilterCollection:
        """Returns the self-made profiles filter collection."""

        return self._filter( "v2/filter/special/selfMade.json" )

    def industry( self, key: Industry ) -> FilterCollection:
        """Returns the industry filter collection."""

        return self._filter( f"v2/filter/industry/{ key.lower() }.json" )

    def age( self, key: AgeGroup ) -> FilterCollection:
        """Returns the age group filter collection."""

        return self._filter( f"v2/filter/age/{ key }.json" )

    def gender( self, key: Gender ) -> FilterCollection:
        """Returns the gender filter collection."""

        return self._filter( f"v2/filter/gender/{ key.lower() }.json" )
