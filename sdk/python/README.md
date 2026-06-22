
# Vantiq SDK for Python

The [Vantiq](http://www.vantiq.com) Python SDK is a Python package that provides an 
API into a Vantiq system from Python applications.  The SDK connects to a
Vantiq system using the 
[Vantiq REST API](https://dev.vantiq.com/docs/system/api/index.html).

## Installation

The SDK is installed from the PyPI repo.  To install this into your system,
use
```commandline
    pip install vantiqsdk
```

Note: depending on your local environment, you may need to use `pip3`
instead of `pip`, or whatever is appropriate to install into your
virtual environment.

The Vantiq SDK for Python requires Python version 3.10 or better.
It is built using `asyncio`, `aiohttp`, and `websockets`. In the documentation
that follows, methods marked as _Async_ must be awaited. For more information
about `asyncio` and `await`, please see the 
[Python `asyncio` documentation](https://docs.python.org/3/library/asyncio.html)).

## Quick Start

You will need valid credentials on a Vantiq server in the form of a
username and password or access token.  If you have a private Vantiq server,
contact your administrator for credentials.  If you wish to use the
Vantiq public cloud, contact [support@vantiq.com](mailto:support@vantiq.com).

The first step is to create an instance of the Vantiq SDK providing the URL of the Vantiq server to connect:

```python
from vantiqsdk import Vantiq, VantiqResources, VantiqResponse
import vantiqsdk

server: str = "https://dev.vantiq.com"

vantiq: Vantiq = Vantiq(server)
```

where `server` is the full URL for the Vantiq server to connect to, such as *https://dev.vantiq.com/*. 
An optional second argument is the version of the API to connect to. 
If not specified, this defaults to the latest version, currently *1*. 
At this point, the *Vantiq* instance has not yet connected to the server.  
To establish a connection to the server, use the `authenticate` method, e.g.,

```python
username = "joe@user"
password = "my-secr3t-passw0rd!#!"

await vantiq.authenticate(username, password)
```

The `username` and `password` are the same credentials used to log into the system.
Note the username and password are not stored either in-memory or persistently after
this authentication call.  After successfully authenticating with the system,
the *Vantiq* instance stores an in-memory access token that subsequent API calls
will use.

Now, you are able to perform any SDK calls to the Vantiq server.  The async methods
on the SDK classes can be immediately awaited to run in, effectively, a synchronous
fashion, or they can return an `Awaitable` that can be _awaited_ later.

```python
vr: VantiqResponse = await vantiq.select(VantiqResources.TYPES)

```

Alternatively,

```python
to_await = vantiq.select(VantiqResources.TYPES)
...
vr: VantiqResponse = await to_await
```

In either case, the response to the operation is available
in the VantiqResponse instance.

## Documentation

For the full documentation on the SDK, see the
[SDK API Reference](https://github.com/Vantiq/vantiq-python-sdk/blob/master/docs/api.md).

## Developers

The project is set up as a `gradle` project.  To run the tests, use

```commandline
./gradlew test
```

or

```commandline
gradlew.bat test
```

in a windows environment.

The tests run will run a mocked version. To execute tests against a _live_ server,
define the following gradle properties in your ~/.gradle/gradle.properties file:

```properties
# Python project values
TestVantiqServer=<Vantiq server url> # Only do the base URL. Ex http://localhost:8080/
TestAccessToken=<access token from that Vantiq system>
TestVantiqUsername=<Vantiq user name>
TestVantiqPassword=<Password for that Vantiq user>
```

Alternatively, when running directly, use the following environment variables:

```commandline
VANTIQ_URL <Vantiq erver url>
VANTIQ_ACCESS_TOKEN <Access token from that Vantiq system>
VANTIQ_USERNAME <Vantiq user name>
VANTIQ_PASSWORD <Password for that Vantiq user>
```

## Copyright and License

Copyright &copy; 2022 Vantiq, Inc.  Code released under the
[MIT license](https://github.com/Vantiq/vantiq-python-sdk/blob/master/LICENSE.txt).
