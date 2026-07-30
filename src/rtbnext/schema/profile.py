"""
Profile

Declares profile records representing individuals, including personal
information, financial data, relationships, media, and historical statistics.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.generic import (
    Gender, Industry, MaritalStatus, MetaData, ProfileStatusFlag, SelfMadeRank
)

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

SearchIndexItem = TypedDict( "SearchIndexItem", {
    "id": str,
    "uri": str,
    "deceased": bool,
    "family": bool,
    "dropOff": bool,
    "embargo": bool,
    "searchName": str,
    "fullName": str,
    "lastName": str,
    "gender": NotRequired[ Gender ],
    "birthDate": NotRequired[ str ],
    "age": NotRequired[ int ],
    "birthCountry": NotRequired[ str ],
    "residenceCountry": NotRequired[ str ],
    "citizenship": NotRequired[ str ],
    "industry": NotRequired[ Industry ],
    "source": NotRequired[ list[ str ] ],
    "networth": NotRequired[ float ],
    "rank": NotRequired[ int ],
    "organization": NotRequired[ str ],
    "maritalStatus": NotRequired[ MaritalStatus ],
    "children": NotRequired[ int ],
    "philanthropyScore": NotRequired[ int ],
    "selfMade": NotRequired[ bool ],
    "selfMadeRank": NotRequired[ SelfMadeRank ],
    "wikidata": NotRequired[ str ],
    "status": NotRequired[ ProfileStatusFlag ],
    "score": NotRequired[ float ],
    "timestamp": str
} )

SearchIndex = TypedDict( "SearchIndex", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ SearchIndexItem ]
} )
