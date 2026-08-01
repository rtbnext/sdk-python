"""
Parser

Implements the HTTP response body parser methods for simple text,
JSON responses and CSV data.
"""

from __future__ import annotations

import csv
import json
from io import StringIO
from typing import Any, Callable, Literal, TypeVar

from rtbnext.core.http_client import HttpResponse

D = TypeVar( "D" )

type ParserFn[ D ] = Callable[ [ HttpResponse ], D ]
type ParserMode = Literal[ "text", "json", "csv" ]


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

    @staticmethod
    def text( res: HttpResponse ) -> str:
        """Convert an HTTP response body to UTF-8 text."""

        if not res.ok:
            raise RuntimeError( f"Request failed with status { res.status }." )
        if not res.body:
            raise RuntimeError( "Response contains no data." )

        try:
            return res.body.decode()
        except Exception as exc:
            raise RuntimeError( f"Failed to decode response: { exc }" ) from exc

    @staticmethod
    def json( res: HttpResponse ) -> Any:
        """Parse an HTTP response body as JSON."""

        try:
            return json.loads( Parser.text( res ) )
        except Exception as exc:
            raise RuntimeError( f"Failed to parse JSON: { exc }" ) from exc

    @staticmethod
    def csv( res: HttpResponse, delimiter: str = "," ) -> list[ list[ str | int | float ] ]:
        """Parse an HTTP response body as CSV."""

        return [
            [ Parser._number( value ) for value in row ]
            for row in csv.reader( StringIO( Parser.text( res ) ), delimiter= delimiter )
        ]


def parser( mode: ParserMode ) -> ParserFn[ D ]:
    """
    Return the parser function based on the given mode.
    Raises if the parser for the given mode is not implemented.
    """

    if not hasattr( Parser, mode ):
        raise ValueError( f"Unsupported parser mode: { mode }" )

    return getattr( Parser, mode )
