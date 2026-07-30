"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.parser import Parser
from rtbnext.core.resource import ResourceLoader, ResourcePool
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.dateable import DateableResource
from rtbnext.resource.time_series import TimeSeriesResource


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for text, JSON, CSV,
    collection, index, time series, and date resources.
    """
