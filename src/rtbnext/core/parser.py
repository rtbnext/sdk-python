"""
PARSER

Implements the HTTP response body parser classes.
"""

from __future__ import annotations

import json

from rtbnext.core.http_client import HttpResponse


class TextParser:
    """
    Parses HTTP response bodies into UTF-8 text.

    The parser validates the response status and ensures that
    the response contains data before decoding it.
    """

    @staticmethod
    def parse ( response: HttpResponse ) -> str:
        """
        Convert an HTTP response body to UTF-8 text.

        Args:
            response:
                HTTP response to parse.

        Returns:
            The decoded response text.

        Raises:
            RuntimeError:
                If the request failed or contains no data.
        """

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
    def parse ( response: HttpResponse ) -> object:
        """
        Parse an HTTP response body as JSON.

        Args:
            response:
                HTTP response to parse.

        Returns:
            The parsed JSON value.

        Raises:
            RuntimeError:
                If JSON parsing fails.
        """

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
        """
        Convert a CSV field value.

        Numeric values are converted to numbers where possible.

        Args:
            value:
                Raw CSV field value.

        Returns:
            Parsed value.
        """

        value = value.strip()

        try:
            if "." in value:
                return float( value )

            return int( value )

        except ValueError:
            return value

    @staticmethod
    def _parse_line ( line: str, delimiter: str ) -> list[ str | int | float ]:
        """
        Parse a single CSV line.

        Args:
            line:
                CSV line.

            delimiter:
                Field delimiter.

        Returns:
            Parsed field values.
        """

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
        """
        Parse an HTTP response body as CSV.

        Args:
            response:
                HTTP response to parse.

            delimiter:
                CSV field delimiter.

        Returns:
            Parsed CSV rows.
        """

        return [
            CsvParser._parse_line( line, delimiter )
            for line in TextParser.parse( response ).splitlines()
            if line.strip()
        ]
