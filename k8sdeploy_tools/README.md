# `k8sdeploy_tools`

# Tools to Deploy & Manage Vantiq Installations in Kubernetes

## Overview

This repo is the home to the Vantiq Kubernetes (K8s) deployment utilities. Using the tasks defined in the
tools in this repo, you can perform a complete deployment of Vantiq and its core dependencies into any
compliant Kubernetes cluster.

The repo also contains documents with background info on how these tools and a Vantiq installation work, and
other documents on how to manage a Vantiq installation.

The docs which contain the details of these tasks are referenced below. They are separated by subject
(each one has a specific focus on a single area of deploying or managing a Vantiq installation).

For information on how to perform initial setup and configuration of these tools, please see the
[Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](docs/k8sdeploy_toolsBootstrap.md)
document.

If you have already followed these instructions then you will have a copy of this repository on your
local disk. It is a good practice to make sure to update your copy of the tools any time you are
going to use them (to ensure that you have the most recent version). This can be accomplished with
the command `git pull` executed in the root directory of the repository (typically named
`k8sdeploy_tools`).

If you are starting out learning about these tools, it is recommended to read the docs in the order
listed below, to help you understand the info in all of them more fully.

It is expected that once you have learned these tools by reading the docs listed below, you will continue to
reference the following docs as needed:

 - [Installing Vantiq](docs/Installation.md) when installing Vantiq
 - [Managing Vantiq Installations](docs/ManagingVantiqInstallations.md) when managing a Vantiq installation
 - [Vantiq Installation Patch Procedure](docs/VantiqInstallationPatchProcedure.md) when patching a Vantiq installation
 - [Vantiq Installation Upgrade Procedure](docs/VantiqInstallationUpgradeProcedure.md) when upgrading a Vantiq installation

&nbsp;

## Knowledge Prerequisites for People

In order to be successful installing and managing a Vantiq private cloud, the people doing it (and the
people creating and managing the infrastructure on which Vantiq runs) need to meet certain knowledge
prerequisites.

The details of these knowledge prerequisites can be found in the
[Vantiq Private Cloud Ops People Prerequisites doc](docs/VantiqPCloudOpsPeoplePrereqs.md), and are
summarized below.

In some organizations, the "installing and managing Vantiq" team and the Infrastructure team are separate.
In other organizations, the same team will do both of these functions. Regardless, the people "installing and
managing Vantiq" will need to have the knowledge described in the
[Knowledge Prerequisites to Install and Manage Vantiq](docs/VantiqPCloudOpsPeoplePrereqs.md#vantiq_admin_knowledge)
section, and the people doing the infrastructure part will need to have the knowledge described in the
[Create and Manage Infrastructure](docs/VantiqPCloudOpsPeoplePrereqs.md#infrastructure_knowledge) section.

**A note for organizations with separate Infrastructure and "Installing and Managing Vantiq" teams:** both teams
should meet to clarify responsibilities for infrastructure areas, as well as infrastructure detail choices
if there are such choices to be made. It is highly recommended to have this conversation as early in the
project as possible. Also, please note that if your combination of chosen Kubernetes and underlying
infrastructure is not one that has previously been certified by Vantiq, additional time (and Vantiq ProServ
hours) will need to be built into the project to certify your chosen infrastructure.

### Knowledge Prerequisites - Vantiq Private Cloud Admins

The knowledge prerequisites for anyone installing and/or managing a Vantiq private cloud include:

  - The ability to read & understand technical English
  - Basic understanding of the parts of a Vantiq installation (the Vantiq server, MongoDB, nginx, Keycloak, InfluxDB, Grafana etc)
    - Understand their function in a Vantiq installation
    - Know how to examine their logs via `kubectl logs`
  - Software Used by k8sdeploy_tools Tools
    - Basic knowledge of Git and kubectl (at a minimum, know how to run the `git` and `kubectl` commands in the docs)
    - Some knowledge of Helm and Gradle is recommended
  - Infrastructure
    - A basic understanding of Kubernetes
      - K8s resources - containers, pods, PVs/PVCs etc
      - Networking - how it works within Kubernetes itself
      - Storage - PVs & PVCs
      - Your K8s distribution
    - Some understanding of general infrastructure: Linux, networking, storage etc.
    - Some understanding of your cloud or on-prem infrastructure


### Knowledge Prerequisites - Ops/Infrastructure Admins

The knowledge prerequisites to create and maintain the infrastructure needed for a Vantiq private
cloud mirror the infrastructure required. These infrastructure requirements are found in the
[Private Cloud Infrastructure Prerequisites doc](PrivateCloudInfrastructurePrerequisites.md). This
infrastructure must be created by your Infrastructure team before the team who will install and
manage Vantiq can begin their work.

Generally the list of knowledge prerequisites for Ops/infrastructure admins is similar to the
Infrastructure section of the list above for Vantiq Private Cloud Admins, but more in-depth
knowledge is required. For the details on this, please see the
[*Knowledge Prerequisites for Creating & Managing Infrastructure* section of the *Vantiq Private Cloud Ops People Prerequisites* doc](docs/VantiqPCloudOpsPeoplePrereqs.md).

&nbsp;

## Documents Listing

The following primary documents exist in this repo:

| Document | Purpose |
|----------|---------|
| README.md | This file - top-level info |
| [Deploying and Managing Vantiq Installations - Background Reference](docs/BackgroundReference.md) | Understand how the `k8sdeploy_tools` tools work, and how the components of a Vantiq installation interact |
| [Vantiq Private Cloud Infrastructure Prerequisites](docs/PrivateCloudInfrastructurePrerequisites.md) | Infrastructure prerequisites for a Vantiq installation |
| [Vantiq Private Cloud Ops People Prerequisites doc](docs/VantiqPCloudOpsPeoplePrereqs.md) | Knowledge prerequisites for people installing and managing a Vantiq private cloud, and the people creating and managing the infrastructure on which Vantiq runs |
| [Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](docs/k8sdeploy_toolsBootstrap.md) | How to bootstrap the `k8sdeploy_tools` tools |
| [Installing Vantiq](docs/Installation.md) | How to deploy a new Vantiq installation, and update existing Vantiq installations such as performing version upgrades & updates. |
| [Vantiq Deployment Configurations](docs/VantiqDeploymentConfigurations.md) | The various deployment configuration options for a Vantiq installation (such as `production` or `development`) and the resource requirements for them. |
| [Secrets Management in Vantiq](docs/SecretsManagement.md) | Managing secrets (sensitive configuration) in Vantiq |
| [Centrally Managing Cluster Definitions - Vantiq Ops Method](docs/VantiqManagedDefinition.md) | The method Vantiq Ops uses to centrally manage cluster definitions in GitHub |
| [Locally Managing Cluster Definitions](docs/LocallyManagedDefinition.md) | The method you can use to manage cluster definitions locally on your machine using Git |
| [Centrally Managing Cluster Definitions - Customer Methods](docs/CustomerManagedDefinition.md) | The method customers can use to centrally manage cluster definitions in GitHub or other Git-based service |
| [Vantiq Kubernetes Cheat Sheet](docs/VantiqK8sCheatSheet.md) | Kubernetes cheat sheet for managing Vantiq installations |
| [Managing Vantiq Installations](docs/ManagingVantiqInstallations.md) | How to manage existing Vantiq installations. Mainly this documents the System dashboards, and also includes some important patterns to follow when using them. |
| [Vantiq Installation Patch Procedure](docs/VantiqInstallationPatchProcedure.md) | Procedure to patch (update from v1.X.Y to v1.X.Y+1) a Vantiq installation |
| [Vantiq Installation Upgrade Procedure](docs/VantiqInstallationUpgradeProcedure.md) | Procedure to upgrade (minor release, from v1.X.Y to v1.X+1.0) a Vantiq installation |
| [Availability Monitoring of Vantiq Installations](docs/AvailabilityMonitoring.md) | How to monitor the availability of Vantiq installations using the Heartbeat and Monitor Vantiq Applications |

There are also the following special-purpose documents in this repo:

| Document | Purpose |
|----------|---------|
| [Advanced Use Cases](docs/AdvancedUseCases.md)  | Advanced installation use cases such as complex networking scenarios and air-gapped installs |
| [Vantiq R1.37 Upgrade Instructions for AI Components](docs/R1dot37Upgrade.md) | Extra steps when upgrading Vantiq from R1.36 to R1.37, to add new AI components (the AI Assistant and the QDrant vector db for semantic indexes). |
| [Vantiq R1.37 Upgrade Instructions - Alternate Non-AI Config for R1.37 and Later Releases](docs/R1dot37AltNonAI.md) | Extra steps when upgrading Vantiq from R1.36 to R1.37, while disabling the new AI components because you wish to not run them in your private cloud. |
| [Vantiq R1.39 Upgrade Instructions for QDrant, Keycloak, and GenAI Flow Connectors](docs/R1dot39Upgrade.md) | Extra steps when upgrading Vantiq from R1.38 to R1.39, required to upgrade QDrant to v1.9.2, Keycloak to v24, and how to deploy any needed GenAI Flow connectors after the upgrade. |
| [Vantiq R1.40 Upgrade Instructions to update QDrant & Vantiq Volumes, Add `unstructured-api`](docs/R1dot40Upgrade.md) | Extra steps when upgrading Vantiq from R1.39 to R1.40, required to update QDrant & Vantiq to use new volumes, and add the new `unstructured-api` statefulset. |
| [Vantiq R1.42 Upgrade Instructions to update QDrant to multi-node config with resilient collections](docs/R1dot42Upgrade.md) | Extra steps when upgrading Vantiq from R1.41 to R1.42, required to update QDrant to a multi-node config with replicated & sharded collections. |

Also note that the main documents such as [Installing Vantiq](docs/Installation.md) and the `bootstrap` files
have had the items from the above special upgrade docs merged into them. So, if you are doing a fresh install,
all the info you need should be in the main files and you should not need to reference the special upgrade docs.

&nbsp;

## Documentation Changes

Some documentation sections that used to be in this file and were referenced in Vantiq documentation, have
been moved elsewhere. This section will help you find their new location.

<a name="configuration-overrides"></a>
### Previous *Configuration Overrides* section

The *Configuration Overrides* section previously found in this document is now the
[*More Complex Configuration Overrides* section of the *Advanced Use Cases* doc](docs/AdvancedUseCases.md#complex_overrides).
Please see that section for the details on how to implement more complex configuration overrides.

The most common use of this info is for branding / white-labeling, which is covered in the 
[*Branding / White-Labeling* section of the *Advanced Use Cases* doc](docs/AdvancedUseCases.md#whitelabeling)
(the next section right after the complex configuration overrides section).
