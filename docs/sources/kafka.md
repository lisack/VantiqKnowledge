# Kafka Source Integration

Apache Kafka is a popular open-source project for building data processing pipelines. Vantiq offers direct integration with Kafka through sources, which can both consume and produce messages on Kafka topics. For more information on Kafka, take a look at the [Apache Documentation](https://kafka.apache.org/documentation/).

The basic process for starting up a Kafka Source and reading messages as they arrive on a topic is as follows:

* An administrator defines a Kafka source by identifying the bootstrap.servers endpoint and the topics that messages will be consumed from. This is accomplished in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.
* Once the Kafka source has been defined, the server will begin listening for messages as they arrive on the specified topics.
* When a message arrives on the source endpoint an event is generated which will trigger the execution of any subscribed rules.  The event may also be delivered to any clients with transient subscriptions on the event's id.
* Source processing rules are encouraged to store any persistent state in the Vantiq automation model.  This enables the rule itself to be stateless making it easier to support various load balancing approaches such as executing the rule across a cluster or partitioning work between multiple Vantiq servers.

## Kafka Source Representation

A **source** resource defines the integration with a set Kafka topics and contains the following properties:

* **name** the name given the stream by the user
* **type** must be the string **KAFKA** indicating this is a Kafka source.
* **config** a JSON object containing additional Kafka configuration parameters:
	* **bootstrap.servers** the endpoint of a broker in the Kafka cluster used to initiate the consumer.
	* **consumer.topics** the list of topics from which the stream will consume messages.

The [Kafka Broker Configuration Documentation](https://kafka.apache.org/documentation/#brokerconfigs) describes many 
additional configuration values which can also be applied in a Kafka source config. Additional config properties should 
be defined in the config object the same way as "_bootstrap.servers_" (see example below). Any config values that should 
only apply to the consumer should be prefixed with "_consumer._" (i.e: "consumer.key.deserializer"), while configs that 
only apply to producing messages should be prefixed with "_producer._" (i.e: "producer.key.serializer"). 

NOTE: The values of numeric configuration properties, such as "max.in.flight.requests.per.connection", must be expressed 
as strings in quotes rather than as numbers. If values are expressed as numbers in the source configuration you may
encounter the following error `org.apache.kafka.common.config.ConfigException` because of a type mismatch. If you see
this error, double check the source configuration for any numeric values and try wrapping the values in quotes. 

## Create a Kafka Source

The following example illustrates how to create a Kafka source using the REST API. Kafka sources can also be defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
	"name": "myKafkaSource",
	"type": "KAFKA",
	"config": {
		"bootstrap.servers": "localhost:9092",
 		"consumer.topics": ["topic1", "topic2", "topicX"]
	}
}
```

If the source is intended to only publish messages, do not specify the `consumer.topics` property.

## Delete a Kafka Source

The example Kafka source named **myKafkaSource** can be deleted using the REST API by issuing the following request:

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/myKafkaSource
```
    
## Produce Messages on a Kafka Topic 
Messages are produced on Kafka topics in VAIL with the **PUBLISH** command. The **PUBLISH** request for Kafka sources takes a minimum of three parameters: the value (and optionally key) to send, the Kafka source, and topic to which the publish is sent. For example:

```
PUBLISH { value: "somevalue", key: "somekey"} TO SOURCE myKafkaSource USING { topic: "topicX" }
```

Note that in the above example, the key in the published object is optional. To trigger a rule whenever a message is consumed from a kafka source, use the following rule trigger: 

```
RULE myKafkaRule
WHEN EVENT OCCURS ON "/sources/myKafkaSource" AS msg
log.info("Received message: {}", [msg])
```

One important note is that by default, keys and values produced and consumed from kafka topics will be serialized and deserialized as strings. So even if a message is written to a kafka topic external to the Vantiq system, and the value is in JSON format, when the message is consumed by a Vantiq rule the value will be encoded as a string.

## Consume Messages
A Kafka source is configured to consume messages from one or more topics by specifying the `consumers.topics` property.
The consumer group, defined by the `group.id` property, defaults to `<namespace>:<source_name>`. Once Kafka has assigned 
the topics' partitions to group consumers, messages are read and delivered from their last committed offset.

In development phase, it might be useful to start reading messages from the last offset instead of the last committed
offset, so messages published while the source is not active are skipped. This can be done be specifying the consumer 
configuration property `seekToEnd` and setting it to `true`. When not specified, this configuration property
defaults to `false`.

For example,
```
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "consumer.seekToEnd": "true"
    }
}
```

Note that setting `seekToEnd` does not guarantee to skip all missed messages as Kafka might deliver some before
moving the partition offset to the end.

## QoS

The default QoS for a published message is `AT_LEAST_ONCE`. This default can be changed by using
standard Kafka configuration settings. For example, adding the following to a source configuration,
```
    "producer.acks": "0"
```
changes a publisher QoS to `AT_MOST_ONCE`.

The QoS for a Kafka consumer is `AT_LEAST_ONCE`: a message received from a Kafka broker
is acknowledged by the Vantiq server _after_ proper processing. For example, 
if a source is configured for a `Delivery Mode` of `At Least Once`, events received by the source consumers
are persisted before being acknowledged to the Kafka broker. 

The  Kafka consumer QoS `AT_LEAST_ONCE` defines the QoS between Kafka broker and Kafka consumer. A source `Delivery Mode` setting defines the QoS between Kafka consumer and Vantiq resources. For example, a rule receiving an event
from a Kafka source has a QoS composed of two segments: the QoS from the Kafka broker to the Kafka consumer (`AT_LEAST_ONCE`) and the QoS from the Kafka consumer to the Vantiq rule ([`Delivery Mode`](../reliability.md)).

## Serialization and contentType

A Kafka source always defines the message wire format by specifying a serializer and deserializer. A serializer defines the wire format for publishing messages and a deserializer the format for consuming messages.

By default a Kakfa source is configured to use a `StringSerializer` and `StringDeserializer` for both key and message value. The default setting used by the Kafka source is,

```
"key.deserializer": "org.apache.kafka.common.serialization.StringDeserializer"
"value.deserializer": "org.apache.kafka.common.serialization.StringDeserializer"
"key.serializer": "org.apache.kafka.common.serialization.StringSerializer"
"value.serializer": "org.apache.kafka.common.serialization.StringSerializer"
```

To override this default setting to specify a different message wire format, you can specify a [`contentType` property](#content-type) or define a different value for `value.serializer` and/or `value.deserializer`.

For example, to publish and receive JSON messages, you could define

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "value.deserializer": "io.vertx.kafka.client.serialization.JsonObjectDeserializer",
        "value.serializer": "io.vertx.kafka.client.serialization.JsonObjectSerializer"
    }
}
```

Note that in the above example key settings are not provided and would therefore default to `StringSerializer` and `StringDeserializer`.

### Content Type

You can specify the message wire format by setting the configuration property `contentType` to one of the following values:

```
text/plain
application/json
application/xml
```

The property `contentType` can be specified on the source configuration, on the source consumer configuration and/or source producer configuration. For example,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "contentType": "application/json"
    }
}
```

would set the wire format to be JSON for both producer and consumer and is equivalent to,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "consumer.contentType": "application/json",
        "producer.contentType": "application/json"
    }
}
```

And,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "contentType": "application/json",
        "consumer.contentType": "text/plain"
    }
}
```

would set the wire format to JSON for publishing messages and String for receiving messages. Which is equivalent to,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9092",
        "consumer.topics": ["topic1", "topic2"],
        "consumer.contentType": "application/json",
        "producer.contentType": "text/plain"
    }
}
```

Any `value.serializer` or `value.deserializer` setting takes precedence over a `contentType` setting.

`consumer.contentType` and `producer.contentType` override the configuration `contentType` (see examples above).

If neither `value.serializer`/`value.deserializer` nor `contentType` properties are defined, a Kafka configuration uses its default `StringSerializer` and `StringDeserializer` settings, equivalent to `text/plain`.

The `contentType` property only applies to the message wire format. If a key wire format must be changed from its default String serializer, use an explicit `key.serializer`/`key.deserializer` setting.

For published messages (producer), the message value type must match the type implied by the `contentType` setting. For JSON, the message value type must be a VAIL Object, for Text this must be a String and for XML this must be an Object representing an XML structure (e.g., as returned by the `parseXml` parsing procedure).

Similarly, a received message value (consumer), has the type implied by its `contentType` setting: a JSON Object representation (VAIL Object), a String or an Object representing an XML structure.

## Azure Event Hubs Configuration examples

To create a Kafka Azure Source configuration use the content of an Azure Connection String located in Azure Shared Access Policies. 

The below examples assume an Azure namespace `vqhubns`, an Event Hub named `vqs_eventhub` and the Policy `EventUser` with the following Connection String:

```http
Endpoint=sb://vqhubns.servicebus.windows.net/;SharedAccessKeyName=EventUser;
         SharedAccessKey=QzaPHKfvqH28m2n9OycDo2Y7o7Nrwkx8z3pXziNz2C0=
```

Please refer to the Azure documentation for configuration details.

### Producer

A Kafka source configuration to publish messages to the above Azure Event Hub is:

```json
{
    "bootstrap.servers": "sb://vqhubns.servicebus.windows.net:9093",
    "sasl.jaas.config": "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"Endpoint=sb://vqhubns.servicebus.windows.net/;SharedAccessKeyName=EventUser;SharedAccessKey=QzaPHKfvqH28m2n9OycDo2Y7o7Nrwkx8z3pXziNz2C0=\";",
    "sasl.mechanism": "PLAIN",
    "security.protocol": "SASL_SSL",
    "request.timeout.ms": "25000",
    "metadata.max.idle.ms": "180000",
    "connections.max.idle.ms": "180000",
    "metadata.max.age.ms": "180000"
}
```  

### Producer and consumer

A Kafka source configuration acting both as producer and consumer for the above Azure Event Hub is:

```json
{
    "bootstrap.servers": "sb://vqhubns.servicebus.windows.net:9093",
    "sasl.jaas.config": "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"Endpoint=sb://vqhubns.servicebus.windows.net/;SharedAccessKeyName=EventUser;SharedAccessKey=QzaPHKfvqH28m2n9OycDo2Y7o7Nrwkx8z3pXziNz2C0=\";",
    "sasl.mechanism": "PLAIN",
    "security.protocol": "SASL_SSL",
    "consumer.group.id": "$Default",
    "producer.request.timeout.ms": "25000",
    "producer.metadata.max.idle.ms": "180000",
    "connections.max.idle.ms": "180000",
    "metadata.max.age.ms": "180000",
    "consumer.topics": [
        "vqs_eventhub"
    ]
}
```  

Note that configuration settings must follow [Microsoft recommendations](https://learn.microsoft.com/en-us/azure/event-hubs/apache-kafka-configurations). For example `connections.max.idle.ms` in the configuration above takes into account the default
Azure idle inbound TCP connection timeout. Setting this property allows the client to initiate a clean connection
termination when communication between client and Azure Event Hubs remains idle. If left unspecified, Azure
drops connection first which can leave a client connection in a phantom state and cause timeouts when publishing
requests, until the client eventually detects that the connection has been terminated.

## SSL Setup

A Kafka source can be configured to connect over SSL using the `ssl.*` 
[configuration properties](https://kafka.apache.org/documentation.html#security_ssl).

Both one-way and two-way SSL are supported, providing the proper configuration.

For example, assuming that `kafka_client_truststore.jks` contains the server certificate signing CA,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9093",
        "consumer.topics": ["topic1", "topic2"],
        "security.protocol": "SSL",
        "ssl.truststore.location": "kafka_client_truststore.jks",
        "ssl.truststore.password": "store_password"
    }
}
```

Also, assuming proper configuration with a server set to require client certificate authentication (`ssl.client.auth=required`) and a client key store containing the client certificate,

```json
{ 
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9093",
        "consumer.topics": ["topic1", "topic2"],
        "security.protocol": "SSL",
        "ssl.truststore.location": "kafka_client_truststore.jks",
        "ssl.truststore.password": "store_password",
        "ssl.keystore.location": "kafka_client_keystore.jks",
        "ssl.keystore.password": "keystore_password",
        "ssl.key.password": "key_password"
    }
}
```

Relying on the support for [PEM format for SSL certificates and private key](https://cwiki.apache.org/confluence/display/KAFKA/KIP-651+-+Support+PEM+format+for+SSL+certificates+and+private+key),
it is possible to configure a Kafka source using the PEM format of cryptographic keys and certificates.

For example, assuming we have the server certificate signing CA in PEM format, the above one-way configuration could be expressed as,

```json
    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9093",
        "consumer.topics": ["topic1", "topic2"],
        "security.protocol": "SSL",
        "ssl.truststore.certificates": "-----BEGIN CERTIFICATE-----\nMIIDQj21........3xIRUUSGcUdTw==\n-----END CERTIFICATE-----",
        "ssl.truststore.type": "PEM"
    }
```

Note that the base64 representation of the certificate is specified as one line without `\n`.

The certificate value can also be stored as a Secret and [referenced in the configuration](source.md#using-secrets),

```json
# With the base64 representation of the certificate stored as a Secret named Root_CA

    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9093",
        "consumer.topics": ["topic1", "topic2"],
        "security.protocol": "SSL",
        "ssl.truststore.certificates": "-----BEGIN CERTIFICATE-----\n@secrets(Root_CA)\n-----END CERTIFICATE-----",
        "ssl.truststore.type": "PEM"
    }
```

and,

```json
# With the certificate PEM value stored as a Secret named PEM_Root_CA

    "name": "myKafkaSource",
    "type": "KAFKA",
    "config": {
        "bootstrap.servers": "localhost:9093",
        "consumer.topics": ["topic1", "topic2"],
        "security.protocol": "SSL",
        "ssl.truststore.certificates": "@secrets(PEM_Root_CA)",
        "ssl.truststore.type": "PEM"
    }
```

If you create a secret with the PEM value make sure to escape the PEM header and footer `\n` character.

For example,

```
 Name:        PEM_Root_CA
 Description: Root Certificate
 Secret:      -----BEGIN CERTIFICATE-----\\nMIIDQj21........3xIRUUSGcUdTw==\\n-----END CERTIFICATE-----
```
