# Vantiq SDK for Python

This package contains the Vantiq  SDK for the Python language.

The SDK consists of the following classes

* `Vantiq` -- this is a class handling the client's interaction with the Vantiq system
* `VantiqError` -- structured errors returned from Vantiq
* `VantiqException` -- Exception raised from Vantiq when necessary
* `VantiqResponse` -- Structured resposne from Vantiq operations
* `VantiqResources` -- Names for Vantiq resources that may be used in for Vantiq operations

The Vantiq SDK is built atop the asyncio-based aiohttp. Consequently, operations marked as async must be awaited.
See [the Python asyncio documentation](https://docs.python.org/3/library/asyncio.html) for more details.
The [Coroutines and Tasks documentation](https://docs.python.org/3/library/asyncio-task.html) has examples of
_asyncio_ Python programs.

Note that some Windows environments may require the setting of the _event loop policy_.
Please see [asyncio policy documentation](https://docs.python.org/3/library/asyncio-policy.html) for details.

## VantiqResources

Defines the set of Vantiq Resources

More details about these resources can be found in the
[Vantiq Resource Reference Guide](https://dev.vantiq.com/docs/system/resourceguide/index.html).

The following constants are defined for these Vantiq system resources.

* AUDITS 
* CATALOGS 
* CLIENTS
* COLLABORATIONS
* COLLABORATION_TYPES
* CONFIGURATIONS
* DESIGN_MODELS
* DISCUSSIONS
* DOCUMENTS
* EVENT_GENERATORS
* GENAI_FLOWS
* GROUPS
* K8S_CLUSTERS
* K8S_INSTALLATIONS
* LLMS
* NAMESPACES 
* NODES
* ORGANIZATIONS 
* PROCEDURES
* PROFILES
* PROJECTS 
* RULES
* SCHEDULED_EVENTS
* SECRETS
* SEMANTIC_INDEXES
* SERVICES
* SERVICE_CONNECTORS
* SOURCES
* SOURCE_IMPLS 
* STORAGE_MANAGERS
* SUBSCRIPTIONS
* SYSTEM_MODELS
* TESTS
* TEST_REPORTS
* TEST_SUITE_REPORTS
* TEST_SUITES
* TOKENS
* TOPICS
* TRACKING_REGIONS
* TYPES
* USERS


## VantiqError

Contains an error from the Vantiq system.


A VantiqError contains three (3) properties:

* _code_ : str -- The short string identifying the error
* _message_ : str -- The message template for the errors
* _params_ : list -- The parameters for the message template.

Message templates look and behave like strings for which the Python format() can supply values.
_E.g._,

```python
VantiqError("io.vantiq.python.short.code",
             "This is an error parameterized by an argument: {0}",
             ["an argument"])
```

<a name="VantiqException"></a>
## VantiqException(RuntimeError)
Contains an exception from the Vantiq system.

A VantiqException is a RuntimeError and contains three (3) properties:

* _code_ : str -- The short string identifying the error
* _message_ : str -- The message template for the errors
* _params_ : list -- The parameters for the message template.

Message templates look and behave like strings for which the Python format() can supply values.

## VantiqResponse

A response from a Vantiq operation

A Vantiq response contains information returned from a Vantiq operation. This information is represented by the following properties:

* _is_success_ : bool -- Did the operation succeed
* _content_type_ : str -- The content type of the message returned.  Usually 'application/json'.
* _count_ : int -- Where applicable, the number of items returned for a successful operation.  This is generally available after a count() or delete() operation.
* _errors_ : list -- A list of VantiqError entries outlining a failed operation
* _body_ : list | dict | StreamReader -- The results of the operation.


## Vantiq
The interface for working with the Vantiq System.

This class consists of operations that can be performed using the Vantiq system. More information about these operations can be found in the 
[Vantiq Resource Reference Guide](https://dev.vantiq.com/docs/system/resourceguide/index.html)
and the [Vantiq API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html) .

Logging for this class can be configured using a `logging.ini` file that is present in the working directory of the running program.

The Vantiq object instance can be used as a context manager.

```python
async with Vantiq(<server url>) as client:
    resp: VantiqResponse = client.select(VantiqResource, ...)
```

As noted, most of the operations in the Vantiq object are `async` and must be awaited for them to run. See [the Python Asyncio documentation](https://docs.python.org/3/library/asyncio.html)
for more details about working with async operations.

### Vantiq Object

Create a Vantiq client object.

#### Parameters

* _server_ : str -- URL String at which to find the Vantiq Server
* _api_version_ : str (optional) -- Version of the API to use. Defaults to '1'
* ... : After the _api_version_ parameter, you can provide a list of keyword arguments. These will be passed to the
        `aiohttp.client.ClientSession` connection's `get()`, `post()`, `put()`, and `delete()` calls and,
         in the case of a subscription, the `websockets.connect()` call. This allows a caller to modify the connection
         as required.  A typical use case would be for disabling SSL certificate checking for test environments using
         self-signed certificates.

#### Returns
    Vantiq object with which to interact with the Vantiq system.

The Vantiq object can be used as a context manager.

#### Examples

Context manager

```python
async with Vantiq('https://dev.vantiq.com') as client:
    ...
```

Or, in a client object:

```python
    client = Vantiq('https://dev.vantiq.com')
    ...
    await client.close()
```

Or, in a client object with SSL checking disabled:

```python
    client = Vantiq('https://dev.vantiq.com', 1, ssl=False)
    ...
    await client.close()
```

### Vantiq.connect() (async)

Make the connection to the Vantiq server

#### Parameters
No parameters required
#### Returns
None
#### Raises
`VantiqException`

#### Notes
Should precede the [Vantiq.authenticate()](#authenticate) call. 
If this is not done before the [Vantiq.authenticate()](#authenticate) or
[Vantiq.set_access_token()](#set_acess_token) call,
it will be done automatically.

### Vantiq.get\_server()

#### Returns
Returns the server url used for this connection.

### Vantiq.get\_api\_version()
#### Returns
Returns the API version used for this connection.

### <a name="set_access_token" id="set_access_token"></a>Vantiq.set\_access\_token() (async)
Set the access token for server access.

Access to the Vantiq server is controlled.  Access can be granted by using an access token (recommended) or a username and password.

#### Parameters

* _access_token_ : str -- Access token to be used to gain access to the Vantiq system

        
### Vantiq.get\_access\_token()
#### Returns
Returns the access token currently in use.
        
### Vantiq.set\_username()
Set the username to be used to access the Vantiq server

#### Parameters

* _username_ : str -- user name to be used to gain access to the Vantiq system

### Vantiq.get\_username()
#### Returns
Returns the username currently in use.
        
### Vantiq.is\_authenticated()

#### Returns
Returns a boolean indicating whether this Vantiq instance is authenticated.

### Vantiq.authenticate() (async)

(Async) Use a username and password to connect to the Vantiq system.

#### Parameters

* _username_ : str -- The username to be used to authenticate to the Vantiq server.
* _password_ : str -- The password to be used to authenticate to the Vantiq server.

#### Raises
`VantiqException`

#### Example
```python
 await client.authenticate('vantiquser', 'secret')
```

### Vantiq.refresh() (async)
Refresh the access token with the Vantiq Server.

        
### Vantiq.close() (async)
End the Vantiq session

        
### Vantiq.select() (async)

Return items from a Vantiq resource.

Select specific items from a Vantiq resource. Selection and details of the return are controlled
by the parameters.

#### Parameters

* _resource_ : str -- The name of the resource to be returned.  System resource names are provided via the VantiqResource class.
* _properties_ : list(str) -- (optional) The list of properties for the resource to be returned. If missing, return all properties.
* _where_ : dict(str: \*) -- (optional) The "where clause" to be used to restrict the selection.  The contents is defined in the [API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html).
* _sort_spec_ : dict(str: int) -- (optional) Defines the sort order of the returned values.  The key name defines the property on which to sort, and the value determines the order
(1 = ascending, -1 = descending).  See the [API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html) for details.
* _limit_ : int -- (optional) Limit the number of records returned
* _options_ : dict (str, \*) -- (optional) Additional query parameter options

#### Returns

`VantiqResponse`

#### Examples
```python
vr: VantiqResponse = await client.select('myType')
if vr.is_success:
    ...
...
```

### Vantiq.select\_one() (async)
Select a single item from a Vantiq resource

#### Parameters
    
* _resource_ : str -- The name of the resource from which to select.
* _resource_id_ : str -- The identifier for the specific item within the resource.

#### Returns

`VantiqResponse`

#### Example

```python
vr: VantiqResponse = await client.select_one('myType', 'type name')
if vr.is_success:
    ....
...
```
   
### Vantiq.delete() (async)

Delete item(s) from a Vantiq resource.

### Parameters:

* _resource_ : str -- The name of the Vantiq resource from which to delete items
* _where_ : dict (str: \*) -- The "where clause" to be used to determine which items to delete. The contents is defined in the [API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html). Note that if `where` is None, this will delete all objects in the resource type.

#### Returns
`VantiqResponse`

The count property of the VantiqResponse will provide the number of objects deleted.

#### Examples

```python
vr: VantiqResponse = await client.delete('myType', {'name': 'some name'}
if vr.is_success:
    print('Count of items deleted: ', vr.count)
```
### Vantiq.delete\_one() (async)
Delete a single item from a resource.

#### Parameters

* _resource_ : str -- The name of the Vantiq resource from which to delete.
* _resource_id_ : str -- The key for the item to delete.

#### Returns

`VantiqResponse`


### Vantiq.insert() (async)
Insert an item into Vantiq Resource.

#### Parameters

* _resource_ : str -- Name of the Vantiq resource into which to insert.
* _instance_ : dict -- The values to be inserted.  The key names in the _instance_ parameter 
must match the property names in the Vantiq object.

#### Returns

`VantiqResponse`


### Vantiq.upsert() (async)

Upsert an item into Vantiq Resource.

#### Parameters

* _resource_ : str --  Name of the Vantiq resource into which to upsert.
* _instance_ : dict -- The values to be upserted.   The key names in the _instance_ parameter 
must match the property names in the Vantiq object.

#### Returns

`VantiqResponse`

### Vantiq.update() (async) 

Update an item in a Vantiq Resource.

#### Parameters

* _resource_ : str -- Name of the Vantiq resource in which to update.
* _resource_id_ : str -- The key of the record to look up for replacement.  The _id property can be used.
* _instance_ : dict -- The values to be updated.  The key names in the _instance_ parameter 
must match the property names being updated in the Vantiq object.

#### Returns

`VantiqResponse`

### Vantiq.download() (async)
Download content from a Vantiq Document, Image, Video, or TensorflowModel.

#### Parameters

* _path_ : str -- The path from which to obtain the data. This is found in the `content` field of the base object.

#### Returns

`VantiqResponse`. In this case, the response's `body` field is an `aiohttp.StreamReader` that can be used to fetch the content returned.

#### Examples

```python
vr: VantiqResponse = await client.select_one(VantiqResources.DOCUMENTS, 'mydoc')
mydoc = vr.body
if vr.is_success:
    download_vr: VantiqResponse = await client.download(mydoc.content)
    if download_vr.is_success:
        reader = download_vr.body
        while True:
            data = await reader.read(100)  # Read our data 100 bytes at a time
            if len(data) == 0:
                break
            # Do something with the data
            ...
```

### Vantiq.upload() (async) 
Upload a file (or in-memory data), creating a object to hold that data.

This allows the upload of a file to create a document, image, video, or tensorflow model.

#### Parameters
   
* _resource_ : str -- The Vantiq resource type to create.
* _content_type_ : str -- The type of data contained in the file.  This will be set as the `contentType` of the resulting object.
* _filename_ : str -- The name of the file to upload.
* _doc_name_ : str -- (optional) The name of the object to create. If this is missing, use the filename.
* _inmem_ : str | bytes | bytearray -- (optional) Content to be uploaded.  Used when the content is contained in memory.
When this value is present (and not None), `filename` or `doc_name` can be used to name the resulting
Vantiq Document. Providing both `filename` and `doc_name` in this case is an error.

#### Returns
`VantiqResponse`

### Examples
```python
vr: VantiqResponse = await client.upload(VantiqResources.DOCUMENTS, 'image/png', 'path/name.png')
if vr.is_success:
    # Here, we will have uploaded a file named `path/name.png`,
    # and created a Document named `path/name.png`.

vr: VantiqResponse = await client.upload(VantiqResource.DOCUMENTS, 'text/plain', None,
                                         'my document', 'some content for my document')
if vr.is_success:
    # Here, we will have created a document named 'my document' with the content
    # 'some content for my document'

```

### Vantiq.count() (async)
Return the number of items in a Vantiq resource that satisfy the where clause

#### Parameters:

* _resource_ : str -- The name of the resource to be counted.  System resource names are provided via the VantiqResource class.
* _where_ : dict(str: \*) -- (optional) The "where clause" to be used to restrict the counting.  The where clause is defined in the [API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html).

#### Returns

`VantiqResponse` --  where the `count` field contains the count requested.

#### Vantiq.query() (async) 

Send a query message to a Vantiq source

#### Parameters

* _source_id_ : str --  Name of the source to which to send the query
* _query_ : dict | List[dict] -- The message describing the query to be sent.  These messages are source specific.

#### Returns

VantiqResponse indicating the success or failure of the query.  The body field will contain the results of the query (if applicable).


### Vantiq.execute() (async)

Execute a Vantiq procedure.

#### Parameters:

* _procedure_id_ : str -- The name of the procedure to execute.
* _params_ : dict -- The parameters provided for the procedure's execution.  The key names are the parameter names, and the values their values.

#### Returns
`VantiqResponse` where the body contains the results of the procedure execution, if any.


### Vantiq.publish() (async)

Publish a message to a Vantiq Service, Source, or Topic.

#### Parameters

* _resource_ : str --  The resource to which to publish.  Must be either VantiqResources.SERVICES, VantiqResources.SOURCES, or VantiqResources.TOPICS.
* _resource_id_ : str -- The specific service, source, or topic to which to publish.
* _msg_ : dict -- The message to publish

#### Returns
`VantiqResponse`

### Vantiq.get\_namespace\_users() (async)

Returns an array containing objects which map between "username" and "preferredUsername"

#### Parameters:

* _namespace_ : str -- The name of the namespace from which to get the list of users.
 
#### Returns:

`VantiqResponse`


### Vantiq.start\_subscriber\_transport() (async) 

Start a task to handle subscriptions.

To handle incoming messages from the Vantiq server that arise from subscriptions, you must start an
asyncio task to do this work.  This method does that work.

If the transport does not exist when subscribe() is called, subscribe() will start
the transport on your behalf.

#### Parameters

(none)

#### Returns
The task created. Can be used to wait or manage that task.

If the subscriber connection already exists, None is returned as there is no new task.
    

### Vantiq.subscribe() (async)

Subscribe to an event from the Vantiq server, specifically to a specific topic, source, or type event.

For sources, this will subscribe to message arrival events.  The name of the
source is required (_e.g._, `MySource`).

For topics, this will subscribe to any messages published on that topic.  The
name of the topic is required (_e.g._, `/some/topic`).

For services, this will subscribe to any messages published to the named service event. The name of the
service and service event is required, and should be passed into the resource id as service_name/event_name.

For types, this will subscribe to the specified type event.  The name of the
type and the operation (_i.e._, `insert`, `update`, or `delete`) are required.

#### Parameters
 
* _resource_ : str -- The resource type for which this subscription is being made
* _resource_id_ : str -- The identifier of the specific instance of the `resource` in question.
* _operation_ : str -- The operation to which to subscribe when subscribing to a VantiqResources.TYPES event. Should be `None` for other resource types.
* _callback_ : Callable[[str, dict], Awaitable[None]] -- A callback function to call when a subscribed event arrives. The callback will be called with the
type of the callback (`connect`, `message`, `error`) and the message contents.
<br><br>
The callback message contains the following properties:

    * _status_ : int -- the status of the event
    * _contentType_ : str -- the content type of the message
    * _path_ : str -- the event specification
    * _value_ : dict -- the value of the event (type inserted, topic contents, etc.)
    
* _params_ : dict -- (optional) Parameters for the subscription. May be subscription dependent,
but can usually be ignored.


#### Returns

`VantiqResponse`

For details, see the [API Reference Guide](https://dev.vantiq.com/docs/system/api/index.html).

### Vantiq.ack() (async)

Acknowledge the receipt of a reliable message from reliable resources after creating a persistent subscription.

#### Parameters 

* _request_id_ : str -- id of the request. This can be found in the 'X-Request_id' header of the callback for the subscription
* _subscription_id_ : str -- id of the subscription that delivered the message. This is found in the `[body][name]` field of the callback for the subscription message.
* _msg_ : dict -- message being acknowledged.  This should be the `[body]` field of the message (`value` field) delivered to the subscription callback.
        
#### Raises:

`VantiqException`

### Vantiq.register_subscriber\_on\_close()

Register a callback to be called when the subscriber is closed. Useful for the subscriber to know that there's no
longer any subscriber active (for whatever reason).  This could happen due to issues at the server side or with the
connection between the client & server.

#### Parameters:
* _callback_ : Callable[[], Awaitable[None]]
        The callback to be called when the subscriber is closed. This call can be made at most once per subscriber.
