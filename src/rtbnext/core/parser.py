"""Implements the HTTP response body parser classes."""

from __future__ import annotations

import json
from typing import Any, Callable, TypeVar

from rtbnext.core.http_client import HttpResponse

D = TypeVar( "D" )
ParserFn = Callable[ [ HttpResponse ], D ]


class TextParser:
    """
    Parses HTTP response bodies into UTF-8 text.

    The parser validates the response status and ensures that
    the response contains data before decoding it.
    """

    @staticmethod
    def parse ( response: HttpResponse ) -> str:
        """Convert an HTTP response body to UTF-8 text."""

        if not response.ok:
            raise RuntimeError( f"Request failed with status { response.status }." )
        if not response.body:
            raise RuntimeError( "Response contains no data." )

        return response.body.decode( "utf-8" )


class JsonParser ( TextParser ):
    """
    Parses HTTP response bodies as JSON.

    Extends TextParser by decoding the response body and
    converting it into Python objects.
    """

    @staticmethod
    def parse ( response: HttpResponse ) -> Any:
        """Parse an HTTP response body as JSON."""

        try:
            return json.loads( TextParser.parse( response ) )
        except Exception as exc:
            raise RuntimeError( f"Failed to parse JSON: { exc }" ) from exc


class CsvParser ( TextParser ):
    """
    Parses CSV response bodies into structured arrays.

    The parser converts numeric values into integers or floats
    while keeping non-numeric values as strings.
    """

    @staticmethod
    def _parse_value ( value: str ) -> str | int | float:
        """Convert a CSV field value."""

        value = value.strip()

        try:
            return ( float( value ) if "." in value else int( value ) )
        except ValueError:
            return value

    @staticmethod
    def _parse_line ( line: str, delimiter: str ) -> list[ str | int | float ]:
        """Parse a single CSV line."""

        values: list[ str | int | float ] = []
        value = ""
        quoted = False
        index = 0

        while index < len( line ):
            char = line[ index ]

            if char == '"':
                if quoted and index + 1 < len( line ) and line[ index + 1 ] == '"':
                    value += '"'
                    index += 1
                else:
                    quoted = not quoted

            elif char == delimiter and not quoted:
                values.append( CsvParser._parse_value( value ) )
                value = ""

            else:
                value += char

            index += 1

        values.append( CsvParser._parse_value( value ) )
        return values

    @staticmethod
    def parse ( response: HttpResponse, delimiter: str = "," ) -> list[ list[ str | int | float ] ]:
        """Parse an HTTP response body as CSV."""

        return [
            CsvParser._parse_line( line, delimiter )
            for line in TextParser.parse( response ).splitlines()
            if line.strip()
        ]
