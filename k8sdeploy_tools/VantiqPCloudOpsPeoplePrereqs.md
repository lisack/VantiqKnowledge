# Vantiq Private Cloud Ops People Prerequisites

## Overview

This document describes the knowledge prerequisites for people who will be installing and managing a Vantiq
private cloud. Anyone who wants to understand and follow the docs in this repo will need to meet the knowledge
prerequisites listed in the next section.

If you are missing a basic understanding of Vantiq admin topics, we recommend you first address that by
taking training in that area. Some resources you can use for that are:

  - Vantiq Documentation
    - [Administrators Reference Guide](https://dev.vantiq.com/docs/system/namespaces/)
    - [Workload Management](https://dev.vantiq.com/docs/system/workloadmanagement/)
  - Vantiq Training
    - [Vantiq Organization & Namespace Administration (Vantiq Admin)](https://community.vantiq.com/courses/organization-namespace-administration/)
    - [Vantiq Deployment & System Administration (the class on k8sdeploy_tools)](https://community.vantiq.com/courses/vantiq-deployment-system-administration/)

In addition, this document describes infrastructure knowledge prerequisites (basic for Vantiq admins, more
advanced for the Ops/Infrastructure people who will create & maintain the underlying infrastructure such as
Kubernetes, networking, storage etc. required by Vantiq).

**Note:** In some organizations, the Ops/Infrastructure people will be a separate team from the team doing the
Vantiq install and management. In other organizations, the same team will do both of these functions. Regardless,
the people doing the infrastructure part will need to have the more in-depth infrastructure knowledge described
in the Infrastructure section which follows the Vantiq install and management section. The team doing the
Vantiq install and management will only need the more limited infrastructure knowledge described within the
Infrastructure subsections of the Vantiq install and management section.

If you are Vantiq admin person who is missing a basic understanding of one of these infrastructure
prerequisites, or you are an infrastructure person who needs more in-depth knowledge than you currently have,
we recommend you first address that by taking training in that area. Some resources you can use for that are:

  - Cloud & Kubernetes Classes (free)
    - kubernetes.io
      - [List of kubernetes.io tutorials](https://kubernetes.io/docs/tutorials/)
      - [Kubernetes Basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
    - Killercoda (interactive)
      - [Kubernetes playground](https://killercoda.com/kubernetes/scenario/playground)
      - [Linux Fundamentals](https://killercoda.com/pawelpiwosz/course/linuxFundamentals)
      - [Linux Foundation Certified System Administrator (LFCS)](https://killercoda.com/lfcs)
      - [Helm](https://killercoda.com/helm-scenarios)
      - [Git](https://killercoda.com/pawelpiwosz/course/gitFundamentals)
    - [KubeAcademy from VMware](https://kube.academy/)
    - Docker
      - [Play With Kubernetes](https://training.play-with-kubernetes.com/)
      - [Kubernetes Workshop](https://training.play-with-kubernetes.com/kubernetes-workshop/)
  - Cloud & Kubernetes Classes (paid)
    - Udemy
      - [Kubernetes classes](https://www.udemy.com/topic/kubernetes/)
      - [Hands-On Kubernetes Networking](https://www.udemy.com/course/hands-on-kubernetes-networking/)
      - [Cloud Computing Fundamentals](https://www.udemy.com/course/welcome-to-cloud-computing-world)
    - [Pluralsight Cloud Guru classes](https://www.pluralsight.com/cloud-guru)
    - Linux Foundation
      - [Cloud & Containers classes](https://training.linuxfoundation.org/cloud-containers/)
      - [Kubernetes Fundamentals (LFS258)](https://training.linuxfoundation.org/training/kubernetes-fundamentals/)

This list of possible classes is not meant to be an endorsement of any particular source of training, just a
list to help you if you don't know where to start. You are welcome to find other sources of training that you
believe to be more effective.

#### Don't Panic

For both the "Installing and Managing Vantiq" role and the Infrastructure role, please note:

  - We don't expect one person to know every item listed, a team collectively can have the knowledge
  - For any area where you don't have anyone with that knowledge, you can hire Vantiq ProServ to handle that area

&nbsp;

## Table of Contents

* [Overview](#overview)
* [Knowledge Prerequisites for Install and Management of a Vantiq Private Cloud](#vantiq_admin_knowledge)
    * [Vantiq Admin Knowledge - Overview](#vantiq_admin_overview)
    * [Language](#vantiq_admin_language)
    * [Software Within (or external but used by) a Vantiq Installation](#vantiq_admin_vantiqsw)
    * [Software Used by k8sdeploy_tools Tools](#vantiq_admin_kdtsw)
    * [Kubernetes (Infrastructure)](#vantiq_admin_k8s)
    * [General Infrastructure](#vantiq_admin_geninfra)
    * [Cloud or On-Prem Infrastructure](#vantiq_admin_cloudinfra)
* [Knowledge Prerequisites for Creating & Managing Infrastructure Needed for a Vantiq Private Cloud](#infrastructure_knowledge)
    * [Infrastructure Knowledge - Overview](#infra_knowledge_overview)
    * [General Infrastructure](#infra_knowledge_geninfra)
    * [Cloud Infrastructure](#infra_knowledge_cloudinfra)
    * [Kubernetes](#infra_knowledge_k8s)
    * [Managed Cloud Vendor Kubernetes](#infra_knowledge_cloudk8s)
    * [Software Within (or external but used by) a Vantiq Installation](#infra_knowledge_vantiqsw)
    * [Software Used by k8sdeploy_tools Tools](#infra_knowledge_kdtsw)

&nbsp;

<a name="vantiq_admin_knowledge"></a>
## Knowledge Prerequisites for Install and Management of a Vantiq Private Cloud

<a name="vantiq_admin_overview"></a>
### Vantiq Admin Knowledge - Overview

In order to know if you have enough "basic understanding" of the following areas, you should start by reading
the docs in this repo. If there are areas of the docs you don't understand, that likely indicates areas of
knowledge you need to learn.

We also recommend you take the matching
[Vantiq Deployment & System Administration](https://community.vantiq.com/courses/vantiq-deployment-system-administration/)
class, which covers the same info found in the k8sdeploy_tools docs but as a class.

For all sections below that are infrastructure (Kubernetes, general and cloud
infrastructure), you should discuss with your Infrastructure team the areas you and they will be responsible
for, in order to determine the areas of infrastructure knowledge you will need to learn. In some cases the
Infrastructure team may handle all such work and you will only need enough understanding to know which parts
do what.

For everything in this section, a basic level of knowledge should be enough to use k8sdeploy_tools to deploy
and manage a Vantiq installation. Again, read the k8sdeploy_tools docs (and take the
[matching class](https://community.vantiq.com/courses/vantiq-deployment-system-administration/)) which
should help you identify any areas where you need to learn more. You are also likely to find that the more
basic your knowledge level is of a given area, if you have a problem in that area the more likely you will
need to get assistance from a more experienced co-worker (or your Infrastructure team, for the infrastructure
areas) to find the root cause. As you gain a deeper level of understanding of a given area, you are more
likely to be able to determine a root cause and fix it yourself.

<a name="vantiq_admin_language"></a>
### Language

Since the docs and class materials are in English, the ability to read & understand technical English is required.

<a name="vantiq_admin_vantiqsw"></a>
### Software Within (or external but used by) a Vantiq Installation

Understanding how Java-based applications behave will help you manage the Vantiq server cluster. You also
may need to diagnose any one of these other software elements by examining their logs, and possibly running
commands on their pods directly. You are not expected to be an expert in each of these, but you should
understand their function in a Vantiq installation. You should also know how to examine their logs via 
`kubectl logs` and/or the logging system in your environment.

  - Java (the Vantiq server is a Java application)
  - MongoDB - stores Vantiq user and system data
  - nginx - terminates TLS connections into Vantiq
  - Keycloak - provides Vantiq user management
  - PostgreSQL - stores Keycloak data, normally does not require any manual intervention
  - InfluxDB - storage of performance metrics from Vantiq and from Kubernetes
  - Grafana - visualization of performance metrics from InfluxDB
  - MySQL - small db to store Grafana config data, normally does not require any manual intervention
  - SMTP server (delivers system and namespace invites)

<a name="vantiq_admin_kdtsw"></a>
### Software Used by k8sdeploy_tools Tools

Our tools use the following software to do the install/update work. It is possible to run our tools with
only a basic knowledge of Git and kubectl: knowing how to run the git and kubectl commands in the docs in
this repo is the minimum required. However, if you only have this minimal knowledge and you encounter any
problems, you will find it difficult to diagnose them. A bit deeper knowledge of Git and kubectl, along
with a basic knowledge of Helm and Gradle, is recommended.

  - Git – our tools use 3 Git repos, one of which you need to modify each time you modify a Vantiq installation
  - kubectl – interact with and modify a Kubernetes cluster
  - Helm - the Kubernetes package manager, all Vantiq installation components are deployed via Helm charts
  - Gradle - the tools themselves are written in Gradle

Gradle in particular can be challenging for those not already familiar with it. There is a
[*Gradle Tips* section in the *Installation* doc](Installation.md) that has some helpful info. If you have
a problem with our tools whose root cause appears to be in Gradle, the error message may or may not be
helpful. In such cases you can consult any Java developers in your organizations who have more Gradle
knowledge, but if that does not lead to a solution please contact [Vantiq Support](mailto:support@vantiq.com).

<a name="vantiq_admin_k8s"></a>
### Kubernetes (Infrastructure)

A basic understanding of Kubernetes:

  - Kubernetes resources - containers, pods, statefulsets & deployments, services, storage classes, PVs/PVCs etc
  - Networking - how it works within Kubernetes itself (inter-pod communication, network policy)
  - Storage - what PVs & PVCs are (some pods in a Vantiq installation use PVCs for storage)
  - What K8s are you using? Cloud provider managed K8s such as EKS, AKS, OCI, GKE vs. vanilla K8s on VMs (RKE2, OpenShift or BYO)
  - Advanced: how cert-manager can provide free, auto-renewing SSL certificates from Let's Encrypt

<a name="vantiq_admin_geninfra"></a>
### General Infrastructure

A basic understanding of the following general infrastructure elements:

  - Linux - all our containers are Linux-based so Linux skills & knowledge are needed
  - Networking - some understanding of how TCP/IP & load balancers work is useful
  - Storage - how your block storage becomes Kubernetes PVs/PVCs, and the "bucket" storage for your MongoDB backups
  - SSL Certificates - how they provide a working HTTPS connection
  - How to use the logging/monitoring/alerting systems in your environment set up by your Infrastructure team
  - Compute capacity planning - baseline needs for nodes, and what will be needed if you want to scale up
  - Business continuity / disaster recovery - what your plans are to respond to a major infrastructure outage

<a name="vantiq_admin_cloudinfra"></a>
### Cloud or On-Prem Infrastructure

A basic understanding that maps the general infrastructure knowledge listed above into the specifics of your chosen cloud (IaaS) vendor or on-prem infrastructure:

  - Networking - how does yours work, what are your load balancer details (which maps to your K8s service of type LoadBalancer)
  - Storage - how your block storage works (may need to include a discussion of performance choices and snapshot details with your Infrastructure team)
  - CLI - if you need to perform infrastructure tasks, using the cloud vendor CLI is faster and more repeatable than clicking in a console


<a name="infrastructure_knowledge"></a>
## Knowledge Prerequisites for Creating & Managing Infrastructure Needed for a Vantiq Private Cloud

<a name="infra_knowledge_overview"></a>
### Infrastructure Knowledge - Overview

In order to know if you have enough knowledge of the following areas, you should start by reading the docs in
this repo that relate to infrastructure. We recommend you read the following docs in this order:

  - Understand how these tools work, and how the components of a Vantiq installation interact, by reading
    [Deploying and Managing Vantiq Installations - Background Reference](BackgroundReference.md).
  - The infrastructure prerequisites for a Vantiq installation are listed in the
    [Vantiq Private Cloud Infrastructure Prerequisites](PrivateCloudInfrastructurePrerequisites.md) which
    is the most important document for you to read and understand.
  - The [*Deployment Prerequisites* section of the *Installation* doc](Installation.md#deployment-prerequisites)
    lists these same infrastructure prerequisites, and is worth a review to see them in the context of doing an
    actual Vantiq install.
  - Part of [Vantiq Deployment Configurations](VantiqDeploymentConfigurations.md) contains infrastructure
    details (mainly resource requirements), which are driven by the choice of deployment options for your Vantiq installation(s).
  - You should review [Managing Vantiq Installations](ManagingVantiqInstallations.md). This mainly covers how
    to manage existing Vantiq installations using the System dashboards in Grafana, but some of those involve
    infrastructure elements such as pod CPU and memory use. At times you will need to work with the Vantiq admins
    to correlate this pod CPU and memory use with the node-level CPU and memory use in your realm. Depending on
    the skillsets of the Vantiq admins and Ops/Infrastructure Admins, you may need to assist in diagnosis of
    patterns in the Java _Memory Usage_ panes of the _Vantiq Resources_ dashboard.
  - You may find it useful to review the [Vantiq Kubernetes Cheat Sheet](VantiqK8sCheatSheet.md) to see
    some of the `kubectl` commands useful for managing Vantiq installations.

If there are areas of the above docs you don't understand, that likely indicates areas of knowledge you need
to learn. For everything in this section, a level of knowledge sufficient to create and maintain the 
infrastructure listed in the
[Vantiq Private Cloud Infrastructure Prerequisites](PrivateCloudInfrastructurePrerequisites.md)
should be all you need.

<a name="infra_knowledge_geninfra"></a>
### General Infrastructure

Understanding of how standard infrastructure elements function, and how they are interrelated:

  - Linux - unless you run Windows-based Kubernetes nodes (not recommended), all infrastructure VMs and Kubernetes pods will be Linux-based so a solid foundation of Linux skills & knowledge is needed
  - Networking - how TCP/IP & load balancers work
  - Storage - block storage basics that you can apply to the cloud vendor specifics and Kubernetes PVs/PVCs & CSI
  - SSL Certificates - how they work
  - Logging/Monitoring/Alerting systems - which are you using? The Vantiq team will need to be trained on these
  - Provisioning automation - Vantiq SRE uses Terraform but you can use anything that works for you (automation is faster and more repeatable than clicking in a console)
  - Long-term infrastructure management: capacity planning, business continuity / disaster recovery

<a name="infra_knowledge_cloudinfra"></a>
### Cloud Infrastructure

A basic understanding that maps the general infrastructure knowledge listed above into the specifics of your chosen cloud (IaaS) vendor:

  - Networking - cloud virtual network (VPC/VNet/VCN), cloud vendor load balancer details
  - Storage - how the cloud vendor block storage works, including performance-level choices and snapshot details
  - CLI - how to use the cloud vendor to perform needed tasks (faster and more repeatable than clicking in a console)

<a name="infra_knowledge_k8s"></a>
### Kubernetes

A good understanding of Kubernetes:

  - Kubernetes resources - containers, pods, statefulsets & deployments, services, storage classes, PVs/PVCs etc
  - Networking
    - How it generally works within Kubernetes itself (inter-pod communication, network policy implementation)
    - How it is implemented by the Kubernetes networking you use (CNI, Flannel/Calico/Cillium/etc)
    - Advanced: how it is implemented on the nodes (iptables or equiv, overlay networking, integration with cloud networking)
  - Storage - PVs/PVCs, CSI, snapshot support, how your cloud storage behavior can affect PV/PVC behavior
  - Vantiq-supported cloud provider K8s (EKS, AKS, OCI) vs. others (GKE) vs. vanilla K8s on VMs (RKE2, OpenShift or BYO)
  - Advanced: obtaining free SSL certificates from Let's Encrypt using cert-manager

<a name="infra_knowledge_cloudk8s"></a>
### Managed Cloud Vendor Kubernetes

Understand how the managed Kubernetes of your chosen cloud vendor (EKS, AKS, OCI etc) works, especially how it differs from standard Kubernetes:

  - Networking
    - How do they implement Kubernetes network policy?
    - Do they short circuit traffic to your LB frontend to keep it on the nodes? This can affect network policy.
    - Kubernetes networking elements (CNI, Flannel/Calico/Cillium) - which choices are available, and which are optimal?
    - Advanced: how do they implement Kubernetes networking on the nodes (iptables or equiv, overlay networking, integration with cloud networking)?
  - Storage - details of their CSI, snapshot support, how their cloud storage affects PV/PVC behavior
  - Kubernetes upgrade process
  - Other differences in behavior from standard Kubernetes, if any

<a name="infra_knowledge_vantiqsw"></a>
### Software Within (or external but used by) a Vantiq Installation

Understanding how Java-based applications behave will help your Vantiq team manage the Vantiq server cluster. If their experience in this area is limited and yours is more extensive, they may need to consult with you to diagnose problems.

They also may need to diagnose any one of these other software elements by examining their pod logs either with kubectl logs or in the log management system you deploy. You should ensure they know how to use the log management system, since the data in kubectl logs typically has limited retention.

It is possible they may need additional expertise with some of this software to either diagnose problems or optimize data. For example, if you have people with expertise in some of these packages (such as DBAs for MongoDB or InfluxDB, or someone with deeper nginx experience), your Vantiq team may need to consult with these experts if they are trying to do something outside of Vantiq.

  - Java (the Vantiq server is a Java application)
  - MongoDB - stores Vantiq user and system data
  - nginx - terminates TLS connections into Vantiq
  - Keycloak - provides Vantiq user management
  - PostgreSQL - stores Keycloak data
  - InfluxDB - storage of performance metrics from Vantiq and from Kubernetes
  - Grafana - visualization of performance metrics from InfluxDB
  - MySQL - small db to store Grafana config data
  - SMTP server (delivers invites)

<a name="infra_knowledge_kdtsw"></a>
### Software Used by k8sdeploy_tools Tools

Our tools use the following software to do the install/update work. As noted above, while it is possible to run our tools with only a basic knowledge of Git and kubectl, your Vantiq team will find it difficult to diagnose any problems they have. A deeper knowledge of Git and kubectl, along with a basic knowledge of Helm and Gradle, is recommended. If your team has this knowledge, your Vantiq team may need help from them.

  - Git – the tools use 3 Git repos, one of which you need to modify each time you modify a Vantiq installation
  - kubectl – interact with and modify a Kubernetes cluster
  - Helm - the Kubernetes package manager, all Vantiq installation components are deployed via Helm charts
  - Gradle - the tools themselves are written in Gradle
