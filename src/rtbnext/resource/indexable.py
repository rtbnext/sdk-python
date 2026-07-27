from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, cast

from rtbnext.core.http_client import HttpResponse
from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.resource import Resource

R = TypeVar( "R" )
IndexFn = Callable[ [ tuple[ str, ... ] ], R ]
KeysFn = Callable[ [ object ], tuple[ str, ... ] | None ]


@dataclass ( slots= True )
class IndexOptions( Generic[ R ] ):
    """Configuration for index traversal."""

    index: IndexFn[ R ]
    keys: KeysFn | None = None
