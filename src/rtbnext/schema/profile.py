"""
Profile

Declares profile records representing individuals, including personal
information, financial data, relationships, media, and historical statistics.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.generic import MetaData

ProfileIndexItem = TypedDict( "ProfileIndexItem", {
    "uri": str,
    "name": str,
    "text": str,
    "aliases": list[ str ],
    "desc": NotRequired[ str ],
    "image": NotRequired[ str ]
} )

ProfileIndex = TypedDict( "ProfileIndex", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ ProfileIndexItem ]
} )
