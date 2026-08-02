"""
Filter Endpoint

Provides access to filter collections for special categories,
demographics, and indices.
"""

from __future__ import annotations

from rtbnext.endpoint.base import EndpointBase
from rtbnext.resource.collectable import CollectableResource
from rtbnext.schema.filter import Filter, FilterIndex, FilterItem


class FilterEndpoint( EndpointBase ):
    """
    Endpoint implementation for filter resources.

    Provides access to filter collections for special categories,
    demographics, and indices.
    """
