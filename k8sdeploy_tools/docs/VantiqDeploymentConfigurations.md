# Vantiq Deployment Configurations

## Overview

Vantiq supports a range of deployment options for the Vantiq platform. Most of them are cloud options, and
for those cloud options there are different deployment configurations (`production` and `development`). The
choice of deployment configuration will determine the number of pods for the `vantiq` and `mongodb`
statefulsets, which in turn will determine the number of nodes needed for those statefulsets.

&nbsp;

## Deployment Options

Vantiq supports a range of deployment options for the Vantiq platform. Customers select the option that best
matches their business and technical requirements. These options are:

 - Vantiq Cloud
 - Private Cloud
   - Vantiq Managed (Vantiq manages on behalf of the customer)
   - Customer Managed (the customer manages it themselves)
 - Vantiq Edge

A customer must choose one of Vantiq Cloud or Private Cloud for application development and production
deployment. A customer can choose to develop on the Vantiq Cloud and deploy into production on a Private
Cloud. Vantiq Edge is only for edge processing in conjunction with a Vantiq Cloud or Private Cloud deployment.  

These deployment options are described in more detail in the
[Vantiq Deployment Configurations](https://vantiq.sharepoint.com/:w:/g/EUf0rFP3C8xMnsLaZc9yJu4BJOh8V99DS_QqJ9X6dsRMMw?e=OvIE2Q)
document in Vantiq's Sharepoint.

### Vantiq Cloud  

For customers, operating on a Vantiq Cloud is the simplest option. 

All aspects of a Vantiq Cloud are deployed and managed by Vantiq:

 - Compute and other infrastructure resources
 - Monitoring to maintain performance and to detect and correct any faults
 - Scaling as needed to support the workload from currently active customers
 - Backups to enable disaster recovery in the event of a catastrophic infrastructure outage 
 - Operate the cloud in conformance with contracted service level agreements

Customer responsibility is to use the system within the terms of their contract:  

 - Adhere to the resource usage levels specified in their contract
 - Perform application development activities only on the designated development cloud 
 - Deploy production systems only to the designated production cloud 

Customers must not deploy applications into production on a development Vantiq Cloud and must not do
development on a production Vantiq Cloud. 

Customers are also responsible for validating their systems when new releases are introduced by Vantiq two
or three times per year. New releases are announced in advance. Release updates to the development Vantiq
Clouds precede release updates to the production Vantiq Clouds by 15 to 30 days. This gives customers time to
requalify their applications in a development environment before the new release is introduced to production.

A Vantiq Cloud is multi-tenant, so customer applications share system resources. Access to the Vantiq Cloud
is secure, with only authorized users allowed access to the Vantiq Cloud and only to the namespaces to which
they have been granted access. Vantiq ensures that there is no data sharing among customers unless the
customer explicitly authorizes such sharing.


### Private Cloud  

Private Cloud deployments of Vantiq products are operated exclusively for a single customer. 

Customers typically choose this option due to one or more of the following requirements:  

 - For regulatory, security, privacy, corporate policy, or other reasons the customer is not allowed to
deploy in a shared, multi-tenant environment such as the Vantiq Cloud deployments described in the previous
section.  
 - A desire to make sure that all resources in the cloud deployment are allocated to their applications
rather than being shared in a multi-tenant environment.  
 - Have applications or customers that cannot requalify their applications on the schedule required by
Vantiq Cloud deployments. In a Private Cloud the upgrade schedule and the number of upgrades introduced
is at the discretion of the customer. 

There is no option to “skip over” interim minor releases. At the time of an upgrade, each minor release
between the currently deployed release (v1.X.Y) and the target release (v1.X+N.Y) must be installed in
turn (v1.X+1.Y, v1.X+2.Y, until v1.X+N.Y is reached).  

### Vantiq Edge 

Vantiq Edge deployments are deployments of the Vantiq Edge Edition. Vantiq Edge Edition is a simple,
single-server Vantiq configuration specifically designed for deployment by customers on smaller compute
nodes, typically located at or near the network edge. 

Vantiq Edge Edition may not be substituted for a Vantiq Cloud deployment or a Private Cloud deployment.
Vantiq Edge Edition always operates in conjunction with a Vantiq Cloud or Private Cloud deployment.  

&nbsp;

## Vantiq Cloud Deployment Configurations

For the cloud deployment options, there are two deployment configurations, `production` and `development`. The
`production` configuration has several options: minimal private, minimal public, and from there any number of
options scaled up from minimal public to any performance level needed. The choice of deployment configuration
will determine the number of pods for the `vantiq` and `mongodb` statefulsets, which in turn will determine
the number of nodes needed for those statefulsets.

Along with infrastructure prerequisites, these cloud deployment configuration options are detailed in the
[Private Cloud – Customer Managed: Prerequisites](https://vantiq.sharepoint.com/:w:/g/EcTxHoSkRE1ClMLwnv2r8ToBtRnBrcIKfoZ_cSy0BnYWyg?e=6UfswH)
document.

If you are part of Vantiq Ops, note that the
[Private Cloud – Vantiq Managed: Prerequisites](https://vantiq.sharepoint.com/:w:/g/EbhnBnqg5_ZLu094Cc93_mMBGB0l41f-FWqXcf9voTnawQ?e=CU8adM)
document contains the same cloud deployment configuration options but for a Vantiq-managed private cloud
instead of a customer-managed private cloud.

Both of these documents are the detailed complete "single source of truth" for these cloud deployment
configuration options. The simplified summary info found here is for reference within the docs of this repo,
and are not intended to be a replacement for the Vantiq Sharepoint documents.

**Note:** You will only be able to reach these internal Vantiq documents directly if you are a Vantiq
employee. If you are a Vantiq customer who has purchased a customer-managed private cloud, you should have
been given a copy of the above documents by Vantiq Sales as part of the private cloud sales process before
being granted access to this repo. If this step was somehow missed, please contact your Vantiq Sales team
immediately to obtain a current copy of these documents.

### Vantiq Cloud Deployment: `development` Configuration

The `development` configuration is a minimal development deployment which provides a single Vantiq server and
single copy of each of the supporting services used by the Vantiq platform including MongoDB. A minimal
development deployment has the following characteristics: 

 - Reduced availability since there is no fault tolerance available
 - Potential for data loss since the associated data store is not replicated
 - Reduced performance since there is only a single server to support the Vantiq workload
 - No QDrant database so no semantic indexes for AI

The minimal development deployment consists of four nodes with the following uses:

| Purpose | vCPU | Memory (GB) | Comment |
|---------|:----:|:-----------:|---------|
| Vantiq server | 2 | 4 | |
| MongoDB server | 2 | 16 | |
| Monitoring server (InfluxDB) | 2 | 8 | |
| Shared | 2 | 4 | Used for nginx, keycloak and grafana |

Performance can be improved in this configuration by increasing the node vCPUs and memory.

Note: this configuration is selected by setting the `deployment` parameter to `development` in
`cluster.properties`. One of the results of using this setting is that the Java heap size will
be set automatically to 2GB as follows:

```
vantiq.defaults: 'export JAVA_OPTS="-Xms2G -Xmx2G -DVANTIQ_CLUSTER_SIZE=${VANTIQ_CLUSTER_SIZE:=0}"'
```

If you do increase the the compute node memory so you can increase the Vantiq server pod memory,
you can increase the Java heap size by setting an override in `deploy.yaml`.

### Vantiq Cloud Deployment: Minimal Private `production` Configuration

A minimal private production deployment provides replication for the Vantiq server as well as each of the
critical supporting services used by the Vantiq platform. A minimal private production deployment has the
following characteristics:

 - Higher availability since the clustered services are fault tolerant
 - Data loss is unlikely since the associated data store is replicated (backups are still recommended)
 - Increased performance since there are clustered servers to support the Vantiq workload

The minimal production deployment consists of 14 nodes with the following uses:

| Purpose | vCPU | Memory (GB) | Node Qty | Comment |
|---------|:----:|:-----------:|:---:|---------|
| Vantiq servers | 2 | 4 | 4 | 3 for vantiq, 1 for metrics-collector |
| Database servers | 2 | 16 | 7 | 3 for MongoDB, 3 for QDrant, 1 for InfluxDB |
| Shared | 2 | 4 | 3 | Used for Nginx, Keycloak and Grafana |

Note: this configuration is selected by setting the `deployment` parameter to `production` in
`cluster.properties`, which will result in the Java heap size being set to 4GB by `k8sdeploy` as
follows:

```
vantiq.defaults: 'export JAVA_OPTS="-Xms4G -Xmx4G -DVANTIQ_CLUSTER_SIZE=${VANTIQ_CLUSTER_SIZE:=0}"'
```

If using this "minimal private production" deployment where the `compute` nodes have only 4GB of
memory, you will need to decrease the Java heap size to 2GB by setting an override in `deploy.yaml`:

```
vantiq.defaults: 'export JAVA_OPTS="-Xms2G -Xmx2G -DVANTIQ_CLUSTER_SIZE=${VANTIQ_CLUSTER_SIZE:=0}"'
```

### Vantiq Cloud Deployment: Minimal Public `production` Configuration

Like a minimal private production deployment, a minimal public production deployment provides replication for
the Vantiq server and critical supporting services used by the Vantiq platform. It has larger minimum node
sizes and the option to deploy a second MongoDB replicaset for user data. A minimal public production
deployment has the following characteristics:

 - Higher availability since the clustered services are fault tolerant
 - Data loss is unlikely since the associated data store is replicated (backups are still recommended)
 - Increased performance since there are clustered servers to support the Vantiq workload

The option of implementing a second `userdb` MongoDB replicaset can be implemented if desired. You may want
to implemented the `userdb` statefulset if you are using a private cloud to offer public-facing Vantiq
applications to your own customers, and you have concerns of being perceived by MongoDB (the company) as
offering MongoDB as a Service as defined in section 13 of
[the MongoDB SSPL](https://www.mongodb.com/licensing/server-side-public-license), despite the details in the
[SaaS using MongoDB section of the MongoDB SSPL FAQ](https://www.mongodb.com/licensing/server-side-public-license/faq).
If this is the case, then you can run a single `mongodb` statefulset using MongoDB 3.6.8 and continue to use
it as long as Vantiq supports MongoDB 3.6.8.

If you have such concerns you can also use MongoDB 3.6.8 only for Type data in Vantiq applications (the
`userdb` statefulset), and use a newer MongoDB version for the Vantiq system data (the `mongodb`
statefulset). This requires 3 more pods for the `userdb` MongoDB replicaset, which in turn requires 3 more
database nodes.

The minimal public production deployment consists of 14 or 17 nodes with the following uses:

| Purpose | vCPU | Memory (GB) | Qty | Comment |
|---------|:----:|:-----------:|:---:|---------|
| Vantiq servers | 4 | 8 | 4 | 3 for vantiq, 1 for metrics-collector |
| Database servers | 4 | 32 | 7 or 10 | 3 for MongoDB (3 more if implementing userdb), 3 for QDrant, 1 for InfluxDB |
| Shared | 2 | 4 | 3 | Used for nginx, keycloak and grafana |

### Vantiq Cloud Deployment: Larger `production` Configurations

Beyond the minimal public production deployment above, a Vantiq installation can be scaled in a number of
ways. For all these examples we are not implementing userdb.

The first and simplest of these is to scale up by increasing the memory limit of the `vantiq` pods (which
in turn requires more memory on the nodes where they run). For example:

| Purpose | vCPU | Memory (GB) | Qty | Comment |
|---------|:----:|:-----------:|:---:|---------|
| Vantiq servers | 4 | 16 | 4 | 3 for vantiq, 1 for metrics-collector |
| Database servers | 4 | 32 | 7 | 3 for MongoDB, 3 for QDrant, 1 for InfluxDB |
| Shared | 2 | 4 | 3 | Used for nginx, keycloak and grafana |

This could also be combined with a scale-out of adding 2 more `vantiq` pods/nodes:

| Purpose | vCPU | Memory (GB) | Qty | Comment |
|---------|:----:|:-----------:|:---:|---------|
| Vantiq servers | 4 | 16 | 6 | 5 for vantiq, 1 for metrics-collector |
| Database servers | 4 | 32 | 7 | 3 for MongoDB, 3 for QDrant, 1 for InfluxDB |
| Shared | 2 | 4 | 3 | Used for nginx, keycloak and grafana |

Note: for optimal operation of the `vantiq` pods, you should always have an odd number of pods. The base
number is 3, but if you scale out (more pods) rather than up (larger pods) you should increase the
`vantiq` pod count to 5, 7, 9, 11 and so on.

You can also scale up instead of out. Here is an example of doubling the resources of the first example
in this section (2x size for the `vantiq` pods/nodes, adjusting the pod CPU and memory limits to match).
In this case (or the scale-out example) you may want to also scale up the database nodes to match. Here is
an example of that:

| Purpose | vCPU | Memory (GB) | Qty | Comment |
|---------|:----:|:-----------:|:---:|---------|
| Vantiq servers | 8 | 32 | 4 | 3 for vantiq, 1 for metrics-collector |
| Database servers | 8 | 64 | 7 | 3 for MongoDB, 3 for QDrant, 1 for InfluxDB |
| Shared | 2 | 4 | 3 | Used for nginx, keycloak and grafana |

Which of these changes are the proper fit for your private cloud will depend on your application workloads.
Before making such changes, you should monitor the CPU and memory use of your installation pods (both
`vantiq` and `mongodb`) under load using the Vantiq Resources system dashboard in Grafana. This should
provide you with the data to determine where you need more resources (and if so, which resources you need).

### Infrastructure Requirements for `production` Vantiq Cloud Deployment Configurations

For `production` Vantiq cloud deployment configurations, the nodes used for each system component which
has multiple pods for fault tolerance (Vantiq, MongoDB, Keycloak, nginx) must be allocated across three
availability zones. Such a configuration enables the multi-pod statefulsets and deployments to survive
the outage of a whole availability zone. 

All pods which require persistent volumes (MongoDB, InfluxDB etc.) require the storage to be provided
by cloud volumes that can be provisioned dynamically and bound to any any node, allowing Kubernetes to
schedule the matching pods to any node in the same availability zone as the volume.
