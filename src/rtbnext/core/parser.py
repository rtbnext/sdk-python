"""
Parser

Implements the HTTP response body parser methods for simple text,
JSON responses and CSV data.
"""

from __future__ import annotations

import csv
import json
from io import StringIO
from typing import Any, Callable, TypeVar

from rtbnext.core.http_client import HttpResponse

D = TypeVar( "D" )

type ParserFn[ D ] = Callable[ [ HttpResponse ], D ]


class Parser:
    """
    Parses HTTP response bodies into text or objects.

    The parser validates the response status and ensures that
    the response contains data before decoding it.
    """

    @staticmethod
    def _number( value: str ) -> str | int | float:
        """Parses an individual CSV field value, converting numeric strings to numbers."""

        value = value.strip()

        try:
            return float( value ) if "." in value else int( value ) if value else value
        except ValueError:
            return value
