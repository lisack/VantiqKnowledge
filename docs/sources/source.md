# External Source Reference Guide

Vantiq supports the integration of external data sources into the automation service. A source may supply data or be a recipient of notifications produced by Vantiq or both supply data and be a recipient of notifications. At the present time Vantiq supports following source types:

* MQTT
* Email servers
* REST services
* VIDEO service
* AMQP
* SMS services
* Kafka topics
* Google Cloud Pub/Sub (GCPS)
* Enterprise Connectors

**Enterprise Connectors** comprise a class of sources that run and can be developed outside of Vantiq.

A source implements one or more of the following capabilities:

* **Stream data** This provides a continuous stream of objects from the source.  Examples of this include an MQTT topic with new messages delivered asynchronously to the server or a web site that is read periodically to produce a stream of data.
* **Query the source for data** This requests a specific result be retrieved from the source.  For example, you can send a request to a REST API in order to interact with some external service. 
* **Publish data to the source** This sends data from the Vantiq server to the specified source.  Examples include sending a message to an AMQP topic or sending a push notification via SMS.

## Source

Sources are defined by creating a **source** resource that represents the definition of the source and submitting the definition to Vantiq for registration. Once registered, the source will immediately begin reading and processing messages if a stream is configured and will also immediately be available for query and publish operations.

The specific details of the ArsSource properties required are described in the separate documentation for each source class:

* [EMAIL](email.md)
* [SMS](sms.md)
* [MQTT](mqtt.md)
* [AMQP](amqp.md)
* [REMOTE](remote.md)
* [VIDEO](video.md)
* [CHATBOT](chatbot.md)
* [KAFKA](kafka.md)
* [GCPS](gcps.md)
* [Enterprise Connectors](entcon.md)

The general representation of a source resource is defined in [Resource Reference Guide: Source](../resourceguide.md#source). In summary, a source contains the following properties:

* **name** - the name assigned to the source.
* **type** - the type of source. Currently, a type specified by an Enterprise Connector or one of these string values:
	* EMAIL
	* SMS
	* MQTT
	* AMQP
	* REMOTE
	* VIDEO
	* CHATBOT
	* KAFKA
	* GCPS
* **config** - contains the source type specific parameters associated with the source. The detailed contents of **config** is defined in the source type specific documentation referenced above.
* **autoUnwind** -- indicates whether the source should automatically "unwind" any event data that it receives.  If `true`, then if an array is received as event data, the system will immediately process the array and generate one event for each array member (instead of one containing the array itself).

## Source Operations

As described above sources can support up to 3 operations, all of which operate on data in the form of "messages".  The operations and message formats supported are specific to each source implementation and described in the source specific documentation.  Here we describe the general capabilities.

### Content Types

Vantiq supports 3 distinct content types for data sent and received by sources:

* JSON - JSON data is sent and received using the standard JSON textual notation.  At runtime JSON objects are native VAIL objects and are manipulated using standard JavaScript syntax.
* XML -- XML data is sent and received using the standard XML textual notation.  At runtime XML objects are manipulated using the [Groovy GPath](https://groovy-lang.org/processing-xml.html#_gpath) notation.
* Text -- text data is unformatted and uninterpreted by the system.  It will be transmitted and received using the UTF-8 character set.

Each source implementation is responsible for transforming data sent and received between the external form supported by the source and one of these 3 content types supported by the Vantiq system.  For example, an Email source may accept a JSON document which describes the elements of an Email message and transform that document into the actual SMTP message.

For some sources (_e.g._, the REMOTE source), Vantiq supports sending other content types as well. Please see the [REMOTE source documentation](remote.md#docImgVidOps) for details.

### Streaming Data

A stream of information is read from the external system using either an asynchronous model or a synchronous (polling) model depending on the capabilities of the external system. The process stream method must run continuously and may not terminate until the source is shut down. For example, the MQTT source type asynchronously reads messages when they are published to the corresponding MQTT topic while the REMOTE source periodically polls the specified REST endpoint for new data.

When a message arrives on a streaming source an event is generated which will be delivered to any subscribed rules or event streams for processing.  The event may also be delivered to any web socket clients which have subscribed to the event's id.

#### Source Schema

The definition of a stream source may optionally include a reference to a schema type which represents the structure of the data produced by the source.  This schema is purely informational and is used by Modelo and Pronto to make it easier to process the source events.  However, the system will not validate if the data produced by the source actually matches the referenced schema type.  Some sources support the receipt of data from multiple "locations" (for example, an MQTT source may receive data from multiple topics).  In these cases it is assumed that all of the data conforms to the same underlying schema.  If that isn't true, you should define a distinct source for each desired schema.

### Query

A query can be presented to sources that support queries to obtain data from the external system. A query is executed by invoking the **query** function from the body of a rule. The query method is provided with the source type specific object that defines the query to execute. For example, the REMOTE source type that supports REST endpoints is invoked with an object that defines the URL, headers and body for the REST request that obtains the data from the remote endpoint.

### Notify

A source can send data or notifications to the external system or, perhaps more appropriately, via the external system since the ultimate receiver of the notification may be a person. Examples of notify method uses:

* MQTT source - posts the message to the specified MQTT topic. Ultimately, the message will be delivered to all MQTT clients subscribed to the MQTT topic.
* EMAIL source - the message is emailed to the set of recipients attached to the message.
* REMOTE source - the message is POSTed to the URL defined on the remote source.

The notify function is invoked from a rule to send data or notifications via a source.

### Using Secrets
Sources that connect to external systems often need to be secured by passwords, access tokens, or secrets. These 
credentials often need to be secured in such a way that users of a source don't have access to the 
underlying credentials. To secure credentials in a source configuration, certain config properties can contain references 
to secrets, which store a credential securely. Users of the source can see the name of the secret, but not the value
associated with that secret. The credentials configuration properties that can contain a reference to a secret are specific to the
type of source. For example, email sources must specify a username and password for the credentials used to access the 
email server, and the password configuration property can be a reference to a secret. View the documentation for each
source type to see which credentials properties can use secrets.

Besides the need to secure credentials, it can sometimes be necessary to secure a configuration property value.
For example an HTTP header containing an API key. To secure such property values, a general
scheme that applies to all source configurations is to reference a secret using the syntax `@secrets(<secret_name>)`.

For example, a Remote source might define the following header: `{"apiKey": "@secrets(apikey)"}` where `apikey` would
be a secret name. As the source gets activated the reference to the `apikey` secret name `@secrets(apikey)`
is replaced with the secret value.

One note about secrets: If the secret value associated with a secret is updated you must deactivate and reactivate the
source that references the secret in order for the secret update to take effect for the source. Until reactivation, the
old secret value will continue to be used. 

### Source Status

If the external resource to which a source is connected becomes unavailable (e.g., an unreachable MQTT broker due 
to network issues), then the source's status becomes `unhealthy` and a possible cause 
message gets attached to its status (if available). The source health status is shown in the IDE as a green/red arrow 
on the Source pane.

If a source becomes unhealthy, the system will automatically attempt reactivation within 5 minutes.
If the source remains unhealthy after this attempt, the source becomes unavailable and will not reactivate _until the
source is changed_. This state is recorded by setting the property _isUnavailable_ to `true`. The source can be reactivated by any change to the source definition (including a change of setting `active` to true) or a change to a resource configuration targeting the source. The rationale is that if automated source reactivation is still failing, then someone needs to 
address the issue (network connectivity, remote broker unavailable, etc.). Note that a source can always 
be deactivated or reactivated using VAIL code so any custom logic required to react to network or broker failure 
can be tailored to an application.

## Source Mocking

Sources can be placed in `Mock Mode`, which allows the developer to override the publish and query operations on the Source with VAIL procedures.
A Source that is in Mock Mode does not connect to the 
outside world. This means that any messages produced by the external Source do not reach Vantiq and no outbound messages
from Vantiq will reach the Source.

A Boolean property called `mockMode` represents whether or not a Source is in Mock Mode.
 When `mockMode` is true, the Source uses its Mocking Procedures to define its behavior.
 
Vantiq developers interact internally with Sources in two key ways: Query and Publish operations. By default, when a Source is in Mock Mode,
Publishing to and Querying from the Source has no effect.
However, a user may override the source's Query and Publish operations.

An Object property called `mockProcedures` represents the configuration for a source's Mocking behavior. 
The `mockProcedures` object has two keys: 
 * **query** (String): The name of the Procedure that runs on query from Source when `mockMode` is _true_
 * **publish** (String): The name of the Procedure that runs on publish to Source when `mockMode` is _true_

Developers may use built-in Procedures to turn Mock Mode on and off. 
`Test.startSourceMocking(sourceName, mockQueryProcedure, mockPublishProcedure)` turns on Source Mocking for the source _sourceName_
and `Test.stopSourceMocking(sourceName)` turns it off. For more information,
please see the [VAIL Rule and Procedure Reference Guide](../rules.md#test).

### Query

The Query Mock Procedure takes in the query descriptor as a single parameter called `queryDesc` and may return anything the 
developer desires.

For example:
```
PROCEDURE getPageSize(queryDesc)
var result = { "code":"404","message":"city not found" }

if (queryDesc.query.q.includes("London")) {
    result =
       {
          "coord": {
             "lon": -0.13,
             "lat": 51.51
          },
          "weather": [
             {
                "id": 802,
                "main": "Clouds",
                "description": "scattered clouds",
                "icon": "03n"
             }
          ],
          "timezone": 0,
          "id": 2643743,
          "name": "London",
          "cod": 200
       }
} else if (queryDesc.query.q.includes("Honolulu")){
    result =
       {
          "coord": {
             "lon": -157.86,
             "lat": 21.3
          },
          "weather": [
             {
                "id": 500,
                "main": "Rain",
                "description": "light rain",
                "icon": "10d"
             }
          ],
          "timezone": -36000,
          "id": 5856195,
          "name": "Honolulu",
          "cod": 200
       }
}
return result
```
If `getPageSize` was set as the query Mock Procedure then executing the query:

```
SELECT FROM SOURCE weather with query = {"q":"London", "APPID":"REPLACE_ME"}
```
would return 

```
[{
    "coord": {
        "lon": -0.13,
        "lat": 51.51
    },
    "weather": [{
        "id": 802,
        "main": "Clouds",
        "description": "scattered clouds",
        "icon": "03n"
    }],
    "timezone": 0,
    "id": 2643743,
    "name": "London",
    "cod": 200
}]
```

### Publish 

The Publish Mock Procedure takes in the publish descriptor as a single parameter called `pubDesc`.

Because a PUBLISH is a “fire and forget” operation, the Procedure’s return value is ignored

For example:

```
PROCEDURE insertToTypeProc(pubDesc)
var message = pubDesc.message
INSERT MyType( name: message.name, messageValue: message.messageValue )
```

If `insertToTypeProc` is set as the Publish Mock Procedure then the following publish:

```
PUBLISH {topic: topic, message: {name: "Test", messageValue:  10}} to SOURCE mySrc
```

would result in a new instance of Type MyType to be inserted with messageValue == 10.

### Creating a Source Event

Developers may call the procedure [`Test.sendMockSourceEvent()`](../rules.md#test) to Mock an incoming source event. Whether or 
not the Source is in `mockMode`, the *message* will be delivered to all active subscribers of the Source.

For example, given the following Rule:
```
RULE sourceListener
WHEN EVENT OCCURS ON "/sources/mySource" AS event

INSERT testType(event.name)
```

Running the Procedure:
```
PROCEDURE proc()
Test.sendMockSourceEvent("mySource", {name: "ABC"})
```

would result in a new instance of `testType` with `name == "ABC"`.
