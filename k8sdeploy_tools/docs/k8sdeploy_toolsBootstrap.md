# k8sdeploy_tools Initial Setup and Configuration

## Overview

This document describes how to setup and configure the Vantiq Kubernetes Deployment tools. The machine on which
this process is performed is known as the *deployment machine*. We support execution of the tools on Windows
(with some caveats that will be explained), MacOS, and Linux. These instructions assume that the deployment
machine has full and direct access to the Internet (no proxies or access restrictions). 

If you have not already read the 
[Deploying and Managing Vantiq Installations: Background Reference](BackgroundReference.md) doc, then you
should do that first to understand how the pieces fit together, before proceeding with the initial setup and
configuration steps in this doc.

## Installation Prerequisites 

Before you can download and configure the deployment tools you must first install the following software: 

1) Java 11 (either [Oracle](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html)
or [OpenJDK](https://jdk.java.net/archive/)). This must be at least the JRE and you must end up with “java”
in your path. When done you should be able to run “java -version” from the command line. 
1) [Git](https://git-scm.com/downloads). **Note**: if you are running on Windows, you must also install
Git Bash, and this must be used as your shell when running the tools.
1) [GitHub CLI](https://docs.github.com/en/github-cli/github-cli/quickstart). This is optional, and is not
needed if you can configure your Git client to access GitHub in some other way.
1) [Kubectl](https://kubernetes.io/docs/tasks/tools/) (Kubernetes CLI). The version should be within one
release either direction of the K8s clusters you are using. As of this writing that is 1.32.x which can be
used with K8s 1.31, 1.32 and 1.33.
1) [Helm](https://helm.sh/). The version should be Helm 3 (as of this writing, 3.18).
1) [Kubeseal](https://github.com/bitnami-labs/sealed-secrets). This is optional, but is required
if using sealed secrets. Install the current version, as of this writing 0.30.0.

## Installation and Configuration 

Once the above prerequisite software has been installed and their basic operation confirmed, the next step
is to download and configure the Vantiq deployment tools themselves. In order to do this, you must have
at least read access to the Vantiq [k8sdeploy_tools (this repo)](https://github.com/Vantiq/k8sdeploy_tools)
and [k8sdeploy](https://github.com/Vantiq/k8sdeploy) Git repositories. If you do not yet have that access,
then you should contact [Vantiq support](mailto:support@vantiq.com).

You will also need to know your Git credentials and have your Git client set up correctly on your machine
to use them. This varies by OS but may be as simple as running the GitHub CLI command `gh auth login`. The
[Git Quickstart on GitHub](https://docs.github.com/en/get-started/quickstart/set-up-git) is one reference
that can help you to set up your Git client. Depending on your environment, you may need to use the same
username and password that you use to log into GitHub, or you may need to use a personal access key in
place of the password.

Once you are ready, perform the following steps: 

1) Change directory to the directory under which you want to deploy the tools. We recommend that this be
your home directory or some sub-directory thereof. If you already have a directory in which you put other
Git repositories, then that is a good candidate as well. 
1) Run the command `git clone https://github.com/Vantiq/k8sdeploy_tools`. This will create a directory
called `k8sdeploy_tools` in your current directory. You may or may not be prompted for your credentials,
depending on whether this is the first time you have used Git.
1) Change directory to the newly created `k8sdeploy_tools` directory. Unless otherwise specified, all
commands are run from this directory. 
1) Run the command `./gradlew configureClient`. This command needs to download quite a bit of software,
so depending on the speed of your network connection it may take some time to complete. If you get an
error, stop and contact Vantiq operations. When it completes you should see something like this (there
may be more text about welcome to Gradle, but these should be the last few lines of output):

```
Starting a Gradle Daemon (subsequent builds will be faster) 
$HELM_HOME has been configured at /root/.helm. 
Happy Helming!
"vantiq" has been added to your repositories 

BUILD SUCCESSFUL in 20s 
3 actionable tasks: 3 executed
```

<ol start="5">
<li>Edit the file <code>.gradle/gradle.properties</code>. Set the properties to be your GitHub username
and password. For <code>gitPassword</code> you will need to use a personal access key instead of your
GitHub UI password. You should see the following contents:
</li> 
</ol>

```
gitUsername= 
gitPassword= 
```

If you are using them, you should also add the `clusterRepo`, `vantiqSystemRepo` and `helmChartRepo` Gradle
properties to `.gradle/gradle.properties` at this time.

For details on using the `clusterRepo` Gradle property, see the next step (step 6) and the
[*Initializing and Using a Custom Cluster Repo by default for `targetCluster`* section of the *Centrally Managing Cluster Definitions by a Customer*](CustomerManagedDefinition.md#clusterrepo)
doc.

If you are also using a custom `k8sdeploy` repo, you should see the details on using the `vantiqSystemRepo`
and `helmChartRepo` Gradle properties in the
[*Using a Custom `k8sdeploy` Repo* section of the *Centrally Managing Cluster Definitions by a Customer*](CustomerManagedDefinition.md#k8sdeployrepo)
doc.

*Note*: if you have not yet set up a personal access token in your GitHub account, see the
[Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
doc on GitHub for details on how to do that.

<ol start="6">
</li>
<li>Initialize a Non-default Cluster Repo <i>(required for first-time customer-managed private
clouds):</i> if you are a customer-managed private cloud (PC-CM) customer who is installing
your first Vantiq installation, you will have not yet set up your Git repo to store your cluster
configs. In this case you will need to set up that repo by following the instructions in the
<a href="CustomerManagedDefinition.md#clusterrepo">
<i>Initializing and Using a Custom Cluster Repo by default for <code>targetCluster</code></i>
section of the <i>Centrally Managing Cluster Definitions by a Customer</i></a> doc to create
and initialize your cluster repo. Note that the instructions there include running the
<code>./gradlew configureVantiqSystem</code> command, so if you run this step you should skip
step 7. If you already have a cluster repo set up
(<code>https://github.com/Vantiq/k8sdeploy_clusters</code> if you are Vantiq SRE, some other
cluster repo if you are a PC-CM customer) you should do step 7 instead of this step.
</li> 
</ol>

<ol start="7">
</li>
<li>Run <code>configureVantiqSystem</code><i>(if you skipped step 6 because you already have
an existing cluster repo)</i>: if you skipped step 6, run the command
<code>./gradlew configureVantiqSystem</code>. If you see an error, stop and contact Vantiq
operations. This should create the directories <code>vantiqSystem</code> and
<code>targetCluster</code>.
</li> 
</ol>

At this point you are ready to use the tools to install the Vantiq System. Instructions on how to do
this can be found in the [Installing Vantiq](Installation.md) document. 

