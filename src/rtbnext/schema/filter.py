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
    "items": list[ FilterItem ],
    "count": int
} )
