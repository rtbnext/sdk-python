"""
PARSER

Implements the HTTP response body parser classes.
"""

from __future__ import annotations

import json
from typing import Any, TypeVar, cast

from rtbnext.core.http_client import HttpResponse


T = TypeVar( "T" )


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
    def parse ( response: HttpResponse ) -> Any:
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
            return json.loads ( TextParser.parse( response ) )
        except Exception as exc:
            raise RuntimeError( f"Failed to parse JSON: { exc }" ) from exc
