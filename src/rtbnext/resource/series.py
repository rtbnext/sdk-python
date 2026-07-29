"""
Time Series Resource

Implements the resource wrapper for time-series endpoints.
"""

from typing import TypedDict


class TimePoint( TypedDict ):
    """Ensure `date` is included in the dict."""
    date: str
