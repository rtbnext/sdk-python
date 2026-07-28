"""
Indexable Resource

Implement the resource wrapper for nested indexable endpoints.
"""


from __future__ import annotations
from typing import Callable, Generic, TypeVar
from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.base import Resource
R = TypeVar( "R" )
IndexFn = Callable[ [ tuple[ str, ... ] ], R ]
KeysFn = Callable[ [ object ], tuple[ str, ... ] | None ]
