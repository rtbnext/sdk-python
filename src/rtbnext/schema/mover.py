"""
Mover

Declares movers as the largest gains and losses over predefined time periods.
"""

from typing import TypedDict

from rtbnext.schema.generic import MetaData, ChangeItem


MoverItem = TypedDict( "MoverItem", {
    "uri": str,
    "name": str,
    "value": float
} )

MoverEntry = TypedDict( "MoverEntry", {
    "winner": list[ MoverItem ],
    "loser": list[ MoverItem ]
} )

MoverBucket = TypedDict( "MoverBucket", {
    "total": ChangeItem,
    "networth": MoverEntry,
    "percent": MoverEntry
} )
