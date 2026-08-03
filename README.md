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

