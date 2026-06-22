# Vantiq R1.39 Upgrade Instructions - QDrant, Keycloak, GenAI Flow Connectors

## Overview

Vantiq R1.39 makes several changes to components in Vantiq installations which require additional
upgrade steps (see below).

After the upgrade, the new GenAI Flow connector will need to be deployed for each Org using the GenAI
Builder, if you have any.

The extra steps for R1.39 upgrades of private clouds are detailed in this document. Please follow these
additional instructions as part of the R1.39 upgrade process (along with the standard upgrade instructions)
to ensure the upgrade is done properly.

&nbsp;

## Additional Steps for the R1.38 -> R1.39 upgrade process

### Summary of Steps

As noted above, in addition to the normal upgrade steps, the R1.38 -> R1.39 upgrade process requires
some extra steps:

  - k8sdeploy 3.14.3 (the minimum version for R1.39) upgrades several components:
    - Upgrades QDrant to v1.9.2. This requires an intermediate upgrade to v1.8.3 to update the schema properly.
    - Upgrades Keycloak to v24, with a chart change that requires a `deploy.yaml` change
  - If you have multiple installations on the same private cloud:
    - The first installation to be upgraded to R1.39 will require the others to have some overrides added to keep their config correct for R1.38
    - Later when you upgrade these other installations to R1.39, these overrides will need to be removed

*Note*: in the example below, the installation name is `myvantiq`, you will need to change this to the
actual installation name(s) you are upgrading.

### A Note About Multi-installation Private Clouds

If you are running a private cloud with multiple installations and you are upgrading the first of these
installations to R1.39 while leaving the others at R1.38, there are some changes you will need to make
to the R1.38 installations that are detailed in the prep steps below.

Later, as you upgrade the other installation(s) from R1.38 to R1.39, you will need to undo those changes
since they are not needed for R1.39. These are also noted in the prep steps below.

In the example below, there is one installation `myoldvantiq` remaining at R1.38, with the `myvantiq`
installation being upgraded to R1.39.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

#### 1. Ensure Needed `orgCompute` Node Resources for GenAI Flow Connectors

When you upgraded to R1.37, you should have created at least one `orgCompute` node to run the the AI
Assistant pod. For any Org which will use the GenAI Builder that is new in R1.39, you will need to
deploy a GenAI Flow connector for that Org. These connector pods run on an `orgCompute` node, and each
requires 1 CPU and 1Gi memory.

While it is likely your existing `orgCompute` node has enough resources for several GenAI Flow
connectors, you should add up the total amount of CPU and memory needed for all of them and compare
that to the available CPU and memory resources on the node. If needed, scale up one or more additional
`orgCompute` nodes to provide the capacity needed for your GenAI Flow connectors.

#### 2. Update `vantiq_system_release` in `cluster.properties` to `3.14.3` or Later

R1.39 requires a minimum `3.14.3` k8sdeploy release. As of this writing (10 Jul 2024) there is not
a newer release, but as newer releases are created they should continue to work for R1.39 (subject
to the recommendations in the
[*k8sdeploy* release map reference](https://github.com/Vantiq/k8sdeploy/blob/master/ReleaseMap.md)).
Change the `vantiq_system_release` value in your `cluster.properties` file to the desired k8sdeploy
release, so it will be ready to apply with `deployVantiq` at upgrade time.

#### 3. Update `deploy.yaml` to R1.39 Values

Make the following changes to your `deploy.yaml` files so they will be ready to apply with
`deployVantiq` at upgrade time:

##### 3a. Update the vantiq image tag `vantiq.installations.myvantiq.image.tag`

Update the vantiq image tag `vantiq.installations.myvantiq.image.tag` to `1.39.X` where `X` is the
desired patch release (currently `1.39.6`).

##### 3b. Update the Keycloak Database Parameter to Match the Keycloak v24 Chart

Keycloak was updated to v24 in k8sdeploy `3.14.2` and it has an updated chart which changed the
database parameter.

To implement this, the database parameter of the keycloak section needs to be changed
from:

```
keycloak:
  persistence:
    dbHost: my-keycloakdb.somedomain.com
```

to

```
keycloak:
  database:
    hostname: my-keycloakdb.somedomain.com
```

##### 3c. For Installations Remaining at R1.38 Only: Set QDrant Version to v1.7.4

*If you only have a single Installation in your private cloud, you can skip this step.*

As noted above, if you are running a private cloud with multiple installations and you are
upgrading the first of these installations to R1.39 while leaving the others at R1.38, this is
one of the steps you will need to do for each of the installations remaining at R1.38. In the
example here, there is one installation remaining at R1.38, `myoldvantiq`.

Since updating to k8sdeploy `3.14.3` will change the QDrant version tag to v1.9.2 (the correct
version for R1.39), any installations remaining at R1.38 will need to have their QDrant
version set to v1.7.4 (the version they are already running).

To implement this, in the installation sections for each such R1.38 installation 
(`vantiq.installations.myoldvantiq` in this example) the vectordb subsection needs to be changed
from:

```
        vectordb:
          enabled: true
          persistence:
            size: 30Gi
```

to

```
        vectordb:
          enabled: true
          image:          
            tag: v1.7.4
          persistence:
            size: 30Gi
```

##### 3d. For Previous R1.38 Installations Upgrading to R1.39 Only: Remove QDrant Version Override

*If you only have a single Installation in your private cloud, you can skip this step.*

Conversely, if you are running a private cloud with multiple installations and you are now
upgrading later installations to R1.39 from R1.38 where you previously added a QDrant version
override, you will now need to remove that override to allow the default QDrant version tag of
`v1.9.2` in k8sdeploy `3.14.3` to be used. In the example here, there is one such installation,
named `myoldvantiq`.

To implement this, in the installation sections for each such R1.38 installation 
(`vantiq.installations.myoldvantiq` in this example) the vectordb subsection needs to be changed
from:


```
        vectordb:
          enabled: true
          image:          
            tag: v1.7.4
          persistence:
            size: 30Gi
```

to

```
        vectordb:
          enabled: true
          persistence:
            size: 30Gi
```

#### 4. For Multi-installation Private Clouds Only: Add or Remove `load-model` Config Override File

*If you only have a single Installation in your private cloud, you can skip this step.*

##### 4a. For Installations Remaining at R1.38 Only: Add `load-model` Config Override File

*If you only have a single Installation in your private cloud, you can skip this step.*

As noted above, if you are running a private cloud with multiple installations and you are
upgrading the first of these installations to R1.39 while leaving the others at R1.38, this is
one of the steps you will need to do for each of the installations remaining at R1.38. In the
example here, there is one installation remaining at R1.38, `myoldvantiq`.

Since updating to k8sdeploy `3.14.3` will change the `io.vantiq.vertx.BootstrapVerticle.json`
file for the `load-model` container to the R1.39 version, any installations remaining at R1.38
will need to have their `io.vantiq.vertx.BootstrapVerticle.json` file for the `load-model`
container overridden.

To implement this, create the needed override file (in this example
`deploy/vantiq/config/myoldvantiq/vantiq/loadModel/io.vantiq.vertx.BootstrapVerticle.json`)
with the following contents:

```
{
  "startupMode": "loadResourcesOnly",
  "verticles": [
    {
      "main": "guice:io.vantiq.security.SecurityManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.security.SecurityMgrModule",
            "io.vantiq.security.authn.internal.AuthenticationModule"],
          "auditsEnabled": false
        },
        "instances": 1
      }
    },
    {
      "main": "guice:io.vantiq.rulemgr.RuleManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.rulemgr.RuleMgrModule"]
        },
        "instances": 1
      }
    },
    {
      "main": "guice:io.vantiq.executionmgr.ExecutionManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.executionmgr.ExecutionMgrModule"]
        },
        "instances": 1
      }
    },
    {
      "main": "guice:io.vantiq.modelmgr.ModelManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.modelmgr.ModelMgrModule"]
        },
        "instances": 1
      }
    },
    {
      "main": "guice:io.vantiq.sourcemgr.SourceManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.sourcemgr.SourceMgrModule"]
        },
        "instances": 1
      }
    },
    {
      "main": "guice:io.vantiq.federation.FederationManager",
      "options": {
        "config": {
          "modules": ["io.vantiq.service.storage.DatabaseServiceModule", "io.vantiq.federation.FederationMgrModule"]
        },
        "instances": 1
      }
    }
  ]
}
```

##### 4b. For Previous R1.38 Installations Upgrading to R1.39 Only: Remove `load-model` Config Override File

*If you only have a single Installation in your private cloud, you can skip this step.*

Conversely, if you are running a private cloud with multiple installations and you are now
upgrading later installations to R1.39 from R1.38 where you previously added a `load-model` config
override file, you will now need to remove that override file to allow the default R1.39 version
of the `io.vantiq.vertx.BootstrapVerticle.json` file for the `load-model` container to be used. 

To implement this, remove the override file (in this example
`deploy/vantiq/config/myoldvantiq/vantiq/loadModel/io.vantiq.vertx.BootstrapVerticle.json`).

#### 5. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `cluster.properties` and `deploy.yaml` and `io.vantiq.vertx.BootstrapVerticle.json`
config override files in your `targetCluster` cluster branch, then push the changes to your remote
cluster repository.

&nbsp;

### Upgrade Steps


#### 1. Do the first (intermediate) manual upgrade of QDrant to v1.8.3

Edit the QDrant statefulset (`vantiq-myvantiq-vectordb` in this example) with the command

```
  kubectl edit sts -n myvantiq vantiq-myvantiq-vectordb
```

and change the image version to `qdrant/qdrant:v1.8.3`.

When you save this change, it should cause a restart of the QDrant pod (`vantiq-myvantiq-vectordb-0`
in this example). The Qdrant schema will upgrade from v1.7.4 to 1.8.3 as the QDrant pod restarts
and reaches a `Running` state. If it does not reach a `Running` state you will need to investigate
why.

*Note:* there is no indication in the vectordb pod log that the schema migration is happening, or
that it has completed.

Once the new pod is in a `Running` state, you should be able to move ahead
with the rest of the upgrade.

#### 2. Scale down all Vantiq statefulsets

Scale down the vantiq and metrics-collector statefulsets with the commands

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=0
  kubectl scale sts vantiq -n myvantiq --replicas=0
```

Also scale down all Isolated Org Compute statefulsets, if you have any.

#### 3. Upgrade the installation with `deployVantiq`

Run `deployVantiq` to upgrade the installation components, and observe the R1.39 upgrade process
as usual (watch the log of the `load-model` init container as it runs to confirm the schema update
worked, then watch the log of the `vantiq` container to confirm it starts properly).

The Qdrant schema will also upgrade from v1.8.3 to v1.9.2 as the vectordb pod restarts and reaches
a `Running` state. If it does not reach a `Running` state you will need to investigate why. As with
v1.8.3, there is no indication in the vectordb pod log that the schema migration is happening, or
that it has completed.

#### 4. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.

### Post-Upgrade - Deploy the GenAI Flow Service Connector As Needed

Once the upgrade is complete and you have confirmed proper operation of the installation, you should
deploy the GenAI Flow service connector for each Org that will be using the GenAI Builder. See the
[*Deploying the GenAI Flow Service Connector* section of the *Administrators Reference Guide*](https://dev.vantiq.com/docs/system/namespaces/#deploying-the-genai-flow-service-connector)
for the link to the zip file containing the project to deploy. You should save a copy of this zip file
to use in step 2.

For each Org that will use GenAI Builder, deploy the GenAI Flow service connector with the following
steps.

#### 1. Add `k8sResources` Quota to the Org

Before the GenAI Flow service connector can be deployed into the cluster, the Org must
first have sufficient `k8sResources` quota. This quota must be granted by a user with
`System Admin` privs in the `system` namespace.

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

#### 2. Deploy GenAI Flow Connector for Each Orgs As Needed

Now that the Org has the needed K8s quota, deploy the GenAI Flow service connector for each Org that
will be using the GenAI Builder.

Deploy the connector by doing the following:

  1. As a user with Org Admin privs for that Org, switch into the root namespace of the Org
  2. Import the service connector by doing the following:
      1. Click on `Project` -> `Import`
      2. Drag and drop the service connector zip file into the `Drop folder or zip for import here` area
      3. Click the `Import` button.

#### 3. Confirm proper operation of any GenAI Flow Connectors

If you have deployed a GenAI Flow connector for any Orgs as described in step 2, you can test each
of them by using the GenAI Builder to create an app in a namespace in that Org, then running the app.

A simple way to do this is to import the
[GenAI Builder Tutorial](https://api.vantiq.com/docs/system/tutorials/genaibuilder/), set the
`OPENAI_KEY` secret to a valid value, then run the *tellAJoke* GenAI procedure.
