# Managing Vantiq Installations

## Overview

This document contains the details of how to manage a Vantiq cloud installation at the systems admin level. To
do this you will need access to the `system` namespace with System Admin privileges. This will give you access
to the System dashboards in Grafana, proper use of those is the bulk of this document.

If you are not already familiar with the information in the [Background Reference doc](BackgroundReference.md),
it is highly recommended that you review that doc first before reading this one. Doing so will help you
understand this doc more fully. It contains info such as:

  - Components of a Vantiq installation
  - How the `k8sdeploy_tools`, `k8sdeploy` (which populates `vantiqSystem`) and `k8sdeploy_clusters` (which populates `targetCluster`) repos are related
  - The basics of how `helm` works with the overrides in `deploy.yaml` and `k8sdeploy`
  - Best Practices for deploying Vantiq

&nbsp;

## Table of Contents

* [Overview](#overview)
* [Related Documents](#related-documents)
    * [Administrators Reference Guide](#admin_guide)
    * [Workload Management](#workload-management)
    * [Monitoring Namespaces with Grafana](#namespace_grafana)
* [Log Management](#log-management)
    * [Direct Kubernetes Pod Logs via `kubectl logs`](#k8s_pod_logs)
    * [Implement a Log Management System](#log_mgmtsys)
* [Metrics Management](#metrics-management)
    * [Cloud Infrastructure Metrics](#cloud-infrastructure-metrics)
    * [Diagnostic Tools: System Dashboards vs. Cloud Provider Console/Portal](#sysdash_vs_cloudportal)
* [System Dashboards](#system-dashboards)
    * [Selecting the Correct Installation](#select_ins)
    * [Selecting a Single Pod Etc.](#select_pod)
    * [Tips & Shortcuts](#tips)
        * [Changing the Displayed Time Range](#change_timerange)
        * [Moving Through Absolute Time Ranges](#move_timerange)
        * [Shortcut to Select an Absolute Time Range](#select_timerange)
        * [Selecting Items in a Pane](#select_inpane)
        * [Temporary Dashboard Changes](#temp_changes)
    * [Diagnostic Tools: System Dashboards vs. Cloud Provider Console/Portal](#sysdash_vs_cloudportal)
    * [Vantiq Resources](#vantiq-resources)
        * [CPU Utilization](#vr_cpu)
        * [Request Rate and Request Duration](#vr_nginx)
        * [Active WebSockets](#vr_websocket)
        * [Garbage Collector Panes: Times, Heap, Non-Heap](#vr_gc)
            * [See Info on *GC Death Spiral* Pattern](#vr_gcdeath)
            * [Non-Heap Allocation](#vr_nonheap)
        * [Mongo Connection Pool & Requests](#vr_mongo)
    * [Metric Collection Resources](#metric-collection-resources)
        * [CPU Utilization](#mc_cpu)
        * [Garbage Collector Panes: Times, Heap](#mc_gc)
        * [Event Processing](#mc_events)
    * [MongoDB Monitoring](#mongodb-monitoring)
        * [Open Connections, Virtual Memory and CPU Usage](#mongo_cpuetc)
        * [Operations Counters and Active / Queued Operations](#mongo_ops)
        * [Network Activity and Memory](#mongo_netmem)
        * [Wired Tiger Cache, Flushes / Faults and TTL Activity](#mongo_engine)
    * [UserDB Monitoring](#userdb-monitoring)
    * [Organization Activity](#organization-activity)
        * [Usage Cautions for *Organization Activity* and *Organization Activity with Top Namespaces* Dashboards](#oa_cautions)
        * [*Organization Activity* Dashboard Pane Details](#oa_details)
        * [Total Requests Processed and Top Request Rate](#oa_trp_trr)
        * [Global Credit Usage, Top Credit Usage and Top Quota Violations](#oa_credit_quota)
        * [Activity in *ORG*: Credit Usage and Quota Violations](#oa_inorg)
    * [Organization Activity with Top Namespaces](#oatn)
    * [InfluxDB Internals](#influxdb-internals)
* [Important Patterns](#important-patterns)
    * [GC Death Spiral](#gc-death-spiral)
    * [Matching CPU Spikes with Organization Activity](#match_cpu_with_oa)
* [Cautionary Note: Rare Issues with Hazelcast Cluster Formation](#hc_caution)
    * [Option 1: watch all pods, fix them as needed](#hc_caution_fixopt1)
    * [Option 2: scale down everything except `vantiq-0`, then scale back up](#hc_caution_fixopt2)

&nbsp;

## Related Documents

This document is focused only on managing entire Vantiq installations at the System Admin level, which is
mainly done from the `system` namespace. There are several other documents that are useful to reference along
with this document.

<a name="admin_guide"></a>
### Administrators Reference Guide

The first of these is the
[Administrators Reference Guide](https://dev.vantiq.com/docs/system/namespaces/index.html) which covers the
basics for Vantiq administrators: how to authorize users to access a Vantiq installation, how (and why) to
create Vantiq namespaces, etc. Nearly everything in the *Administrators Reference Guide* applies to Org Admins,
but anyone with System Admin privileges in a Vantiq installation should know how to perform Org Admin tasks so
make sure to read it.

### Workload Management

The [Workload Management](https://dev.vantiq.com/docs/system/workloadmanagement/index.html) guide describes
the workload management system inside the Vantiq server. This system controls each Organization's resource
usage to minimize the impact of excess resource usage by one application system on all other application
systems. The workload management techniques used by the Vantiq server include:

* Quotas
* Rate Limiting
* Credit-based Work Management
* Buffering
* Isolated Organizations

You should read the *Workload Management* doc to gain understanding of these Vantiq server features, in order
to understand some of the Grafana system dashboards documented below such as the `Organization Activity`
dashboard.

<a name="namespace_grafana"></a>
### Monitoring Namespaces with Grafana

Related to the Workload Management guide is the
[Monitoring Namespaces with Grafana](https://github.com/lisack/grafana/blob/main/grafana.md) guide which
documents the Vantiq-level Grafana dashboards used by Vantiq application developers and Org Admins. These
dashboards allow them to see in detail how their applications are behaving.

Note that there is a passing reference to the Vantiq-level Grafana dashboards in the
[*Development App* section of the *Vantiq IDE User’s Guide*](https://dev.vantiq.com/docs/system/ide/index.html#administer)
but it contains no information about the Vantiq-level Grafana dashboards themselves. The *Monitoring
Namespaces with Grafana* guide contains that info, and is currently a document created and maintained by the
Vantiq Training department for use with our training classes.

Since you are managing entire Vantiq installations at the System Admin level, you will mainly be focused on
the system dashboards. However, even with dashboards like the `Organization Activity` dashboard your ability
to see the details of what is happening in an application are limited, that detail is found in the
Vantiq-level Grafana dashboards. You should encourage your application developers to use these dashboards so
they understand what is happening as their applications run, which will help them optimize the applications.
You should be familiar with these dashboards as well, so you are able to work with your application developers
to diagnose problems that you see at the System Admin level.

&nbsp;

## Log Management

While the System dashboards in Grafana are the primary tool for managing a Vantiq installation, there are
times you will need to examine log output from Kubernetes pods (mainly the `vantiq` pods) to diagnose problems
in the installation.

<a name="k8s_pod_logs"></a>
### Direct Kubernetes Pod Logs via `kubectl logs`

The most direct way to access Kubernetes pod logs is with the `kubectl logs` command. 

However, K8s only keeps a limited amount of log data available. When the amount of log data reaches the
maximum amount K8s will retain (which varies by implementation) the oldest log data will drop out. For this
reason, you must implement a log management system to retain pod logs for a longer time/volume period.

<a name="log_mgmtsys"></a>
### Implement a Log Management System

While viewing direct Kubernetes pod logs via `kubectl logs` is useful, as noted in the previous section K8s
only keeps a limited amount of log data available. You must implement a log management system to retain pod
logs for a longer period. There are many choices for such systems. If you are using a commercial cloud
provider, you may find it simplest to use the log management service from that provider. The details of how
to implement any of these log management choices are beyond the scope of this document.

As of this writing, Vantiq Ops uses [Sumologic](https://www.sumologic.com/) for this purpose for all
installations we manage. This is not an endorsement of Sumologic and you are not required to use it, you just
need to implement some type of log management system to capture log output beyond the short-term log data that
K8s itself retains.

&nbsp;

## Metrics Management

The System dashboards in Grafana use metrics data that is fed to InfluxDB from multiple sources, both from
the Vantiq installation components and from K8s itself. These provide your baseline metrics to manage the
installation, and often are all you need.

However, there are times you will need to examine metrics from the cloud infrastructure layer in order to
get the full picture of what is happening.

<a name="grafana_vantiq"></a>
### Grafana/InfluxDB Metrics in Vantiq

As noted, the System dashboards in Grafana visualize a variety of metrics fed to InfluxDB from both from
the Vantiq installation components and from K8s itself. These baseline metrics are often all you need to
manage the Vantiq installation.

The details on each System dashboard and how to use them are found below.

### Cloud Infrastructure Metrics

At times the System dashboards do not provide the data you need, such as when you need to know what is
happening on a node VM, or details of the cloud networking. In such you cases will need to examine metrics
from the cloud infrastructure layer in order to get the full picture of what is happening. All cloud
providers have a basic set of infrastructure metrics visualization features built into their console/portal.

You may find that a more sophisticated tool to correlate these metrics with log data helps you to have a
more robust operations capability. Often such tools are commercial offerings which involve a cost to
implement. Even open-source options that are "free" in terms of software cost still involve the cost of
the infrastructure on which to run them and the cost of the time to set them up and maintain them. You will
need to do a cost/benefit analysis to determine if a more sophisticated tool is worth the costs.

As of this writing, Vantiq Ops uses [Sumologic](https://www.sumologic.com/) for this purpose for all
installations we manage. This is not an endorsement of Sumologic and you are not required to use it.

&nbsp;

<a name="sysdash_vs_cloudportal"></a>
## Diagnostic Tools: System Dashboards vs. Cloud Provider Console/Portal

While your primary tool for managing a Vantiq installation and diagnosing should always be the System
dashboards, there will be times you will need to diagnose resources at the cloud infrastructure
layer. The cloud provider console/portal is typically the tool used for that (and the cloud infrastructure
metrics mentioned in the previous section are what is being visualized). It is important to understand
the differences between what the System dashboards show you about Vantiq vs. what the cloud provider
console/portal shows you about the cloud infrastructure.

One example is the CPU pane in the *Vantiq Resources* dashboard. That shows the CPU utilization of each
`vantiq` pod and displays 100% for each vCPU (so a 4-vCPU pod that has maxed out its CPU will show as
400% utilization). For pods that are the only one running on a node such as `vantiq` and `mongodb`, the
pod CPU utilization will often track with the node (VM) CPU utilization but not always. Also, in most
cloud provider console/portal CPU graphs the scale is 0% to 100%.

There are other panes such as the *Network Activity* pane in the *MongoDB Monitoring Dashboard* that show
pod-level network metrics for a MongoDB pod, which can usually be correlated with the matching cloud
provider console/portal network graphs for the VM where that pod is running but will not always match.
Bottom line, remember that the System dashboards are showing pod metrics and cloud provider console/portal
graphs for a VM are showing data for that VM.

&nbsp;

## System Dashboards

Like the Vantiq dashboards, the System dashboards are built using Grafana. To build your basic knowledge of
how to use Grafana, please see the [Grafana docs](https://grafana.com/docs/). 

A few of the particular docs you should read are
[Use Dashboards](https://grafana.com/docs/grafana/latest/dashboards/use-dashboards/) and
[Grafana dashboard best practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/).

The section below for each dashboard contains a screenshot of the dashboard, with the dashboard panes
numbered on the screenshot to match the pane sections below that. You can also click on each screenshot to
see a full-sized version.

<a name="select_ins"></a>
### Selecting the Correct Installation

Note that in a multi-installation cluster you will need to make sure the installation whose metrics you wish
to view is selected in the `installation` dropdown at the top of each dashboard. In a single-installation
cluster you can ignore the `installation` dropdown since it only has the one value of the single installation,
which will always be selected.

<a name="select_pod"></a>
### Selecting a Single Pod Etc.

You can also select individual pods from the `pod` dropdown at the top of each dashboard to see only data for
that pod rather than for all pods at once. There are other constraint dropdowns which vary by dashboard.

It can be useful to limit the data you are viewing to a specific pod or other constraint in order to zero
in on specific metrics without others cluttering your view. Just keep in mind that you have constrained the
data you are seeing so there is other data you are not seeing: make sure the all the data you wish to see is
being displayed.

<a name="tips"></a>
### Tips & Shortcuts

There are a few tips & shortcuts which can help you navigate the System dashboards and use them more
effectively.

<a name="change_timerange"></a>
#### Changing the Displayed Time Range

Normally each dashboard has a relative time range set as the default when you first start it, these can be
1 hour (from `now-1h` to `now`), 5 minutes (from `now-5m` to `now`) or some other range. The default
auto-refresh value is normally set to 30 seconds and enabled, so every 30 seconds the graph will be refreshed
with the data from the selected time range.

To zoom in to a smaller time range, drag-select that time range on any of the panes. The time range will
reset to whatever absolute time range you have selected and turn off auto-refresh.

To zoom out to a larger time range, click on the *zoom out* icon to the right of the time range dropdown.
This will also turn off auto-refresh if it is not off already.

To select any of the relative time ranges, select the one you want from the time range dropdown. This will
also turn on auto-refresh if it is not on already.

<a name="move_timerange"></a>
#### Moving Through Absolute Time Ranges

Once you have selected an absolute time range, it is often useful to move that ranges backwards or forwards,
which you can do with the `<` and `>` on either side of the time range dropdown.

<a name="select_timerange"></a>
#### Shortcut to Select an Absolute Time Range

If you wish to select a specific absolute time range (especially one that is hours or days ago), it helps to
start with any absolute time range selected with a quick drag-select then edit it. For example, let's say
you want to select the absolute time range of 11:00 to 11:07 from 2 days ago. Drag-select any pane to select
an absolute time range as a starting point, then click the time range dropdown to edit the *From* and *To*
fields to the specific absolute time range you want. You can always type the *From* and *To* values in from
scratch, but doing it this way saves time.

This is especially useful for the *Organization Activity* and *Organization Activity with Top Namespaces*
dashboards since the time range for those needs to be kept small (typically no more than 7 to 10 minutes
wide) for the reasons noted below.

<a name="select_inpane"></a>
#### Selecting Items in a Pane

As noted above you may wish to select a single pod or other constraint via its dropdown at the top of the
dashboard, at which point the constraint will affect all panes. You may instead wish to constrain only what
is displayed in a single pane, by clicking on a legend item in that pane. This can especially be useful for
panes that do not have a constraint at the dashboard level. For example, in the *Request Rate* and *Request
Duration* panes in the *Vantiq Resources* dashboard you can constrain to a specific `nginx` pod by clicking
its name in the pane's legend.

<a name="temp_changes"></a>
#### Temporary Dashboard Changes

It is rare but there are times you may wish to make a temporary change to one or more panes on a dashboard.
This can be done without changing the normal dashboard behavior, by not saving these changes when switching
to a different dashboard. If you have made any changes to a dashboard and not saved them, when you switch
dashboards a dialog will pop up asking `Do you want to save your changes?`. Click on the `Discard` button
to switch to the new dashboard while leaving the old dashboard unchanged (discarding your changes).

For example, the *Total Requests Processed* pane in the *Organization Activity with Top Namespaces* is
set to show only the top 10 metrics based on the calculated `sumprocessed` field with ops/sec values at
least 5, to show only "useful" data. You may find that you need more data shown so you want show ops/sec
values at least 2, or you may need less data shown so you want to show ops/sec values at least 200. In
either case you would apply the change to the pane query temporarily by clicking `Edit` in the dropdown of
the pane title bar, then editing the query to change the part near the end from `WHERE sumprocessed > 5`
to `WHERE sumprocessed > 2` or `WHERE sumprocessed > 200` based on what you need.

(*Note*: changing the query for the *Total Requests Processed* pane in the *Organization Activity with Top
Namespaces* dashboard is the most common reason to make a temp pane query change like this.)

There may be times you wish to save changes to your dashboards to customize your environment. Keep in mind
that such customization is fine, but will be overwritten by new versions of the dashboards when you import
them from `deploy/vantiq/dashboards` in `k8deploy` (`vantiqSystem/deploy/vantiq/dashboards` in your local
copy of `k8deploy_tools`). You will need to re-apply any customization after importing new dashboard
versions.

Vantiq creates new versions of the System dashboards as needed, which only happens occasionally. For
example, new versions were created when K8s switched from `Docker` runtime to the `containerd` runtime
which changed the names of some K8s metrics. When these new System dashboard versions are created, you
should rename your existing System dashboards, then import these new versions using the same process as you
would for a new installation which as documented in
[*Add Grafana Dashboards for System Users*](Installation.md#add_grafana_dashboards) in the Installation
doc. Once you are satisfied the new System dashboards are working properly, you can delete the old versions
of the dashboards that you previously renamed.

### Vantiq Resources

The *Vantiq Resources* dashboard shows basic metrics for the `vantiq` pods such as CPU utilization, garbage
collection and MongoDB requests & connection pool. It also shows the request rate and duration from nginx,
and the number of active WebSocket connections. This is the dashboard which shows the general health of the
main installation components and will likely be the dashboard you have open most often.

Reference this screenshot for the details of each pane below. The panes are numbered in the screenshot to
match the sections below, and you can click on the screenshot to see a full-sized version.

[ ![](images/VantiqResources-sm.png) ](images/VantiqResources.png)

The *Vantiq Resources* dashboard consists of the following panes.

<a name="vr_cpu"></a>
#### CPU Utilization &nbsp; <span style="font-size:2em;">&#10112;</span>

The *CPU Utilization* pane shows the CPU utilization for each `vantiq` pod. By default you can see all pods
at once, each with a different color. As noted above it can sometimes be useful to limit the data you are
viewing to a specific pod by selecting it from the pod dropdown.

This pane's scale displays 100% for each vCPU, so a 4-vCPU pod that has maxed out its CPU
will show as 400% utilization. Since `vantiq` pods are the only pod of consequence on their node, the pod CPU
utilization will often track with the node (VM) CPU utilization but not always. Also, in most cloud provider
console/portal CPU graphs the scale is 0% to 100%.

This pane and the garbage collector panes are usually the ones you will want to watch most closely. A normal
CPU utilization pattern should show fluctuations over time, usually a steady level with spikes to a higher
level. The actual steady level (whether 5% or 300%) and spike peaks (whether to 50% or 350%) will vary but
should correspond to actual work being done by the applications running on the installation and not abnormal
activity.

An abnormal CPU utilization pattern will show a much higher steady level and/or periods of sustained high
CPU utilization instead of the typical spikes. In the worst case, these sustained periods of high CPU
utilization are at the maximum level (e.g. at or near 400% for a 4-vCPU pod), which is almost always an
abnormal condition that indicates a serious problem in one or more of your applications.

You should also compare abnormally high CPU utilization levels with the garbage collector panes to see if
the pod is headed toward (or has reached) the "GC death spiral" state. Please see the
[*GC Death Spiral* section below](#gc-death-spiral) for more info on this pattern.

For a normal CPU utilization pattern, the actual steady level (whether 5% or 300%) and spike peaks (whether
to 50% or 350%) will vary but should correspond to actual work being done by the applications running on
the installation.

The "actual work" should be evident either in the *Organization Activity* (OA) or *Organization Activity
with Top Namespaces* (OATN) dashboards, or in the Vantiq-level dashboards in the application namespaces.
Activity in the *Total Requests Processed* pane of the OA and OATN dashboards often correlates with CPU
utilization. If you are looking for the source of CPU utilization you believe is too high, the first place
you should check is the *Total Requests Processed* pane of the OA and/or OATN dashboards to see if there
is matching activity.  Please see the
[*Matching CPU Spikes with Organization Activity* section below](#matching-cpu-spikes-with-organization-activity)
for more info on this pattern.

However, also keep in mind that some types of application activity can drive up CPU utilization without
driving up *Total Requests Processed* ops in the OA and OATN dashboards. This is dependent on the nature
of the applications running on your installation.

Vantiq has algorithms to spread the installation workload across the pods, but some workloads are tied to
a specific pod so CPU utilization is not always even across the pods. If you are searching for the cause of
CPU utilization on a specific pod, you should constrain the data displayed to only that pod when examining
the activity in the OA or OATN dashboards.

<a name="vr_nginx"></a>
#### Request Rate and Request Duration &nbsp; <span style="font-size:2em;">&#10113;</span>

The *Request Rate* and *Request Duration* panes show metrics from the `nginx` pods as inbound requests
come into them from the cloud load balancer. The request rate is ops/second and the request duration is
in seconds.

There is no dropdown at the top of the dashboard to constrain the view to a specific `nginx` pod, but you
can do that at the pane level by clicking the pod name in the pane's legend.

It is difficult to characterize normal or abnormal patterns for these panes. One thing that can be an
abnormal pattern is if you examine these panes for past time periods and compare them to the current time
period and notice a substantial difference.

<a name="vr_websocket"></a>
#### Active WebSockets &nbsp; <span style="font-size:2em;">&#10114;</span>

The *Active WebSockets* pane shows exactly that, the number of active WebSockets for all `vantiq` pods.
This is not often an important metric, but if it seems abnormally high (again, compare to past time
periods) it is worth investigating to determine the root cause.

<a name="vr_gc"></a>
#### Garbage Collector Panes: Times, Heap, Non-Heap &nbsp; <span style="font-size:2em;">&#10115;</span>

The *Garbage Collector* panes show the garbage collector (and non-heap) metrics for each `vantiq` pod. By
default you can see all pods at once, each with a different color. As noted above it can be useful to limit
the data you are viewing to a specific pod by selecting it from the pod dropdown.

The *GC Times* pane shows how long GCs are taking, with each GC type shown with a different color. The one
most often of interest is the *G1 Humongous Allocation* type which matches the *G1 Old Gen* heap space in
the *Heap allocation* pane. If GC times are rising above 100ms it may indicate that one or more applications
is using and/or holding onto too much heap space.

The *Heap allocation* pane shows the allocation space, with each allocation type shown with a different
color. The one most often of interest is the *G1 Old Gen* type which matches the *G1 Humongous Allocation*
GC type in the *GC Times* pane. In general, each GC should be "productive" meaning it recovers some heap
space. If the Old Gen GCs of a `vantiq` pod are unproductive so the heap allocation continues to rise over
time toward your maximum heap size (set by the`-Xmx` setting in your `JAVA_OPTS` in your `vantiq-config`
configmap), it may indicate that pod is headed toward a "GC death spiral" as described in the next section.

*Note: the above details are based on the G1 garbage collector which is the default for Java 11 and the one
used in most Vantiq installations as of this writing. If you are using a different garbage collector, you
will need to adjust these details for the garbage collector you are using. For more info on the G1 garbage
collector, please see
[Getting Started with the G1 Garbage Collector](https://www.oracle.com/technetwork/tutorials/tutorials-1876574.html).*

The *Non-Heap allocation* pane shows the non-heap allocation space for each `vantiq` pod, with each non-heap
allocation type shown with a different color. It is rare that non-heap allocation space becomes a problem,
but you can keep an eye on it with this pane.

If you need to modify any of the non-heap allocation settings such as Code Cache (set by
`-XX:ReservedCodeCacheSize`) or Metaspace (set by `-XX:ReservedCodeCacheSize`), you can do that by setting
them in the `VANTIQ_SERVER_OPTS` environment variable in the `vantiq.configuration.vantiq.defaults` section
of `deploy.yaml`.

<a name="vr_gcdeath"></a>
##### See Info on *GC Death Spiral* Pattern Below

As noted above, GCs should be "productive" meaning they recover some heap space. If the Old Gen GCs of a
`vantiq` pod are unproductive so the heap allocation continues to rise over time toward your maximum heap
size, it may indicate that pod is headed toward a "GC death spiral". This means that over time the Old Gen
GCs recover less and less memory, resulting in an upward slope of the Old Gen level after each GC.

Please see the [*GC Death Spiral* section below](#gc-death-spiral) for more info on this pattern.

<a name="vr_mongo"></a>
#### Mongo Connection Pool & Requests &nbsp; <span style="font-size:2em;">&#10116;</span>

The *Mongo Connection Pool* and *Mongo Requests* panes show the interaction of the Vantiq pods with the
`mongodb` pods. This data, along with the *MongoDB Monitoring* dashboard, can be useful if you are diagnosing
a problem with Vantiq's use of MongoDB.

The *Mongo Connection Pool* pane shows the current number of connections (`currentPoolSize`) the `vantiq`
pods have open to the primary `mongodb` pod, as well as the maximum connection pool setting (`maxPoolSize`).
If MongoDB requests start getting backed up, you will also see `requestsWaiting` show up on this pane but
normally there is no `requestsWaiting` data so it is not displayed.

The *Mongo Connection Pool* pane will also show any times where a `vantiq` pod loses connectivity with
`mongodb` entirely. For a `vantiq` pod to feed metrics about its `mongodb` connection to InfluxDB, that
connection must exist. If you see gaps in this pane for a given `vantiq` pod, that means the pod did not have
a connection to `mongodb` during the gaps. This may be because all `mongodb` pods were down, or it may be
due to networking problems either on that `vantiq` pod or at the K8s or cloud infrastructure level.

The *Mongo Connection Pool* pane also shows you the primary `mongodb` pod of the replicaset, so if the primary
fails over to a different pod you can see that in this pane.

The *Mongo Requests* pane shows the number of active (`activeSubscribers`) and pending (`pendingSubscribers`)
MongoDB commands from the Vantiq pods.

### Metric Collection Resources

The *Metric Collection Resources* dashboard shows metrics for the `metrics-collector` pod. Some are the same
as the *Vantiq Resources* dashboard, but two are unique to this dashboard.

The `metrics-collector` pod processes raw metrics sent from the `vantiq` pods into computed metrics which are
then sent to InfluxDB. For the reasons noted in the
[*Metrics Collector* section of the Background Reference doc](BackgroundReference.md#metrics-collector),
it is recommended you deploy a dedicated `metrics-collector` pod in production installations.

Reference this screenshot for the details of each pane below. The panes are numbered in the screenshot to
match the sections below, and you can click on the screenshot to see a full-sized version.

[ ![](images/MCResources-sm.png) ](images/MCResources.png)

The *Metric Collection Resources* dashboard consists of the following panes.

<a name="mc_cpu"></a>
#### CPU Utilization &nbsp; <span style="font-size:2em;">&#10112;</span>

This is the same as the *CPU Utilization* pane on the *Vantiq Resources* dashboard, but for the the
`metrics-collector` pod instead of the `vantiq` pods.

<a name="mc_gc"></a>
#### Garbage Collector Panes: Times, Heap &nbsp; <span style="font-size:2em;">&#10113;</span>

These are the same as the *GC Times* and *Heap allocation* panes on the *Vantiq Resources* dashboard, but for
the `metrics-collector` pod instead of the `vantiq` pods.

<a name="mc_events"></a>
#### Event Processing &nbsp; <span style="font-size:2em;">&#10114;</span>

The *Event Throughput* and *Processing Time* are unique to this dashboard. They provide metrics that give you
a view of the events passing through the entire installation.

The *Event Throughput* pane shows the throughput level in ops/second for all events passing through the
installation.

The *Processing Time* pane shows the processing time in ms to compute histogram data for all metrics passing
through the installation.

It can be useful to examine both of these panes to see if the event throughput level or event processing time
changes after installation modifications such as patch updates or upgrades, compared to the levels before
them. In general both of these levels should stay the same after a patch update, and usually after an upgrade
as well. If the event throughput level drops after a patch update or upgrade, it may indicate that some
applications are not running the same as they were which could indicate a problem. If the event throughput
level rises significantly after a patch update or upgrade, it may indicate that some applications are running
in an abnormal way that spiked event throughput and could also indicate a problem.

### MongoDB Monitoring

The *MongoDB Monitoring* dashboard shows metrics for the `mongodb` pods such as database operations, CPU usage
and network activity, and server internals such as memory and cache use.

If you are looking at this dashboard before determining the MongoDB primary from the *Mongo Connection Pool*
pane in the *Vantiq Resources* dashboard, it is usually obvious which pod is primary by selecting them one by
one from the `pod` dropdown. The primary is shown in the screenshot below, notice the level of activity in the
*Operations Counters* pane which will not be the case on a secondary.

Reference this screenshot for the details of each pane below. The panes are numbered in the screenshot to
match the sections below, and you can click on the screenshot to see a full-sized version.

[ ![](images/MongoDBMonitoring-sm.png) ](images/MongoDBMonitoring.png)

The *MongoDB Monitoring* dashboard consists of the following panes.

<a name="mongo_cpuetc"></a>
#### Open Connections, Virtual Memory and CPU Usage &nbsp; <span style="font-size:2em;">&#10112;</span>

The *Open Connections*, *Virtual Memory* and *CPU Usage* panes provide metrics that give you a basic view
of how the `mongodb` pod is doing.

The *Open Connections* pane shows how many connections are open to the `mongodb` pod currently selected.

The *Virtual Memory* pane shows the total amount of virtual memory in use by the `mongodb` pod currently
selected.

The *CPU Usage* pane shows the CPU utilization graph for the `mongodb` pod currently selected.

<a name="mongo_ops"></a>
#### Operations Counters and Active / Queued Operations &nbsp; <span style="font-size:2em;">&#10113;</span>

The *Operations Counters* and *Active / Queued Operations* panes provide metrics that give you a view of the
database operations coming into MongoDB from the `vantiq` pods.

The *Operations Counters* pane shows a graph of the level of various types of database operations such as
*query*, *insert*, *delete* etc. in ops/second for the `mongodb` pod currently selected. This pane can be
correlated with the *CPU Utilization* pane in the *Vantiq Resources* dashboard, and database application
activity either in the *Organization Activity* (OA) or *Organization Activity with Top Namespaces* (OATN)
dashboards, or in the Vantiq-level dashboards in the application namespaces.
 
If you are looking for the source of database activity in the *Operations Counters* pane you believe is
abnormal, the first place you should check is the *Total Requests Processed* pane of the OA and/or OATN
dashboards to see if there is matching activity.

The *Active / Queued Operations* pane shows the number of active and queued operations that have taken
locks.

<a name="mongo_netmem"></a>
#### Network Activity and Memory &nbsp; <span style="font-size:2em;">&#10114;</span>

The *Network Activity* and *Memory* provide additional metrics that give you a basic view of other aspects
of the `mongodb` pod.

The *Network Activity* pane shows inbound and outbound kB or MB per second, which indicates the volume of
data that goes along with the database operations shown in the *Operations Counters* pane. It can also be
correlated with the network graphs in the cloud provider console/portal for the node (VM) where the
`mongodb` pod is running.

The *Memory* pane shows the total amount of resident (physical) and virtual memory in use by the `mongodb`
pod. The virtual memory value should match the *Virtual Memory* pane above. The mapped values will always
be zero since we use the WiredTiger engine which does not do memory mapping of files.

<a name="mongo_engine"></a>
#### Wired Tiger Cache, Flushes / Faults and TTL Activity &nbsp; <span style="font-size:2em;">&#10115;</span>

The *Wired Tiger Cache*, *Flushes / Faults* and *TTL Activity* panes provide metrics that provide insight
into the pod's MongoDB internals.

The *Wired Tiger Cache* pane shows the memory use of various types cache pages in the WiredTiger engine. If
you are interested in a specific type of cache page you can click on it to see the graph for only that type,
since the only types visible when all types are displayed are *total* and *Max*.

The *Flushes / Faults* pane shows the value of the `extra_info.page_faults` counter, see
[the *extra_info* section of the doc page for the *serverStatus* command](https://www.mongodb.com/docs/manual/reference/command/serverStatus/#extra_info)
for details.

The *TTL Activity* pane shows the value of the `metrics.ttl.deletedDocuments` and `metrics.ttl.passes`
counters, see
[the *metrics.ttl* section of the doc page for the *serverStatus* command](https://www.mongodb.com/docs/manual/reference/command/serverStatus/#mongodb-serverstatus-serverstatus.metrics.ttl)
for details.

### UserDB Monitoring

The *UserDB Monitoring* dashboard is the same as the *MongoDB Monitoring* dashboard, but for the `userdb` pods
instead of the `mongodb` pods. This dashboard will of course only have data if you are using the `userdb`
statefulset for user data types and the `mongodb` statefulset only for system collections, rather than using
the `mongodb` statefulset for both these types of data.

For info about all aspects of this dashboard, see the *MongoDB Monitoring* dashboard section above.

### Organization Activity

The *Organization Activity* dashboard shows a System-level view of the same application metrics shown in the
Vantiq-level dashboards in the application namespaces. The *Total Requests Processed* and *Top Request Rate*
panes show the activity levels of the resource managers and Orgs. The *Global Credit Usage*, *Top Credit
Usage* and *Top Quota Violations* panes show the state of the Credit and Quota systems (see the
[Workload Management](https://dev.vantiq.com/docs/system/workloadmanagement/index.html) guide for details
on those). The *Activity in ORG* panes show the Credit and Quota detail for each Org.

<a name="oa_cautions"></a>
#### Usage Cautions for *Organization Activity* and *Organization Activity with Top Namespaces* Dashboards

<span style="color:red;">WARNING!</span>

For most of the System dashboards, it does not matter how large of a time range you choose, the amount of
data returned by the pane queries will not put an excessive load on InfluxDB. The *Organization Activity*
and *Organization Activity with Top Namespaces* dashboards are the exception. These are the only System
dashboards where you need to think about the amount of data that is returned from InfluxDB based on the
selections you make in the dashboard for time range and other constraints via the dropdown menus. You should
limit the amount of data returned so you can navigate these dashboards without undue delays and without
overwhelming InfluxDB.

At a minimum, large queries will cause you to wait (sometimes more than a minute) for the *Total Requests
Processed* and *Top Request Rate* panes to complete their queries and display their data. In extreme
cases large queries can overwhelm InfluxDB to the extent that it will cause the `influxdb-0` pod to become
unresponsive to health checks, which in turn will cause K8s to restart the pod.

For this reason, the default for these dashboards (the state they are in when you first start them) is to
have the Vantiq org (which normally has little or no activity) pre-selected and the time range set to *Last
5 minutes*. This ensures that very little data is queried when you first start these dashboards.

Remember that relative time spans by default will refresh every 30 seconds unless you set the auto-refresh
dropdown to *Off*, or select an absolute time range which will do that automatically.

The first and best way to limit the amount of data returned is to limit the time range. The default 5-minute
range is ideal, although a 7-minute range usually works OK. A 10-minute range usually must be combined with
other constraints such as Org or Pod to work OK. In general you should <span style="color:red;">never</span>
select a time span of more than 15 minutes.

The other two constraints that will limit the amount of data returned is selecting a specific Org and/or pod
from the dropdowns for those. Selecting a specific pod is often what you want anyway, since you will often
be diagnosing a CPU utilization or other issue on a specific pod. Selecting a specific Org will also limit
data significantly: if it is clear from querying with *Organization* set to *All* that much of the activity
is in a specific Org (the TRR pane will show this) then you can select just that Org from the dropdown and
your queries will run more quickly.

Normally only the *Total Requests Processed* and *Top Request Rate* panes will take more than 1 second to
query and display. After the delay for a large query, the *Top Request Rate* pane will finish first, and the
*Total Requests Processed* pane will take the longest. Depending on how much you have constrained the data
as described above, the TRP pane query can take from 5 to 45 seconds to complete.

Rule of thumb: if the *Total Requests Processed* pane query takes more than 1 minute to run, you are querying
too much data and you should apply more constraints as described above. Experiment with these dashboards to
learn the optimal limits for your installation given your Orgs and applications. Start as constrained as
possible, then slowly broaden the amount of data you are querying until you start to see delays over 5-10
seconds in the TRP pane. After that, proceed with caution.

<a name="oa_details"></a>
#### *Organization Activity* Dashboard Pane Details

Reference this screenshot for the details of each pane below. The panes are numbered in the screenshot to
match the sections below, and you can click on the screenshot to see a full-sized version.

[ ![](images/OrgActivity-sm.png) ](images/OrgActivity.png)

The *Organization Activity* dashboard consists of the following panes.

<a name="oa_trp_trr"></a>
#### Total Requests Processed and Top Request Rate &nbsp; <span style="font-size:2em;">&#10112;</span>

The *Total Requests Processed* and *Top Request Rate* panes show two views of the requests processed by
each resource manager inside the Vantiq server: ModelManager handles database requests, ExecutionManager
handles procedure requests and so on. You can constrain the data queried and displayed on the dashboard to
a single resource manager by selecting it from the Resource Manager dropdown. Similarly you can constrain
the data by pod and/or Org by selecting one of those from their dropdown.

See the *Usage Cautions* section above for the reasons it is important to constrain the data on this
dashboard as much as possible.

The *Total Requests Processed* pane shows a graph of the resource manager activity level, in ops/second.
By default you see all resource managers at once, each with a different color, unless you constrain to a
single resource manager as noted above. The levels shown are for all pods and all Orgs, unless those too
are constrained by their dropdown.

The *Top Request Rate* pane shows, for each period (normally 30 seconds per period), the Org that had the
top request rate for that period and what that top rate was. Each period's rate will be the sum of whatever
is selected in the three dropdowns for the dashboard. If all three are set to *All* then each rate will be
the sum of the values of all resource managers on all pods for all Orgs. If any of the three dropdowns
constrain the data for the dashboard, each rate will be the sum of the values reflecting those constraints.

This pair of panes are particularly useful for determining which Orgs are the largest source of activity
in the system. If you then wish to drill down further to see which namespaces are the most active, you can
switch to the *Organization Activity with Top Namespaces* dashboard and select the Org that you found most
active by using this dashboard. Please see the
[*Matching CPU Spikes with Organization Activity* section below](#match_cpu_with_oa)
for an example of this diagnostic process.

<a name="oa_credit_quota"></a>
#### Global Credit Usage, Top Credit Usage and Top Quota Violations &nbsp; <span style="font-size:2em;">&#10113;</span>

The *Global Credit Usage*, *Top Credit Usage* and *Top Quota Violations* panes show the state of the Credit
and Quota systems inside the Vantiq server. Please see the
[Workload Management](https://dev.vantiq.com/docs/system/workloadmanagement/index.html) guide for details
on those systems and how they provide each Org with its fair share of resources, even when applications in
other Orgs are using their full allotment of resources.

The *Global Credit Usage* pane shows the percentage of global credit that each resource manager is using.
You can show this data for all resource managers at once, each with a different color, or constrain the
data queried and displayed on the dashboard to a single resource manager by selecting it from the Resource
Manager dropdown. Similarly you can constrain the data by pod by selecting one of those from the *pod*
dropdown. You cannot constrain the data by Org since this is a global pane (selecting an Org from the
*Organization* dropdown has no effect on this pane).

The *Top Credit Usage* and *Top Quota Violations* panes show which Orgs (if any) are the top credit users
and quota violators respectively. If there are no top quota violators, the *Top Quota Violations* pane will
show no data. The *Top Credit Usage* pane, however, will always show something, but note when the top credit
usage is 0% in that pane, it means there are no top credit users.

<a name="oa_inorg"></a>
#### Activity in *ORG*: Credit Usage and Quota Violations &nbsp; <span style="font-size:2em;">&#10114;</span>

There is one *Activity in ORG* box for each Org. Within each of these boxes, the Credit Usage pane shows the
credit usage for that Org, and the *Quota Violations* pane shows the Quota Violations for that Org, similar
to the *Top Credit Usage* and *Top Quota Violations* panes but there is one for each Org. For example, in the
*Organization Activity* screenshot above, the box containing the first pair of these is for the `Secontoso`
Org so it is labeled `Activity in Secontoso`.

<a name="oatn"></a>
### Organization Activity with Top Namespaces

The *Organization Activity with Top Namespaces* dashboard is the same as the *Organization Activity*
dashboard, but with the addition of namespace data added to the query for the *Total Requests Processed* pane.
This adds additional data to the query for the TRP pane in this dashboard, making the warnings in the *Usage
Cautions* section above even more important.

Once you have determined the Org of interest using the *Organization Activity* dashboard, you may wish to
drill down further to see the namespaces in that Org that are causing whatever problem it is you wish to
diagnose. That it when you will want to switch to this dashboard, and select the Org in question to constrain
the data to focus only on that Org.

Other than that, for info about all aspects of this dashboard, see the *Organization Activity* dashboard
section above.

### InfluxDB Internals

The *InfluxDB Internals* dashboard contains data on the internal operations of InfluxDB. You generally will
only need to use this dashboard for two purposes:

1) The *InfluxDB Heap Usage* pane will show spikes when you are doing larger queries. You can see just how
much these are affecting InfluxDB using this pane.
2) You can see how many points (rows) there are in each database in the *Series By Database* pane. If you are
having InfluxDB disk space issues, this can show you which collections are taking up the most space.

&nbsp;

## Important Patterns

### GC Death Spiral

As noted above, GCs should be "productive" meaning they recover some heap space. If the Old Gen GCs of a
`vantiq` pod are unproductive so the heap allocation continues to rise over time toward your maximum heap
size, it may indicate that pod is headed toward a "GC death spiral". This means that over time the Old Gen
GCs recover less and less memory, resulting in an upward slope of the Old Gen level after each GC, which
looks like this:

![](images/GCDS-example.png)

This is only the *Heap allocation* pane so you can't see the time range. A view of the whole *Vantiq
Resources* dashboard shows that the time range is 19 days (17 Feb to 8 Mar):

![](images/GCDS-example-allVR.png)

Depending on how rapidly the process is progressing, it may only be visible over a 1 to 2 week time range.
Here is the same *Heap allocation* pane but over a time range of 4 days (4 Mar to 8 Mar):

![](images/GCDS-example-4d.png)

You can see the process progressing over this 4 day time range, but it is less pronounced.

As this process progresses, the Old Gen GCs will happen more frequently and when it reaches the terminal
stage the pod can be doing Old Gen GCs every few minutes and using a significant part of CPU to do the
garbage collection. At this point you will be forced to terminate the pod (`kubectl delete` it so the K8s
scheduler will create a new one). It is preferable to predict when it is a day or two before this crisis
point and terminate/recreate the pod at a time of your choosing.

You may notice on the screenshots that the garbage collector in use is the older one that was the default
for Java 8. As of R1.35 Vantiq is using Java 11 and the G1 garbage collector, which so far are not having
this problem.

<a name="match_cpu_with_oa"></a>
### Matching CPU Spikes with Organization Activity

When you see CPU spikes in the *Vantiq Resources* dashboard, you should check in the *Organization Activity*
dashboard to see if you can find the source. If you do find an Org that appears to be the source of abnormal
activity, you can then check the *Organization Activity with Top Namespaces* dashboard to see which namespace
in that Org is the source. This section shows an example of this process.

Let's start in the *Vantiq Resources* dashboard. Let's say you look at that dashboard and see the following:

[ ![](images/BurnCPUVantiqResources-sm.png) ](images/BurnCPUVantiqResources.png)

*Note: click on these screenshots to enlarge them if you wish to see more detail.*

You can clearly see an abnormal CPU spike, the `vantiq-4` pod's CPU is maxed out. You should note when the
CPU spike starts, in this case it's just after 12:45 on 2023-04-17.

At this point you don't know the cause, so you switch to the *Organization Activity* dashboard to try to
find the cause. As noted above, when you first start that dashboard it should be displaying the last 5
minutes of data and should have the `Vantiq` org selected in the dropdown. Follow the process in the
*Organization Activity* dashboard section above to select an absolute time period from 12:45 to 12:50 on
2023-04-17, then select `All` from the *Organization* dropdown. Once you do, the dashboard will look like
this:

[ ![](images/BurnCPUOA-sm.png) ](images/BurnCPUOA.png)

You can see several things at this point. In the TRP pane you can see the `ExecutionManager` and
`ModelManager` are processing thousands of ops/second, and in the TRR pane you can see that the `BurnCPU`
org is the source of the top request rates. You can also see in the *Top Quota Violations* pane that
the `BurnCPU` org is violating their quota at 2K ops/second with errors: an application in that org is
not only running at a high rate but has many errors. In other cases you may see a high rate of activity
but few or no errors.

Since it's so clear which Org is causing the problem, next you switch to the *Organization Activity with
Top Namespaces* dashboard to try to find the namespace in that Org that is the cause. You repeat the same
process you used in the *Organization Activity* dashboard but here you select the `BurnCPU` org (not `All`)
from the *Organization* dropdown. Once you do, the dashboard will look like this:

[ ![](images/BurnCPUOATN-sm.png) ](images/BurnCPUOATN.png)

You see a similar picture to the one you saw with the *Organization Activity* dashboard, but now you can
see that the `ExecutionManager` and `ModelManager` are processing thousands of ops/second in the `Grinding`
namespace. You can now contact the `BurnCPU` Org admin and let them know they have a problem in their
`Grinding` namespace they should investigate and fix.

Note that this process does not always unfold in such a straightforward way. Some types of application
activity can drive up CPU utilization without driving up *Total Requests Processed* ops in the OA and OATN
dashboards. This is dependent on the nature of the applications running on your installation.

&nbsp;

<a name="hc_caution"></a>
## Cautionary Note: Rare Issues with Hazelcast Cluster Formation

*Note: normally in the k8sdeploy_tools docs, the term `cluster` refers to a Kubernetes cluster, or the cluster
definition that defines a complete set of shared Vantiq components and one or more Vantiq installations running
on that Kubernetes cluster. In this section however, the term `cluster` refers to the Hazelcast cluster formed
by a collection of Vantiq pods, which communicate with each other over a Vert.x bus.*

As of this writing (April 2023), there are multiple statefulsets that are all part of the same Vantiq cluster
managed by [Hazelcast](https://docs.hazelcast.com/hazelcast/latest/): `vantiq`, `metrics-collector` and
sometimes `vision-analytics` and/or any Isolated Org Compute ones. In rare circumstances during rolling
restarts of these statefulsets, the Hazelcast cluster manager does not correctly handle members joining the
cluster. This only happens very rarely, but if it does there are two options to deal with this problem.
If the first option does not work for you, you can escalate to the second.

<a name="hc_caution_fixopt1"></a>
### Option 1: watch all pods, fix them as needed

As the rolling restarts proceed, monitor the cluster members leaving and returning. It's best to do this
from the first cluster member to restart, which is normally `metrics-collector-0`. Let's say you are doing
these rolling restarts in the `dev` installation on the `prod-us` cluster described in the
[Vantiq K8s Cheat Sheet](docs/VantiqK8sCheatSheet.md) doc, which uses the `kcus` alias for `kubectl`. You
would monitor the `metrics-collector-0` log (once that pod restarts) with the command:

```
kcus logs metrics-collector-0 -n dev -f
```

You should be following the standard update procedure, so you will already be monitoring the pod
terminations and starts in another window with the command:

```
kcus get pod -A -w
```

As you monitor the pod terminations and restarts via `kcus get pod -A -w`, you should see each pod leave
and rejoin the cluster in the `metrics-collector-0` log which should look something like this:

```
(cluster member leaves)

Members {size:3, ver:103} [
        Member [10.10.161.165]:5701 - d7d79857-f221-4a8c-9567-196ed4bfb81f this
        Member [10.10.190.68]:5701 - 0c411a0e-2863-4bda-962a-96f989e9f56b
        Member [10.10.173.226]:5701 - e8848686-574c-4268-b611-c8890a959fcc
]

(cluster member rejoins)

Members {size:4, ver:104} [
        Member [10.10.161.165]:5701 - d7d79857-f221-4a8c-9567-196ed4bfb81f this
        Member [10.10.190.68]:5701 - 0c411a0e-2863-4bda-962a-96f989e9f56b
        Member [10.10.173.226]:5701 - e8848686-574c-4268-b611-c8890a959fcc
        Member [10.10.186.235]:5701 - 5e19293c-6060-4ab5-8119-895d8fb102db
]
```

If you wish to confirm that a pod did or or did not join the cluster, you can also examine the log for that
pod.

If any of the pods do not properly join the cluster, they will need to be restarted by deleting them (which
will terminate them) so the Kubernetes scheduler will start a new one.

For example, if `vantiq-1` did not properly complete startup and join the cluster, delete it with the command:

```
kcus delete pod vantiq-1 -n dev
```
<a name="hc_caution_fixopt2"></a>
### Option 2: scale down everything except `vantiq-0`, then scale back up

In extreme circumstances where pods are having trouble joining the cluster even after restart, you can take the
maximal step of scaling all cluster pods down except for `vantiq-0`, then scale them back up. You would first
scale down everything except `vantiq-0` with the commands:

```
kcus scale sts metrics-collector -n dev -replicas=0
kcus scale sts vision-analytics -n dev -replicas=0   (if using vision-analytics)
kcus scale sts <IOCsts> -n dev -replicas=0           (if using IOC... repeat for each sts)
kcus scale sts vantiq -n dev -replicas=1
```

Once all pods except `vantiq-0` have terminated, scale the statefulsets back up to the number of replicas
they had before (in this example, 3, 1, 2 and 3 respectively):

```
kcus scale sts vantiq -n dev -replicas=3
kcus scale sts metrics-collector -n dev -replicas=1
kcus scale sts vision-analytics -n dev -replicas=2    (if using vision-analytics)
kcus scale sts <IOCsts> -n dev -replicas=3            (if using IOC... repeat for each sts)
```
