# Availability Monitoring - Heartbeat Provisioning

***Last updated 08 Sep 2021***

Availability Monitoring is composed of two distinct pieces acting together: a Vantiq monitor project installed
on a monitoring site and a Vantiq heartbeat project installed on the site to be monitored. This document is about
the heartbeat project, explaining how to install a heartbeat to monitor the availability of a Vantiq installation.
A different document, [`Monitor Provisioning`](AvailablityMonitoring_AsSupport.md) explains how to install a monitor.

## Prerequisites

Contact [Vantiq Support](mailto:support@vantiq.com) to get the following information:

- `monitor name` - a short string value characterizing the site to be monitored
- `monitoring site URL` - address where heartbeat requests are sent
- `authentication token` - authentication to the monitoring site so heartbeat requests can be sent

additionally you might also decide on,

- `monitor friendly name` - a string value characterizing the site that appears in email notifications
- `operators emails` - persons receiving availability email notifications

## Heartbeat setup

A heartbeat is sent from the monitored site to the monitoring system every 5 seconds via the `heartbeat` project.
If no heartbeat is received by the monitoring site within a 60 seconds window, the monitored system is considered
`offline`. As soon as a heartbeat is received again the monitored site is considered back `online`.

On the site to monitor,

- create a `vantiq_monitor` Namespace in the Vantiq Organization, then switch to `vantiq_monitor` Namespace,
- create a `heartbeat` project
- create a `heartbeatVantiq` Rule and replace `<monitor_name>` below by the monitor name provided by *Vantiq Support*

```
  RULE heartbeatVantiq 
  WHEN EVENT OCCURS ON "/topics/monitor/heartbeat"

  PUBLISH {name: "<monitor_name>"} TO TOPIC "/heartbeat/signal" PROCESSED BY ars_properties.role == "supervisor"
```

- create a `heartbeatEvent` scheduled event, publishing to `/monitor/heartbeat` topic. Make it active,
set interval to 5 seconds
- optionally create a ScheduledEventChecker subscription
- create a monitor Node named `monitor` using the `monitoring site URL` and `authentication token` values provided
by *Vantiq Support*. Specify a property named `role` with value `supervisor`. Test the Node connection.

Make sure that the `heartbeatVantiq` is saved and active, then let *Vantiq Support* know that the heartbeat
is setup.

## Example

A development Vantiq installation is deployed for the company Acme as a Vantiq Managed Private Cloud.
Alice is responsible to install a heartbeat on this Vantiq installation.

Alice contacts *Vantiq Support* and gets the following information:

- `monitor name`: acme-dev
- `monitoring URL`: https://api.vantiq.com
- `authentication token`: G8eSb5XF38uuaraVkn5E6IC0U4YXhEyAQ278cLHjd4E=  *(token example)*

additionally, Alice tells Support which person(s) should be automatically notified by the availability monitoring
system and agree on a friendly name that will get included in the email notifications,

- `monitor friendly name`: Acme Development
- `operators emails`: support@vantiq.com, bob@dev.acme.org *(additional person)*

Alice creates a `vantiq_monitor` Namespace as described in the setup instructions, creating the `heartbeatVantiq` Rule
and `monitor` Node with the provided information,

```
  RULE heartbeatVantiq 
  WHEN EVENT OCCURS ON "/topics/monitor/heartbeat"

  PUBLISH {name: "acme-dev"} TO TOPIC "/heartbeat/signal" PROCESSED BY ars_properties.role == "supervisor"
```

```
  Type:            Peer
  Name:            monitor
  URI:             https://api.vantiq.com
  Credential Type: Access Token
  Access Token:    G8eSb5XF38uuaraVkn5E6IC0U4YXhEyAQ278cLHjd4E=
  Properties:
      name:        role
      value:       supervisor
```

After completing the instructions, Alice notifies Support that the heartbeat is installed on the monitored site
so Support can complete the Acme monitoring setup.

## Template project

A [Heartbeat project template](HeartbeatTemplateProject.zip) can be found in this document directory.
If you use this project template,

- edit the `heartbeatVantiq` Rule to specify the correct `monitor name`
- create a `monitor` Node as shown above, with the correct `monitoring URL` and `authentication token` information
