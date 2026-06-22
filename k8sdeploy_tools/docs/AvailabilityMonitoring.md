# Availability Monitoring

## Overview

This document is about monitoring of Vantiq installations. Monitored Vantiq installations send regular
heartbeat messages to Vantiq Monitoring installations. Monitoring installations alert a set of pre-defined
users whenever heartbeats are not received within a one-minute window.

Availability Monitoring is composed of two distinct Vantiq applications acting together: an application
sending heartbeats (installed on the installation being monitored) and an application processing heartbeat
reception (installed on the monitoring side, by default this is https://api.vantiq.com but that is not
required).

## Setting Up Availability Monitoring Vantiq Applications

The following two documents describe how to monitor a new Vantiq installation:

- [Heartbeat Provisioning](AvailabilityMonitoring_AsUser.md): how to install and provision a Vantiq heartbeat
on the installation to monitor. The person responsible for the heartbeat installation contacts *Vantiq
Support*, collects a set of required information then proceeds with heartbeat installation following the
document instructions.
- [Monitor Provisioning](AvailabilityMonitoring_AsSupport.md): how to install a new monitor to collect and
process the heartbeat messages received from the new monitored installation. This document is targeted at a
person acting as *Vantiq Support* with administrative access to the monitoring installation.

## Setting Up Availability Monitoring via Opsgenie Heartbeats

An additional mechanism to monitor an installation's availability is to use
[Opsgenie Heartbeats](https://support.atlassian.com/opsgenie/docs/add-heartbeats-to-monitor-external-systems/).
This is optional and can be done in addition to the Vantiq heartbeats described above. Two documents
describe this process:

- [Opsgenie Heartbeat Provisioning](AvailabilityMonitoringOpsgenie_AsUser.md): how to install and provision an
Opsgenie heartbeat on the installation to monitor (a Vantiq project configured to send Opsgenie heartbeats).
- [Opsgenie Monitor Provisioning](AvailabilityMonitoringOpsgenie_AsSupport.md): how to create a new Opsgenie
heartbeat within Opsgenie, so Opsgenie heartbeats received from the new monitored installation can be
accounted for and alerts raised when heartbeats are not received. This document is targeted at a person acting
as *Vantiq Support* with administrative access to Opsgenie.

If you are managing a private Vantiq cloud installation and using an alerting system other than Opsgenie for
monitoring infrastructure, you may be able to use these Opsgenie documents as a roadmap to set up similar
monitoring in the alerting system you are using.
