# Vantiq Private Cloud Infrastructure Prerequisites

## Overview

A Vantiq customer-managed private cloud requires a number of infrastructure prerequisites before it can be
installed. These are detailed in the
[Private Cloud – Customer Managed: Prerequisites](https://vantiq.sharepoint.com/:w:/g/EcTxHoSkRE1ClMLwnv2r8ToBtRnBrcIKfoZ_cSy0BnYWyg?e=6UfswH)
document. A summary of those prerequisites is found below.

If you are part of Vantiq Ops, note that the
[Private Cloud – Vantiq Managed: Prerequisites](https://vantiq.sharepoint.com/:w:/g/EbhnBnqg5_ZLu094Cc93_mMBGB0l41f-FWqXcf9voTnawQ?e=CU8adM)
document is the same set of requirements but for a Vantiq-managed private cloud instead of a customer-managed
private cloud. The summary of the prerequisites found below applies to a Vantiq-managed private cloud as well.

Both of these documents are the detailed complete "single source of truth" for these requirements. The
simplified summary info found here is for reference within the docs of this repo, and are not intended to
be a replacement for the Vantiq Sharepoint documents.

**Note:** You will only be able to reach these internal Vantiq documents directly if you are a Vantiq
employee. If you are a Vantiq customer who has purchased a customer-managed private cloud, you should have
been given a copy of the above documents by Vantiq Sales as part of the private cloud sales process before
being granted access to this repo. If this step was somehow missed, please contact your Vantiq Sales team
immediately to obtain a current copy of these documents.


## Summary of Infrastructure Prerequisites

A summary of the infrastructure prerequisites to run a Vantiq private cloud are found in this section.

### Kubernetes

A properly functioning Kubernetes cluster with the capability to:
 - Create dynamic PVs/PVCs
 - Pull container images from hub.docker.com, quay.io & gcr.io
 - Create a service of type `LoadBalancer` that connects to an external L4 load balancer

Currently the supported Kubernetes options are AWS EKS and Azure AKS, which are both managed Kubernetes
offerings from commercial cloud providers. If you are using a Kubernetes other than one of these, it should
work as long as it is a fully functional Kubernetes with the above capabilities. However, before using an
unsupported Kubernetes version to run a Vantiq installation, verification of that Kubernetes environment
must first be done by your Vantiq Sales and Professional Services teams, in cooperation with Vantiq
Engineering.

#### Kubernetes Node Requirements

These requirements change as the Vantiq platform evolves, please see the infrastructure prerequisites docs for
the current details. As of this writing (June 2023), the node requirements for a production Vantiq
installation are:

| Node Pool | Purpose | vCPU | Memory (GB) | Qty | Comment |
|-----------|---------|:----:|:-----------:|:---:|---------|
| compute | vantiq, metrics-collector | 4 | 16 | 4 | 3 for vantiq, 1 for metrics-collector |
| database | mongodb, influxdb | 4 | 32 | 4 or 7 | 3 for mongodb (6 if implementing userdb), 1 for influxdb |
| shared | nginx, keyloak, grafana | 2 | 8 | 4 | nginx, keycloak and grafana share these nodes |

### PostgreSQL Database for Keycloak

To deploy Keycloak for Vantiq authentication, a PostgreSQL database must be provisioned to store the Keycloak
realm data. This database must be accessible from the Kubernetes cluster’s worker nodes.

It is recommended (but not required) that access to the PostgreSQL endpoint be restricted to inside the
cluster network (not externally accessible) for maximum security. 

#### PostgreSQL Config and Credentials Info

The following information must be provided to the person performing the Vantiq install process:  

 - The host name & port used to access the PostgreSQL server 
 - The name of the PostgreSQL admin user for the “keycloak” database if it is not “keycloak”
 - The password of the PostgreSQL admin user for the “keycloak” database

### Outbound Internet Connectivity 

As noted above, the Kubernetes cluster must have the ability to pull the container images needed for the
installation pods. Normally these are pulled from the container images registries listed, which requires
outbound Internet connectivity.

If your IaaS infrastructure does not allow outbound connections to the Internet, these registries or their
mirrors cannot be accessed. In such cases the customer is responsible for making the required images
available in a private container images registry that is accessible within the IaaS infrastructure. The
customer is also responsible for updating the Kubernetes configurations to reference these alternate
registries. 

Also note that this is not a one-time task, as new images are produced for each Vantiq update and must be
transferred to the private registry before each Vantiq update can be installed. This additional maintenance
process should be included in the planning of a non-Internet-connected Vantiq installation.

Vantiq Professional Services can be contracted to assist in setting up these private registries.

### Pod Log Capture

The log output of each pod can most easily be accessed with the `kubectl logs` command. However, this will
only provide the most recent log output. Depending on the Kubernetes config and the verbocity of the pod
log output, the amount of data from the `kubectl logs` command can be limited to the most recent few days,
hours or minutes. It is therefore required to implement a system to capture pod log output so that data can
be retained as long as desired. For example, the Vantiq Ops team retains log data for 60 days.

Any system that retains this data will work. Every cloud vendor normally has a service available which you
can deploy to provide this function. You can also deploy software (open source or commercial) on your own
to to provide this function. For example, the Vantiq Ops team uses Sumo Logic for this purpose.

### Additional Items

The following items must be also be provided:

 - The FQDN (fully qualified domain name) of the Vantiq installation (this should not change for the life of the installation)
 - A DNS entry (`A` record or `CNAME` record) for the FQDN
 - An SSL certificate for the FQDN (or plan to set up [cert-manager](https://cert-manager.io/) to obtain one from [Let's Encrypt](https://letsencrypt.org/))
 - Credentials to an SMTP server that is able to send automated emails from the Vantiq installation
