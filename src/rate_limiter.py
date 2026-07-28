"""
Rate Limiter

Implements a token-based rate limiter with support for burst and spread strategies.

Supports two strategies:
- `burst`: allows short bursts of requests
- `spread`: distributes requests evenly over time
"""

