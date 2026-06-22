# Availability Monitoring - Opsgenie Monitor Provisioning

***Last updated 08 Oct 2021***

Availability Monitoring with Opsgenie is composed of two distinct pieces acting together: an Opsgenie heartbeat
defined within Opsgenie and a Vantiq Opsgenie heartbeat project installed on the site to be monitored. This document
explains how to configure Opsgenie to create a heartbeat definition.

The reader of this document acts as [Vantiq Support](mailto:support@vantiq.com), referred to below as *Support*.
The person provisioning the site that must be monitored follows the instructions described in the
[`Opsgenie Heartbeat Provisioning`](AvailablityMonitoringOpsgenie_AsUser.md) document and is referred to below
as the *User*.

## Prerequisites

As *Support*, work with the *User* to agree on the heartbeat name. The heartbeat name
must be unique across all Opsgenie heartbeat names. The following naming pattern is suggested : `aliveness-<site_name>`.

Discuss with the *User* about any additional person that should receive notification emails. Note that any
additional person must be a known Opsgenie member in order to receive email notifications.

Create an API Key. Assuming sufficient Opsgenie privileges, go to Settings / API Key management and create a new API
key named `AlivenessHeartbeatKey_<site_name>`. Access Rights must be set to `Create and Update`.

We suggest creating one API Key per heartbeat definition but the same API key can be used for many
heartbeat definitions.

Provide the *User* with both the `aliveness-<site_name>` heartbeat name and an API key value. Key value must be provided
out of band in a secure fashion.

## Heartbeat definition

Assuming the necessary Opsgenie privileges, go to Settings / Heartbeats and click on `Create heartbeat`.

- in the `Name` field, enter the value `aliveness-<site_name>` that you provided to the *User*
- enter a `Description` value, for example,

```text
No heartbeat received from <site_url> within the last minute. Check that <site_url> is up.
```

or, copy/edit a description from another existing heartbeat definition.

- select the `Team` - it should include the additional persons that the *User* specified
- set the `Alert` properties (P2 or P1)
- initially, select an `Interval` of 1 day but do *not* activate the heartbeat yet

Once the *User* is done setting up the monitored site and heartbeats are expected to be received, enable the heartbeat.

In the list of heartbeats, refresh the browser and check the `Last received at` column. It must be updated every
minute since a heartbeat should be received every 10 seconds. If not, the monitored site is not correctly provisioned.

Once you confirmed that the `Last received at` column is being updated, change the heartbeat Interval to 1 minute and
activate the heartbeat.

You can tell the *User* that the heartbeat is now live.

## Template project

Because all definitions are performed within Opsgenie there is no Vantiq Monitoring project involved.

## Technical Background

This section provides some technical background about Opsgenie Heartbeats and how they can be integrated into in a
Vantiq Heartbeat project (what the *User* is setting up on the monitored site).

### Definition

An Opsgenie Heartbeat is defined with:

- name
- description
- team
- interval (minutes, hours or days)
- alert message

Ping messages must be sent to the Heartbeat within the defined interval otherwise an Alert is sent to the Team.

### Request

The following message sends a ping message to an Opsgenie Heartbeat:

```
curl -X GET 'https://api.opsgenie.com/v2/heartbeats/<heartbeat_name>/ping' --header 'Authorization: GenieKey <api_key>'
```

The Verb could also be POST, PATCH or PUT (same outcome).

The API Key must have the access rights `Create and update`.

If the API Key does not have the proper access rights, the ping request fails:

```
{"code":40301,"message":"API Key is not granted with write access.","took":0.0,"requestId":"170546ed-46ea-4983-a44d-4fe0276a1580"}
```

If the specified `<heartbeat_name>` is incorrect (i.e., does not exist), the ping request *succeeds* and no heartbeat
gets updated within Opsgenie.

### VAIL code

To send a Heartbeat request to Opsgenie a `Remote` source (to Opsgenie) must be defined with:

- Source URI (to OpsGenie)
- Credentials (API key)
- Authentication Realm (`GenieKey`)

For example,

```
# Remote Source "OpsGenieHeartbeatSource"

{
    "accessTokenType": "secret",
    "accessToken": "/system.secrets/OpsGenieAccess",
    "realm": "GenieKey",
    "pollingInterval": 0,
    "uri": "https://api.opsgenie.com/v2/heartbeats/",
    "query": {},
    "requestDefaults": {}
}
```

The example above assumes a Secret named `OpsGenieAccess` where the API key has been set (PlainText works but Secret
is better to protect the API key).

Then the VAIL code to send a ping request is one line, for example:

```
select from SOURCE OpsGenieHeartbeatSource with path = "myHeartbeat/ping"
```

the return value is,

```
var pong = select from SOURCE OpsGenieHeartbeatSource with path = "myHeartbeat/ping"
log.info(stringify(pong))

[{"result":"PONG - Heartbeat received","took":0.009,"requestId":"3e099963-a928-4d0a-920d-7699ec2fcd3d"}]
```
