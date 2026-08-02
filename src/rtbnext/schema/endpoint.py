"""
Endpoint

Declares all available SDK endpoint types.
"""

from typing import TypedDict

from rtbnext.endpoint.profile import ProfileEntity
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.indexable import IndexableResource
from rtbnext.schema.filter import Filter, FilterItem
from rtbnext.schema.generic import AgeGroup, Gender, Industry, MaritalStatus

type FilterCollection = CollectableResource[ Filter, FilterItem, ProfileEntity[ FilterItem ] ]

FilterIndexTree = TypedDict( "FilterIndexTree", {
    "industry": dict[ Industry, FilterCollection ],
    "citizenship": dict[ str, FilterCollection ],
    "country": dict[ str, FilterCollection ],
    "state": dict[ str, FilterCollection ],
    "gender": dict[ Gender, FilterCollection ],
    "age": dict[ AgeGroup, FilterCollection ],
    "maritalStatus": dict[ MaritalStatus, FilterCollection ],
    "special": dict[ str, FilterCollection ]
} )

type FilterIndex = IndexableResource[ FilterIndex, FilterIndexTree ]
