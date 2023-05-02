# Metis API client

[![DOI](https://zenodo.org/badge/563802198.svg)](https://doi.org/10.5281/zenodo.7693569)
[![PyPI](https://img.shields.io/pypi/v/metis_client.svg?style=flat)](https://pypi.org/project/metis-client)

<p align="center"><img src="https://github.com/tilde-lab/metis.science/blob/master/src/assets/img/metis.svg" width="300" height="300" /></p>

This library allows for programmatic interactions with the [Metis infrastructure](https://metis.science).

## Installation

`pip install metis_client`

## Usage

There are two client flavors - asyncronous `asyncio` client
and simplified synchronous client.

### Asynchronous client

There is a asynchronous client `MetisAPIAsync`. Example of usage:

```python
from metis_client import MetisAPIAsync, MetisTokenAuth

async def main():
    async with MetisAPIAsync(API_URL, auth=MetisTokenAuth("admin@test.com")) as client:
        print(await client.v0.auth.whoami())
        data = await client.v0.datasources.create(content)
        results = await client.v0.calculations.create_get_results(data["id"])
        print(resuls)
```

See `examples` directory for more examples.

### Synchronous client

There is a synchronous client `MetisAPI`. Example of usage:

```python
from metis_client import MetisAPI, MetisTokenAuth

client = MetisAPI(API_URL, auth=MetisTokenAuth("admin@test.com"))
data = client.v0.datasources.create(content)
results = client.v0.calculations.create_get_results(data["id"])
print(results)
```

## License

Author Sergey Korolev, Tilde Materials Informatics

Copyright 2023 BASF SE

BSD 3-Clause
  * [ ] 
