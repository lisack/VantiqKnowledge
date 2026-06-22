# Availability Monitoring - Opsgenie Heartbeat Provisioning

***Last updated 08 Oct 2021***

Availability Monitoring with Opsgenie is composed of two distinct pieces acting together: an Opsgenie heartbeat
defined within Opsgenie and a Vantiq Opsgenie heartbeat project installed on the site to be monitored. This document
is about the Opsgenie heartbeat project, explaining how to install a heartbeat based on Opsgenie to monitor
the availability of a Vantiq installation. A different document, `Opsgenie Monitor Provisioning` explains
how to create the Opsgenie heartbeat definition within Opsgenie.

Note that a site can be monitored by both an Opsgenie heartbeat project *and* a Vantiq heartbeat project (see
[Heartbeat Provisioning](AvailablityMonitoring_AsUser.md)). These two mechanisms are independent and not exclusive.

## Prerequisites

Contact [Vantiq Support](mailto:support@vantiq.com) to get the following information:

- `heartbeat name` - a short heartbeat string name characterizing the site to monitor
- `Opsgenie API Key` - credential token necessary to send heartbeat requests to Opsgenie

additionally you might also decide with *Support* on any additional person that should receiving availability email
alerts from Opsgenie.

## Heartbeat setup

A heartbeat request is sent from the monitored site to an Opsgenie Heartbeat URL every 10 seconds
via the `heartbeatOpsgenie` project.
If no heartbeat is received by Opsgenie within a 60 second window, the monitored system is considered
`offline`. As soon as a heartbeat is received again by Opsgenie the monitored site is considered back `online`.

On the site to monitor,

- if the `vantiq_monitor` Namespace does not exist, create a `vantiq_monitor` Namespace in the Vantiq Organization
- switch to `vantiq_monitor` Namespace
- import the [`heartbeatOpsgenie` project](HeartbeatOpsgenieProject.zip), the project includes:
  - Procedure - `sendOpsgenieHeartbeat` *- no need to change*
  - Rule - `heartbeatOpsgenie` *- need to specify the heartbeat name and activate the Rule*
  - ScheduledEvent - `heartbeatEventOpsgenie` *- need to activate the Scheduled Event*
  - Source - `OpsgenieHeartbeatSource` *- need to specify Access Token Secret and activate the Source*
  - Topic - `/opsgenie/heartbeat`

- create a Secret named `OpsgenieAccessKey` using the `Opsgenie API Key` value provided by *Support*
- edit the Source to specify this Secret as the Access Token Credential, then activate the Source
- edit the Rule `heartbeatOpsgenie` Rule and replace `<opsgenie_heartbeat_name>` with the `heartbeat name` provided by
*Support*
- save the Rule and make sure that the Rule is active
- activate the Scheduled Event starting now

Save the `heartbeatOpsgenie` project then let *Support* know that the Opsgenie heartbeat is setup.

## Example

A development Vantiq installation is deployed for the company Acme as a Vantiq Managed Private Cloud.
Carol is responsible to install an Opsgenie heartbeat on this Vantiq installation.

Carol contacts *Vantiq Support* and gets the following information:

- `heartbeat name`: aliveness-acme-dev
- `Opsgenie API Key`: b7cafe4d-8372-3971-efac-4e2c4fcfcafe  *(key example)*

additionally, Carol tells Support which person(s) should be automatically notified by the Opsgenie heartbeat system.

Carol creates a `vantiq_monitor` Namespace as described in the setup instructions, and imports the `heartbeatOpsgenie`
project, then following the instructions:

- define a Secret named `OpsgenieAccessKey` with the value `b7cafe4d-8372-3971-efac-4e2c4fcfcafe` provided by
*Support*.
- edit the Source to specify the Access Token Secret

```text
  Credential Type = Access Token
  Access Token Type = Secret
  Access Token = OpsgenieAccessKey
  Realm = GenieKey
```

- activate and save the Source
- edit the Rule `heartbeatOpsgenie` and replace `<opsgenie_heartbeat_name>` by `aliveness-acme-dev`
- activate and save the Rule
- activate the Scheduled Event `heartbeatEventOpsgenie`, starting now
- save the project

Carol notifies *Support* that the Opsgenie heartbeat is installed on the monitored site so *Support* can complete
the Opsgenie monitoring setup for the Acme site.

## Template project

An [Opsgenie Heartbeat project template](HeartbeatOpsgenieProject.zip) can be found in this document directory and
imported as directed above.
