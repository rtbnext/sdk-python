"""
Filter

Declares filter entries, documents and the index.
"""

from typing import Any, TypedDict

from rtbnext.schema.generic import (
    AgeGroup, FilterSpecial, Gender, Industry, MaritalStatus, MetaData
)

FilterItem = TypedDict( "FilterItem", {
    "uri": str,
    "name": str,
    "value": Any
} )

Filter = TypedDict( "Filter", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ FilterItem ]
} )

FilterIndex = TypedDict( "FilterIndex", {
    "$metadata": MetaData,
    "industry": list[ Industry ],
    "citizenship": list[ str ],
    "country": list[ str ],
    "state": list[ str ],
    "gender": list[ Gender ],
    "age": list[ AgeGroup ],
    "maritalStatus": list[ MaritalStatus ],
    "special": list[ FilterSpecial ]
} )
