# Vantiq Catalog API Reference Guide

This guide covers the publicly available interfaces to the Vantiq Catalog. For more information on the Catalog, Vantiq's 
Intelligent Advanced Event Broker, and the Service Catalog please refer to the [Catalog Reference Guide](broker.md).

## Overview
The Vantiq IDE makes it easy to define entries as well as publish and subscribe to entries in the Catalog. When building
applications outside of the Vantiq Platform that depend on the Event Catalog, these convenient
interfaces in the IDE are not available. The same functionality can be achieved by operations on the catalogs resource.

Vantiq provides the following publicly available SDKs:

* [Node.js](https://github.com/Vantiq/vantiq-sdk-node)
* [iOS](https://github.com/Vantiq/vantiq-sdk-ios)
* [Java](https://github.com/Vantiq/vantiq-sdk-java)

If your application development environment cannot support any of the above SDKs, it's always possible to 
interact with the Catalog directly though the [Vantiq REST API](api.md).

## Catalog Operations

Many of the interactions with a catalog occurs through special operations defined for the catalog resource. All of these
operations act on the "system.catalogs" resource and require the resourceId (*name*) to be specified. When using the 
[REST API](api.md#rest-over-http-binding) for the special operations the HTTP method is POST
and the body must be formatted as `{"op": <operation>, "data": <data object>}`. Any calls using 
[remote processing](rules.md#distributed-processing) must have the object formatted in the same way. For all 
other cases and bindings, treat the op and object normally. 

### Host Catalog

Hosting a catalog is done by creating or updating a catalog resource with the *host* field set to true. The *allowEdge* field may also be set, a Boolean indicating whether the catalog will accept edge connections.

### Unhost Catalog

Unhosting a catalog is done by deleting the catalog instance with *host* set to true. This will delete all hosted events,
services, and assemblies, then disconnect all members.

### Connect to Catalog

Connecting to a catalog is done with the standard UPSERT operation, with the body containing the following properties.
Any additional fields are ignored when a connection is created.

* `accessToken` -- An access token from the catalog namespace. It must have sufficient permissions in the catalog namespace, i.e. admin permissions.
* `uri` -- The uri of the Vantiq installation containing the target catalog.
* `useVQS` -- A Boolean indicating whether the catalog should treat this namespace as an edge node. If not provided, it will be treated as `false`

The response for this upsert is not the created instance, but is instead the JSON object with the following properties.

* `name` -- The name of the catalog.
* `managerNode` -- The definition of the node used to connect to the catalog.
* `selfNode` -- The definition of the node used by the catalog to connect back to the member namespace.

### Disconnect from Catalog

Disconnecting a member from a catalog is done by deleting the catalog instance in the member namespace, or the catalog
member instance in the catalog namespace. This will unregister the member from all entries and remove the connection to
the catalog.

### Create Entry

* `op` -- "createEntry"

Creates an entry in the catalog, to which members can publish or subscribe. The body's format depends on the type of the
entry. Currently only Event and Assembly entries can be created this way.  Services cannot be created through
this operation, and instead must be created by registering as a publisher.

Event type entries have the following properties in the body of createEntry:

* `type` -- "event"
* `name` -- The name of the event. Must begin with the "/" character.
* `schema` -- The schema definition to be used for the event.
* `description` -- Optional. A description of the event.
* `isReliable` -- Optional. Whether the event uses [reliable messaging](reliability.md#reliable-messaging-in-vantiq). Defaults to false.
* `ars_group` -- Optional. Restricts visibility of this event to the specified group. Can only be set by the host namespace. Defaults to null, i.e. visible to all member namespaces.
* `ars_properties` -- Optional. An arbitrary JSON object, typically used in where clauses or to hold extra information. If the "tags" field is set to an array of strings, the Modelo UI will consider those strings when filtering events.

Assembly entries have the following properties in the body of createEntry. Note that some publish validations cannot be performed in this case, so a successful creation does not mean that the Assembly and its resources can be successfully installed.

* `type` -- "assembly"
* `name` -- The name of the assembly to be created. An Assembly with this name must exist inside the provided zip.
* `fileName` -- The name of the Document holding the zipped resources. The contents of the zip must be formatted like an export, and supports directly using the UI export and using a zipped CLI project export. Each resource file must be stored in either `<resource name>/<file>` or `<single folder>/<resource name>/<file>`, and the two formats must not be mixed in the same zip file.

### Remove Entry

* `op` -- "removeEntry"

Removes an entry from the catalog. By default, only the host has permissions to remove event entries. The body must be a JSON object
with the following properties:

* `type` -- The type of the entry.  Currently either `event`, `service`, or `assembly`.
* `name` -- The name of the entry.

### Register

* `op` -- "register"

Register as a publisher or subscriber for an entry. The body is a JSON object with the properties detailed below. The response is the given
entry with an additional *error* field if an error occurred while registering, or an error if the provided entry has an 
invalid format. Unless the entry has an invalid format, the entry is added to *requestedEntries* regardless of success.

Event entries are registered with the following properties:

* `type` -- "event"
* `operation` -- "publish" or "subscribe"
* `name` -- The event's name.
* `localName` -- For the "subscribe" operation only. The topic that will receive the events, e.g. "/my/subscribing/topic".
* `localEvent` -- For the "publish" operation only. The resource that will send the events, e.g. "/topics/my/publishing/topic" or "/sources/myPublishingSource".

Service entries are registered with the following properties:

* `type` -- "service"
* `operation` -- "publish" or "subscribe"
* `name` -- The service's name.
* `changeLog` -- For the "publish" operation only. A String describing the change from the previous version. This isn't stored in `requestedEntries`.

Assembly entries are registered with the following properties:

* `type` -- "assembly"
* `operation` -- "publish" or "install"
* `name` -- The assembly's name.
* `description` -- For the "publish" operation only. A description for the entry. This isn't stored in `requestedEntries`.
* `changeLog` -- For the "publish" operation only. A String describing the change from the previous version. This isn't stored in `requestedEntries`.
* `configuration` -- For the "install" operation only. A configuration for the assembly, in the same format as for 
  [Assembly Configurations](resourceguide.md#assembly-configurations). This isn't stored in `requestedEntries`.

### Unregister

* `op` -- "unregister"

Unregister from an entry. The body is a JSON object in the same format as the register operation. The response is the given
entry with an additional *error* field if an error occurred while unregistering, or an error if the provided entry has an 
invalid format. If the entry was in *requestedEntries*, it is removed from that list regardless of success.

### Resolve

* `op` -- "resolve"

Attempt to complete registration for any unresolved entries in *requestedEntries*. The response is an array of all
entries that failed to resolve with an additional *error* field in each, in the format of the response for the
[register](#register) operation. No body is required.

### Repair Catalog

* `op` -- "reconnect"
* `accessToken` -- An access token that can be used to connect to the catalog. Optional. If not provided, the repair will assume that the catalog connection is valid and will fail if not.
* `uri` -- The uri of the catalog. Optional. If `accessToken` is not provided, this field is ignored. If not provided, the repair will try to find the existing catalog node and use its uri.

Attempt to repair all connections to the catalog and relevant catalog members. Note that this will update all Services and Event Types as part of the process.

## Catalog Procedures
The helper procedures to interact with the Catalog are organized into 3 services:

* **Broker** - procedures for interacting with the Catalog or the Catalog Namespace
* **Publisher** - procedures for adding and removing a publisher in a Catalog Member namespace.
* **Subscriber** - procedures for adding and removing a subscriber in a Catalog Member namespace.

Most of the Broker procedures can only be run in the context of the Catalog Namespace and not from a Catalog Member 
Namespace. To use these Broker procedures from a Member namespace, there are a couple options, all of which rely on
using the node defined in the Member Namespace that points to the Catalog Namespace.

* Execute the procedure in a VAIL rule or procedure using [PROCESSED BY](rules.md#execute)
* Switch the token used by the SDK to be the token found in the node pointing from the Member Namespace to the Catalog 
Namespace.
 
## Broker Service
Use the procedures in the Broker service to connect to and disconnect from a Catalog Namespace, fetch Event Types from 
the Catalog, and to create new Event Types in the Catalog.

### Managing Catalog
* **Broker.createCatalog(name, allowEdge)** - Makes the current namespace into the manager of a Catalog Namespace. This is identical to
performing the upsert described in [Host Catalog](#host-catalog). If *name* is provided then the created catalog will use that value, otherwise it will call `Broker.makeNodeName()` and use the result as the name. If *allowEdge* is set to true, it will allow edge members to connect and will allow the catalog namespace to be used as a bridge between edge nodes.
* **Broker.removeManager()** - Disconnects all Catalog Members from all Catalog entries, severs the connection to each,
and makes the current namespace no longer a Catalog Namespace. This is identical to deleting a hosting catalog object.
* **Broker.createSharedCatalog(catalogName, uri, token)** - Creates a [Public Catalog](broker.md#public-catalogs). Can only be run in an Organization or System namespace.

### Managing Catalog Connections
* **Broker.connect(token, uri, useVQS)** - Connect the current namespace to a Catalog Namespace. The URI is
the URI where the Catalog Namespace is defined and the token is an Access Token created by an administrator of the
Catalog Namespace that will grant the user access to the Catalog Namespace. *useVQS* is a Boolean that specifies if the connection should be treated as an edge connection. Not all catalogs support this option. This is identical to performing the upsert described in [Connect to Catalog](#connect-to-catalog).
* **Broker.connectToSharedCatalog(catalogName, isOrg, useVQS)** - Connects to the specified Public Catalog. The names can be obtained from the resource *system.sharedcatalogs*. The *isOrg* parameter is a Boolean that indicates whether the Public Catalog is from the current Organization or not, in which case it's from the System namespace. It should be true if the desired catalog has the *organization* field set to a non-null value, false otherwise. *useVQS* is a Boolean that specifies if the connection should be treated as an edge connection. Not all catalogs support this option.
* **Broker.disconnect(catalogName)** - Disconnect a catalog member from a Catalog. This can only be called
from within a Catalog Member namespace (not a Catalog Namespace). The catalogName should be the name of the Catalog
resource. This is identical to deleting a connecting catalog object.

### Custom Operations

These are wrappers for the custom operations described in [Catalog Operations](#catalog-operations). 

* **Broker.createEntry(catalogName, type, entry)** - *type* is the type of the new entry and *entry* is an Object
containing all the other values required for creating an entry. This can be called in a member namespace or a catalog namespace.
* **Broker.createAssembly(catalogName, assemblyName, zipFileName)** - *assemblyName* is the name of the assembly in the provided zip. *zipFileName* is the name of the Document that holds the assembly and its resources. This is identical to performing the [createEntry](#create-entry) operation for an Assembly.
* **Broker.removeEntry(catalogName, type, entry)** - *type* is the type of the entry to be removed and *entry* is an Object
containing all the other values required for removing an entry. This can be called in a member namespace or a catalog namespace.
* **Broker.registerEntry(catalogName, type, operation, entry)** - Registers the current namespace to a given entry. *type* and 
*operation* are the type of entry and operation for which you are registering. *entry* is an Object containing all the
other values required for registering this type and operation, as seen in [Register](#register). This procedure calls 
the register entry operation, and if the result has the *error* field it throws the exception.
* **Broker.unregisterEntry(catalogName, type, operation, entry)** - Unregisters the current namespace to a given entry. *type* and 
*operation* are the type of entry and operation for which you are registering. *entry* is an Object containing all the
other values required for unregistering this type and operation, as seen in [Register](#register). This procedure calls
the unregister entry operation, and if the result has the *error* field it throws the exception.
* **Broker.resolve(catalogName)** - Attempts to complete registration for all unresolved entries in the given catalog's
*requestedEntries*. This calls the resolve operation.

### Managing Event Types
* **Broker.getAllEvents(catalogName)** - Fetch the complete Event Catalog from the Catalog Namespace. The catalogName 
should be the name of the Catalog resource for the catalog.
* **Broker.getAllServices(catalogName)** - Fetch the complete Service Catalog from the Catalog Namespace. The catalogName
should be the name of the Catalog resource for the catalog.
* **Broker.getAllAssemblies(catalogName)** - Fetch the complete Assembly Catalog from the Catalog Namespace. The catalogName
should be the name of the Catalog resource for the catalog.
* **Broker.getAllSemanticIndexes(catalogName)** - Fetch the complete Semantic Index Catalog from the Catalog Namespace. The catalogName should be the name of the Catalog resource for the catalog.
* **Broker.deleteEvent(name)** - Delete an event type by **name** from the catalog and remove all publishers and subscribers. 
Broker.deleteEvent can only be invoked from the Catalog Namespace. This is identical to performing the [Remove Entry](#remove-entry)
operation for events in the catalog namespace.

### Utilities
* **Broker.makeNodeName(namespace, uri)** - Creates the default name for a catalog. Both parameters are optional,
defaulting to the local namespace and the local uri respectively. The name appends the uri and the namespace name, with
illegal characters replaced by underscores. For example, with the uri "http://api.vantiq.com" and namespace "myCatalog"
the name would be "api_vantiq_com_myCatalog".
* **Broker.isManager(catalogName)** - Determine if there is a catalog with the given name.  The catalogName
should be the name of the Catalog resource for the catalog, and the procedure will return true if the namespace
targeted by the node hosts a Catalog.

## Publisher Service
Use the Publisher service to register and remove a namespace as a publisher of an Event Type in a Catalog, or to publish,
update, or remove a Service or Assembly. These procedures must be invoked in the Publisher Namespace.
These are all wrappers for the register and unregister operations.

* **Publisher.addEventPublisher(name, localEvent, catalogName)** - Register the current namespace as a publisher of the Event
Type identified by **name** in the Catalog **catalogName**. Use the **localEvent** event path 
(e.g: `/sources/MySource` or `/topics/my/topic`) in the current namespace as the source of the events, and begin
forwarding all events from the **localEvent** path to all subscribers of the Event Type.
* **Publisher.removeEventPublisher(name, localEvent, catalogName)** - Undo the registration of a Publisher in the current 
namespace and stop forwarding events from the **localEvent** path to subscribers. Events will still continue to occur 
locally in the current namespace.
* **Publisher.publishService(serviceName, catalogName, changeLog)** - Add the service **serviceName** to the Catalog
**catalogName** with the current namespace as the publisher. All public procedures in the service will be published. **changeLog** is an optional String to inform subscribers of the changes since the last update.
* **Publisher.updatePublishedService(serviceName, catalogName, changeLog)** - Update the Catalog **catalogName** about 
changes to the Service **serviceName**. The current namespace must be the publisher of the Service to succeed. Does not update any 
subscribers, they must update themselves. This is equivalent to registering as publisher for a service you have already published. **changeLog** is an optional String to inform subscribers of the changes since the last update.
* **Publisher.removeServicePublisher(serviceName, catalogName)** - Removes the Service from the Catalog 
**catalogName** and makes the subscriber's copies stop working. The current namespace must be the publisher
of the Service in order to succeed.
* **Publisher.publishAssembly(assemblyName, catalogName, description, changeLog)** - Add the assembly **assemblyName** to the Catalog
**catalogName** with the current namespace as the publisher. This is also used to update already published assemblies. **changeLog** is an optional String to inform subscribers of the changes since the last update.
All resources in the assembly will be stored in a zip file in the catalog. If provided and non-null, **description**
will set the entry's description.
* **Publisher.removeAssemblyPublisher(assemblyName, catalogName)** - Removes the assembly from the Catalog 
**catalogName**. The current namespace must be the publisher of the assembly in order to succeed. Any existing
subscribers will keep their copies of the resources.
* **Publisher.publishSemanticIndex(indexName, catalogName, changeLog)** - Add the semantic index **indexName** to the Catalog **catalogName** with the current namespace as the publisher. This is also used to update already published semantic indexes. **changeLog** is an optional String to inform subscribers of the changes since the last update.
* **Publisher.removeSemanticIndexPublisher(indexName, catalogName)** - Removes the specified semantic index from the Catalog **catalogName**. The current namespace must be the publisher of the semantic index in order to succeed. Any existing subscribers will be unsubscribed.

## Subscriber Service
Use the Subscriber service to register and remove a namespace as a subscriber to an Event Type or Service in a Catalog. These 
procedures must be invoked in the Subscriber Namespace. These are all wrappers for the register and unregister operations.

* **Subscriber.subscribeToEvent(name, localName, catalogName)** - Register the current namespace as a subscriber of the Event 
Type identified by **name** in the Catalog **catalogName**. The events will arrive in the local namespace
on the topic specified by **localName**.
* **Subscriber.unsubscribeFromEvent(name, localName, catalogName)** - Undoes the registration of a subscriber to an Event Type in
the current namespace identified by **name** in the Catalog **catalogName**.
* **Subscriber.subscribeToService(serviceName, catalogName)** - Register the current namespace as a subscriber of 
the Service identified by **serviceName** in the Catalog **catalogName**. Local procedures will be
created named `<service name>.<procedure name>` for each procedure. 
* **Subscriber.updateService(serviceName)** - Update the local version of a Service to what is in the Catalog. Recreates each
procedure and copies any new schema added by the publisher. This is equivalent to registering as a subscriber to a 
service you have already subscribed to.
* **Subscriber.unsubscribeFromService(serviceName)** - Undoes the registration of a subscriber to a Service in
the current namespace identified by **serviceName**.
* **Subscriber.installAssembly(assemblyName, catalogName, configuration)** - Install or update the
the assembly identified by **assemblyName** from the Catalog **catalogName**. If provided and non-null,
**configuration** will be placed in the assembly configuration. All of the assembly's resources will be placed in the
namespace, but they will be hidden unless the publisher intended them to be visible.
* **Subscriber.uninstallAssembly(assemblyName)** - Uninstalls assembly identified by
**assemblyName** from the current namespace. Deletes all resources in the assembly and all its assembly configurations.
* **Subscriber.subscribeToSemanticIndex(indexName, catalogName, qaProcedure, defaultQAModel)** - Subscribe to a semantic index, creating a local version of the index. This is equivalent to registering as a subscriber to a semantic index. It can also be used to update semantic indexes.
* **Subscriber.unsubscribeFromSemanticIndex(indexName)** - Undoes the registration of a subscriber to a semantic index in the current namespace identified by **indexName**.

## Integrating Applications With the Catalog
Below are a few examples of using the SDKs to interact with the Catalog. Every action done with the SDK can be done directly  
through the [REST API](api.md).  

### Authenticate
In Vantiq servers that use OAuth Identity Providers, you cannot authenticate using username and password directly 
through the SDK. You should instead create an Access Token in the IDE for the namespace you wish to connect to, and
set the token on the SDK object to the token obtained through the IDE. For example

```js
// Require the SDK
var Vantiq = require('vantiq-sdk');

// Instantiate an instance of the Vantiq SDK
var vantiq = new Vantiq({
        server:     'https://dev.vantiq.com',
        apiVersion: 1
    });

vantiq.accessToken = <ACCESS TOKEN FROM IDE>

// Now the SDK can be used without further authentication
```

It's recommended that you do not place the access token directly in your source code and instead retrieve the token
from an environment variable or a file on disk to avoid creating unnecessary security risks by exposing the token in 
your source code control system.

Note that all of the below examples assume you have already authenticated into a Vantiq namespace and have either an 
Access Token for making subsequent requests, or the Vantiq SDK object has already gone through the authentication process.

### Fetch All Connected Catalogs
To fetch all catalogs connected to the current namespace, select all catalogs with the following query constraint:
`{"host": {"$ne": true}}`. This constraint expresses that we are only interested in catalogs that are not hosted
locally.

Using the NodeJS SDK, this would look like:

```js
// Note: vantiq is already instantiated and the accessToken has already been set

// Create a promise for the request
var catalogPromise = vantiq.select("system.catalogs", [], {"host": {"$ne": true}});
var catalog;

// Define success and failure behaviors
catalogPromise.then((catalogs) => {
    // catalogs is an array of JSON objects, each containing a catalog
    if (catalogs && catalogs.length > 0) {
        catalog = catalogs[0];
    }
}).catch((err) => {
    // Handle error
});
```

### Fetching Event Types Defined In A Catalog
Assuming the above step fetched a list of nodes that represent the catalogs the current namespace is connected to, 
fetch the list of Event Types in a catalog with the following:

```js
// Note: vantiq is already instantiated and the accessToken has already been set
// Note: assume the catalog variable set in the last step is defined here as well
var catalogName = catalog.name

// Use the SDK to execute the Broker.getAllEvents procedure
var catalogPromise = vantiq.execute("Broker.getAllEvents", {catalogName: catalogName});
var interestingEvent;

// setup success and error handlers for processing the result of the procedure execution 
catalogPromise.then((events) => {
    // events is an array of JSON Objects, each representing an Event Type in the Catalog
    if (events && events.length > 0) {
        interestingEvent = events[0];
    }
}).catch((err) => {
    // Handle error
});
```

### Subscribe To An Existing Event Type
There are 2 parts to subscribing to an Event Type in the Catalog. The first is registering the current namespace as a
subscriber of the Event Type. This tells all registered publishers of the Event Type to forward every instance of the
event to the subscribing namespace. The second part is to open a WebSocket that can receive the events in real-time, as
they are forwarded by the publishers.

```js
// Note: vantiq is already instantiated and the accessToken has already been set
// Note: assume the catalog variable set in the last step is defined here as well
// Note: assume interestingEvent was set to an Event Type fetched in the previous example

// Grab the name of the Event Type from the last step
var eventTypeName = interestingEvent.name;
// Grab the name of the catalog node from the step before that
var catalogName = catalog.name;
// Define the name of a topic in the current namespace where events should be delivered
var localTopicName = "/my/local/topic";

// Define an object containing the parameters for the procedure
var params = {
    localName: localTopicName,
    name: eventTypeName,
    catalogName: catalogName
};

// Register the subscription through the SDK by executing the procedure Subscriber.subscribe
var subscribePromise = vantiq.execute("Subscriber.subscribe", params);

// Setup the success and error handlers
subscribePromise.then((results) => {
    // Since the procedure succeeded, the current namespace is now set up to receive
    // events on the local topic "/my/local/topic". We still need to open a websocket
    // to handle the real-time events.
    
    // Define a callback handler function that will execute every time an event arrives
    var eventCallbackHandler = function(event) {
        // just log each event
        console.log(event);
    };
    
    // Setup the WebSocket subscription through the SDK so it will call our callback
    vantiq.subscribe('topics', localTopicName, eventCallbackHandler);
}).catch((err) => {
    // Handle error
});
```
