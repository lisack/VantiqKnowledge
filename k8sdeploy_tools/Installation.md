# Installing Vantiq

## Overview

This document contains the details of how to deploy a Vantiq cloud installation to a Kubernetes (K8s) cluster using the
*k8sdeploy_tools* deployment utilities. Using the tasks defined in this document you can perform a complete deployment of
Vantiq and its core dependencies into any compliant K8s cluster. For information on how to perform initial setup and
configuration of these tools, please see the
[Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](k8sdeploy_toolsBootstrap.md) document.

If you have already followed these instructions then you will have a copy of this repository on your local disk. It is
a good practice to make sure to update your copy of the tools any time you are going to use them (to ensure that you 
have the most recent version). This can be accomplished with the command `git pull` executed in the root directory
of the repository (typically named `k8sdeploy_tools`).

If you are not already familiar with the information in the [background reference doc](BackgroundReference.md), it is
highly recommended that you review that doc first before reading this one. Doing so will help you understand this
doc more fully. It contains info such as:

  - Components of a Vantiq installation
  - How the `k8sdeploy_tools`, `k8sdeploy` (which populates `vantiqSystem`) and `k8sdeploy_clusters` (which populates `targetCluster`) repos are related
  - The basics of how `helm` works with the overrides in `deploy.yaml` and `k8sdeploy`
  - Best Practices for deploying Vantiq

You should also review the [Vantiq Kubernetes Cheat Sheet doc](VantiqK8sCheatSheet.md) which contains `kubectl`
commands that are useful for managing Vantiq installations.

Note on <span>&#x1F6A7;</span> sections or items: where you see something marked with the <span>&#x1F6A7;</span> symbol,
it means that section or item needs to be done by (or in cooperation with) your Infrastructure team.

&nbsp;

## Table of Contents

* [Gradle & Helm Tips](#gradle_helm_tips)
    * [Using Gradle's `clean` task to re-run deploy tasks regardless of whether they have changes](#rerun_all_tasks)
    * [Using Helm's `--dry-run` option to Check Command Results Before Executing](#using_dryrun)
    * [Using Gradle's Debug Options to Find the Cause of Errors](#using_debug)
* [Installation Summary / Checklist](#installation_summary)
* [Pre-Installation Tasks](#preinstallation)
    * [Configuring the Cluster Definition](#configure_cluster_defn)
        * [Choose a Method to Manage the Cluster Definition](#managing_cluster_defn)
    * [Document Target: Deploying To a New Cluster](#target_new_cluster)
    * [Connecting to the Cluster](#connecting-to-the-cluster)
        * [Note for Accessing AWS EKS Clusters](#aws_clusters)
        * [Note for Accessing OCI OKE Clusters](#oci_clusters)
    * [Updating an Existing Cluster Definition](#update_existing_cluster)
* [Deploying the Vantiq System](#deploying-the-vantiq-system)
    * [Deployment Prep](#deployment-prep)
        * [Deployment Prerequisites](#deployment-prereqs) <span>&#x1F6A7;</span>
        * [Describing the Configuration of the Cluster](#describing_the_configuration)
            * [Managing Non-Sensitive Configuration](#managing_nonsensitive)
            * [Managing Sensitive Configuration](#managing_sensitive)
* [Deployment Tasks](#deployment-tasks)
    * [Setting Cluster Properties](#setting-cluster-properties)
    * [One-time Setup of Cluster](#onetime_setup)
    * [Using `deploy.yaml` to Configure the Installation(s)](#deploydotyaml)
    * [`deploy` -- Perform a Full Deployment](#deploytask)
    * [`deployNginx` -- Deploy Nginx Ingress Controller](#deploynginx)
        * [Values Needed for `nginx` section of `deploy.yaml` when using Azure](#nginx_azure)
        * [Values Needed for `nginx` section of `deploy.yaml` when using OCI](#nginx_oci)
        * [Values Needed for `nginx` section of `deploy.yaml` when using AliCloud](#nginx_alicloud)
        * [Obtaining the Load Balancer FQDN or IP](#obtaining_host_ip)
        * [Troubleshooting Nginx/Loadbalancer Problems](#troubleshooting_nginx)
        * [Updating DNS to Create the FQDN for the Installation(s)](#updating_dns)
        * [Deploying Vantiq with an Preexisting Nginx Ingress Controller](#existing_nginx_controller)
        * [Installing cert-manager - First Chance](#cert-manager-firstchance)
    * [`deployShared` -- Deploy Shared Components](#deployshared)
        * [Run `createInfluxDBAdmin` to Create InfluxDB Credentials](#influxdb_creds)
    * [`deployVantiq` -- Deploy Vantiq Components](#deployvantiq)
        * [Using a Custom Image Repo](#custom_image_repo)
        * [Additional Configuration Overrides in `deploy/vantiq/config`](#addl_config_overrides)
        * [mongobackup](#mongobackup)
            * [AWS S3 backup credentials](#aws-s3-backup-credentials)
            * [Azure backup credentials](#azure-backup-credentials)
            * [AliCloud backup credentials](#alicloud-backup-credentials)
        * [mongorestore](#mongorestore)
        * [Vantiq Deployment Command](#vantiq-deployment-command)
            * [Capture the Admin Key Upon Running the Vantiq Deployment Command](#capture_admin_key)
    * [AI Components](#ai-components)
        * [Disabling Vantiq's AI features](#disabling_ai)
    * [Installing cert-manager to Obtain Free SSL certificates from Let's Encrypt](#cert-manager)
    * [Support for Isolated Organization Compute](#support_ioc)
        * [`orgCompute` Nodes are Not Just For Isolated Organization Compute](#orgcompute_nodes)
    * [Storage Classes](#storage_classes)
        * [Default vs. Custom Storage Classes](#default_storage_classes)
        * [CSI-based Storage Classes](#csi_storage_classes)
        * [Best Practice: Use CSI drivers on K8s 1.26 or later](#use_csi_drivers)
        * [Defining Custom Storage Classes in `deploy.yaml`](#custom_storage_classes)
* [Post-Installation Tasks](#post_install)
    * [Initial Post-Installation Tasks](#initial_pi_tasks)
        * [Working Around Keycloak Email Problems](#kc_email_workarounds)
            * [Keycloak Email Workaround #1: Fixing Keycloak Email Directly](#kc_email_workaround1)
            * [Keycloak Email Workaround #2: Manually "Verifying" A User's Email](#kc_email_workaround2)
    * [Add Keycloak Admins](#add-keycloak-admins)
    * [Grafana Dashboards for System Users](#grafana_system_dashboards)
        * [InfluxDB Credentials for Data Sources](#grafana_creds)
        * [Grafana System Dashboards and Data Sources](#grafana_system_dashanddatasrc)
    * [Post-Install Tasks for AI Features](#ai_postinstall)
        * [Add One or More `orgCompute` Nodes <span>&#x1F6A7;</span>](#ai_add_orgcompute)
        * [Add Secrets for `vantiq-worker` and AI Components](#ai_add_secrets)
            * [1. Create a new vantiq worker Access Token](#ai_add_secrets_s1)
            * [2. Create new AI and vantiq-worker secrets](#ai_add_secrets_s2)
            * [3. Run `deployVantiq` to Push the New Secrets](#ai_add_secrets_s3)
            * [4. Confirm proper operation of the AI Assistant](#ai_add_secrets_s4)
            * [5. Confirm K8s Network Policy is Working with Test curls from AI Assistant Pod](#ai_add_secrets_s5)
        * [Deploy the GenAI Flow Service Connector As Needed](#ai_genaiflow)
            * [1. Add `k8sResources` Quota to the Org](#ai_genaiflow_s1)
            * [2. Deploy GenAI Flow Connector for Each Org As Needed](#ai_genaiflow_s2)
            * [3. Confirm proper operation of any GenAI Flow Connectors](#ai_genaiflow_s3)

&nbsp;

<a name="gradle_helm_tips"></a>
## Gradle & Helm Tips

These tools use [Gradle](https://gradle.org/) to do the work of executing the various deploy tasks. There are a
few Gradle tips that can be useful when needed.

<a name="rerun_all_tasks"></a>
### Using Gradle's `clean` task to re-run deploy tasks regardless of whether they have changes

We use Gradle to keep track of what work needs to be done when executing the various deploy tasks. This means that 
if you make changes to your `deploy.yaml` file (or whatever file you used to hold your deployment values) the tool 
will figure out which components need to be updated and which haven't changed. Usually this is exactly the behavior 
you want, but there may be a time when you want to re-run all deployment tasks even though nothing has changed for
some of them. Should this happen you can use the `clean` task to reset the tools state and force a full re-deploy
the next time another task is run.

<a name="using_dryrun"></a>
### Using Helm's `--dryrun` option to Check Command Results Before Executing

Sometimes you wish to check what the results of a tools task such as `deployVantiq` would be, before actually
executing it. You can do this by adding the `-Pdry-run` option to the task, which will add the `--dry-run` flag
to the call to Helm which will output details of all task actions. The output of `-Pdry-run` can be verbose, so it
is recommended to direct the output into a file and then examine the file:

```
$ ./gradlew -Pcluster=mycoolcluster deployVantiq -Pdry-run > my-deployVantiq-dryrun.out 2>&1
$ less my-deployVantiq-dryrun.out
```

<a name="using_debug"></a>
### Using Gradle's Debug Options to Find the Cause of Errors

At times a tools task will result in an error rather than the welcome `BUILD SUCCESSFUL` result you are
expecting. Ideally the error itself will clearly point to the cause. However, sometimes the cause is not found
in the initial error. In such cases you may find the cause by using the `-Pdry-run` option described in the
previous section. If none of these provides an answer, there are two debug options which can provide more info.

The first is `--debug` which causes the log to output in debug mode and includes a normal stacktrace. This is
typically the debug option you will wish to use.

In rare cases you will also need to add the `--stacktrace` option, which will print out the stacktrace for
user exceptions (e.g. compile errors) in addition to the normal stacktrace.

As with `-Pdry-run`, the debug output can be verbose, so it is useful to direct the output into a file and then
examine the file. Here is an example of that, using the `--debug` option:

```
$ ./gradlew -Pcluster=mycoolcluster deployVantiq --debug > my-deployVantiq-debug.out
$ less my-deployVantiq-debug.out
```

&nbsp;

<a name="installation_summary"></a>
## Installation Summary / Checklist

The process to deploy a Vantiq installation involves many parts. The details of those tasks are either below
or are detailed in other documents that are linked to below. You may use this section as a ToDo checklist, but
only after going through the details in the sections below.

The summary of the process is:

  - Installation Prep Tasks
    - Provision all needed infrastructure <span>&#x1F6A7;</span>
    - Choose a method using Git to manage the cluster definition
    - Connect to the cluster for the first time
      - Set `provider` property in `cluster.properties` file
      - Obtain the cluster's kubeconfig and put it in `targetCluster/kubeconfig`
      - Run `clusterInfo` task
      - Grant full privileges to the `keycloak` database for the `keycloak` PostgreSQL user, if needed

  - Installation Tasks
    - Set remaining installation-wide properties in `cluster.properties` file
    - Run one-time `setupCluster` task
    - Run one-time `configureSealedSecrets` task, if using Sealed Secrets
    - Set non-sensitive installation properties in `deploy.yaml` file
    - Set sensitive installation properties (secrets) in `secrets.yaml` file
    - Run `generateSecrets` task to create secrets YAML files in `targetCluster/deploy/secrets`
    - Commit the secrets YAML files in `targetCluster/deploy/secrets` to the cluster config repo
    - Run `deployNginx` task to deploy nginx, which should also provision the cloud load balancer
    - Update DNS to create the FQDN for the installation(s) <span>&#x1F6A7;</span>
    - Run `deployShared` task to deploy shared components (Keycloak etc) and push shared secrets
    - Run `deployVantiq` task to deploy MongoDB and Vantiq and push MongoDB and Vantiq secrets
      - Monitor `vantiq-0` log as that pod starts, capture the admin key when it is output
      - (Optional) install and configure cert-manager if using it to obtain SSL certificates

  - Post Installation Tasks
    - Initial Tasks (these tasks must be repeated for each installation if you have more than one)
      - Register your account on the installation login page (includes verifying your email address)
      - Enter the admin key in the `Enter code:` field to make your account the first system admin user
      - Modify the `GenericEmailSender` source in the system namespace to point to the same SMTP server Keycloak uses
      - Modify the `self` node in the system namespace to set its URI property to point to the installation FQDN
      - Set up system admin org & users
        - Create the org for the admin users (for Vantiq-managed installations this is the `Vantiq` org)
        - Invite other system admin users to the admin org
          - Once they register their account, grant them system admin privs
          - Grant them Keycloak admin privs
      - Create the first non-admin org and invite some users to it
      - Add Grafana system dashboards in the system namespace



&nbsp;

<a name="preinstallation"></a>
## Pre-Installation Tasks

<a name="configure_cluster_defn"></a>
### Configuring the Cluster Definition

<a name="managing_cluster_defn"></a>
#### Choose a Method to Manage the Cluster Definition

Each cluster into which you will install the Vantiq System must have a definition managed as a branch in a Git
repository. This allows us to version the configuration, control changes to it, and track those changes over time.
Before creating this definition you must first decide how it will be managed. Vantiq cluster definitions can
be managed in one of 3 ways:

* [Centrally by Vantiq](VantiqManagedDefinition.md) -- this is the process used by Vantiq Ops for all Vantiq 
managed clouds.
* [Centrally by a Vantiq Customer](CustomerManagedDefinition.md) -- this allows a customer to manage the definition 
for a customer managed cloud in the same way that Vantiq does.
* [Locally on a deployment machine](LocallyManagedDefinition.md) -- this supports ad-hoc installation of Vantiq 
into a cluster. Ideally it should only be used for short term installations that will not be maintained over time. It
is important to know that clouds managed in this manner will never benefit from future automation work. They will
always require manual installation.

The links above provide the details about how to establish and manage the cluster definition. You should be
familiar with the option you will be using for a given cluster before proceeding to the remainder of this document.

<a name="target_new_cluster"></a>
### Document Target: Deploying To a New Cluster

These instructions are primarily targeted at creating and initializing a brand new cluster. If you are managing an
already existing cluster then skip to [Updating an Existing Cluster](#update_existing_cluster).

Start by following the instructions in one of the above links to create the initial cluster definition. This will
give you a *default* cluster definition which contains some templates for the various configuration files, as well
as some samples that illustrate some of the more common configuration options.

The default versions of these files are not ready to be used, you will first need to edit them to add all needed
parameters before using them for deployment. Another option for this, if you have an already-working cluster
definition for an existing installation, is to start with that definition as noted in
[optional step 2 of Cluster Definition Centrally Managed by Vantiq](VantiqManagedDefinition.md#new_cluster).

### Connecting to the Cluster

Your first step is to get the information needed to connect the deployment tools to the target K8s cluster. For
this you will need to obtain the `kubeconfig` file for the cluster. This is the file that is used by the Kubernetes
client tools (`kubectl` and `helm`) to connect to and authenticate with a specific cluster. The details of how to
get the `kubeconfig` and what it contains are cluster provider specific, so you'll need to consult the documentation
for your cluster to find out how to obtain the `kubeconfig`. Anyone who is an admin for your cluster should be
able to help you get a copy of the file, and likely already has it as an entry in their `~/.kube/config`.

Once you obtain the `kubeconfig` you need to copy it to the file `targetCluster/kubeconfig` (this will replace 
the placeholder file that comes with the default cluster definition). Note that if you are copying a
`~/.kube/config` file to `targetCluster/kubeconfig` then editing it down to only the elements (cluster/context/user)
for the specific cluster you are using, make sure to set `current-context` to the context in the
`targetCluster/kubeconfig`file so the `kubectl` and `helm` commands in the tools will work correctly.

Next, edit the file `targetCluster/cluster.properties` and find the property called `provider`.  By default it
should look something like this:

```
provider=aws|oci|azure|alicloud
```

This is a list of all of the providers that are currently supported (it will change over time) and you need to pick
one based on the provider of your target cluster. For example, if you are deploying to an AWS EKS cluster then you
should set this line to be:

```
provider=aws
```

(**Note:** If you are using AWS EKS, see the [note below](#aws_clusters) about the unique way
that `kubectl` must authenticate to AWS to access EKS clusters.)

Once you have selected the correct provider in `targetCluster/cluster.properties` you should execute the command

```
./gradlew -Pcluster=<yourClusterName> clusterInfo
```

If everything is configured properly then you should see something like this:

```text
Client Version: v1.22.1
Server Version: v1.22.16-eks-ffeb93d

BUILD SUCCESSFUL in 10s
2 actionable tasks: 2 executed
```
<a name="aws_clusters"></a>
#### Note for Accessing AWS EKS Clusters

Unlike some cloud providers who embed the cluster access credentials entirely in the `kubeconfig` file,
AWS uses auth performed by their CLI to dynamically obtain a token for `kubectl` access to EKS. This
means in order to authenticate to an AWS EKS cluster to use `kubectl`, you must have the AWS CLI
installed and have the proper IAM credentials (an access key consisting of an access key ID and an
access key secret) configured into your AWS CLI credentials file `~/.aws/credentials`, in a profile
which is properly configured to access the EKS cluster you are using.

One way to test this is with the AWS CLI command `aws eks describe-cluster`. For example, if you are using
a cluster named `foo` in the AWS account accessed with the `prodwest` profile, the command

```
aws --profile prodwest eks describe-cluster --name foo
```

should output a description of the `foo` cluster. If this command works, you know your AWS CLI is working
and able to access the AWS account where your EKS cluster resides.

You should next set up your ability for k8sdeploy_tools to access the cluster with `kubectl` by creating
a standlone `kubeconfig` file in your `targetCluster` directory for that. You would generate that file
with the correct contents for the above cluster by running the command

```
aws --profile prodwest eks update-kubeconfig --name foo --kubeconfig targetCluster/kubeconfig
```

in the k8sdeploy_tools dir.

You will also want to merge the contents of the `targetCluster/kubeconfig` into your main `~/.kube/config`
file so you can run your own `kubectl` commands outside of the tools. If this is your first time using
`kubectl` and you don't yet have a `~/.kube/config` file, you can simply copy `targetCluster/kubeconfig`
to `~/.kube/config`. However if you already have a `~/.kube/config` file, you will want to edit it to
incorporate the contents of the `targetCluster/kubeconfig` you just created.

When you are first setting up your AWS CLI profile and your EKS cluster, be aware that the AWS profile
can have the same name as the cluster you will be accessing although that is not required. What is
required is that the `AWS_PROFILE` property in the user section of the `kubeconfig` match the EKS
cluster you are using.

You can also specify the profile name via the `AWS_PROFILE` environment variable or the `AWS_PROFILE`
property in the `gradle.properties` file. However, it is best practice to specify the AWS profile in the
user section of the `kubeconfig` for EKS clusters.


See [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
and [Setting up the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
for details on how to install and set up your AWS CLI.

See [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
for details on managing AWS access keys.

<a name="oci_clusters"></a>
#### Note for Accessing OCI OKE Clusters

Like AWS, OCI uses auth performed by their CLI to dynamically obtain a token for `kubectl` access to EKS.
This means in order to authenticate to an OCI OKE cluster to use `kubectl`, you must have the OCI CLI
installed and have the proper CLI credentials (your user OCID, key file etc) configured into your OCI CLI
config file `~/.oci/config`, in a profile which is properly configured to access the OKE cluster you are
using.

One way to test this is with the OCI CLI command `oci ce cluster list`. For example, if you are using
a cluster in the OCI compartment accessed with the `prodwest` profile, the command

```
oci --profile prodwest ce cluster list
```

should output a description of OKE clusters in that compartment. If this command works, you know your OCI
CLI is working and able to access the compartment where your OKE cluster resides.

You should next set up your ability for k8sdeploy_tools to access the cluster with `kubectl` by creating
a standlone `kubeconfig` file in your `'targetCluster` directory for that. You would generate that file
with the correct contents for the above cluster by running the command

```
oci --profile prodwest ce cluster create-kubeconfig --cluster-id ocid1.cluster.xxx --file targetCluster/kubeconfig
```

in the k8sdeploy_tools dir. You will need to use the actual OCID of the cluster in place of `ocid1.cluster.xxx`
in the above `oci ce cluster create-kubeconfig` command, which is in the output of the `oci ce cluster list`
command above.

You will also want to merge the contents of the `targetCluster/kubeconfig` into your main `~/.kube/config`
file so you can run your own `kubectl` commands outside of the tools. If this is your first time using
`kubectl` and you don't yet have a `~/.kube/config` file, you can simply copy `targetCluster/kubeconfig`
to `~/.kube/config`. However if you already have a `~/.kube/config` file, you will want to edit it to
incorporate the contents of the `targetCluster/kubeconfig` you just created.

See [OCI CLI Install Quickstart](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
and [Configuring the OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm)
for details on how to install and set up your OCI CLI.

<a name="update_existing_cluster"></a>
### Updating an Existing Cluster Definition

If you are updating the definition of an existing cluster then there will already be a branch for the cluster
someplace. If it is centrally managed, then you can make the changes from anywhere and get them incorporated
into the cluster definition using the appropriate process (as outlined above). If the definition is locally
managed then you will need to have access to the machine/file system on which the definition is stored. At
that point the changes can be made directly in the cluster's branch as you did when performing initial setup.

While most of this document is targeted at creating and initializing a brand new cluster, much of the info
applies to managing an already existing cluster. For example, you will run the `deployVantiq` task many times
to update and upgrade your Vantiq installations.

The detailed process for doing updates and upgrades of your Vantiq installations is detailed in the
[Vantiq Installation Patch Procedure](VantiqInstallationPatchProcedure.md) and
[Vantiq Installation Upgrade Procedure](VantiqInstallationUpgradeProcedure.md) docs, but mainly you will just
update the `vantiq.image.tag` value(s) in your `deploy.yaml` file (and sometimes update the
`vantiq_system_release` value in your `cluster.properties` file) following the Git workflow you chose. You
will then run the `deployVantiq` task to push this updated config to your cluster. The deploy tasks sections
below provide much detail about the deploy tasks, so they are a useful reference for managing an already
existing cluster. 

&nbsp;

## Deploying the Vantiq System

### Deployment Prep

<a name="deployment-prereqs"></a>
#### Deployment Prerequisites <span>&#x1F6A7;</span>

In order to deploy the Vantiq system into a target K8s cluster there are a number of infrastructure prerequisites that
must be met before you can start on the install process:

* You must have access to the cluster and sufficient privileges to perform the deployment tasks.
* The cluster must have sufficient worker node capacity to support the target deployment configuration.  
See [Vantiq Deployment Configurations](VantiqDeploymentConfigurations.md) for details.
* You must know the name of the domain in which you are deploying.
* You must have a valid Vantiq license for that domain, used for the `vantiq-license` secret. <sup>Vantiq-provided</sup>
* You must have a valid username & password to access Vantiq's quay.io image repos, for the `registry-creds` secret. <sup>Vantiq-provided</sup>
* You must have the ability (directly or indirectly) to create new host entries in the DNS for the domain. Typically
this means the ability to create `CNAME` records in the domain's DNS service.  (NOTE -- it is possible to work around
this on a short term basis in order to verify the Vantiq installation, see 
[Dealing with missing DNS entries](AdvancedUseCases.md#dealing-with-missing-dns-entries))
* You must either have purchased an SSL certificate for that domain, or be prepared to
[install cert-manager in the cluster](https://cert-manager.io/docs/installation/kubectl/) to obtain your SSL certificates
from Let's Encrypt for free. Please note the following about these SSL certificates:
    * If purchasing commercial SSL certificates:
        * If you intend to deploy more than one Vantiq installation in a given domain, you will either need a single
multi-SAN certificate for all FQDNs or you will need a single certificate for each Vantiq installation.
        * You must have the private key associated with the certificate(s).
        * You must make sure to carefully set the certificate path(s) in `secrets.yaml` so that the correct cert is used
by each host.
    * If using cert-manager to obtain free SSL certs from Let's Encrypt you must:
        * [Install cert-manager in the cluster](https://cert-manager.io/docs/installation/kubectl/).
        * Configure a
[Let's Encrypt ClusterIssuer](https://cert-manager.io/docs/tutorials/acme/nginx-ingress/#step-6---configure-a-lets-encrypt-issuer)
and a [Certificate resource](https://cert-manager.io/docs/usage/certificate/) in each installation namespace so cert-manager
will obtain free SSL certs from Let's Encrypt and install them in the `vantiq-ssl-cert` secrets.
        * Note that the `cert-manager` option creates and maintains each `vantiq-ssl-cert` secret outside of our tools,
so you must comment out the `vantiq-ssl-cert` section(s) in your `secrets.yaml` file.
* There must be a PostgreSQL database available in which the database `keycloak` has been created (unless you have elected
to exclude Keycloak from the Vantiq system deployment). This database must be accessible from the cluster's worker
nodes. You will need to know:
    * The host name used to access the DB.
    * The port used if it is not the default of 5432.
    * The name of the admin user of the `keycloak` database if it is not also `keycloak`.
    * The password of the admin user.
    * The admin user must have full permissions to the `keycloak` database. If the infrastructure team did not already grant this,
these privileges, follow [the example instructions provided below](#grant_keycloak_privs).
* There must be an SMTP server that can be used for sending email. You will need to know:
    * The host name of the server.
    * The server port
    * The email address from which to send email.
    * The server's authentication options (STARTTLS, SSL, etc...)
    * The username to use when authenticating.
    * The password to use when authenticating.
* You must have the backup bucket credentials for the `dbbackup-creds` secret - see the [mongobackup section](#mongobackup) below for details.
* If you plan to use push notifications on iOS and Android, you must have an APNS certificate from Apple and a Firebase certificate from Google (for the `vantiq-push` secret).

Most of these items will need to be provided by your Infrastructure team. <span>&#x1F6A7;</span>

Any items noted with <sup>Vantiq-provided</sup> should be provided by [support@vantiq.com](mailto:support@vantiq.com).

<a name="describing_the_configuration"></a>
#### Describing the Configuration of the Cluster

Once you have all the prerequisites in place you can proceed with the deployment. A Vantiq installation consists of
three collections of components (known as sub-systems), each of which is deployed into its own K8s namespace. These 
are:

* nginx -- this subsystem contains the Nginx controller which is used to provide access to the public services of the 
Vantiq system.  This is deployed into the `shared` namespace.
* shared -- this subsystem contains the other shared resources that are part of the Vantiq system, such as Keycloak and 
the monitoring stack. These resources are also deployed into the `shared` namespace.
* vantiq -- this deploys the Vantiq specific resources. There will be one copy of these services for each distinct
Vantiq installation that is deployed in the cluster. They are deployed into a namespace that matches the hostname
of the installation (so the namespace for the `dev` installation is also called `dev`).

For example, consider Vantiq's US production cluster.  In this case there is one copy of the shared resources 
supporting the "internal", "dev", and "api" Vantiq installations and 3 copies of the Vantiq resources. The cluster has
5 namespaces -- default, shared, internal, dev, and api.

Before deploying each subsystem, you must first provide a description of how it should be configured. This is done
through files created/edited in the `targetCluster` directory under the main tools directory.  Since the final
configuration of a cluster represents all the knowledge of how to deploy the Vantiq system into the cluster it
should be managed in a controlled fashion. This is why we use a Git repository to manage the files contained in
`targetCluster`, as described in the [Managing Cluster Definition](#managing_cluster_defn) section above. The
configuration for a cluster is divided into 2 parts -- sensitive and non-sensitive.

<a name="managing_nonsensitive"></a>
##### Managing Non-Sensitive Configuration

The non-sensitive configuration can be stored as-is, in plain text. This is done using the `cluster.properties` and
`deploy.yaml` files which live at the root of the `targetCluster` directory. Prior to running the deployment tasks
you must update the `cluster.properties` file with the configuration values that apply to the whole cluster, and the
`deploy.yaml` file with the configuration values for each component being deployed.

In `deploy.yaml` each component has a top-level key and under that are the values for that component. When you create
a new cluster branch you will be given a template for the file along with several sample versions that illustrate
different scenarios.  You can use these as a starting point when creating your own configuration. The required values
for each component are discussed below along with their deployment.

It is useful to keep in mind that the contents of `deploy.yaml` are overrides which are merged together with overrides
and Helm charts from the `k8sdeploy` repo, and in some cases default external Helm charts. For details on how these
multiple elements are merged into the configuration of the statefulsets and deployments of a Vantiq installation,
please see the [Background Reference doc](BackgroundReference.md).

<a name="managing_sensitive"></a>
##### Managing Sensitive Configuration

The sensitive configuration contains information such as credentials which should be protected and which cannot be 
safely stored without some form of encryption. The use of
[Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets/) to encrypt the configuration of secrets is optional
but recommended. In either case, the sensitive configuration is managed independently from its non-sensitive
counterpart in `deploy.yaml`. The general process is as follows:

* Enter the sensitive configuration values in the `secrets.yaml` file.
* Run the `generateSecrets` task which consumes the information in `secrets.yaml` and creates the secrets YAML
config files in `targetCluster/deploy/secrets`. Later, the config in these files will be pushed to the cluster to
create the actual secrets as part of the `deployShared` and `deployVantiq` tasks described below.
* Commit the secrets YAML files in `targetCluster/deploy/secrets` to the cluster or issue branch in the
`targetCluster` directory (which is the cluster config repo). Note: having these files contain encrypted rather
than Base64-encoded data in the cluster config repo is the reason you should use sealed secrets.
* Delete the initial input files as they are no longer needed. This last step is not strictly necessary, but it is
a good practice since retaining the information is not necessary and only creates a potential risk.

Note that the YAML files that the `generateSecrets` task creates in `targetCluster/deploy/secrets` will contain:

* If you are **not** using sealed secrets, these files will be plain secrets definitions, containing Base64 encoded
values of the plaintext values in `secrets.yaml`. This is the same data you should see if you later run
`kubectl get secret XXXXX -o yaml` to output the contents of a secret in the cluster.
* If you are using sealed secrets, these files will be encrypted sealedsecrets definitions created by `kubeseal`
interacting with the sealed secrets controller running on the cluster. When the `deployShared` and `deployVantiq`
tasks push these config files to the cluster, they will create sealedsecrets which will cause the sealed secrets
controller to create a matching secret for each sealedsecret.

There are many details about the contents you need to provide in `secrets.yaml` and using
[Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets/). Please review those details in the
[Secrets Management doc](SecretsManagement.md) to gain a full understanding of secrets management in a Vantiq
installation.

&nbsp;

## Deployment Tasks

The following tasks are used to perform various aspects of deploying Vantiq. Each one is executed using the Gradle
wrapper script located in this directory (e.g. `./gradlew <taskName>`). Each task also requires a setting for the 
`cluster` property, identifying the target cluster in which the work is being done. This can be supplied on the 
command line using an argument of the form `-Pcluster=<clusterName>`. If you want to avoid this you can also set it 
in the `.gradle/gradle.properties` file; however, you should be careful about using this option if you plan to switch 
between multiple clusters.

Each main deploy task section below provides the info needed about a specific task, then the task command itself at
the end of the section. The first deployment task is to set the remaining cluster properties as described in the
first deploy task section, and run the one-time setup tasks.

### Setting Cluster Properties

The file `cluster.properties` holds property settings that are global for the entire cluster.  You have already used
it in the [Connecting to the Cluster](#connecting-to-the-cluster) step to set the provider for the cluster, now you
need to set the remaining properties as desired. The initial `cluster.properties` file that you are given has a number
of specialized properties, along with an explanation of their use, but unless you encounter one of those situations
they can be ignored. Instead, focus on the properties that will likely need to be updated for every cluster:

* `vantiq_system_release` -- this specifies the version of the Vantiq system definition that will be used to
perform the installation. This is one of the most important properties because it determines which configuration files
(Helm charts & overrides) are used, and the versions of shared cromponents. Vantiq system releases are specified using
[semantic versioning](https://semver.org/). You can learn more about Vantiq system releases from the
[*k8sdeploy* releases listing](https://github.com/Vantiq/k8sdeploy/releases) and the
[*k8sdeploy* release map reference](https://github.com/Vantiq/k8sdeploy/blob/master/ReleaseMap.md). If you are unsure
of which system release version to use, you should contact Vantiq support.
* `deployment` -- this specifies the deployment configuration to use.  The current choices are `development` and
`production`.  [Vantiq Deployment Configurations](VantiqDeploymentConfigurations.md) explains these options in detail.
* `vantiq.installation` -- the name of the Vantiq installation being deployed.  This name is used to construct both
the v-host of the Vantiq installation and the Kubernetes namespace in which it is deployed. As such it must consist
only of ASCII letters and numbers and the `-` character.  If you plan to deploy more than one Vantiq installation
into the cluster then you should specify their names in `deploy.yaml` and not use this property (it is common practice
to do so even with a single-installation cluster definition, to ease later multi-installation configuration).
* `excludeKeycloak` -- this property enables the Vantiq system to deploy **without** Keycloak / OAuth based authentication.
The system falls back to using the basic internal user name and password mechanism. Excluding Keycloak also removes
the need for a PostgreSQL database as a prerequisite for system deployment. The reasoning behind this is that some
private cloud deployments do not need or want OAuth or 3rd party authentication and requiring both Keycloak and a fault
tolerant (i.e. replicated) PostgreSQL unnecessarily complicates the process. However, best practice is the default of
including Keycloak to enable the many options for OAuth it offers.
* `enableVisionAnalytics` -- this property controls whether it is possible to deploy the Vantiq Vision Analytics
server as part of the Vantiq system.  The default value is `false` which means that the VA server will not be deployed.
A value of `true` means that it can be (though individual installations may choose not to) and also allows the
target cluster to be configured to support the VA server as necessary (the VA server requires at least one worker node
which supports GPU based computing).  You will need to re-run cluster setup any time this value is changed.
* `encryptVolumes` -- this property once controlled whether or not the volumes created during installation of Vantiq
would be encrypted. As of July 2023, unencrypted volumes are no longer supported by `k8sdeploy_tools` so this
property is no longer used and will result in warnings if set. The `configureCluster` task in `setup/setup.gradle` has
been changed to only deploy storage classes that create encrypted volumes. If you are a private cloud customer who
needs to use unencrypted volumes, you will need to create unencrypted storage classes manually and then specify use
of those storage classes as overrides in `deploy.yaml`.
* `enableSealedSecrets` -- this property controls whether the secrets generated for the Vantiq system will be
"sealed" (aka encrypted). It is recommended to use sealed secrets for any cluster whose definition will be stored
in an external Git repository (even if that repository is considered secure). The default value is `false`. Use of
sealed secrets requires [kubeseal](https://github.com/bitnami-labs/sealed-secrets/releases).
* `workloadPreference` -- this property controls the type of "node affinity" used when defining how to schedule
the Vantiq system pods in the K8s cluster. By default we use `soft` affinity which means that if the workload labels
are present on the nodes they will be used by the K8s scheduler, but if they are not the pods will still be scheduled.
A setting of `hard` indicates that the labels are mandatory and that pods should not be scheduled onto a node without
the correct workload label. Vantiq uses the node label `vantiq.com/workload-preference` to help assign pods to the
appropriate nodes. The possible values used for this workload label are:
    * `shared` -- indicates that the node should be used for any of the general purpose, shared applications such as
    Nginx, Keycloak, and Grafana. The applications can run on any general purpose node type.
    * `database` -- indicates that the node should be used for a database application such as MongoDB and InfluxDB.
    These applications require more memory and faster disk access.
    * `compute` -- indicates that the node should be used for compute intensive applications such as the Vantiq server.
    * `orgCompute` -- indicates that the node should be used for Isolated Org Compute pods, a special version of the
    Vantiq server that provides dedicated execution of rules and procedures for a specific org in a multi-tenant
    Vantiq installation.
    * `gpu` -- indicates the node should be used for workloads that require direct GPU access such as the Vantiq
    vision analytics server. 

<a name="onetime_setup"></a>
### One-time Setup of Cluster

Now that you can connect to the cluster and have set its global properties, you are ready to perform the one-time setup
tasks.  These tasks will initialize the cluster and perform any necessary configuration to make it ready to deploy the
Vantiq system. To do that run:

```
./gradlew -Pcluster=<yourClusterName> setupCluster
```

Once this task has been run on a given cluster there is no need to run it again, unless the configuration of
the cluster (as described in `cluster.properties`) changes.

If you have enabled sealed secrets in the cluster by setting `enableSealedSecrets=true`, the `setupCluster` task will
also deploy the sealed secrets controller. You should monitor the sealed secrets controller pod startup with
`kubectl get pod -n kube-system -w` and wait until the pod is in a `Running` state.  Once that is true, run the
command:

```
./gradlew -Pcluster=<yourClusterName> configureSealedSecrets
```

This will create some files in your `targetCluster` directory.  At this point you should also
[extract the cluster's private sealing key](https://github.com/bitnami-labs/sealed-secrets#how-can-i-do-a-backup-of-my-sealedsecrets)
and store it somewhere secure. The private sealing key is required if you ever need to reconstruct the cluster,
but exposure of the key puts your sealed secrets at risk so store it in a secure manner similar to your cloud
admin credentials.

<a name="deploydotyaml"></a>
### Using `deploy.yaml` to Configure the Installation(s)

The final configuration file in the cluster branch is the `deploy.yaml` file. This is an aggregate Helm values file 
which covers configuration of all the charts used to deploy the Vantiq system. The initial version of this file is
a template which has placeholders for the most commonly used configuration options. A newly created cluster branch
will also have several files in the `samples` directory which illustrate some of the more frequently encountered
variants.  More details about the various options and their meanings are given in the individual deployment tasks
sections below for `deployNginx`, `deployShared` and `deployVantiq`.

<a name="deploytask"></a>
### `deploy` -- Perform a Full Deployment

Once the initial cluster config is specified in `cluster.properties`, `deploy.yaml` and `secrets.yaml` and the
initial `setupCluster` and `generateSecrets` tasks are run, you are ready to move on to the actual deployment
tasks.

You can perform deployment of all of the components by running the `deploy` task. This will run the three main
deploy tasks (`deployNginx`, `deployShared` and `deployVantiq`) described in the next sections. However, it is
best practice
to run each of these main tasks separately, checking after each one that the resources that were deployed are functioning properly before moving on to the next main task.

If you do wish to run the the single `deploy` task, do that as follows:

```
./gradlew -Pcluster=<yourClusterName> deploy
```

<a name="deploynginx"></a>
### `deployNginx` -- Deploy Nginx Ingress Controller

The `deployNginx` task deploys the Nginx Ingress Controller which is used to allow access to the Vantiq services from
outside of the cluster (normally via a load balancer created by the cloud provider). The controller is deployed in
the cluster's `shared` namespace along with the shared components deployed by `deployShared` (the next main task). The
Nginx Ingress Controller provides routing for the Ingress resources created when deploying the other Vantiq components.

For some cloud providers such as AWS, there are typically no values that must be supplied for the `nginx:` section in
`deploy.yaml`. If you believe you may need to override some of the default values of the ingress-nginx chart in the
`nginx:` section in `deploy.yaml`, please see the
[full chart description](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx) for the
available options.

Both Azure and AliCloud do require you to supply values for the `nginx:` section in `deploy.yaml` to function
properly. Please see the [`nginx` values when using Azure](#nginx_azure) or
[`nginx` values when using AliCloud](#nginx_alicloud) section below for details if you are using one of those.

Once any needed values have been set in `deploy.yaml` you can run the task as follows:

```
./gradlew -Pcluster=<yourClusterName> deployNginx
```

Once the deployment has completed, the tool should output the address of the load balancer that was created for the
Nginx Ingress controller. Sometimes there is a delay in the creation of the load balancer by your cloud provider.
When that happens you can run the `showIngressHost` task directly, see 
[Obtaining the Load Balancer FQDN or IP](#obtaining_host_ip) for details.

<a name="nginx_azure"></a>
#### Values Needed for `nginx` section of `deploy.yaml` when using Azure

In Azure, when the AKS cluster is created it also creates the cloud load balancer for the cluster. The Vantiq
Terraform modules for Azure create a dedicated inbound public IP and attach it to the AKS load balancer, as
well as giving it a DNS label hostname (either specified in the top-level Terraform code, or the default in
the `azure_aks` module will be used). The domain `REGION.cloudapp.azure.com` will be added to the DNS label
hostname to create the Azure FQDN of the public IP.

You will need the public IP and DNS label for the the `nginx:` section in `deploy.yaml`. You will also need
the Azure FQDN as the destination of the installation `CNAME` when you create that in your DNS as described in
the [Updating DNS to Create the Installation FQDN](#updating_dns) section below.

For example, let's say your AKS cluster is in the `westus2` region, the public IP you created for inbound
connections was `20.30.40.50`, and you gave it a DNS label of `mydnslabel`. The `nginx:` section of your
`deploy.yaml` would need to be:

```yaml
nginx:
  controller:
    service:
      loadBalancerIP: "20.30.40.50"
      annotations:
        service.beta.kubernetes.io/azure-dns-label-name: "mydnslabel"
```

When you create the installation `CNAME` in your DNS, the destination of the `CNAME` would be
`mydnslabel.westus2.cloudapp.azure.com`.


<a name="nginx_oci"></a>
#### Values Needed for `nginx` section of `deploy.yaml` when using OCI

In OCI, the OCI network load balancer (NLB) that is created when the `deployNginx` task is run supports
proxy-protocol v2, which Vantiq uses and must be enabled for proper NLB operation. The annotation to enable
it in an automated way is `is-ppv2-enabled`, but it is very new so it has not yet been added to k8sdeploy
as a default. This means you will need to add it to the `nginx.controller.service` section of your
`deploy.yaml`. Eventually, we will add this annotation to k8sdeploy as a default, at which point you will
no longer need to add it to your `deploy.yaml`.

One annotation you will continue to need to add to the `nginx.controller.service` section of your
`deploy.yaml` is the `oci-network-security-groups` annotation, because the correct network security group
must be associated your NLB once it is created. It is best practice to do this via an annotation in
`deploy.yaml` rather than manually.

To have both of these required annotations on your NLB, the `nginx:` section of your `deploy.yaml` should
look like this:

```yaml
nginx:
  controller:
    service:
      annotations:
        oci-network-load-balancer.oraclecloud.com/oci-network-security-groups: "ocid1.networksecuritygroup.xxxx"
        oci-network-load-balancer.oraclecloud.com/is-ppv2-enabled: "true"
```

The actual OCID of the correct NSG will need to be entered where it shows `ocid1.networksecuritygroup.xxxx`
above. You will first need to determine the correct NSG, and get its OCID.

One way to find the NSG OCID, if you used Terraform to create your infrastructure, is by using the Terraform
commands `terraform state list` and `terraform state show`. You may need to consult your infrastructure team
for help on this. <span>&#x1F6A7;</span>

Another way is to use the OCI CLI. If you have provisioned your OCI networking and OKE cluster using the
[*Terraform OKE for Oracle Cloud Infrastructure* modules](https://github.com/oracle-terraform-modules/terraform-oci-oke),
the name of your public load balancer network security group should start with `pub_lb`. You should then be
able to find its OCID using the OCI CLI command

```
oci network nsg list | egrep 'ocid1.networksecuritygroup|vcn-id|pub_lb'
```

The output of this command should include one or more NSGs with the `display-name` starting with `pub_lb`.
If there is more than one of these, you will need to determine which of them is the one in the VCN where your
OKE cluster resides. The first `vcn-id` line after the `display-name` line of the correct NSG can help confirm
that you have the correct one. The `id` line immediately after the `display-name` line of the correct NSG is
the OCID of the NSG that you seek.

A third way to determine the correct OCID is to explore your network security groups in the OCI console, by
navigating to `Networking` <span>&#8594;</span> `Virtual Cloud Networks` <span>&#8594;</span> `(VCN name)`
<span>&#8594;</span> `Network Security Groups`.

Once your NLB has been created, you can confirm that the NSG has been associated with it by using the command

```
oci nlb network-load-balancer list | egrep '^            "ip-address"|display-name|ocid1.networksecuritygroup|ocid1.networkloadbalancer'
```

which should show the same OCID of the NSG that is in your `oci-network-security-groups` annotation.

<a name="nginx_alicloud"></a>
#### Values Needed for `nginx` section of `deploy.yaml` when using AliCloud

*Note: AliCloud support was deprecated in mid-2023. The contents of this section were accurate at that time,
but if you are trying to use AliCloud at a later date then you should verify these instructions still work.*

In AliCloud, the load balancer (SLB, in AliCloud terms) is created dynamically when the `deployNginx` task
is run, similar to AWS. The Vantiq Terraform modules for AliCloud do create a dedicated inbound public IP
for use on the SLB, but it must be manually attached to the SLB via the AliCloud console once the SLB is
created. This is because the SLB must be set to type VPC-internal (`intranet`) to communicate with the
cluster network. Attaching a public IP to the SLB allows it to be accessed from outside the VPC (from
the Internet).

For the the `nginx:` section in `deploy.yaml`, you will need the installation FQDN, and the master and
slave AZs in the region where your cluster and SLB are running. When you create the installation FQDN in
your in your DNS as described in the [Updating DNS to Create the Installation FQDN](#updating_dns) section
below, you will need to create an `A` record using the public IP you manually attached to the SLB.

For example, let's say your installation FQDN is `myhostname.mydomain.com`, your ACK cluster is in the
`ap-southeast-1` region, and you want to use `ap-southeast-1c` and `ap-southeast-1b` respectively as the
master and slave AZs for the SLB. The `nginx:` section of your `deploy.yaml` would need to be:

```yaml
nginx:
  controller:
    service:
      annotations:
        # Set the SLB instance address type to intranet, which is counter-intuitive but needed for EIP
        service.beta.kubernetes.io/alicloud-loadbalancer-address-type: intranet
        # Select a slightly larger LB size than the default of slb.s1.small
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-spec: "slb.s2.medium"
        # Set backend type to "eni" since we're using terway networking
        service.beta.kubernetes.io/backend-type: "eni"
        # Set master and slave AZs for the SLB
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-master-zoneid: "ap-southeast-1c"
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-slave-zoneid: "ap-southeast-1b"
        # Set FQDN for the SLB
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-hostname: "myhostname.mydomain.com"
        # Set idle timeout for the SLB
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-idle-timeout: "3600"
      # Set externalTrafficPolicy to Cluster to work around the IPVS problem
      externalTrafficPolicy: Cluster
      # Add this loadBalancerSourceRanges entry to eliminate a Helm error from the default chart
      loadBalancerSourceRanges:
        - 0.0.0.0/0
      # In AliCloud, need to specify targetPorts by number, grrrrr
      targetPorts:
        http: 80
        https: 443
```

Note you can also set the size of the load balancer VM to a different value if desired. Other annotations
and settings of the controller service shown above should be used as-is, unless you are sure they should
be changed.

As mentioned above, there is one manual step you will need to do in the AliCloud console once the SLB has
been created: manually attach the public IP to the SLB. Once you have done that, you should be able to to
create an `A` record in your DNS using the public IP you manually attached to the SLB and test to make sure
everything works.


<a name="obtaining_host_ip"></a>
#### Obtaining the Load Balancer FQDN or IP

At any time, if you need to see the FQDN (hostname.domainname) or IP (whichever is available) for the cloud
load balancer associated with the Nginx Ingress controller used by Vantiq, you can run the `showIngressHost`
task:

```
./gradlew -Pcluster=<clusterName> showIngressHost
```

This task is the final one run at the end of the `deployNginx` task, but if the load balancer service
has not yet synced with the actual cloud load balancer then the initial run of the `showIngressHost`
task may not yet show a result. Running the `showIngressHost` task again should show the FQDN or IP of
the external (cloud) load balancer in the service once the sync process has completed.

<a name="troubleshooting_nginx"></a>
#### Troubleshooting Nginx/Loadbalancer Problems

If the `showIngressHost` task continues to not show the FQDN or IP of the external (cloud) load balancer
in the service, you will need to diagnose the problem. The first step is to describe the service with

```
kubectl describe svc -n shared ingress-nginx-controller
```

and examine any events listed in the output. For example, most commercial cloud vendors use the
[Cloud Controller Manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/)
to sync (aka `ensure`) the service with the load balancer. If something went wrong with that process
you may see an event containing the message `failed to ensure load balancer`. Such event messages
should contain additional info which should point you toward a root cause.

If this does not yield results, the next step is to examine the ingress-nginx-controller pod logs to
see if they indicate a root cause.

You may need to enlist the help of your Infrastructure team for such diagnosis. <span>&#x1F6A7;</span>

<a name="updating_dns"></a>
#### Updating DNS to Create the FQDN for the Installation(s) <span>&#x1F6A7;</span>

Once you know the cloud provider FQDN (or IP, if no FQDN is available) of the load balancer, you must
create new host entries in the DNS service for the domain you are using for the Vantiq installation(s)
to provide them with a working FQDN. Typically this is done by creating a `CNAME` record in the domain's
DNS service, pointing to the cloud provider load balancer FQDN. The advantage of this approach vs. using
an `A` record with the load balancer's IP address, is that if the IP address changes the installation FQDNs
will pick up the new IP address as soon it changes in the load balancer FQDN. In some cases (such as
AliCloud) there is no cloud provider load balancer FQDN and you must use the load balancer IP to create
an `A` record in your DNS.

Once the you have run the `deployNginx` task successfully and created the installation FQDN entries in
your domain's DNS, you can test that everything is working so far by accessing the installation FQDN
with a web browser. At this point there is no Vantiq or Keycloak running so all you should get is the
default nginx 404 page.

Note: correct DNS is required in order for a Vantiq installation to properly function. However, it is
possible to work around missing DNS on a short term basis in order to verify the Vantiq installation,
see [Dealing with missing DNS entries](AdvancedUseCases.md#missing_dns_entries) for details.


<a name="cert-manager-firstchance"></a>
#### Installing cert-manager - First Chance <span>&#x1F6A7;</span>

You may wish to install [cert-manager](https://cert-manager.io/docs/) to obtain free SSL certificates
from [Let's Encrypt](https://letsencrypt.org/) rather than buying a commercial SSL certificate. Keep
in mind that k8sdeploy_tools will install a commercial SSL certificate into the `vantiq-ssl-cert`
secrets using the certificate chain and private key files as described in the
[Deployment Prerequisites](#deployment-prereqs) section above and the comments in the `secrets.yaml`
bootstrap file. However, cert-manager manages the `vantiq-ssl-cert` secrets *outside* of
k8sdeploy_tools. Either way works fine, you just need to be clear that cert-manager is not part of
k8sdeploy_tools.

Once you have updated DNS to create the FQDN for the installation(s) as described in the previous
section, you now have the first chance to install cert-manager and configure your certificate request(s)
in it, which should obtain your certificates and put them in your `vantiq-ssl-cert` secrets. To do this,
you will first need to create the installation namespace(s) manually (this would otherwise be done
automatically later by the `deployVantiq` task). You can then follow the
[Installing cert-manager to Obtain Free SSL certificates from Let's Encrypt](#cert-manager) section
below to install and configure cert-manager, your ClusterIssuer and your Certificate resource(s).

It is simpler to wait until after completing the `deployVantiq` step to install cert-manager, but if
you wish to install it at this point (to confirm your DNS, load balancer and nginx are all working,
for example) you can do that.

<a name="existing_nginx_controller"></a>
#### Deploying Vantiq with an Preexisting Nginx Ingress Controller

In some cases such as Rancher RKE2 clusters, you will want to use a preexisting Nginx ingress controller. In
this case you would skip this `deployNginx` step and just move on to deploying the rest of the Vantiq
system, after making some minor adjustments in your `deploy.yaml` as documented in
[Deploying Vantiq with an Preexisting Nginx Ingress Controller](AdvancedUseCases.md#existing_nginx_controller).

<a name="deployshared"></a>
### `deployShared` -- Deploy Shared Components

The `deployedShared` task deploys all the shared components of Vantiq. Currently those components are:

* Keycloak -- installed from the [Keycloak Helm chart](https://github.com/codecentric/helm-charts/tree/keycloakx-2.3.0/charts/keycloakx).
* GrafanaDB -- a MySQL database for storing Grafana information, installed from the 
[MySQL Helm chart](https://github.com/helm/charts/tree/master/stable/mysql)
* Grafana -- installed from the [Grafana Helm chart](https://github.com/helm/charts/tree/master/stable/grafana)
* InfluxDB -- installed from the [InfluxDB Helm chart](https://github.com/influxdata/tick-charts/tree/master/influxdb)
* Telegraf-DS -- installed from the [Telegraf-DS Helm chart](https://github.com/influxdata/tick-charts/tree/master/telegraf-ds)

All of these components use their standard Helm chart, with overrides defined in k8sdeploy. As noted
elsewhere, further overrides can be made in `deploy.yaml`. The keys for each of these components in
`deploy.yaml` are the lower case version of the component name.

The only values for Shared components that must be supplied in `deploy.yaml` are:

| Key | Description |
|-----|-------------|
| keycloak.database.hostname | The FQDN or IP of the Keycloak PostgreSQL server. |
| keycloak.database.port | The port of the Keycloak PostgreSQL server.  Only needs to be set if your server uses a non-default port. |

The other values that can be optionally set for the shared components (to override the defaults) are:

| Key | Description |
|-------|-------------|
| influxdb.persistence.storageClass | The storage class to use for the InfluxDB persistent volume. |
| influxdb.persistence.size | The size (typically expressed as Gi, e.g. `200Gi`) of the InfluxDB persistent volume. |
| grafanadb.persistence.storageClass | The storage class to use for the Grafana DB (MySQL) persistent volume. |
| grafanadb.persistence.size | The size (typically expressed as Gi, e.g. `10Gi`) of the Grafana DB persistent volume. |
| grafana.persistence.storageClassName | The storage class to use for the Grafana (config) persistent volume. Note this is `storageClassName` not `storageClass`.|
| grafana.persistence.size | The size (typically expressed as Gi, e.g. `5Gi`) of the Grafana persistent volume. |

Please see the [section on using custom storage classes](#custom_storage_classes) below for
details on setting these to use the new CSI-based storage classes (or any other custom storage
classes).

Once these have been set in the `deploy.yaml` values file you can run the task as follows:

```
./gradlew -Pcluster=<yourClusterName> deployShared
```

Note that as of June 2025, the `keycloak` statefulset has an init container that automatically
creates the `keycloak` database in PostgreSQL and adds the proper permissions grants to it so
Keycloak can store its data. This step was previously done manually.

<a name="influxdb_creds"></a>
#### Run `createInfluxDBAdmin` to Create InfluxDB Credentials

Starting with Vantiq System 3.10, the Vantiq chart defaults to secure InfluxDB. A secured
InfluxDB means that InfluxDB is set to require authentication. This implies that Data
Source definitions also require credentials to access InfluxDB.

Once your `deployShared` task has run properly so your InfluxDB pod is running, you should
run the following task to create the InfluxDB credentials:

```
./gradlew -Pcluster=<clusterName> createInfluxDBAdmin
```

This task - in addition to ensuring proper admin provisioning - creates the users and
passwords, as well as `READ` grants, on the InfluxDB databases used by the system
dashboards installed during the [Post-Installation Tasks](#post_install).

If InfluxDB is not secured, none of the Data Sources require a User or Password.

<a name="deployvantiq"></a>
### `deployVantiq` -- Deploy Vantiq Components

The `deployVantiq` task deploys all of the Vantiq server components for one or more specified Vantiq
installations. The first thing you need to do is determine the name of the installation(s) being
deployed. The Vantiq installation name is used in 2 ways. It is used to create the K8s namespace in
which the Vantiq components will be deployed. It also becomes the hostname portion of the Vantiq
installation FQDN.

Whether you are deploying a single Vantiq installation or multiple Vantiq installations into the
cluster, you should specify these using the `vantiq.installations` key in `deploy.yaml`. This key is
an array where each sub-key is the name of a Vantiq installation (and its sub-keys are overrides
applied just to that installation). For example, the vantiq section snippet of a sample `deploy.yaml`
describes two installations, `test` and `staging` with slightly different configurations:

```yaml
vantiq:
  installations:
    - test:
        image:
          tag: 1.40.15
        deployment: development
    - staging:
        image:
          tag: 1.39.7
```

Once the installation name is chosen you then need to fill out the deployment values under the "vantiq"
key in the `deploy.yaml` file. The values that can be set are:

| Key | Description |
|-------|-------------|
| vantiq.configuration.vantiq.defaults | Used to create the `vantiq.defaults` section of the `vantiq-config` configmap, to set the `VANTIQ_SERVER_OPTS` and `JAVA_OPTS` environment variables. |
| vantiq.image.repository | The container image repo from which to pull the Vantiq server images. *Only needed when using a custom image repo*. |
| vantiq.image.tag | The version of the Vantiq server to install. |
| vantiq.ingress.host.domain | The domain of the Vantiq installation.  Defaults to `vantiq.com` |
| vantiq.ingress.tls.cert | The SSL certificate file for the Vantiq installation. |
| vantiq.ingress.tls.key | The SSL key file for the Vantiq installation. |
| vantiq.keycloak.smtp.host | The SMTP server host. |
| vantiq.keycloak.smtp.port | The SMTP server port. |
| vantiq.keycloak.smtp.auth | SMTP authentication enabled (true/false). |
| vantiq.keycloak.smtp.starttls | SMTP auth uses STARTTLS (true/false). |
| vantiq.keycloak.smtp.ssl | SMTP auth uses SSL (true/false). |
| vantiq.keycloak.smtp.user | SMTP user to authenticate as when sending email. |
| vantiq.keycloak.smtp.from | The "from" email to use when sending password verification/reset email. |
| vantiq.keycloak.smtp.fromDisplayName | The "from" display name to use when sending password verification/reset email. |
| vantiq.mongodb.client.maxPoolSize | The maximum connection pool size Vantiq uses for MongoDB connections. |
| vantiq.mongodb.configmap.storage.wiredTiger.engineConfig.cacheSizeGB | The cache size in GB for the MongoDB WiredTiger storage engine. Typically set to (pod memory GB / 2) + 1.|
| vantiq.mongodb.configmap.storage.wiredTiger.engineConfig.directoryForIndexes | Set to `true` if you want the MongoDB WiredTiger storage engine to have a directory for indexes. |
| vantiq.mongodb.persistentVolume.storageClass | The storage class to use for MongoDB persistent volumes. |
| vantiq.mongodb.persistentVolume.size | The size (typically expressed as Gi, e.g. `500Gi`) of the MongoDB persistent volumes for data. |
| vantiq.mongodb.persistentVolume.indexsize | The size (typically expressed as Gi, e.g. `200Gi`) of the MongoDB persistent volumes for indexes. |
| vantiq.mongodb.persistentVolume.journalsize | The size (typically expressed as Gi, e.g. `30Gi`) of the MongoDB persistent volumes for journals. |
| vantiq.snapshotVolume.size | The size (typically expressed as Gi, e.g. 100Gi) of the volume created for the Vantiq server to store temporary snapshot files. Snapshot files are created to handle `dump` requests from the Vantiq CLI (e.g. `dump type` or `dump semanticindex`) |
| vantiq.snapshotVolume.storageClass | The storage class to use for the snapshot volume on `vantiq` pods. |

Note #1: these values can be set at the top `vantiq:` level, in which case they apply to all
installations. They can also be set at the `vantiq.installations` level for each installation, as shown
in the above example where there are different `vantiq.image.tag` values set for different installations.

Note #2: two of the values above refer to files (the SSL cert and key). The named files must be
placed in the directory listed in the path to files for the `vantiq.ingress.tls.cert` and
`vantiq.ingress.tls.key` entries, which is a relative path from the `targetCluster` directory. The
standard directory to use is the `targetCluster/deploy/sensitive` directory, since the key file is
sensitive data so it should not be checked into Git.

For example, the `vantiq.ingress` section snippet of a sample `deploy.yaml` using that standard directory
containing the cert file `mycert-chain.pem` and key file `mycert-key.pem` would look like this:

```yaml
vantiq:
  ingress:
    tls:
      cert: deploy/sensitive/mycert-chain.pem
      key: deploy/sensitive/mycert-key.pem
```

Note #3: if you implement the `userdb` statefulset as described in the
[*MongoDB* section of the *Background Reference* doc](BackgroundReference.md#mongodb), you will
have a second set of `vantiq.userdb` keys matching all the `vantiq.mongodb` keys above. To enable the
`userdb` statefulset, you must set the `vantiq.userdb.enabled` key to `true` in the `vantiq.userdb`
section of `deploy.yaml`:

```yaml
vantiq:
  userdb:
    enabled: true
```

Note #4 - single-installation special case: if you are deploying a single Vantiq installation into
the cluster then you can instead set its name by using the `vantiq.installations` property in the
`cluster.properties` file and avoid needing the `vantiq.installations` section in `deploy.yaml`.
However, keeping all installation-specific config in `deploy.yaml` is typically more clear for anyone
making changes to the config later, even for single-installation deploymemts.

<a name="custom_image_repo"></a>
#### Using a Custom Image Repo

If you are using a custom image repo for your Vantiq container images rather than the default
`quay.io/vantiq/vantiq-server` repo, you will need to include `vantiq.image.repository` in your
`vantiq.image` section, not just `vantiq.image.tag` which specifies the version. Normally, that section
of your `deploy.yaml` would look like this:

```yaml
vantiq:
  image:
    tag: 1.40.15
```

With only the tag in your `vantiq.image` section, the default `vantiq.image.repository` value of
`quay.io/vantiq/vantiq-server` defined in `k8sdeploy` will be used.

To specify a custom image repo you must add `vantiq.image.repository` containing the value of
your custom repo (hostname and repo path):

```yaml
vantiq:
  image:
    repository: myquay.somecompany.com/vantiq/vantiq-server
    tag: 1.40.15
```

This must also be done for the `vantiq.metricsCollector` section if you are using metrics collector.
In that case you must add a `vantiq.metricsCollector.image` section and specify the custom image
repo by changing

```yaml
vantiq:
  metricsCollector:
    enabled: true
```

to

```yaml
vantiq:
  metricsCollector:
    enabled: true
    image:
      repository: myquay.somecompany.com/vantiq/vantiq-server
```

The same is true for any `image:` section, but making such changes to anything other than Vantiq
image definitions is beyond the scope of this document.

**Note:** if you are using a custom image repo, you may also be using a custom repo for `k8sdeploy` rather than
the default one at `https://github.com/Vantiq/k8sdeploy`. If this is the case, you should have already
followed the instructions on how to do that by setting the `vantiqSystemRepo` and `helmChartRepo` Gradle
properties in `.gradle/gradle.properties` as described in the
[*Using a Custom `k8sdeploy` Repo* section of the *Centrally Managing Cluster Definitions by a Customer*](CustomerManagedDefinition.md#k8sdeployrepo)
doc. Please see that for further info.

<a name="addl_config_overrides"></a>
#### Additional Configuration Overrides in `deploy/vantiq/config`

The configuration associated with each component of the Vantiq deployment is normally overridden by
adding the desired configuration to the `deploy.yaml` file as described above. There is an additional
way to specify configuration overrides, by putting them in files the `deploy/vantiq/config` directory.
This approach can be necessary when you are adding very large files and/or binary files to the
configuration.

The most common reason for doing this is when you want to deploy a "white label" version of the Vantiq
web UI in a Vantiq Private Cloud installation, and you want to change certain labels and icons. See
[White Labeling Vantiq](https://dev.vantiq.com/docs/system/idebranding/index.html) for details on the
"white label" process.

Further details of applying configuration overrides via the `deploy/vantiq/config` directory can be
found in the
[More Complex Configuration Overrides section of the Advanced Use Cases](AdvancedUseCases.md#complex_overrides)
doc.

#### vectordb

Some of the new AI features use
[semantic indexes](https://www.sikich.com/insight/semantic-indexes-the-secret-sauce-for-supercharging-generative-ai-performance/)
which are provided by [QDrant](https://qdrant.tech/), known as `vectordb` in a Vantiq installation.

Configuration values that can be set for `vectordb` include:

| Key | Description |
|----|----------|
| vantiq.vectordb.enabled | \<true \| false\> |
| vantiq.vectordb.persistence.storageClassName | The storage class to use for the vectordb storage volume. |
| vantiq.vectordb.snapshotPersistence.storageClassName | The storage class to use for the vectordb snapshot volume. |

#### mongobackup

Backups of the mongodb database are handled via a Kubernetes `cronjob` in the vantiq chart. Like Unix
cron jobs they can be configured with a schedule. For details on K8s cronjob schedules see
[Writing a CronJob spec](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#writing-a-cronjob-spec),
and keep in mind the schedules are identical to Unix cron job schedules as described in the
[FreeBSD cronjob(5) man page](https://www.freebsd.org/cgi/man.cgi?crontab%285%29).

The `mongobackup` cronjob itself is designed to work with a cloud provider object store to hold the
resulting backup files. Currently, we support AWS S3, OCI Object Storage in S3 mode, Azure Blob Storage,
and Alicloud OSS. In order to take advantage of `mongobackup` you will need credentials to upload files
to the object store. If you do not have them, then you should set the `vantiq.mongodb.backup.enabled`
value to `false` and manage MongoDB backups with an alternative mechanism.

The configuration values for mongobackup include:

| Key | Description |
|----|----------|
| vantiq.mongodb.backup.enabled | \<true \| false\> |
| vantiq.mongodb.backup.provider | \< aws \| oci \| azure \| alicloud\> |
| vantiq.mongodb.backup.schedule | the [schedule](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#writing-a-cronjob-spec) on which to start the backups. e.g. `"@daily"` |
| vantiq.mongodb.backup.bucket | object store bucket for backup files |

Each time the `mongobackup` job runs, the backup files will be uploaded to the object store
provider in the specified bucket under a folder named the same as the vantiq installation. The
backup file itself has the installation name prepended followed by a sequence of numbers
representing the date and time the backup was taken. The following backup file:

```
my-mongodumps/dev/dev.202301060200.gz
```

was created for the `dev` installation on 06-Jan-2023 at 02:00.

In addition, the credentials used to connect to the object store must be provided via the
`dbbackup-creds` secret as part of the sensitive configuration. The exact format of these credentials
varies depending on the provider.

##### AWS S3 backup credentials

The format of this file is that of a standard AWS credentials file.  The one section that must be
present is `[sub]` since that is where the backup scripts look for the primary credentials. Other
sections can be provided if you are using a root account and roles. Here are some examples.

Simple `[sub]` profile:

```
[sub]
aws_access_key_id = <access key id>
aws_secret_access_key = <access key>
```

Access key pair in `[root]` profile and assumed role in `[sub]` profile:

```
[root]
aws_access_key_id = <access key id>
aws_secret_access_key = <access key>

[sub]
role_arn = <ARN for role>
source_profile = root
```

##### OCI S3 backup credentials

At this time, we are using S3 compatibility mode to store `mongobackup` dump files in OCI Object
Storage buckets. This requires using the `aws` backups privider, but with a few changes from the
standard AWS config.

In addition to the normal `vantiq.mongo.backup` section in `deploy.yaml` with `provider: "aws"`,
this `vantiq.backupImage` section must be added to use a newer `mongobackup` image that has a
current AWS CLI which supports alternate `endpoint_url` values required by non-AWS S3-compatible
object storage systems like OCI Object Storage.

```yaml
  backupImage:
    tag: 4.2.5-5
```

In addition, a manual modification must be made to the `mongobackup` CronJob by running the command

```
kubectl edit cronjob mongobackup -n INSTALLATIONAMESPACE
```

then changing the beginning of the `spec.jobTemplate.spec.template.spec` section from

```yaml
        spec:
          containers:
          - env:
            - name: AWS_PROFILE
              value: sub
            - name: AWS_CONFIG_FILE
              value: /root/aws/credentials
```

to

```yaml
        spec:
          containers:
          - env:
            - name: AWS_PROFILE
              value: sub
            - name: AWS_SHARED_CREDENTIALS_FILE
              value: /root/aws/credentials
            - name: AWS_CONFIG_FILE
              value: /root/aws/credentials
```

then save your changes. Keep in mind that any future change to the `mongobackup` CronJob
will overwrite this manual change when you run `deployVantiq`. Fortunately this CronJob
does not change often, and we are working on a k8sdeploy template update for the
`mongobackup` CronJob which will eliminate the need for this manual step.

Finally, the `dbbackup-creds` secret needs to be a profile containing AWS CLI credentials
and the `endpoint_url` you will use to access OCI Object Storage in S3 mode, not just a
credentials block like you would have in your `~/.aws/credentials` file. The secret should
look like this:

```
[profile sub]
aws_access_key_id = YOURACCESSKEYID
aws_secret_access_key = YOURACCESSKEYSECRET
region = us-phoenix-1
endpoint_url = https://axx8wohsma9j.compat.objectstorage.us-phoenix-1.oraclecloud.com
```

In this example, the OCI region is `us-phoenix-1` and the `endpoint_url` is the S3
compatible endpoint for that region. You will need to substitute the correct values
for your OCI region, and use your access keypair values.

Also remember, the profile name needs to be `sub` since that is where the backup scripts
look for the primary credentials.

##### Azure backup credentials

For Azure you will need the Azure Storage account name and account key, which are specific to
the storage account rather than being an account-wide access key pair like AWS. These values
can be found by examining the storage account in the Azure portal, or with the Azure CLI command

```
az storage account show-connection-string --resource-group <RESOURCE GROUP> --name <STORAGE ACCOUNT NAME>
```

Once you have these credentials, put them in the credentials file:

```
export AZURE_STORAGE_ACCOUNT=<account name>
export AZURE_STORAGE_KEY=<account key>
```

##### Alicloud backup credentials

*Note: AliCloud support was deprecated in mid-2023. The contents of this section were accurate at that time,
but if you are trying to use AliCloud at a later date then you should verify these instructions still work.*

The format of the file for Alicloud is the standard config.json credentials file. An example follows:
```json
{
	"current": "default",
	"profiles": [
		{
			"name": "default",
			"mode": "AK",
			"access_key_id": "<access key id>",
			"access_key_secret": "<access key secret>",
			"sts_token": "",
			"ram_role_name": "",
			"ram_role_arn": "",
			"ram_session_name": "",
			"private_key": "",
			"key_pair_name": "",
			"expired_seconds": 0,
			"verified": "",
			"region_id": "ap-southeast-1",
			"output_format": "json",
			"language": "en",
			"site": "",
			"retry_timeout": 0,
			"retry_count": 0
		}
	],
	"meta_path": ""
}
```

#### mongorestore

The `vantiq` chart also creates a `mongorestore` cronjob. This cronjob will never run
automatically because it has its `spec.suspend` value set to `true`. This cronjob is designed for
disaster recovery purposes, and completely replaces the existing MongoDB data with the data in the
backup file that is listed in the `xxx.LATEST-README.txt` file. We provide a tools script for
launching `mongorestore` jobs manually. For details please see the `README.md` in the `scripts`
directory.

**WARNING:** to repeat, `mongorestore` is designed for disaster recovery purposes, so it
completely wipes the existing MongoDB data and replaces it with the contents of the backup file.
**DO NOT** run `mongorestore` unless you wish to do this!

#### Vantiq Deployment Command
 
Once the proper values have been set the Vantiq components can be deployed using:

    ./gradlew -Pcluster=<yourClusterName> deployVantiq

**Note:** If you watch the pods as they start up with the `kubectl get pod -A -w`
command, you will see the `vantiq`, `metrics-collector` and `mongodb` pods starting once the `deployVantiq`
task has completed. You will
notice that the `vantiq-0` pod will be stuck at the `Init:0/3` status while the `mongodb` pods
start up. Once the `vantiq-0` pod can access MongoDB, you will see it continue to start up
until it reaches `Running` status. Likewise, the `metrics-collector-0` pod is not able to
start until the `vantiq-0` pod is running. This behavior is expected, the init containers confirm
the services needed by the pod exist before the main container is started. If however you see
errors in the `kubectl get pod -A -w` output, you should investigate the cause with the
`kubectl describe pod` command.

Once all the deployment steps are complete please see
[Post-Installation Tasks](#post_install) to configure the system and invite users.

<a name="capture_admin_key"></a>
##### Capture the Admin Key Upon Running the Vantiq Deployment Command

You should monitor the progress of the pods starting up in the installation namespace as soon as
you run the `deployVantiq` task, using the command

```
kubectl get pod -n <installation namespace> -w
```

As you monitor the pods starting, you should see the `mongodb` pods start and `vantiq-0` pod start,
but the `vantiq-0` pod startup will continue to fail with an init container error and try starting
again, until the `mongodb` pods are running. Once the `vantiq-0` pod is able to run all three init
containers and the main container starts, you must monitor the `vantiq-0` log as the main container
starts with

```
kubectl logs vantiq-0 -n <installation namespace> -f
```

and capture the admin key when it is output in the log. You will need this later during the
[Initial Post-Installation Tasks](#initial_pi_tasks).

<a name="cert-manager"></a>
### Installing cert-manager to Obtain Free SSL certificates from Let's Encrypt <span>&#x1F6A7;</span>

If you have chosen to install [cert-manager](https://cert-manager.io/docs/) to obtain free SSL
certificates from [Let's Encrypt](https://letsencrypt.org/) rather than buying a commercial SSL
certificate, follow the instructions in this section.

Keep in mind that k8sdeploy_tools will install a commercial SSL certificate into the `vantiq-ssl-cert`
secrets as described in the [Deployment Prerequisites](#deployment-prereqs) section above, whereas
using cert-manager manages the `vantiq-ssl-cert` secrets outside of k8sdeploy_tools. Either way works
fine, you just need to be clear that cert-manager is not part of k8sdeploy_tools.

At this point in the install process, you should have had a successful run of the `deployVantiq`
task and your Vantiq installation(s) should be running. However, if you are using cert-manager and
did not install it right after adding your FQDN(s) to DNS as described in the
[Installing cert-manager - First Chance](#cert-manager-firstchance) section above, you will see a
self-signed cert error when accessing your FQDN with a browser (nginx provides these if there is
not a real cert).

To install cert-manager and configure it you must do the following steps:

  1. [Install cert-manager in the cluster](https://cert-manager.io/docs/installation/kubectl/). The
 simplest way is using the [kubectl apply method](https://cert-manager.io/docs/installation/kubectl/).
  2. Configure a
[Let's Encrypt ClusterIssuer](https://cert-manager.io/docs/tutorials/acme/nginx-ingress/#step-6---configure-a-lets-encrypt-issuer)
by creating a `ClusterIssuer` YAML file and applying it with `kubectl apply`. See below for a suggested one.
  3. Configure a
[Certificate resource](https://cert-manager.io/docs/usage/certificate/) in each installation namespace
so cert-manager will obtain free SSL certs from Let's Encrypt and install them in the `vantiq-ssl-cert`
secrets. Do this by creating a `Certificate` YAML files and applying them with `kubectl apply`. See
below for a suggested example.

Both steps 1 and 3 should result in pods starting which you can observe by first running

```
kubectl get pod -A -w
```

Step 1 should result in the cert-manager pods themselves (`cert-manager`, `cainjector` & `webhook`)
being created. Step 3 should result in a `cm-acme-http-solver` pod being created, and once it is
running, if everything is configured and working properly it should complete and terminate in under
a minute. At that point your certificate should be installed in the `vantiq-ssl-cert` secret and
nginx should pick up that change dynamically, so when you next access your FQDN with a browser it
should show as being a properly secured HTTPS site.

Creation of the `ClusterIssuer` and then the `Certificate` resources should be done with
`kubectl apply -f` once you create your own YAML files for both of them, following the examples
below.

Here is an example `ClusterIssuer.yaml` for mydomain.com, which can issue certificates for the FQDNs
devus.mydomain.com and produs.mydomain.com:

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-mydomain
spec:
  acme:
    email: hostmaster@mydomain.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-account-key
    solvers:
    - http01:
        ingress:
          class: vantiq
      selector:
        dnsNames:
        - 'devus.mydomain.com'
        - 'produs.mydomain.com'
```

Here is an example `devus-mydomain-com.yaml` to create a certificate for the FQDN `devus.mydomain.com` using
the `letsencrypt-mydomain` ClusterIssuer shown above:

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: devus-cert
  namespace: devus
spec:
  secretName: vantiq-ssl-cert
  duration: 2160h
  renewBefore: 768h
  subject:
    organizations:
    - MyOrg Inc.
  isCA: false
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 4096
  usages:
    - server auth
    - client auth
  dnsNames:
  - devus.mydomain.com
  issuerRef:
    name: letsencrypt-mydomain
    kind: ClusterIssuer
```

You may need to enlist the help of your Infrastructure team for this task. <span>&#x1F6A7;</span>

### AI Components

Please note that starting with R1.37 additional AI components were added to Vantiq. You can run
without these components if you don't need them, but this document (and the bootstrap files such
as `bootstrap/deploy.yaml`) assume you will be running AI components.

Note that you will need `orgCompute` nodes to run AI component pods such as the AI Assistant
pod and GenAI Flow Connector pods. See the Isolated Organization Compute section below for
details on the `orgCompute` node pool you will need to run AI component pods. You will need
to scale up enough `orgCompute` nodes (beyond the ones used for Isolated Org Compute, if any)
to run the AI component pods you plan to use, and the number you need will vary based on the
number of AI pods you plan to run. You may only need one such node if you only plan to run
the AI Assistant pod and a few GenAI Flow Connector pods. Adding more GenAI Flow Connector
pods (there is one per Org) will require an additional node (or more) depending on the number
deployed. As of this writing (5 Feb 2025) the resource requests for each GenAI Flow Connector
pod is `500m` CPU (0.5 CPU) and `1Gi` memory.

If you choose not to run AI components, keep in mind the following differences compared to a
standard Vantiq installation that does run AI components:

* You will not have access to any of Vantiq's AI features, such as AI doc search, AI-assisted
development, or the GenAI Builder.
* You will not need to have any `orgCompute` nodes to run AI pods (see the next section for
details about `orgCompute` nodes)

Since Vantiq's AI features are a standard component, you may encounter additional problems
running with those features disabled. Vantiq does not recommend disabling AI features, and
the instructions below on how to do that in a private cloud are provided without certainty
that the system will work 100% correctly once you do so.

Also note that if you disable the `vantiq-worker` component you will not be able to deploy
any additional workloads to your Kubernetes cluster using Vantiq's Kubernetes deployment
features. This includes
[Storage Manager service connectors](https://dev.vantiq.com/docs/system/storagemanagers/)
and other service connectors or K8s workloads you wish to deploy in this way. Please see the
[External Lifecycle Management Guide](https://dev.vantiq.com/docs/system/extlifecycle/) for
details on Vantiq's Kubernetes deployment features.

<a name="disabling_ai"></a>
#### Disabling Vantiq's AI features

In order to disable Vantiq's AI features by not running AI components, disable the `vectordb`
and `vantiq-worker` components in the `vectordb` and `worker` subsections of the `vantiq`
section of your `deploy.yaml`, by setting both of them to `enabled: false`:

```
vantiq:
  vectordb:
    enabled: false
  worker:
    enabled: false
```

**Note:** if you have any Isolated Compute Orgs, then you can't disable the `vantiq-worker`
CronJob and you must skip this section.

<a name="support_ioc"></a>
### Support for Isolated Organization Compute <span>&#x1F6A7;</span>

Vantiq supports Isolated Organization Compute which deploys organization-specfic `vantiq` pods
that run the compute-specfic parts (rules and procedures) of the organization's apps, instead of
those rules and procedures running on the main `vantiq` pods with the other tenants.

The details on how to implement Isolated Organization Compute can be found in the
[Isolated Organization Compute section of the Advanced Use Cases](AdvancedUseCases.md#ioc) doc.

In order to run Isolated Organization Compute pods, you will need to have an `orgCompute` node
pool with enough nodes scaled up to run the Isolated Organization Compute pods you have.

In a private cloud, you can either have all application namespaces in a single org, or you may
choose to isolate one application (or group of applications) from others by implementing multiple
orgs to allow the multi-tenant features built into the Vantiq server to provide the isolation
you desire. You can take this isolation a step further by implementing Isolated Organization
Compute to run an org's rules and procedures on dedicated nodes. Using either, both or none of
these options is up to you and your application's needs.

<a name="orgcompute_nodes"></a>
#### `orgCompute` Nodes are Not Just For Isolated Organization Compute

Note that `orgCompute` nodes are not only used to run Isolated Organization Compute pods. They
are also used to run external connector pods such as the GenAI Flow Connector pods. Even if you
are not using Isolated Organization Compute, you will need to have an `orgCompute` node pool
with enough nodes scaled up to run the pods you have which need such nodes.

<a name="storage_classes"></a>
### Storage Classes

<a name="default_storage_classes"></a>
#### Default vs. Custom Storage Classes

Each component in a Vantiq installation that uses storage (MongoDB, Grafana & InfluxDB) has default
storage classes defined for their PVCs/PVs in [k8sdeploy](https://github.com/Vantiq/k8sdeploy).

These defaults have not changed since the inception of `k8sdeploy` and `k8sdeploy_tools`. If you
do not change the storage classes for any of these in `deploy.yaml` then the default storage classes
in `k8sdeploy` (`vantiq-sc` and `vantiq-xfs`) will be used.

If you have other storage classes you wish to use for any or all of these (such as the new `vantiq-sc2`
and `vantiq-xfs2` storage classes), you can set them as overrides in `deploy.yaml` as described in the
[custom storage classes section](#custom_storage_classes) below.

**Note:** as noted below, you must first migrate your PVs/PVCs to the new storage classes (an
infrastructure task that does not involve k8sdeploy_tools), then update your deploy.yaml to match the
new PVCs.

<a name="csi_storage_classes"></a>
#### CSI-based Storage Classes

A new pair of CSI-based storage classes were added to `k8sdeploy_tools` in mid-2023, the
`vantiq-sc2` and `vantiq-xfs2` storage classes. These are the same as the original `vantiq-sc`
and `vantiq-xfs` storage classes except they use the CSI driver instead of the in-tree driver.
These storage classes are defined for AWS & Azure in `k8sdeploy_tools/setup`, and the appropriate
ones for your cloud provider will be installed in your cluster by running the `setupCluster` task.

To maintain backwards compatibility, the default storage classes in `k8sdeploy` have not changed. For
each installation, when you are ready to switch to the new CSI-based volumes you can do that by first
migrating your PVs/PVCs to the new storage classes as described in the
[*Best Practice: Use CSI drivers on K8s 1.26 or later* section](#use_csi_drivers) below, which is
strictly an infrastructure task and does not involve k8sdeploy_tools.

Once the PVs/PVCs are migrated, you must set the storage parameters to match in `deploy.yaml` as
described in the
[*Defining Custom Storage Classes in deploy.yaml* section](#defining-custom-storage-classes-in-deployyaml)
below.

<a name="use_csi_drivers"></a>
##### Best Practice: Use CSI drivers on K8s 1.26 or later

On Azure AKS, it is not a requirement to use CSI drivers as of this writing in Dec 2023, but
starting with AKS 1.26 Azure no longer supports the in-tree storage drivers (only the CSI drivers).
PVs/PVCs using storage classes which use the in-tree storage drivers will continue to work, but will
no longer be supported by Azure Support so it is sensible to convert your PVs/PVCs to the new
CSI-based storage classes when you upgrade to AKS 1.26 to remain supported. Please see the
[Migrate from in-tree storage class to CSI drivers on AKS](https://learn.microsoft.com/en-us/azure/aks/csi-migrate-in-tree-volumes)
Azure doc for details of the migration process on Azure.

On AWS EKS starting with EKS 1.23, AWS converted to using the CSI drivers for all storage: even
storage classes that use the in-tree AWS drivers actually use the CSI drivers under the covers in
EKS 1.23 and later. In this way, the in-tree AWS drivers continue to be supported by AWS, however it
is still best practice to convert your PVs/PVCs to CSI-based storage classes. There is another reason
you may want to migrate your PVs/PVCs to new storage classes on AWS: at the same time you can switch
the underlying volumes from gp2-based to gp3-based (gp3 is
[both faster and lower-cost](https://aws.amazon.com/blogs/storage/migrate-your-amazon-ebs-volumes-from-gp2-to-gp3-and-save-up-to-20-on-costs/)).
See [Migrating Amazon EKS clusters from gp2 to gp3 EBS volumes](https://aws.amazon.com/blogs/containers/migrating-amazon-eks-clusters-from-gp2-to-gp3-ebs-volumes/)
for details of the migration process on AWS.

Both of these use the same basic process to migrate each volume: create a (cloud-layer) disk
snapshot, then create a K8s VolumeSnapshotContent from the snapshot, then a K8s VolumeSnapshot
referencing the VolumeSnapshotContent, then a PVC referencing the VolumeSnapshot. When the
PVC is mounted upon pod startup, a PV will be dynamically created from the VolumeSnapshot.

As noted above, the volumes/PVs/PVCs migration is strictly an infrastructure task and does not
involve k8sdeploy_tools.

For information on converting the storage elements of your Vantiq config to new storage classes
to match the new storage classes, please see the next section.

<a name="custom_storage_classes"></a>
#### Defining Custom Storage Classes in `deploy.yaml`

To use custom storage classes for the components in a Vantiq installation, you must specify those
non-default storage classes in `deploy.yaml` as overrides, as noted in the
[`deployShared`](#deployshared) and [`deployVantiq`](#deployvantiq) sections above.

Here is an example of the parts of `deploy.yaml` using the new CSI-based storage classes for all
components including MongoDB in the `foo` installation:

```
influxdb:
  persistence:
    storageClass: vantiq-sc2

grafanadb:
  persistence:
    storageClass: vantiq-sc2

grafana:
  persistence:
    storageClassName: vantiq-sc2

vantiq:
  installations:
    - foo:
        snapshotVolume:
          storageClass: vantiq-sc2
        mongodb:
          persistentVolume:
            storageClass: vantiq-xfs2
```

Note that most of these use `storageClass` to define the storage class but for some reason `grafana`
uses `storageClassName`. Make sure you use right parameter name for each component.

We expect at a later date to change the default storage classes defined in `k8sdeploy` from
the original `vantiq-sc` and `vantiq-xfs` storage classes to the new `vantiq-sc2` and `vantiq-xfs2`
CSI-based storage classes, once all known installations have migrated to the new storage classes.
Until then, the new storage classes will need to be defined as custom storage classes as
described here.

&nbsp;

<a name="post_install"></a>
## Post-Installation Tasks

<a name="initial_pi_tasks"></a>
### Initial Post-Installation Tasks

Once you have successfully installed the Vantiq cluster (the above steps have successfully
completed and Kubernetes reports that all pods are running) there are a number of configuration
steps required to make the Vantiq installation ready for use. This section outlines what you
must do.
1. Go to the URI for the Vantiq system which will redirect you to Keycloak.<sup>1</sup>
1. Create a user in Keycloak (the first one) by clicking on `Register user` and perform the required
email verification.
1. On the resulting `Enter code` screen in Vantiq enter the one-time system admin code that
you captured from the `vantiq-0` log during the initial pod startup.
1. Modify the `GenericEmailSender` source in the system namespace to point to the same SMTP server
used by Keycloak (you’ll need the same username and password as well).
1. Modify the `self` node in the system namespace to set its URI property to point to the root
address of the server.
1. Invite other users to be a system admin (if there will be any).
1. Create an organization and invite someone from the customer to be the admin of that. As a
Vantiq system admin, some of the first steps that you typically do are to create a Vantiq
organization and invite users into that organization as either another `Organization Admin` or as
a `User (Developer)`. The new `User (Developer)` users will be able to create namespaces in which
they can work on projects. Project development should __NEVER__ occur in the system namespace.

Note 1: If your installation excluded Keycloak, then obviously you will not be redirected there.
Instead you need to enter the system user and default password at the Vantiq login page. You should
change the default password to something secure. You can also skip the next post install step of
adding Keycloak admins.

<a name="kc_email_workarounds"></a>
#### Working Around Keycloak Email Problems

To perform the required email verification in step 2 above, email from Keycloak must be working
properly. If email from Keycloak is not working properly so you don't receive the verification
email, there are two ways to work around the problem.

<a name="kc_email_workaround1"></a>
##### Keycloak Email Workaround #1: Fixing Keycloak Email Directly

The first and preferred option is to log into Keycloak directly as the Keycloak admin user and
fix the email config. Do this by accessing the `/auth` path for your installation as described
below in the [Add Keycloak Admins](#add-keycloak-admins) section.

Then, check and test the Keycloak email config as described in the
[*Configuring email for a realm* section of the Server Administration Guide](https://www.keycloak.org/docs/24.0.5/server_admin/#_email) until
you find and fix the problem with your Keycloak email config.

If you can't fix Keycloak email directly at this point but you just need to have your initial
Vantiq user's email verified for now, move on to option #2 in the next section. You will still
need to come back later to fix Keycloak email, but this will allow you to move ahead with the
rest of the post-install setup.

<a name="kc_email_workaround2"></a>
##### Keycloak Email Workaround #2: Manually "Verifying" A User's Email

As noted in the previous section, the first and preferred option when having Keycloak email
problems in a new installation is to log into Keycloak directly as the Keycloak admin user and
fix the email config. Sometimes though you can't fix Keycloak email at first, and you just need
to have your initial Vantiq user's email verified so you can move ahead with the rest of the
post-install setup. In such cases, follow these steps:

1. Log into the realm as the admin user as described below in the
[Add Keycloak Admins](#add-keycloak-admins) section.
1. Click `Manage` <span>&#8594;</span> `Users`.
1. Click on the user you want to "verify" (in a new installation this should be the only user).
1. Click on the `Details` tab (if it is not already selected).
1. Remove `Verify Email` from the `Required user actions` field.
1. Slide the `Email verified` switch to `Yes`.
1. Save these changes by clicking the `Save` button.

If you have done the steps in this section as a temporary workaround, don't forget that you will
still need to come back later to fix Keycloak email.

### Add Keycloak Admins

In addition, for any system admin that you want to also be an admin of the Keycloak realm you will
need to login as an existing Keycloak admin and do the following steps. The first time this must
be done as the global Keycloak admin user (normally `keycloak` unless you have overridden it),
after that any existing realm admin can do it:

1. To reach the keycloak admin UI you can specify the base Vantiq URI then add the path `/auth`,
e.g. `https://myhostname.mydomain.com/auth`, then log in as the admin user (which should have
the default username `keycloak` unless you changed it).<sup>1</sup>
1. Click `Manage` <span>&#8594;</span> `Users`.
1. Find the user you want to be the admin (if you do this immediately there will just be the one
user created in step 2 above). You may need to click the `View all users` button to see the list
of registered users.
1. Click on the `Role Mappings` tab.
1. From the `Client Roles` dropdown select the `realm management` roles. This will open up 3
lists.  Select all entries in the first list and click `Add Selected`. There is no `Save` button
for this function, once the roles show up under `Assigned Roles` you are done.

As a result the user will be able to log into Keycloak as the admin of that realm directly from
Vantiq web UI, by selecting `Keycloak` from the `Administer` menu. This menu item is only
available when logged into the `system` namespace.

Keep in mind that Keycloak has many options, most of which are not implemented in a standard
Vantiq installation. For a Vantiq private cloud installation, the customer may wish to implement
some of these options, such as OAuth or SAML identity providers. All such Keycloak server config
details are documented in the
[Keycloak Server Admin Guide](https://www.keycloak.org/docs/24.0.5/server_admin/) for any
customer wishing to use them.

Note 1: if you have trouble logging in directly to your installation realm using the above URI,
you can try the alternate method of logging in to the master realm via the URI
`https://myhostname.mydomain.com/auth/admin`. Once you do this initial step, you will then need
to switch to your installation realm via the realm dropdown on the left sidebar, before
proceeding with steps 2-5.

<a name="grafana_system_dashboards"></a>
### Grafana Dashboards for System Users

The per-namespace and per-org Grafana dashboards are created at runtime by the Vantiq server,
each time a new namespace or org is created. The `system` dashboards are instead created once at
Grafana install time by the `grafanaPostInstallSetup` task which is invoked by the `deployGrafana`
task.

Also note that in a cluster with multiple Vantiq installations, the `system`  dashboards are
shared by all Vantiq installations in that cluster.

<a name="grafana_creds"></a>
#### InfluxDB Credentials for Data Sources

Starting with Vantiq System 3.10, the Vantiq chart defaults to secure InfluxDB. A secured
InfluxDB means that InfluxDB is set to require authentication. This implies that Data
Source definitions also require credentials to access InfluxDB. For new installations, you
should have already created these InfluxDB credentials by
[running the `createInfluxDBAdmin` task](#influxdb_creds) just after you ran the
`deployShared` task.

To create these credentials on an existing installation that was created pre-3.10 without
them, you should run the `createInfluxDBAdmin` task when you upgrade to k8sdeploy 3.10.

This task - in addition to ensuring proper admin provisioning - creates the user `vantiq_sysuser`
with `READ` grants on the InfluxDB databases `system`, `vantiq_server`, `kubernetes` and
`_internal`. The `system` data sources use the `vantiq_sysuser` user for access to the data
they query from InfluxDB.

<a name="grafana_system_dashanddatasrc"></a>
#### Grafana System Dashboards and Data Sources
 
As noted above, there is a special set of dashboards and data sources for the `system`
namespace, these are now added automatically by the `grafanaPostInstallSetup` task which is
invoked by the `deployGrafana` task.

Vantiq Admins who did installs prior to June 2025 will recall the creation of the `system`
dashboards and data sources used to be a manual process.

For reference, the data sources added to Grafana by the the `grafanaPostInstallSetup` task are:

| Name | URL | Database | Min Time Interval |
|------|-----|----------|-------------------|
| systemDB | http://influxdb:8086 | system | 30s |
| vantiqServer| http://influxdb:8086 | vantiq_server | 30s |
| kubernetes | http://influxdb:8086 | kubernetes | 30s |
| internals | http://influxdb:8086 | \_internal | 10s |

For reference, the `system` dashboards added to Grafana by the the `grafanaPostInstallSetup`
task are:

  - InfluxDB Internals
  - Metric Collection Resources
  - MongoDB Monitoring Dashboard
  - UserDB Monitoring Dashboard
  - Organization Activity
  - Organization Activity with Top Namespaces
  - Vantiq Resources
  - Vantiq ISO Resources

Once your Vantiq installation is running, you should see the above dashboards in the `system`
namespace. These dashboards should have existing data which displays, if your installation is
functioning properly.


<a name="ai_postinstall"></a>
### Post-Install Tasks for AI Features

Assuming you are using Vantiq's AI features, there are several post-install steps you must
do to enable them.


<a name="ai_add_orgcompute"></a>
#### Add One or More `orgCompute` Nodes <span>&#x1F6A7;</span>

A node with the `vantiq.com/workload-preference=orgCompute` label is needed for the AI Assistant pod
and any GenAI Flow connectors. If you do not yet have an `orgCompute` node pool, you will need to
create one and scale it to at least 1 node. If you already have an `orgCompute` node pool, make sure
one of the nodes has enough available CPU and memory for the AI pods you will be running.

Until you have an `orgCompute` node available to schedule AI pods, you will see those pods stuck in
`Pending` status.

<a name="ai_add_secrets"></a>
#### Add Secrets for `vantiq-worker` and AI Components

Assuming you have enabled the `vantiq-worker` feature which allows Vantiq to deploy Kubernetes
workloads (typically, specialized connectors), you will need to create a `vantiq-worker` secret so
the `vantiq-worker` CronJob can function properly. This cannot be done until post-install, because
it requires you to create a long-lived Vantiq token and put it into the `vantiq-worker` secret.
Until you complete these steps, you will notice your `vantiq-worker` pods are not working properly.

Likewise, to deploy AI components such as the AI Assistant pod and any GenAI flow connectors, you
must first have the `vantiq-worker` CronJob working correctly. Once it is, you should notice the
AI Assistant pod starting and reaching a `Running` state.

You must also create a `vantiq-ai-assistant-env` secret for use by the core AI features in Vantiq,
which contains the environment variables needed to connect to the external LLMs used by the core
AI features. Even once the AI Assistant pod is running, it will not function properly without
a correct `vantiq-ai-assistant-env` secret.

To create these secrets, follow these steps:

<a name="ai_add_secrets_s1"></a>
##### 1. Create a new vantiq worker Access Token

Create a new vantiq worker Access Token in the `system` namespace for use in the `vantiq-worker` secret
created in the next step. This access token should be named something clear like `k8sWorker` and should
use the `system.federatedK8sWorker` profile. Note the value of this access token when you create it,
since you will need it for the next step.

<a name="ai_add_secrets_s2"></a>
##### 2. Create new AI and vantiq-worker secrets

In your `targetCluster` cluster branch, create new `vantiq-ai-assistant-env` and `vantiq-worker` secrets
either in the installation section (or the common section as shown) of your secrets.yaml.

This step requires several parts. First, your `targetCluster/secrets.yaml` file should contain the
following contents:

```
vantiq:
  common:
    vantiq-ai-assistant-env:
      files:
        .env: deploy/sensitive/vantiq-ai-assistant-env.txt
    vantiq-worker:
      data:
        token: TOKENVALUEFROMSTEP1
```

Note that your vantiq-worker token value should be the access token from step 1.

Next, your `targetCluster/deploy/sensitive/vantiq-ai-assistant-env.txt` file should contain the
contents

```
OPENAI_API_KEY=XXXXXX
```

with the private cloud owner's actual OpenAI API key in place of the `XXXXXX`.

Finally, run `generateSecrets` to generate the YAML files for these secrets. After doing so you should
confirm that the two new matching YAML files have been created in `targetCluster/deploy/secrets/vantiq`
as expected. You should then commit these YAML files to your `targetCluster` cluster branch.

<a name="ai_add_secrets_s3"></a>
##### 3. Run `deployVantiq` to Push the New Secrets

Run `deployVantiq` to push these new secrets to your cluster. You should notice the new vantiq-worker
and AI Assistant pods starting and reaching a `Running` state once these secrets exist. If these pods
do not reach a `Running` state, you will need to investigate why.

<a name="ai_add_secrets_s4"></a>
##### 4. Confirm proper operation of the AI Assistant

A simple way to test the AI Assistant is to use the `AI Documentation Search` feature under the `Help`
menu. Type in some questions about Vantiq and it should give you answers from the docs, if the AI
Assistant is functioning properly.

You can also try some simple applications using the `submitPrompt` and `answerQuestion` activity
patterns, if you have such applications. See the
[*Custom Operations* section of the *Resource Reference Guide*](https://dev.vantiq.com/docs/system/resourceguide/#custom-operations_4)
for info on `submitPrompt`, and the [LLM Reference Guide](https://dev.vantiq.com/docs/system/llms/)
for info on a wider range of LLMs, to create such applications.

If at this point you also want to test the connections to the Qdrant vector database which stores
semantic indexes, a simple way to do this is to import the
[GenAI Builder Tutorial](https://dev.vantiq.com/docs/system/tutorials/genaibuilder/), set the
`OPENAI_KEY` secret to a valid value, and set up a semantic index as described in the
[*Custom Formatting and Return Types - Custom Formatting* section of that tutorial which uses *TutorialIndex*](https://dev.vantiq.com/docs/system/tutorials/genaibuilder/#3-custom-formatting-and-return-types)
and then run it several times.

<a name="ai_add_secrets_s5"></a>
##### 5. Confirm K8s Network Policy is Working with Test curls from AI Assistant Pod

There are Kubernetes network policies deployed by k8sdeploy_tools to ensure that any connector pods
which are deployed can only access what they should, and nothing they shouldn't. To ensure these
network policies are working correctly, you should test them once your AI Assistant pod is running.

To test this, exec onto the AI Assistant pod, then run these test curl commands to verify that the
network policy is working:

```
  curl -v http://mongodb-0.vantiq-myvantiq-mongodb.myvantiq.svc.cluster.local:27017
  curl -v https://INSTALLATIONFQDN/
```

You will of course need to use the correct FQDN for your `mongodb-0` pod by substituting your namespace
for `myvantiq` in the first command, and by substituting your actual installation FQDN for
`INSTALLATIONFQDN` in the second command.

The first command should not work (the network policy should block it) and the second one should work
(the network policy should allow it).


<a name="ai_genaiflow"></a>
#### Deploy the GenAI Flow Service Connector As Needed

If any Orgs will be using the [GenAI Builder](https://dev.vantiq.com/docs/system/genaibuilder), those
Orgs will need to deploy the GenAI Flow service connector for their Org. See the
[*Deploying the GenAI Flow Service Connector* section of the *Administrators Reference Guide*](https://dev.vantiq.com/docs/system/namespaces/#deploying-the-genai-flow-service-connector)
for the link to the zip file containing the project to deploy. You should save a copy of this zip file
to use in step 2.

For each Org that will use GenAI Builder, deploy the GenAI Flow service connector with the following
steps.

<a name="ai_genaiflow_s1"></a>
#### 1. Add `k8sResources` Quota to the Org

Before the GenAI Flow service connector can be deployed into the cluster for an Org, that Org must
first have sufficient `k8sResources` quota. This quota must be granted by a user with `System Admin`
privs in the `system` namespace.

Such a user can grant the needed quota by doing the following:

 1. Bring up the Org list (`Administer`-> `Organizations`)
 2. Edit the Org by selecting `Edit` from the `...` menu for the Org
 3. Click on `Edit Quotas` in the Org edit pane that appears

If the existing quota is empty, it should be changed to:

```
{
    "limits": {
        "k8sResources": {
            "vCPU": "1",
            "memory": "1Gi"
        }
    }
}
```

If the existing quota is not empty, the `k8sResources` section above should be added to
the existing quota JSON.

For more info on Org quotas, see the
[*Creating a New Organization* section of the *Administrators Reference Guide*](https://dev.vantiq.com/docs/system/namespaces/#creating-a-new-organization).

<a name="ai_genaiflow_s2"></a>
#### 2. Deploy GenAI Flow Connector for Each Org As Needed

Now that the Org has the needed K8s quota, deploy the GenAI Flow service connector for each Org that
will be using the GenAI Builder. The Org Admin for the Org can do this, or if you have access to the
root namespace for the Org then you can do it for them.

Deploy the connector by doing the following:

  1. As a user with Org Admin privs for that Org, switch into the root namespace of the Org
  2. Import the service connector by doing the following:
      1. Click on `Project` -> `Import`
      2. Drag and drop the service connector zip file into the `Drop folder or zip for import here` area
      3. Click the `Import` button.

Once you do this and a `vantiq-worker` pod runs, your should see the GenAI flow connector pod start
and reach a `Running` state.

<a name="ai_genaiflow_s3"></a>
#### 3. Confirm proper operation of any GenAI Flow Connectors

If you have deployed a GenAI Flow connector for any Orgs as described in step 2, you can test each
of them by using the GenAI Builder to create an app in a namespace in that Org, then running the app.

A simple way to do this is to import the
[GenAI Builder Tutorial](https://dev.vantiq.com/docs/system/tutorials/genaibuilder/), set the
`OPENAI_KEY` secret to a valid value, then run the *tellAJoke* GenAI procedure.
