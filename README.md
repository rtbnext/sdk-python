# rtbnext

**Official Python SDK for the RTBNext API.**

The RTBNext SDK provides a typed, asynchronous interface for accessing billionaire profiles, lists, filters, statistics, historical data and system information from the [RTBNext API](https://api.rtbnext.de).

The SDK follows a consistent resource-oriented design: resources are loaded lazily, cached according to the configured cache mode, and expose typed helper methods for collections, time series and indexed data.

The package includes Python type information and is compatible with static type checkers such as Pyright, Pylance and mypy.

To find a list of all available API endpoints, please refer to the [API Documentation](https://docs.rtbnext.de). Also visit the [API endpoint](https://api.rtbnext.de) or review the [SDK Documentation](https://sdk.rtbnext.de) for additional details. For updates on current issues or maintenance, please refer to the [System Status](https://status.rtbnext.de).

## Installation

Install the package using pip:

```bash
pip install rtbnext
```

## First usage

Every client application **must identify** itself when creating an SDK instance. This information is sent with API requests and helps to provide transparency about API consumers.

```py
import asyncio

from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext(
        client= ClientIdentity(
            name= "my-application",
            version= "1.0.0",
            contact= "https://example.com/contact"
        )
    ) as client:

        stats = await client.stats.global_.data()
        print( stats["count"] )


asyncio.run( main() )
```

The client identity consists of:

- `name` — application or project name
- `version` — application version
- `contact` — optional contact URL
- `email` — optional contact email address

## Core concepts

### Lazy resources

Resources are not downloaded when they are created. Data is loaded only when it is requested.

```py
profile = client.profile.get( "bill-gates" )

# No request has been made yet.

data = await profile.meta.data()
```

### Collections

Collection resources provide filtering, searching, sorting and paging helpers.

```py
profiles = await client.profile.index.collection()

for profile in profiles.search( "bill" ).order_by( "networth", descending= True ).take( 5 ):
    print( item.raw["name"], item.raw["uri"] )
```

### Time series

Historical data can be accessed through typed time-series resources.

```py
history = await client.profile.get( "bill-gates" ).history.series()
print( history.latest )
```

Time series collections support date-based navigation and cursor operations:

```py
history.seek( "2026-01-01" )

while ( point := history.next ) is not None:
    print( point["date"], point["networth"] )
```

## Cache behavior

The SDK includes a configurable resource cache layer that follows HTTP cache semantics. Resources are cached according to the selected cache mode and server-provided cache headers.

Supported cache modes:

- `ttl` — uses the server-defined cache lifetime (`Cache-Control`)
- `revalidate` — performs conditional requests using validators such as `ETag` and `Last-Modified`
- `session` — keeps resources during the lifetime of the SDK instance

The SDK does not bypass HTTP cache validation. Expired resources are refreshed according to the configured mode to prevent serving outdated data indefinitely.

A custom cache implementation can be provided by implementing the `Cache` protocol. This allows applications to integrate their own storage solutions, such as databases, filesystem caches or distributed cache systems.

The cache interface requires the following operations:

- retrieve a cached resource state
- store a resource state
- delete a resource
- clear the cache
- report the current cache size

## Requirements

- Python 3.12+
- httpx 0.28+

## License

**Copyright © 2026 RTBNext**  
Created and maintained by [Paul Köhler](https://komed3.de) (komed3).  
Licensed under the [MIT License](./LICENSE).
