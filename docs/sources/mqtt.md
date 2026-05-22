# MQTT Source Integration

MQTT is commonly used as a means of exchanging streaming data. Vantiq includes direct support for reading MQTT data streams. The essence of the integration is as follows:

* An administrator defines an MQTT source by identifying the MQTT endpoint, any credentials associated with the endpoint and the topic(s) to which to subscribe. This is accomplished via the updateStream request detailed below or in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.
* Once the MQTT source has been defined, the server constructs a separate thread to accept inbound messages from the MQTT source.
* When a message arrives on the source endpoint an event is generated which will trigger the execution of any subscribed rules.  The event may also be delivered to any clients with transient subscriptions on the event's id.
* Source processing rules are encouraged to store any persistent state in the Vantiq automation model.  This enables the rule itself to be stateless making it easier to support various load balancing approaches such as executing the rule across a cluster or partitioning work between multiple Vantiq servers.

## MQTT Source Representation

A **source** resource defines the integration with a specific MQTT stream and contains the following properties:

* **name** the name given to the stream by the user
* **type** must be the string **MQTT** indicating this is an MQTT source
* **config** a JSON object containing additional MQTT configuration parameters:
	* **serverURIs** the endpoint  for the server hosting the stream. Optionally a list of URIs.
	* **topics** the list of topics to which the stream is subscribed. Multiple streams may be defined on a single serverURI that subscribe to separate topics or overlapping topics. No restrictions are placed on the subscriptions by Vantiq.
	* **username** credentials for accessing the MQTT server
	* **password** credentials for accessing the MQTT server
	* **contentType** the MIME content type of MQTT messages
	* **keepAliveInterval** the keep alive interval for the TCP connection
	* **connectionTimeout** the timeout interval for the connection
	* **maxInflight** the maximum number of messages that will be sent without receiving an ack from the server (default 10)
	* **cleanSession** true if state is not preserved across connection failures; false otherwise
	* **automaticReconnect** true if the client should attempt to reconnect on connection failure
	* **qos** Quality of Service level for the topics the stream subscribes to. QoS is defined as a String with one of the following values: `AT_MOST_ONCE`, `AT_LEAST_ONCE` or `EXACTLY_ONCE`. If not specified, defaults to `AT_LEAST_ONCE`. Note that the QoS for PUBLISH must be specified on the VAIL Publish command-line and defaults to `AT_MOST_ONCE`.

While the configuration properties listed above are the most commonly used, the config JSON object maps to the [Vert.x MQTT Client Options](<https://vertx.io/docs/4.2.3/apidocs/io/vertx/mqtt/MqttClientOptions.html>) configuration. Therefore, any property supported by `MqttClientOptions` can be added to the config object, even if it is not explicitly listed here. One
example would be to specify a maximum message size using the `maxMessageSize` property or configure the client [to use SSL](#ssl-setup).

## Create an MQTT Source

The following example illustrates how to create an MQTT source using the REST API. MQTT sources can also be defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "myMqttSource",
    "type": "MQTT",
    "config": {
        "serverURIs": ["tcp://me.vantiq.com:1883"],
        "topics": ["com/accessg2/stream/mqtt/example"],
        "keepAliveInterval": 30,
        "connectionTimeout": 30,
        "username": "user",
        "password": "password",
        "cleanSession": true
    }
}
```

Alternatively, to use a secret password named "MySecret", change the password property to a reference and specify 'secret' 
as the passwordType like this:


```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "myMqttSource",
    "type": "MQTT",
    "config": {
        "serverURIs": ["tcps://me.vantiq.com:1883"],
        "topics": ["com/accessg2/stream/mqtt/example"],
        "keepAliveInterval": 30,
        "connectionTimeout": 30,
        "username": "user",
        "password": "/system.secrets/MySecret",
        "passwordType": "secret",
        "cleanSession": true
    }
}
```

If the MQTT server is configured to require a secure connection then ensure the configured serverURIs are prefixed with
a secure protocol, such as tcps instead of tcp or mqtts instead of mqtt. 

If the source is intended to only publish messages, do not specify the `topics` property. 

## Delete an MQTT Source

The example MQTT source named **myMqttSource** can be deleted using the REST API by issuing the following request:

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/myMqttSource
```
    
## Publish Notifications via MQTT
Notifications are produced by the rules system when **PUBLISH** is called as a rule action. The **PUBLISH** request for MQTT sources takes three parameters: the message object to send and the source and topic to which the publish is sent. 

For example,

```
PUBLISH { message: { data: "somedata" }} TO SOURCE someMQTTSource 
  USING { topic: "the/mqtt/topic" }
```

### QoS

The default QoS for a published message is `AT_MOST_ONCE`. To specify a specific QoS value use the `qos` property. 

For example,
   
```
PUBLISH { message: { data: "somedata" }} TO SOURCE someMQTTSource 
  USING { topic: "the/mqtt/topic", qos: "AT_LEAST_ONCE" }
```

The default QoS for the topics the stream subscribes to is `AT_LEAST_ONCE`. This default setting can be changed in the source
[configuration](#mqtt-source-representation) by specifying the `qos` configuration parameter. Note that the effective subscriber QoS value
is the lowest QoS value set between publisher and subscriber. For example, if the publisher QoS is `AT_MOST_ONCE`, the subscriber effective QoS
is also `AT_MOST_ONCE` even though the subscriber might be configured with `AT_LEAST_ONCE`.

To enable reliable messaging from the MQTT broker across source restarts, the configuration parameters `clientId` and `cleanSession` must be specified.
`clientId` must be set to a fixed unique value and `cleanSession` must be set to false. The `clientId` value
allows the broker to identify the client session so any message that the broker retained while the source was offline can be delivered.
If `clientId` is not provided in the source configuration or if `cleanSession` is set to true, the session between client and broker lasts
for the time of the network connection.

## SSL Setup

An MQTT source can be configured for either one-way or two-way SSL communication by specifying additional [Vert.x MQTT Client Options](<https://vertx.io/docs/4.2.3/apidocs/io/vertx/mqtt/MqttClientOptions.html>) configuration properties expressed as their JSON representation. Below are some usage examples. Note that SSL configuration properties
for AMQP, MQTT and Remote sources are identical in their usage. You can look at the SSL Setup documentation for those
sources for additional examples.

### One-way SSL

This section's examples assume that the MQTT broker is setup to communicate over SSL with a certificate signed by a CA. The CA certificate is available in a trust store named `sourceTrustStore.jks`. An MQTT source is configured to access
the broker over SSL and the user configuring the source has access to the trust store.

If the trust store is accessible on a file system readable by the Vantiq server (e.g., an edge installation), the trust store could be specified as:

```json
{
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
    "username": "user",
    "password": "password",
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
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
    "username": "user",
    "password": "password",
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
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
    "username": "user",
    "password": "password",
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
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
    "username": "user",
    "password": "password",
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
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
    "username": "user",
    "password": "password",
    "pemTrustOptions": {
        "certValues": ["@secrets(CertAuthority1)", "@secrets(CertAuthority2)"]
    }
}
```

### SSL Client Authentication

In addition to specifying a trust store, an MQTT source configuration can also specify a client certificate.
This is necessary if the broker is setup for mutual authentication and requires the client to authenticate
with a certificate.

The examples below assume a key store named `sourceKeyStore.jks` containing the client certificate
signed by the CA.

If the key store is accessible on a file system readable by the Vantiq server,

```json
{
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
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
    "serverURIs": ["tcps://me.vantiq.com:1883"],
    "topics": ["com/accessg2/stream/mqtt/example"],
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

Refer to the [Vert.x MQTT Client Options](<https://vertx.io/docs/4.2.3/apidocs/io/vertx/mqtt/MqttClientOptions.html>)
document for a complete list of configuration options. Note: in that document, a reference to `Buffer`
means that a base64 encoded value can be specified (e.g., trustStoreOptions). Any `add` method translates into an array
(e.g., pemTrustOptions) and any `set` method translates into a single property setting (e.g., path or value).
