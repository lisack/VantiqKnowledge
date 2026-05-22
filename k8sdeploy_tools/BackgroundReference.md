# Deploying and Managing Vantiq Installations:<br/>Background Reference

## Overview

This document is intended to provide background information useful when using this repo to deploy and manage
Vantiq installations.

&nbsp;

## Table of Contents

* [Vantiq Installation Components](#vantiq-installation-components)
    * [Vantiq Server](#vantiq-server)
    * [Metrics Collector](#metrics-collector)
    * [Isolated Organization Compute Servers](#ioc-servers)
    * [Vision Analytics](#vision-analytics)
    * [Nginx](#nginx)
    * [MongoDB](#mongodb)
    * [Keycloak](#keycloak)
    * [Grafana / GrafanaDB](#grafana)
    * [InfluxDB](#influxdb)
* [Kubernetes Background Reference](#k8s-ref)
    * [Why Kubernetes?](#k8s-why)
    * [Vantiq Kubernetes Tools](#k8sdeploytools)
        * [Software Used For These Tools](#k8sdeploytools-sw)
        * [Main Tools Repo: `k8sdeploy_tools`](#k8sdeploytools-repo)
        * [Vantiq System Repo: `k8sdeploy`](#k8sdeploy-repo)
        * [Cluster Config Repo: `k8sdeploy_clusters`](#clusterconfig-repo)
        * [How the Repos are Connected](#repo-connections)
    * [Helm](#helm)
    * [Helm Overrides from `k8sdeploy` and `deploy.yaml`](#helm-overrides)
* [Infrastructure](#infrastructure)
    * [Required Infrastructure](#required-infrastructure)
    * [Best Practices for Infrastructure](#infra-bestpractices)
        * [Deploy Sufficient Compute Resources](#infra-sufcompute)
        * [Deploy `metrics-collector`](#infra-mc)
        * [Use Dynamic Storage](#infra-dynstorage)
        * [Use a Real SSL Certificate](#infra-realssl)
        * [Deploy in 3 Availability Zones (AZs)](#infra-3azs)
        * [Store Backups in a Separate Region](#infra-bkp-sepregion)

---

## Vantiq Installation Components

The following components are part of a Vantiq installation.

![](images/VantiqInstallationComponents.svg)


### Vantiq Server

The Vantiq server is the core of the installation. It consists of the pods in the `vantiq` statefulset
(`vantiq-0`, `vantiq-1` etc.). The Vantiq server pods provide all processing done by Vantiq applications,
such as rules, procedures, storing & retrieving data from Types, and interactions with external sources.

The `vantiq` pods have three init containers which run before the main `vantiq` container starts:

1. `keycloak-init` which checks that Keycloak is up, and initializes the Keycloak realm for the
installation the first time it is run.
1. `mongo-available` which confirms that MongoDB is available. When you first deploy an installation,
this init container in the `vantiq-0` pod will not be able to complete while the MongoDB pods are
starting, so the `vantiq-0` pod will keep restarting until MongoDB is available.
1. `load-model` which checks the existing database schema version for the system catalogs, and upgrades
it when needed. This only happens on the `vantiq-0` pod during an upgrade, and is why you monitor the run
of this container of the `vantiq-0` pod during upgrades.

### Metrics Collector

In production installations it is best practice to deploy the `metrics-collector` statefulset. This is a
specialized Vantiq server that processes raw metrics from the `vantiq` pods, for the specific metrics which
require additional changes before being sent to InfluxDB. This relieves the `vantiq` pods of doing this
additional processing, so they can spend all their CPU and memory resources on application runtime
processing.

Note that there are other raw metrics from the `vantiq` pods which can be used as-is without additional
processing that are always sent directly from the `vantiq` pods rather than being sent to the
`metrics-collector` pod first.

Deployment of `metrics-collector` is not required, but is recommended in production installations. If
it is not deployed then all `vantiq` pods must spend part of their CPU and memory resources on metrics
processing.

<a name="ioc-servers"></a>
### Isolated Organization Compute Servers

In some cases organizations will opt for Isolated Compute. In such cases there will be an additional
set of "isolated org compute" Vantiq servers dedicated to processing only the rules and procedures for
the applications running in that organization's namespaces.

### Vision Analytics

Vantiq has built-in image processing functionality based on TensorFlow models, see the 
[Image Processing Reference Guide](https://dev.vantiq.com/docs/system/imageprocessing/index.html) for
details. In order to use this functionality in a Vantiq installation, the `vision-analytics` statefulset (a
specialized Vantiq server implementing the TensorFlow functionality) must be deployed. The `vision-analytics`
pods require GPU-enabled nodes on which to run. Best practice is to not run the `vision-analytics`
statefulset unless it is required by specific applications, since GPU-enabled nodes are expensive to run.

### Nginx

A Vantiq installation is normally installed on isolated subnets that cannot be accessed directly from the
outside, while the Vantiq pods themselves access the outside via NAT gateways. The Nginx Ingress Controller
is used to allow access to the Vantiq services from outside of the installation, normally via a load balancer
created by the cloud provider.

The controller is deployed in the cluster's `shared` namespace and provides routing for the K8s `ingress`
resources created when deploying the other Vantiq components.

The `nginx` pods also terminate the inbound TLS connections coming in from the load balancer, then
reverse-proxy those connections (to the `vantiq` and `keycloak` pods, for example) via HTTP.

### MongoDB

MongoDB is currently the default storage manager for Vantiq system data and Type data in Vantiq
applications. It is deployed as the `mongodb` statefulset (and sometime the `userdb` statefulset, see below).
In production MongoDB is deployed as a 3-node replicaset with one primary and two secondaries. The replicaset
chooses the primary via the normal MongoDB replicaset election process, and if the primary goes down the two
secondaries will have a new election and one of them will become the new primary (which takes about 30
seconds).

If you have concerns of being perceived as offering MongoDB as a Service as defined in section 13 of
[the MongoDB SSPL](https://www.mongodb.com/licensing/server-side-public-license) despite the
[SaaS using MongoDB section of the MongoDB SSPL FAQ](https://www.mongodb.com/licensing/server-side-public-license/faq)
then you can continue to use MongoDB 3.6.8 as long as Vantiq supports it. If you have such concerns you can
also use 3.6.8 only for Type data in Vantiq applications (the `userdb` statefulset) and use a newer MongoDB
version for the Vantiq system data (the `mongodb` statefulset).

### Keycloak

Keycloak provides the user management component of a Vantiq installation. The initial login process as well
as the user management features are performed by Keycloak. This includes the ability to integrate SAML and
OAUTH2 based authentication providers. A number of common social providers such as Google, Facebook, Twitter,
GitHub, LinkedIn, Microsoft and Apple are available as pre-configured authentication provider options.

For Vantiq public cloud installations, Vantiq chooses which of these providers to enable (and they can only
be enabled or not for all orgs). If you are running a private Vantiq installation, you have the ability to
configure the SAML and/or OAUTH2 based authentication providers you wish, including the social providers you
wish. Note that to use one of these preconfigured providers, you will need to create and register your own
set of credentials for that provider.

<a name="grafana"></a>
### Grafana / GrafanaDB

Grafana provides the visualization of the metrics in the InfluxDB metrics database. This includes the many
Vantiq application metrics dashboards found in each application namespace, and the system dashboards found in
the system namespace.

The installation includes a small MySQL pod which provides storage of the Grafana configuration data.

### InfluxDB

All application metrics from Vantiq are sent to InfluxDB so they can be queried and visualized by Grafana.
This is true whether they are simple raw metrics direct from a `vantiq` pod, or processed metrics from the
`metrics-collector` pod (or a `vantiq` pod if there is no `metrics-collector` pod, see the Metrics Collector
section above).

---

<a name="k8s-ref"></a>
## Kubernetes Background Reference

<a name="k8s-why"></a>
### Why Kubernetes?

Kubernetes provides a number of features which make Vantiq installations more robust, such as auto-restart of
a failed pod. It also provides us with a platform which eliminates many (but not all) differences between
cloud providers, allowing us many choices of cloud providers on which to deploy.

<a name="k8sdeploytools"></a>
### Vantiq Kubernetes Tools

<a name="k8sdeploytools-sw"></a>
#### Software Used For These Tools

There are several software components used by the tools in this repo:

1) Java 11 (either [Oracle](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html) or
[OpenJDK](https://jdk.java.net/archive/)). This is used by Gradle.
1) Gradle. The tools themselves are written in Gradle, so it is usefule to develop knowledge of Gradle if
you wish to examine the Gradle files which make up the tools. The tools themselves handle installing Gradle
so you will not need to install it yourself.
1) [Git](https://git-scm.com/downloads). This is used both to pull down the current `k8sdeploy` version into
your `vantiqSystem` subdirectory, and perform all config changes in your `targetCluster` subdirectory.
1) [GitHub CLI](https://docs.github.com/en/github-cli/github-cli/quickstart). This is used to access GitHub.
It is optional, and is not needed if you can configure your Git client to access GitHub in some other way.
1) [Kubectl](https://kubernetes.io/docs/tasks/tools/) (the Kubernetes CLI). This is used for all commands
that interact with your Kubernetes clusters.
1) [Helm](https://helm.sh/). This is used by the tools to interact with all the Helm charts of the
installation components, and the config files in `k8sdeploy` and generated from `deploy.yaml`.
1) [Kubeseal](https://github.com/bitnami-labs/sealed-secrets#homebrew). This is optional, but is required
if using sealed secrets.

For details on installing the above software, please see the
[Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](k8sdeploy_toolsBootstrap.md) document.

<a name="k8sdeploytools-repo"></a>
#### Main Tools Repo: `k8sdeploy_tools`

The main tools repo is this repo (`k8sdeploy_tools`) which normally resides in the `k8sdeploy_tools`
directory on your local machine. It contains the installation/deployment tools themselves which are Gradle
files, some helper scripts in the `scripts` subdirectory, and other helper files for these tools.

It is also the "top of the tree" as described below in "How the Repos are Connected".

<a name="k8sdeploy-repo"></a>
#### Vantiq System Repo: `k8sdeploy`

The `k8sdeploy` repo contains the base deployment definition of the Kubernetes-based Vantiq system. It
contains Helm charts for some components such as the `vantiq` statefulset itself, and overrides to 3rd-party
charts we use as a base but modify with those overrides. The contents of the `k8sdeploy` repo are pulled into
the `vantiqSystem` subdirectory (that directory is the root for the copy of the `k8sdeploy` repo used by the
tools).

The specific version of the files pulled from the `k8sdeploy` repo into the `vantiqSystem` subdirectory is
determined by the `vantiq_system_release` setting in the `cluster.properties` file in the `targetCluster`
subdirectory, and is done automatically by the tools.

**Note:** if you wish to use a custom repo for `k8sdeploy` rather than the default one at
`https://github.com/Vantiq/k8sdeploy`, you will need to do that by setting the `vantiqSystemRepo` and
`helmChartRepo` Gradle properties in `.gradle/gradle.properties` as described in the
[*Using a Custom `k8sdeploy` Repo* section of the *Centrally Managing Cluster Definitions by a Customer*](CustomerManagedDefinition.md#k8sdeployrepo)
doc. Please see that doc so you can follow the instructions found there.

<a name="clusterconfig-repo"></a>
#### Cluster Config Repo: `k8sdeploy_clusters`

The cluster config repo is pulled into the `targetCluster` subdirectory (that directory is the root for the
copy of the cluster config repo repo used by the tools). For clusters managed by Vantiq Ops, the cluster
config repo is the `k8sdeploy_clusters` repo. If you have a customer-managed private cloud installation,
your cluster config repo will be a different repo.

The specific version of the files pulled from the cluster config repo into the`targetCluster` subdirectory
is determined by the branch matching the `-Pcluster` arg to the tools commands. Typically this branch name is
the same as the cluster name and the context name in `targetCluster/kubeconfig` but that is not required. For
further details on this please see the
[`targetCluster/kubeconfig` section of the Vantiq K8s Cheat Sheet doc](VantiqK8sCheatSheet.md#tc_kubeconfig_in_tc).

**Note:** if you wish to use a custom cluster repo, you will need to do that by setting the `clusterRepo`
Gradle property in `.gradle/gradle.properties` and initializing your custom cluster repo, as described in the
[*Initializing and Using a Custom Cluster Repo by default for `targetCluster`* section of the *Centrally Managing Cluster Definitions by a Customer*](CustomerManagedDefinition.md#clusterrepo)
doc. Please see that doc so you can follow the instructions found there.

<a name="repo-connections"></a>
#### How the Repos are Connected

To summarize the above three sections, the three tools repos are connected as follows:

![](images/VantiqToolsRepos.svg)

The `k8sdeploy_tools` repo is at the top, in the `k8sdeploy_tools` directory. In that repo itself, the
`targetCluster` and `vantiqSystem` subdirectories are empty. The `targetCluster` subdirectory is the root for
the cluster config repo, which is the `k8sdeploy_clusters` repo in the case of Vantiq Ops team but will be a
different repo for customer-managed private cloud installations. The `vantiqSystem` subdirectory is the root
for the `k8sdeploy` repo and is auto-populated from that repo by the tools, determined by the
`vantiq_system_release` setting in the `cluster.properties` file in the `targetCluster` subdirectory.

### Helm

Helm is used by these tools to merge the contents of our own charts (and the 3rd-party charts we use) as a
base, with the overrides in the `k8sdeploy` repo and additional overrides in `deploy.yaml`. The result is a
Helm release containing statefulsets, deployments and other K8s resources that are defined in the base chart
then customized based on the overrides.

You can list all the Helm releases in a given namespace on a given cluster by using the `helm ls` command with
the `--kube-context` and `-n` args. For example, to list the Helm releases in the `dev` namespace on the
`prod-us` cluster, you would run the command

```
helm --kube-context prod-us -n dev ls
```

which will show you info about each release such as its name, status, chart and when it was last updated.

<a name="helm-overrides"></a>
### Helm Overrides from `k8sdeploy` and `deploy.yaml`

The overrides mentioned in the previous section (in the `k8sdeploy` repo and in `deploy.yaml`) are layered
starting with the chart, then the `k8sdeploy` overrides, then the `deploy.yaml` overrides. The later an
override is applied in the merge process the higher priority it will be and will override the same values
from an earlier layer.

Therefore, the priority of which values are used is:

* `deploy.yaml` values
* `k8sdeploy` values (for anything not specified in `deploy.yaml` )
* base chart values  (for anything not specified in `deploy.yaml` or `k8sdeploy`)

---

## Infrastructure

### Required Infrastructure

The required infrastructure to support a Vantiq installation is documented in the
[Private Cloud Infrastructure Prerequisites doc](PrivateCloudInfrastructurePrerequisites.md).

This required infrastructure contains items such as the ones described in the next few sections like:

* A Kubernetes cluster with worker node pools configured to provide the needed nodes for Vantiq (compute,
database and shared nodes). These nodes should be spread across 3 AZs [as noted below](#infra-3azs).
* Pre-purchased SSL certificates or a plan to use ones obtained from
[Let's Encrypt via cert-manager](https://cert-manager.io).

<a name="infra-bestpractices"></a>
### Best Practices for Infrastructure

<a name="infra-sufcompute"></a>
#### Deploy Sufficient Compute Resources

The required infrastructure listed above, particularly the nodes required to run the installation pods, are
defined based on real-world experience. While it might be tempting to try to deploy on fewer and/or smaller
nodes (oversubscribe) to save on infrastructure costs, this will result in an installation that is not able
to run properly under load.

<a name="infra-mc"></a>
#### Deploy `metrics-collector`

For production installations it is highly recommended to deploy the `metrics-collector` pod (and a node to
run it on), as noted in the [Metrics Collector section above](#metrics-collector) for the reason noted there
(to process raw metrics from the `vantiq` pods into computed metrics before they are sent to InfluxDB so the
`vantiq` pods don't have to do that processing).

Again, while it might be tempting to not deploy `metrics-collector` to save on the infrastructure cost of
an additional node to run it on, this will result in an installation that is not able run as large of an
application load. What you spend on the additional `metrics-collector` node, you more than make up for in
increased application load capacity of the `vantiq` pods.

<a name="infra-dynstorage"></a>
#### Use Dynamic Storage

The Vantiq system is designed to deploy into a cluster using dynamic storage for the volumes used by some
statefulsets such as `mongodb` and `influxdb`. These dynamic volumes should be separate from the nodes, not
static on a specific node. That way if there is a problem on a node, the volumes will be remounted by K8s
on the new node where the pod using that volume is scheduled.

If you use static volumes that are on a specific node and that node is down, then the pod using those
volumes will not be able to be scheduled by K8s (it will be stuck in `Pending` status).

<a name="infra-realssl"></a>
#### Use a Real SSL Certificate

You must use real SSL certificates, such as ones pre-purchased from a well-known CA or ones obtained from
[Let's Encrypt via cert-manager](https://cert-manager.io). There are complex ways to work around this as
described in
[*Dealing with DNS and SSL in an Air-Gapped Deployment* section of the *Advanced Use Cases* doc](AdvancedUseCases.md#airgapped_dnsssl)
but this is strongly not recommended.

<a name="infra-3azs"></a>
#### Deploy in 3 Availability Zones (AZs)

The Vantiq system is designed to deploy into 3 availability zones (AZs) for maximum system availability. Each
statefulset such as `vantiq` and `mongodb` has at least 3 pods, and if each of those are in a different AZ
then the failure of a whole AZ will only take out a single pod of the 3 in each statefulset and not impact
uptime.

Note that availability zones in a cloud vendor mean complete separation of all infrastructure components
(power, cooling, networking etc.) between AZs. Typically this means that each AZ is a completely separate
data center.

For example, Azure initially had single-data-center regions with some of the infrastructure components in
separate "failure domains" but these were not true AZs. Eventually they implemented true AZs, but you must
configure the node pools to use the true AZs and not the old single-data-center "failure domains".

Another example is AliCloud which has some regions which do not have 3 or more AZs (in some cases there is
only a single AZ in a region).

In any case where you deploy in a region without 3 AZs, a problem with an AZ can take the entire Vantiq
installation down. If you deploy in a region with 3 AZs as recommended, a problem with a single AZ will not
impact uptime of the Vantiq installation (although it can impact performance due to a decreased number of
running `vantiq` pods).

<a name="infra-bkp-sepregion"></a>
#### Store Backups in a Separate Region

The `mongodb` backups built into a normal Vantiq installations are meant for disaster recovery: in the case
of a total region outage, a new set of infrastructure must be built in a new region and then the `mongodb`
data restored from the latest backup. In such a situation, the backups do no good if they are stored in the
region that is offline and therefore the backups are offline as well.

To eliminate this problem, you should store the backups in a separate region. The easiest way to do this is
when you first provision the backups storage: simply provision it in the region you plan to use for disaster
recovery. The backups script itself runs locally in the cluster, but once it's finished it pushes the
backup file to the backups storage location. If that location is in a different region then you are following
this best practice.








