"""
Assets

Declares shared types for assets, net worth, rankings, performance metrics,
and historical financial data.
"""

from typing import NotRequired, TypedDict

ChangeItem = TypedDict( "ChangeItem", {
    "value": float,
    "percent": float
} )
