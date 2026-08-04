"""
Filter Endpoint

Provides access to filter collections for special categories,
demographics, and indices.
"""

from __future__ import annotations

from typing import TypedDict

from rtbnext.endpoint.base import EndpointBase
from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.indexable import IndexableResource
from rtbnext.schema.filter import Filter, FilterIndex, FilterItem
from rtbnext.schema.generic import AgeGroup, Gender, Industry, MaritalStatus
from rtbnext.utils import sanitize

type FilterResource = CollectableResource[ Filter, FilterItem, ProfileEntity[ FilterItem ] ]
type FilterIndexResource = IndexableResource[ FilterIndex, FilterIndexTree ]

FilterIndexTree = TypedDict( "FilterIndexTree", {
    "industry": dict[ Industry, FilterResource ],
    "citizenship": dict[ str, FilterResource ],
    "country": dict[ str, FilterResource ],
    "state": dict[ str, FilterResource ],
    "gender": dict[ Gender, FilterResource ],
    "age": dict[ AgeGroup, FilterResource ],
    "maritalStatus": dict[ MaritalStatus, FilterResource ],
    "special": dict[ str, FilterResource ]
} )


class FilterEndpoint( EndpointBase ):
    """
    Endpoint implementation for filter resources.

    Provides access to filter collections for special categories,
    demographics, and indices.
    """

    def _filter( self, path: str ) -> FilterResource:
        """Creates a filter collection using the profile endpoint's collection builder."""

        return self._endpoints.profile.collect( path )

    @property
    def deceased( self ) -> FilterResource:
        """Returns the filter collection for deceased profiles."""

        return self._filter( "v2/filter/special/deceased.json" )

    @property
    def drop_off( self ) -> FilterResource:
        """Returns the filter collection for dropped off profiles."""

        return self._filter( "v2/filter/special/dropOff.json" )

    @property
    def family( self ) -> FilterResource:
        """Returns the filter collection for family profiles."""

        return self._filter( "v2/filter/special/family.json" )

    @property
    def self_made( self ) -> FilterResource:
        """Returns the filter collection for self-made profiles."""

        return self._filter( "v2/filter/special/selfMade.json" )

    def industry( self, key: Industry ) -> FilterResource:
        """Returns the filter collection by industry."""

        return self._filter( f"v2/filter/industry/{ sanitize( key ) }.json" )

    def age( self, key: AgeGroup ) -> FilterResource:
        """Returns the filter collection by age group."""

        return self._filter( f"v2/filter/age/{ key }.json" )

    def gender( self, key: Gender ) -> FilterResource:
        """Returns the filter collection by gender."""

        return self._filter( f"v2/filter/gender/{ sanitize( key ) }.json" )

    def marital_status( self, key: MaritalStatus ) -> FilterResource:
        """Returns the filter collection by marital status."""

        return self._filter( f"v2/filter/maritalStatus/{ sanitize( key ) }.json" )

    def citizenship( self, key: str ) -> FilterResource:
        """Returns the filter collection by citizenship, indexed by ISO code."""

        return self._filter( f"v2/filter/citizenship/{ key.upper() }.json" )

    def country( self, key: str ) -> FilterResource:
        """Returns the filter collection by country, indexed by ISO code."""

        return self._filter( f"v2/filter/country/{ key.upper() }.json" )

    def state( self, key: str ) -> FilterResource:
        """Returns the filter collection by U.S. state, indexed by USPS code."""

        return self._filter( f"v2/filter/state/{ key.upper() }.json" )

    @property
    def index( self ) -> FilterIndexResource:
        """Provides the root filter index resource."""

        return self._indexable( "v2/filter/index.json",
            index= lambda path: self._filter( f"v2/filter/{ "/".join( path ) }.json" )
        )
