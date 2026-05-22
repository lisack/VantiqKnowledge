# Google Cloud Pub/Sub Source Integration

The Google Cloud Pub/Sub (GCPS) messaging service provides the ability to send and receive messages over the Google Cloud. Vantiq offers direct integration with GCPS through sources, which can produce messages to Google Topics and consume messages from Google Subscriptions. For more information on GCPS, take a look at the [Google Cloud Documentation](https://cloud.google.com/pubsub/docs/).

The basic process for setting up and using a GCPS Source is as follows:

* An administrator defines a GCPS source by identifying the Google Cloud Project containing the desired set of topics/subscriptions, along with the Google Key that is used to authenticate. Optionally, the administrator can define a list of subscriptions from which the source will listen for messages. This is accomplished in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.
* Once the GCPS source has been defined, the server will begin listening for messages as they arrive on the specified subscriptions (assuming they were included in the source definition).
* When a message arrives on the source endpoint, an event is generated which will trigger the execution of any subscribed rules.  The event may also be delivered to any clients with transient subscriptions on the event's id.
* Source processing rules are encouraged to store any persistent state in the Vantiq automation model.  This enables the rule itself to be stateless, making it easier to support various load balancing approaches such as executing the rule across a cluster or partitioning work between multiple Vantiq servers.

## GCPS Source Representation

A **source** resource defines the integration with a set GCPS topics/subscriptions and must contain the following properties:

* **name:** The name of the stream given by the user
* **type:** Must be the string **GCPS** indicating this is a GCPS source.
* **config:** A JSON object containing additional GCPS configuration parameters:
	* **projectID:** The ID for the Google Cloud Project containing the topics and subscriptions to connect to. This value must be a string.
	* **googleKey:** The Google Key (JSON) used to authenticate. The key can be entered directly here, or it can be stored as a Vantiq Secret, in which case the value would be a secret reference (i.e. "/system.secrets/myGoogleKeySecret").
	* **googleKeyType:** The type for the aforementioned Google Key. This value must either be "secret", or "plain text".
	* **subscriptionsIDs:** (Optional) A list of the GCPS Subscriptions that the source will consume messages from. This must be a list of strings.
	* **pollingInterval:** (Optional) The frequency (in milliseconds) at which the source will poll for messages from GCPS Subscriptions.

## Create a GCPS Source

The following example illustrates how to create a GCPS source using the REST API. GCPS sources can also be defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**.

```
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
	"name": "myGcpsSource",
	"type": "GCPS",
	"config": {
		"projectID": "myGcpsProjectID",
 		"googleKey": "/system.secrets/myGoogleKeySecret",
 		"googleKeyType": "secret",
 		"subscriptionIDs": ["myFirstGcpsSubscription", "mySecondGcpsSubscription", ...],
        "pollingInterval": 500
	}
}
```

## Delete a GCPS Source

The example GCPS source named **myGcpsSource** can be deleted using the REST API by issuing the following request:

```
DELETE https://dev.vantiq.com/api/v1/resources/sources/myGcpsSource
```
    
## Produce Messages on a GCPS Topic 
Messages are produced on GCPS topics in VAIL with the **PUBLISH** command. The **PUBLISH** request for GCPS sources takes a minimum of two parameters:

* **topicID:** The GCPS Topic to which the message will be published  
* At least one of the following:  
    * **message:** Considered the body of the message, this value must be a String.  
    * **attributes:** A series of key-value pairs that must be Strings.

For Example:
```
PUBLISH { topicID: "myGcpsTopic", message: "my message"} TO SOURCE myGcpsSource
```
OR
```
var attribs = {}
attribs.myKey = "myValue"

PUBLISH { topicID: "myGcpsTopic", attributes: attribs} TO SOURCE myGcpsSource
```

Of course, both attributes and messages can be specified in the same PUBLISH command, as follows:
```
var attribs = {}
attribs.myKey = "myValue"

PUBLISH { topicID: "myGcpsTopic", message: "my message", attributes: attribs} TO SOURCE myGcpsSource
```

Additionally, the user can specify an **orderingKey**, so long as the source configuration has set the **enableMessageOrdering** field to `true`. Typically, the **orderingKey** should be one of the keys listed in the **attributes** portion of the message. The **orderingKey** must be a String, as follows:
```
var attribs = {}
attribs.myKey = "myValue"
attribs.count = 1

PUBLISH { topicID: "myGcpsTopic", message: "my message", attributes: attribs, orderingKey: "count"} TO SOURCE myGcpsSource
```

## Consuming Messages from GCPS Subscriptions

The GCPS Source will only listen for messages arriving on subscriptions set in the source configuration. These messages will appear as messages arriving from the given source, and they will be formatted as follows:

```
{
  "data": string,
  "attributes": {
    string: string,
    ...
  },
  "messageId": string,
  "publishTime": string,
  "subscriptionId": string
}
```

* The `data` field is considered the body of the message, and is a string.
* The `attributes` field is a series of key-value string pairs.
* The `messageId` field is set by the Google Cloud, and is unique within the message's topic.
* The `publishTime` field is set by the Google Cloud, and designates the time at which the message was published.
* The `subscriptionId` field specifies the subscription from which the message arrived.

To trigger a rule whenever a message is consumed from a GCPS source, one could use a rule similar to this: 

```
RULE myGcpsRule
WHEN EVENT OCCURS ON "/sources/myGcpsSource" AS msg

// (User can handle msg here, this is just an example)
log.debug("Received a message from {} with publish time: {}, and ID: {}",
          [msg.subscriptionId, msg.publishTime, msg.messageId])

// This assumes that the message has attributes named "count" and "type"
INSERT MyVantiqType(messageBody: msg.data,
                    messageCount: msg.attributes.count,
                    messageType: msg.attributes.type)
```