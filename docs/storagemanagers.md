# Storage Managers

## Introduction

The Vantiq platform provides a way to interact with a persistent data model via the notion of persistent "types."
Persistent types support the full range of create, update, select and delete operations, queries that can leverage a wide
variety of logical operators, and a limited set of aggregation functions.  Persistent types are also supported directly
in the VAIL language using an
embedded SQL dialect. The Vantiq platform implements persistent types using a storage manager based on MongoDB. There are,
however, myriad other data storage and retrieval technologies available with capabilities and strengths that differ from those of
MongoDB. Vantiq applications that work with differing kinds of data can benefit from working with a data store that
specializes in the types of querying or analysis they require. Further, not all stored data relevant to an application
is practical to import into the Vantiq platform. We want applications to be able to work with remotely stored data
in exactly the same way they work with data local to Vantiq. In order to support these remotely managed
data sets Vantiq provides the storage manager resource. Storage managers make remotely accessible data stores "pluggable"
into a given Vantiq namespace. Once installed, types defined using the storage manager expose both the particular
capabilities of the remote store and any pre-existing data sets there, making them available to applications to
use as though they were stored locally.

## Installation and Use

The preferred delivery mechanism for a storage manager is via [assembly](assemblies.md) and the Vantiq
[catalog](broker.md). Installation typically involves some configuration to establish the data store connection
address and authentication credentials. In our reference storage manager for InfluxDB Cloud, installers must provide the
cloud URI as well as the InfluxDB organization name and an access token.

Once installed, users can define types that leverage the remote data store. In the create type dialog of the UI 
when one or more storage manager resources are present, the UI provides a drop-down selector to choose one to manage the
type data.

![Create Type](assets/img/storagemanagers/CreateType.png "Create Type Dialog")

Users can then use the type as they would any VAIL type, subject to any storage manager restrictions. When the user
selects a storage manager, the UI gives them the option to specify an optional non-default connection name as well as
a form for providing name, value pairs in JSON format. The setting of these additional entries will depend on the needs
of the specific storage manager involved.

### Storage Manager Transactions

If the storage manager supports transactions, there are three built-in procedures that can be used to manage them:

* **io.vantiq.StorageManager.startTransaction(storageManager String, options Object): String** - starts a transaction with the named storage manager and returns a transaction ID. The ID is a String that must be passed to all subsequent data manipulation operations (see below). The storageManager parameter is the name of the storage manager resource with which the transaction should be started. The `options` parameter is an Object that may contain additional information about the transaction. The details of the specific options are storage manager specific.
* **io.vantiq.StorageManager.commitTransaction(vantiqTransactionId String, storageManager Object, options Object)** - commits the transaction associated with the specified ID. `vantiqTransactionId` is the value returned by the `startTransaction` procedure, `storageManager` is the storage manager resource, and `options` is an Object that may contain additional information about the transaction. The details of the specific options are storage manager specific.
* **io.vantiq.StorageManager.abortTransaction(vantiqTransactionId String, storageManager Object, options Object)** - The analog to commit, this procedure aborts the transaction associated with the specified ID. `vantiqTransactionId` is the value returned by the `startTransaction` procedure, `storageManager` is the storage manager resource, and `options` is an Object that may contain additional information about the transaction. The details of the specific options are storage manager specific.

#### Storage Manager Transactions in VAIL

Once a transaction is started, it may be referenced in subsequent DML queries and commands via the `WITH` clause. For example:

```
    var vantiqTransactionId = io.vantiq.StorageManager.startTransaction(<storage manager name>, {})
    
    INSERT INTO <type> (id, name) VALUES (1, 'foo') WITH transaction = vantiqTransactionId
    UPDATE <type> ({name: "bar"}) WITH transaction = vantiqTransactionId WHERE id == 1
    SELECT FROM <type> WITH transaction=vantiqTransactionId WHERE id == 1
    
    io.vantiq.StorageManager.commitTransaction(<storage manager name>, vantiqTransactionId, {})
```

Use of the `with transaction = <id>` clause instructs the Vantiq server to work with the storage manager underpinning the type to ensure that the operation is performed in the context of the transaction started with the specified ID. The clause is supported by all the DML operations: `insert`, `update`, `upsert`, `delete`, and `select`.

## Advanced Use Cases

While we expect the vast majority of interactions with storage managers to be simple installation and use, in rare cases a
user might want to create or delete them. Users can see, edit, add or remove Storage Manager resources in the Storage Managers pane. To open it click
`Administer -> Advanced -> Storage Managers`. As the location of this functionality in the menu suggests, it is an
advanced use-case scenario.

![Administer Storage Managers](assets/img/storagemanagers/StorageManagers.png "Storage Managers Pane")

To create a new storage manager click `New`. To delete either select the check-box to the left of the instance(s) or 
click on the ellipsis to right of an instance you want to remove then click `Delete`

When creating a new storage manager resource, users must designate a service responsible for implementing the operations
the storage manager must support.

![AddNewStorageManager](assets/img/storagemanagers/AddStorageManager.png "Add Storage Manager Dialog")

If the specified service does not exist, the UI will generate a new service with the provided name. The generated service
will start with the full interface of procedural entry points, where each entry point has a stubbed implementation.

![StorageManagerService](assets/img/storagemanagers/StorageManagerService.png "Storage Manager Service Pane")

## Storage Manager Service API

Each storage manager identifies a Vantiq service responsible for handling all server requests against each type that references it. The
service must both understand what the Vantiq server is requesting and know how to contact the remote data store to
complete the request, then return the expected response. This is a low-level plug-in to the Vantiq system and here we
outline the details for the API the storage manager service must support.
The API must handle requests related to both definition and data manipulation operations. 

### Restricting Capabilities

One primary motivation for pluggable storage managers is to provide the ability to leverage unique capabilities of different
data management systems. The trade-off for this is that not all storage managers will be capable of supporting all
standard Vantiq data operations or default data store (MongoDB) capabilities. Recognizing this, we provide a procedure in
which a storage manager can explicitly declare what features or operations it does not support. The Vantiq system provides
compile time support for generating errors based on these restrictions. If an application attempts to use one, the code 
generator will reject the attempt raising an error to indicate the type's storage manager does not allow it. In some cases
the Vantiq UI will adjust what is available for users based on these restrictions. For example if the storage manager does
not support indexes, then no `Indexes` tab will appear in the associated Type definition pane.

**getTypeRestrictions():Object**

This procedure should return an Object with the following keys and values:

* **restrictedOps** - the list of operations it does not support
* **restrictedDeclaredTypes** - the list of VAIL types it does not support
* **restrictedTypeProperties** - the list of features on individual types and type properties it does not support

It is probably easiest to understand how to leverage this entry point with an example return value:

```json
{
   "restrictedOps":["createIndex"],
   "restrictedDeclaredTypes":["GeoJSON", "ResourceRef", "Object", "Value", "Map", "Array"],
   "restrictedTypeProperties":["audited", "expiresAfter", "groupEnabled"]
}
```

The above declares the storage manager does not support `createIndex`, or the six listed VAIL types. Further, types cannot
be audited, their instances cannot expire, and they are not group enabled.

The complete list of possibilities is:

```json
{
   "restrictedOps": [
     "createIndex", "select", "selectOne", "insert", "update", "delete", "aggregate", "aggregatePush", "renameType", "startTransaction"
   ],
   "restrictedDeclaredTypes": [
     "String", "Integer", "Real", "Boolean", "Datetime", "Currency", "Decimal", "GeoJSON", "ResourceRef", "Object", "Value", "Map"
   ],
   "restrictedTypeProperties":[
     "audited", "expiresAfter", "groupEnabled"
   ]
}
```

If you create a storage manager using the Vantiq UI, it generates the implementing service and a stub for this procedure
that lists all of the above. Defining a storage manager with all restrictions is not very useful, but does serve as
a starting point to help developers decide what they want to exclude.

Note that the operation `insertMany` (see below) does not show up in the complete list. You can only restrict or allow
`insert` and that choice applies to `insertMany` as well. If you do not want to take any specific action to optimize
for a bulk insert, you can implement `insertMany` as a loop calling `insert` for each Object in the Array.

Similarly, the storage manager must support the `count` operation if it supports `select`. The Vantiq UI leverages both
`select` and `count` when displaying the instances for a type.

Finally, note that the `upsert` operation is not listed as a possible restriction. The reason is that upsert is a shorthand notation for `update` or `insert`. If the storage manager supports `update` and  `insert` as well as `select`, then it also supports `upsert`. Failure to support any of these three operations means the storage manager does not support `upsert`. Additionally, in the Vantiq type system executing an `upsert` requires the definition of a natural key against the underlying type. While the type system handles the issuance of the required `select` against the natural key to determine if an `insert` or an `update` should be performed, the efficient processing of an `upsert` requires the storage manager implementation to efficiently handle the natural key-based look-up. For standard types, the Vantiq system requires the creation of an index against the natural key. However, since we cannot know how a storage manager will execute the `select`, this requirement is relaxed for storage manager types. 

### Defining Types

#### initializeTypeDefinition( proposedType Object REQUIRED, existingType Object REQUIRED ):Object

When a user defines a new storage-manager-based type or updates an existing one, the Vantiq server asks the storage
manager to initialize the new definition or vet the changes. This is a useful place to deal with any requirements inherent to the
underlying data management system. For example a time series database might require a _timestamp_ property of type
DateTime be present in all defined types:

```js
    var properties = proposedType.properties
    if (properties.containsKey("timestamp")) {
        if (properties.timestamp.type != "DateTime") {
            exception("com.vantiq.timeseries.timestamp.property", "Types for the InfluxDB storage manager cannot define a timestamp property -- this property is reserved")
        }
    } else {
        properties.timestamp = {type: "DateTime"}
    }
    return proposedType
```

The arguments to the procedure are the newly proposed type definition and the existing type definition if any. When
defining a new type the existingType parameter is `null`. For details on the contents of the arguments and
expected result see [types](resourceguide.md#types) in the resource guide. The server stores the result as the
definitive type resource instance.
  
The `storageName` type property is specifically designated for use by a storage manager to help
track any mapping from the type resource name to a name or location for the data in the remote data store.

### Data Manipulation

There are a handful of entry points in the API to deal with data manipulation. These correspond to the operations
available for types in the Vantiq system. 

#### Connection Context

In all cases, for data manipulation procedures, the Vantiq server provides the storageManager, a String, with the storage
name and the storage manager reference Object for the type. The latter contains the storage manager name, connection name,
and a bucket of name, value pairs under the properties key. We intend this to be enough information to enable the storage
manager to successfully connect to the remote data store to perform the needed operations.

#### Qualifications

Most of the data manipulation procedures take a `qual` as a parameter. This Object expresses the qualification for the 
operation. The entries can be the simple form:

```
    {
        "<property-name>": {
            "$<operator>": value
        }
    }
```

where the `operator` is one of: `$eq, $gt, $gte, $lt, $lte` and propertyName is the name of one of the properties in the type.
Note that there is also a shorthand notation for this simple qualification:

```
    {
        "<property-name>": value
    }
```

which is equivalent to: `{ "<property-name>": { "$eq": value } }`.

Alternatively, the entries may have the more complex form:

```
    {
        "$logical_operator": [ qual1, qual2, ... qual_n ]
    }
```

where `logical_operator` is one of `$and` or `$or`, while qual<sub>i</sub> is a recursive reference to another simple or
complex qualification expression. A shorthand notation for this more complicated expression denotes an implicit `$and`
expression:

```
    {
        "<property-name1>": value1
        "<property-name2>": value2
        ...
    }
```

This is equivalent to:

```
    {
        "$and": [
            { "<property-name1>": { "$eq": value1 } },
            { "<property-name2>": { "$eq": value2 } }
        ]
    }
```

#### Operations

**insert( storageName String REQUIRED, storageManagerReference Object REQUIRED, values Object REQUIRED ):Object**

To support the insertion of additional data to the underlying data store, the storage manager must provide the insert
procedure. The `values` parameter contains the property names and values of the new instance. Any type property not found
here is unknown or null. Insert should return the actual instance that it inserted into the remote store.

**insertMany( storageName String REQUIRED, storageManagerReference Object REQUIRED, values Object Array REQUIRED ):Object**

This entry point is similar to `insert` where the values parameter is an array of Object instead of just a single Object.
The idea is that it might be more performant to bulk insert many instances instead of inserting them one at a time. See
[Bulk INSERT](rules.md#insert) in the VAIL reference guide. Whether insertMany is a restricted operation
for the storage manager is determined by the status of `insert`. If `insert` is supported, then the developer must also
provide an implementation for `insertMany`.


**update( storageName String REQUIRED, storageManagerReference Object REQUIRED, values Object REQUIRED, qual Object REQUIRED )**

The update procedure translates update requests for the underlying data store. The `values` parameter is an Object
containing only those properties being updated. The keys are the property names, and the values are the new values to 
set. Update should return the updated instance.

**delete( storageName String REQUIRED, storageManagerReference Object REQUIRED, qual Object REQUIRED ): Integer`**

Delete all instances that match the qualification. If possible, delete should return the number of instances removed.

**select( storageName String REQUIRED, storageManagerReference Object REQUIRED, properties Object REQUIRED, qual Object REQUIRED, options Object REQUIRED )**

Select is the procedure that handles data retrieval. The properties parameter is an Object whose keys consist of the
property names for the values the caller wants in the results. The values can be either an aggregate expression (as a String) or just
the name of the property indicating no expression. In VAIL, applications can request expression evaluation
based on the underlying properties of the type. For example:

```json
select result = aggregateExpression(property) from <type name> where <qual>
```

In this case the properties parameter is an Object with `{"result": "aggregateExpression(property)"}`.

In the case of a `select * from <type>` query, the Vantiq server expands the properties parameter to the complete set of
property names as keys and property names as values.
  
##### Select Options

The server uses the options parameter to indicate
if the select results should be sorted and if so on what properties and whether the order is ascending or descending.
For example:

```json
{
    "sort": {
        "name": -1
    }
}
```

Indicates the results should be sorted on the name property in descending order. Ascending order would have a positive
one instead of a negative one.

The server may also indicate that the select procedure call must limit number of results returned:

```json
{
    "limit": 1000
}
```

The above means that select should limit the number of results to 1000 instances.

Finally, the server may also use options to indicate if some initial number of results should be skipped. This mechanism
in combination with the `limit` option provides a simple version of a cursor or paging of the results. The Vantiq UI takes
advantage of this when displaying "all records" for a particular type.

```json
{
  "sort": {
    "name" : 1
  },
  "skip": 100,
  "limit": 25
}
```

The above indicates the results should sort by name ascending, skip the first 100 instances and limit the results to 25
instances.

##### Select Return Value

We purposely leave the return type of the select procedure unspecified (also known as a return type of `any`). In some
cases the procedure will be able
to return an array of Object. Due to memory use considerations this mechanism is limited by the Vantiq server to 10,000
instances. For larger result sets the select procedure should instead return a [sequence](rules.md#sequences) of Object. The most convenient
way to do this is to return the result of a `select sequence ...`, e.g. assuming the storage manager implementation involves working
with a remote source:

```
    return select sequence from source <mysource> with ...
```

This, of course, only works when the source returns a sequence of JSON values which the server then translates to VAIL
Objects. There are also some built-in procedures to help with sequences. See [toSequence(arr)](rules.md#utility-procedures) and
[ResourceAPI.executeOp(message, asSequence)](rules.md#resourceapi).

If it is not feasible for the select procedure to return a sequence, then it is important to support the `skip` and
`limit` options for larger data sets.

**selectOne( storageName String REQUIRED, storageManagerReference Object REQUIRED, properties Object REQUIRED, qual Object REQUIRED, options Object REQUIRED ):Object Array**

`selectOne` is similar to `select` with the exception that the procedure must limit the result set size to one. The implication
is that the qualification parameter inherently ensures that either a single instance matches or no instances match. Since 
a limit of 1 is implied, there is no need for skip and limit options. However, Vantiq sometimes needs to require that a
single result comes back as opposed to no instance. In these scenarios the options parameter contains an entry of
`{required: true}`. If `selectOne` returns an empty Object Array in this case it is an error.

**count(storageName String, storageManagerReference Object, qual Object, options Object): Integer**

The `count` operation returns the count of instances that match the provided qualification. If the storage manager
supports the select operation, it should also provide an implementation for `count`. `count` cannot be restricted
separately from `select`.

### Transaction Support

For some storage managers, it may be possible to support transactions. Toward this end the Storage Manager API provides three entry points: `startTransaction`, `commitTransaction`, and `abortTransaction`. Once a transaction starts, the Vantiq server will route all subsequent data manipulation requests that involve the transaction to the same storage manager instance that started it. To accomplish this, the Vantiq server provides a transaction token on start. This same value will be provided in every request that participates in the transaction using the `options` parameter present in each:
```json
  {
    "transaction": "<Vantiq transaction ID value>"
  }
```
The storage manager must use this ID to facilitate issuing the request to the underlying data store in the context of the associated transaction. How the storage manager accomplishes this is specific to its implementation.

**startTransaction(vantiqTransactionId String, options Object)**

The `startTransaction` operation initiates a transaction. The `vantiqTransactionId` is a unique identifier for the transaction generated by the Vantiq server. The `options` parameter is an Object that may contain additional information about the transaction.

**commitTransaction(vantiqTransactionId String, options Object)**

The `commitTransaction` operation commits the transaction associated with the specified ID. `vantiqTransactionId` is the value returned by the `startTransaction` operation, and `options` is an Object that may contain additional information about the transaction.

**abortTransaction(vantiqTransactionId String, options Object)**

The `abortTransaction` operation aborts or rolls back the transaction associated with the specified ID. `vantiqTransactionId` is the value returned by the `startTransaction` operation, and `options` is an Object that may contain additional information about the transaction.

### Discovery from External Data Store

In some scenarios a storage manager plugs in a remote store with existing data to integrate within the Vantiq platform. When 
installing a storage manager from an assembly, we want to allow the storage manager to define Vantiq types that correspond to data it finds at install time.
To enable this, the Assembly resource provides a post-install hook. Users can designate a procedure that the Vantiq system 
invokes once the assembly installation in a namespace is complete.

#### discoverTypes(config Object)

Users can name the procedure as they like, but it should be designated as the `postInstallProc` for the [assembly](assemblies.md). With the
provided assembly configuration, the procedure should be able to connect to the remote data source and interrogate it for 
candidates to define as types in Vantiq.

### Error Handling

When implementing the storage manager service, developers will inevitably encounter error scenarios. We recommend developers
leverage the VAIL [`exception()`](rules.md#general-utility-procedures) built-in procedure choosing a unique value
of `code` for each type of error they detect. This approach gives application developers that use storage managers a reasonable
opportunity to handle exceptions in consistent ways that make sense for the app. See also: [error handling](rules.md#error-handling).

### Storage Manager Assembly Contents

Ultimately, what goes into an assembly is at the discretion of the author. For storage managers, however, successful
installation requires a handful of resources. They are: the storage manager, the implementing service, all the procedures,
public and private, involved in handling the storage manager service API, and any source needed to connect to the remote
store.

If your storage manager is capable of interrogation of a remote store to determine potential Vantiq types to create at install
time, you should designate the appropriate procedure as the post-install procedure.

The interface for the assembly can be empty. The list of visible resources can also remain empty. There is no requirement
for either of these facilities.

The configuration of the assembly should allow for a way to specify an access token or credentials and any needed information
to connect to the remote store, like the URL for the data store.

## Native Language Implementation

Another advanced use case involves providing a native language based storage manager service implementation instead of VAIL procedures. Primarily for reasons of performance and flexibility, it may make sense to implement your storage manager service in a lower level language. Vantiq provides a skeleton Java framework along with stub implementations for the storage manager API. The framework creates a very simple HTTP server listening for WebSocket connections on a configured port. Connections are initiated by the Vantiq server and, once established, subsequent API calls are unmarshalled and delivered to a VantiqStorageManager interface implementation. Developers can then deploy a Java-based storage manager implementation by defining a service connector resource.

### Service Connectors

The [service connector resource](resourceguide.md#service-connectors) provides mechanism by which developers may provide service procedure implementations in a "native" or lower level language as an alternative to VAIL. It is only used for procedures that are part of the storage manager API. Specifically, the service generated for a storage manager may be updated to reference a service connector. When that is the case, the Vantiq server invokes the native implementation for each storage manager API call through the service connector instead of invoking the VAIL implementation.

Examples are in the [Service Connectors SDK](https://github.com/Vantiq/vantiq-service-connectors). 

The service connector definition consists of a name, an indication of whether the service connector is internal or external (see below), and properties that are specific to each type:
<table>
<tr>
<td><b>Internal</b></td><td>image</td><td>The repository image name and version</td>
</tr>
<tr>
<td></td><td>vCPU</td><td>The number of virtual CPUs to allocate to the connector</td>
</tr>
<tr>
<td></td><td>memory</td><td>The amount of memory in megabytes to allocate to the connector</td>
</tr>
<tr>
<td></td><td>secret</td><td>A Vantiq secret resource reference for a secret to provide to the connector</td>
</tr>
<tr>
<td><b>External</b></td><td>host</td><td>The name of the host on which the service connector is running</td>
</tr>
<tr>
<td></td><td>port</td><td>The port number on which the connector is listening</td>
</tr>
</table>

#### Internal vs. External Service Connectors

Service connectors are either internal or external. Internal service connectors are deployed as part of the Vantiq cluster. External service connectors are deployed outside the Vantiq cluster. The Vantiq server communicates with the connector over a WebSocket connection in both cases. However, the Vantiq server is responsible for deploying and managing the life cycle of internal service connectors. External service connectors are deployed and managed by the developer. 

The main idea behind external connectors is to facilitate their development by allowing developers to attach to and debug the running process. They can be spun up in development environments where that is possible. Once development of the connector is complete, we expect developers to package them as Docker containers and deploy them in Vantiq clustered environments as internal connectors. We do not support running external connectors in production environments.  To create an external connector you must specify a host and port at which the Vantiq server can reach it. A convenient way to develop external connectors is to use an edge server and define the external connector as running local to it.

We deploy internal connectors as part of the Vantiq cluster close to the Vantiq server. Developers must build a containerized image of their service connector implementation and upload it to an image registry (e.g. quay.io) that can be accessed from the target Vantiq cluster. The Java-based framework provides a basic Dockerfile container build file and gradle build targets that create the image and publish it to quay.io (the repository can be configured in the build.gradle file). More details are in the [Service Connectors SDK Readme](https://github.com/Vantiq/vantiq-service-connectors?tab=readme-ov-file#building-docker-images). When creating an internal connector you specify both the amount of virtual CPU and memory to allocate for its use. The Vantiq server works with our Kubernetes infrastructure to create or delete the required resources in the Vantiq cluster to manage the connector lifecycle. While the connectors have access to the wider internet, we configure the internal network in a way that prevents them from accessing *anything* internal to the cluster environment. This is a security measure to prevent internal connectors from either accidentally or intentionally accessing internal resources and potentially causing harm.

#### Internal Connector Resource Quota

Each organization in the Vantiq system has a limit on the amount of compute resources and memory its connectors can consume. This is specified as part of the organization quota. The limits are expressed as a maximum number of virtual CPUs and a maximum amount of memory. The Vantiq server enforces these limits when creating internal connectors. If the creation of a connector would exceed the quota, the Vantiq server will reject the request. An example of an organization's quota is:

```json
{
  "limits": {
    "k8sResources": {
      "vCPU": "8",
      "memory": "10Gi"
    }
  }
}
```

This quota specifies that the organization has up to 8 virtual CPUs and 10 gigabytes of memory available to allocate to its internal connectors. Once the quota is set, any user designated as a namespace administrator for a given namespace can allocate resources against it. 

#### Internal Service Connector Secrets

Typically, a storage manager implementation will require some sort of credentials to connect to the remote store. For internal connectors, the Vantiq server provides a mechanism to securely store and retrieve these credentials. The mechanism is based on Vantiq and Kubernetes secrets resources. When creating an internal connector, the Vantiq server will create a secret resource in the Kubernetes namespace for the connector. The secret resource will contain the contents from the specified Vantiq secret resource. The connector can then retrieve the secret from the local file created by Kubernetes for the running POD.

![StorageManagerService](assets/img/storagemanagers/AddServiceConnector.png "Add Service Connector")

The above example specifies the Vantiq secret `mySecret`. The Vantiq server uses contents of the secret to create a corresponding Kubernetes secret resource. The connector can then retrieve the secret contents from the local path `/opt/vantiq/secret/secret.properties` in the running POD. The contents of the file are `secret = <secret value>`.