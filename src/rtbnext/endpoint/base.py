"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen= True, slots= True, kw_only= True )
class Endpoints:
    """Endpoints available in the RTBNext SDK."""
    ...



