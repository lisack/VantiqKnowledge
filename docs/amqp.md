# AMQP Source Integration

[AMQP](https://www.amqp.org/) is commonly used as a means of passing messages between applications or organizations. Vantiq includes direct support for reading AMQP 1.0 data streams.

> **Important Note** -- by default RabbitMQ uses a proprietary protocol that they describe as [AMQP 0.9.1](<https://www.rabbitmq.com/amqp-0-9-1-quickref.html>). While this was proposed as an early version of the AMQP specification, it is not compatible with the final version of AMQP 1.0. The AMQP support provided by Vantiq is for AMQP 1.0 *only* and does not support this proprietary variant. For most queuing products, support for AMQP 1.0 must be explicitly enabled. Instructions for how to do this can be found in the specific product documentation.

The essence of the integration is as follows:

* An administrator defines an AMQP (Advanced Message Queuing Protocol) source by identifying the AMQP endpoint. This is accomplished via the updateStream request detailed below or by using the [Vantiq IDE](../../../../).
* Once the AMQP source has been defined, the server constructs a separate thread to accept inbound messages from the AMQP source.
* When a message arrives on the source endpoint an event is generated which will trigger the execution of any subscribed rules. The event may also be delivered to any clients with transient subscriptions on the event's id.
* Source processing rules are encouraged to store any persistent state in the Vantiq automation model. This enables the rule itself to be stateless making it easier to support various load balancing approaches such as executing the rule across a cluster or partitioning work between multiple Vantiq servers.

## AMQP Source Representation

An **AMQP source** defines the integration with a specific AMQP data stream and contains the following properties:

* **name** the name given to the stream by the user
* **type** must be the string **AMQP** indicating this is an AMQP source.
* **config** a JSON object containing additional AMQP configuration parameters:
	* **serverURIs** the endpoint for the server hosting the stream. Optionally a list of URIs.
	* **topics** the list of topics to which the stream is subscribed. Multiple streams may be defined on a single serverURI that subscribe to separate topics or overlapping topics. No restrictions are placed on the subscriptions by Vantiq.
	* **username** credentials for accessing the AMQP server
	* **password** credentials for accessing the AMQP server
	* **passwordType** specify whether the password is a plain text password, or a reference to a secret containing the actual password

While the configuration properties listed above are the most commonly used, the config JSON object maps to the [Vert.x AMQP Client Options](<https://vertx.io/docs/4.5.28/apidocs/io/vertx/amqp/AmqpClientOptions.html>) configuration. Therefore, any property supported by `AmqpClientOptions` can be added to the config object, even if it is not explicitly listed here. As an example, you can look at the [SSL setup](#ssl-setup) section.

## Create an AMQP Source
The following example illustrates how to create an AMQP source using the REST API. AMQP sources can also be defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "myAmqpSource",
    "type": "AMQP",
    "config": {
        "serverURIs"     : [ "amqp://localhost:5672" ],
        "topics"         : [ "com.accessg2.stream.amqp.example" ],
        "username"       : "guest",
        "password"       : "guest"
    }
}
```

Alternatively, to use a secret password named "MySecret", change the password property to a reference and specify 'secret' 
as the passwordType like this:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "myAmqpSource",
    "type": "AMQP",
    "config": {
        "serverURIs"     : [ "amqp://localhost:5672" ],
        "topics"         : [ "com.accessg2.stream.amqp.example" ],
        "username"       : "guest",
        "password"       : "/system.secrets/MySecret",
        "passwordType"   : "secret"
    }
}
```

If the source is intended to only publish messages, do not specify the `topics` property.

## Delete an AMQP Source

The example AMQP source named **myAmqpSource** can be deleted using the REST API by issuing the following request:

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/myAmqpSource
```

## AMQP Configuration options

To specify a secure server endpoint specify `amqps` as the URI scheme.

```json
"config": {
    "serverURIs"     : [ "amqps://localhost:5671" ],
    "topics"         : [ "com.accessg2.stream.amqp.example" ],
    "username"       : "guest",
    "password"       : "guest"
}
```

To subscribe to a source requiring the `PLAIN` SASL authentication method (e.g., Azure source), list the authentication method using the `enabledSaslMechanisms` configuration attribute.

```json
"config": {
    "serverURIs"     : [ "amqps://mysample.servicebus.windows.net:5671" ],
    "topics"         : [ "com.accessg2.stream.amqp.example" ],
    "username": "RootManageSharedAccessKey",
    "password": "1Y0MsS2TaiVZ6I+SHyQicKySI/TfSUJlICW/9AZ0lTk=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ]
}
```
Received AMQP messages might contain a contentType value. To enforce usage of the message provided contentType value you can set the attribute configuration `useMessageContentType` to true. If set and a message does not have contentType specified, or if the message contentType value is not supported by the Vantiq system then the setting in the source configuration is used.

## SSL Setup

An AMQP Source can be configured for either one-way or two-way SSL communication by specifying additional [Vert.x AMQP Client Options](<https://vertx.io/docs/4.5.28/apidocs/io/vertx/amqp/AmqpClientOptions.html>) configuration properties expressed as their JSON representation. Below are some usage examples. Note that SSL configuration properties
for AMQP, MQTT and Remote Sources are identical in their usage. You can look at the SSL Setup documentation for those
Sources for additional examples.

### One-way SSL

This section's examples assume that the AMQP broker is setup to communicate over SSL with a certificate signed by a CA. The CA certificate is available in a trust store named `sourceTrustStore.jks`. An AMQP Source is configured to access
the broker over SSL and the user configuring the Source has access to the trust store.

If the trust store is accessible on a file system readable by the Vantiq server (e.g., an edge installation), the trust store could be specified as:

```json
{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "username"      : "guest",
    "password"      : "guest", 
    "trustStoreOptions": {
        "path": "/path/to/sourceTrustStore.jks",
        "password": "my_store_password"
    }
}
```

If the trust store is not accessible by the server in which the remote source is being defined, the trust store content
can be specified as a base64 encoded value,

```json
# Copy/paste the following output to the value property below
$ cat /path/to/sourceTrustStore.jks | base64

{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "username"      : "guest",
    "password"      : "guest", 
    "trustStoreOptions": {
        "value": "/u3+7QAAAAIAAAABAAAAAgAGY2F........SzpeAUc7WXDK1HOg==",
        "password": "my_store_password"
    }
}
```

The value can also be stored as a Secret and [referenced in the configuration](source.md#using-secrets),

```json
# Copy/paste the following output to a Secret named SourceTrustStore
$ cat /path/to/sourceTrustStore.jks | base64
# Also define a Secret named SourceTrustStorePassword containing the trust store password

{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "username"      : "guest",
    "password"      : "guest", 
    "trustStoreOptions": {
        "value": "@secrets(SourceTrustStore)",
        "password": "@secrets(SourceTrustStorePassword)"
    }
}
```

Assuming that two CA certificates must be trusted and are accessible from files in PEM format, files named
`ca-cert-1` and `ca-cert-2`,

```json
{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "username"      : "guest",
    "password"      : "guest", 
    "pemTrustOptions": {
        "certPaths": ["/path/to/ca-cert-1", "/path/to/ca-cert-2"]
    }
}
```

Or with Secrets,

```json
# Copy/paste the following output to a Secret named CertAuthority1
$ cat /path/to/ca-cert-1 | base64
# Copy/paste the following output to a Secret named CertAuthority2
$ cat /path/to/ca-cert-2 | base64

{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "username"      : "guest",
    "password"      : "guest", 
    "pemTrustOptions": {
        "certValues": ["@secrets(CertAuthority1)", "@secrets(CertAuthority2)"]
    }
}
```

### SSL Client Authentication

In addition to specifying a trust store, an AMQP source configuration can also specify a client certificate.
This is necessary if the broker is setup for mutual authentication and requires the client to authenticate
with a certificate.

The examples below assume a key store named `sourceKeyStore.jks` containing the client certificate
signed by the CA.

If the key store is accessible on a file system readable by the Vantiq server,

```json
{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "trustStoreOptions": {
        "path": "/path/to/sourceTrustStore.jks",
        "password": "my_store_password"
    },
    "keyStoreOptions": {
        "path": "/path/to/sourceKeyStore.jks",
        "password": "my_keystore_password"
    }
}
```

Similarly to the trust store examples, any keystore specified using the path syntax can be specified as a base64
encoded value.

For example using Secret definitions,

```json
# Copy/paste the following output to a Secret named SourceTrustStore
$ cat /path/to/sourceTrustStore.jks | base64
# Copy/paste the following output to a Secret named SourceKeyStore
$ cat /path/to/sourceKeyStore.jks | base64
# Also define the store passwords as Secrets (SourceTrustStorePassword and SourceKeyStorePassword)

{
    "serverURIs"    : [ "amqps://localhost:5671" ],
    "topics"        : [ "com.accessg2.stream.amqp.example" ],
    "trustStoreOptions": {
        "value": "@secrets(SourceTrustStore)",
        "password": "@secrets(SourceTrustStorePassword)"
    },
    "keyStoreOptions": {
        "value": "@secrets(SourceKeyStore)",
        "password": "@secrets(SourceKeyStorePassword)"
    }
}
```

Refer to the [Vert.x AMQP Client Options](<https://vertx.io/docs/4.5.28/apidocs/io/vertx/amqp/AmqpClientOptions.html>)
document for a complete list of configuration options. Note: in that document, reference to `Buffer`
means that a base64 encoded value can be specified (e.g., trustStoreOptions). Any `add` method translates into an array
(e.g., pemTrustOptions) and any `set` method translates into a single property setting (e.g., path or value).

## Azure Configuration examples

To create an AMQP Azure Source configuration use the content of an Azure Connection String located in Azure Shared Access Policies.

The topic Source configuration names - both `topics` for Source configuration and `topic` to publish messages - use the syntax as expected by Azure. Please refer to the Azure documentation for additional details.

### Azure Queue
Assuming an Azure namespace `vqsample`, a queue named `vqs_queue` and the Policy `RootManageSharedAccessKey` with the following Primary Connection String:

```http
Endpoint=sb://vqsample.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;
         SharedAccessKey=1Y0MsS2TaiVZ6I+SHyQicKySI/TfSUJlICW/9AZ0lTk=
```

The AMQP Source configuration is:

```json
{
    "contentType": "application/json",
    "serverURIs": [
        "amqps://vqsample.servicebus.windows.net:5671"
    ],
    "topics": [
        "vqs_queue"
    ],
    "username": "RootManageSharedAccessKey",
    "password": "1Y0MsS2TaiVZ6I+SHyQicKySI/TfSUJlICW/9AZ0lTk=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ]
}
```

Note that the SASL mechanism must be defined as PLAIN and the secure port number (5671) must be specified.

To publish a message to the AMQP Source - therefore to the Azure queue - use the queue name (e.g., `vqs_queue`) as the topic name.

### Azure Topic
Assuming the same Connection String as above, a topic named `vqs_topic` and subscription named `MySub`, the AMQP Source configuration is:

```json
{
    "contentType": "application/json",
    "serverURIs": [
        "amqps://vqsample.servicebus.windows.net:5671"
    ],
    "topics": [
        "vqs_topic/Subscriptions/MySub"
    ],
    "username": "RootManageSharedAccessKey",
    "password": "1Y0MsS2TaiVZ6I+SHyQicKySI/TfSUJlICW/9AZ0lTk=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ]
}
```

Note that the `topics` property value has a different syntax for Azure queue and Azure topic. When listening on an Azure topic, the `topics` configuration property has the format  `<topic_name>/Subscription/<subscription_name>`

To publish a message to the AMQP Source on an Azure topic, use the topic name only (e.g., `vqs_topic`).

### Azure Event Hubs
Assuming an Azure namespace `vqhubns`, an Event Hub named `vqs_eventhub` and the Policy `EventUser` with the following Connection String:

```http
Endpoint=sb://vqhubns.servicebus.windows.net/;SharedAccessKeyName=EventUser;
         SharedAccessKey=gCunEMpPqh8uZXqaSqoa87U4YEi1rHZfTp5bBWn3hLA=;EntityPath=vqs_eventhub
```

The AMQP Source configuration is:

```json
{
    "contentType": "application/json",
    "serverURIs": [
        "amqps://vqhubns.servicebus.windows.net:5671"
    ],
    "topics": [
        "vqs_eventhub/ConsumerGroups/$default/Partitions/0"
    ],
    "username": "EventUser",
    "password": "gCunEMpPqh8uZXqaSqoa87U4YEi1rHZfTp5bBWn3hLA=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ]
}
```

To publish a message to the AMQP Source - therefore to the Event Hub - you may use the following as the topic name:

- `vqs_eventhub`
- or, to partition 0: `vqs_eventhub/Partitions/0`
- or, to publisher endpoint: `vqs_eventhub/Partitions/device1`

#### Partition Offset

By default, an AMQP source starts reading from the beginning of an Event Hubs partition. To start reading from the end of the partition and therefore receive only new events, set the `seekToEnd` configuration property to `true`.

```json
{
    "contentType": "application/json",
    "serverURIs": [
        "amqps://vqhubns.servicebus.windows.net:5671"
    ],
    "topics": [
        "vqs_eventhub/ConsumerGroups/$default/Partitions/0"
    ],
    "username": "EventUser",
    "password": "gCunEMpPqh8uZXqaSqoa87U4YEi1rHZfTp5bBWn3hLA=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ],
    "seekToEnd": true
}
```

To have fine-grained control over the initial offset, you can specify the [`AmqpReceiverOptions`](https://vertx.io/docs/4.5.28/apidocs/io/vertx/amqp/AmqpReceiverOptions.html) `selector` property. The `AmqpReceiverOptions` setting is specified within the `options` configuration property,

```
...
    "enabledSaslMechanisms": [
        "PLAIN"
    ],
    "options": {
        "<topic_partition_name>": {
            <AmqpReceiverOptions>
        }
    }

```

For example,

```json
{
    "contentType": "application/json",
    "serverURIs": [
        "amqps://vqhubns.servicebus.windows.net:5671"
    ],
    "topics": [
        "vqs_eventhub/ConsumerGroups/$default/Partitions/0"
    ],
    "username": "EventUser",
    "password": "gCunEMpPqh8uZXqaSqoa87U4YEi1rHZfTp5bBWn3hLA=",
    "enabledSaslMechanisms": [
        "PLAIN"
    ],
    "options": {
        "vqs_eventhub/ConsumerGroups/$default/Partitions/0": {
            "selector": "amqp.annotation.x-opt-offset >= '386547033'"
        }
    }
}
```

The above setting starts reading events from the partition offset 386547033 (included). 

The two special values `-1` and `@latest` can be specified to start reading from the beginning or from the end of the partition: `amqp.annotation.x-opt-offset > '-1'` and `amqp.annotation.x-opt-offset > '@latest'`. Note that specifying `seekToEnd` to `true` is equivalent to specifying the `selector` property to `amqp.annotation.x-opt-offset > '@latest'`.

Events received from an Azure Event Hubs endpoint contain message annotations accessible through the event `properties` property. The following message annotations are available:

| Property | Data Type | Description |
|----------|-----------|-------------|
| `x-opt-offset` | `string` | The offset of the event from the event hub partition stream. The offset identifier is unique within a partition of the event hub stream |
| `x-opt-sequence-number` | `long` | The logical sequence number of the event within the partition stream of the event hub |
| `x-opt-enqueued-time` | `date` | UTC time when the event was enqueued |

Any of the property `x-opt-offset`, `x-opt-sequence-number` or `x-opt-enqueued-time` might be used to specify a `selector` query.


For example,

```json
{
    ...
    "options": {
        "vqs_eventhub/ConsumerGroups/$default/Partitions/0": {
            "selector": "amqp.annotation.x-opt-sequence-number >= 8362"
        }
    }
}
```

Note that an Event Hubs endpoint also exposes a Kafka endpoint. While the above options give you fine-grained control over offset management, you might consider using a Kafka source, relying on its automatic checkpoint offset management. Typically, a Kafka source which is deactivated then reactivated automatically receives events from the last checkpointed offset.
