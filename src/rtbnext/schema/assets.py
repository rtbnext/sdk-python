"""
Assets

Declares shared types for assets, net worth, rankings, performance metrics,
and historical financial data.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.generic import AssetType

ChangeItem = TypedDict( "ChangeItem", {
    "value": float,
    "percent": float
} )

AssetInfo = TypedDict( "AssetInfo", {
    "exchange": str,
    "ticker": str,
    "shares": NotRequired[ float ],
    "price": float,
    "currency": str,
    "exRate": float
} )

Asset = TypedDict( "Asset", {
    "type": AssetType,
    "label": str,
    "value": NotRequired[ float ],
    "info": NotRequired[ AssetInfo ]
} )
