"""
Indexable Resource

Implement the resource wrapper for nested indexable endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.core.parser import ParserFn
from rtbnext.resource.base import Resource

D = TypeVar( "D" )
R = TypeVar( "R" )

type Path = tuple[ str, ... ]
type IndexFn[ R ] = Callable[ [ Path ], R ]
type KeysFn = Callable[ [ object ], Path | None ]
