# Vantiq R1.37 Upgrade Instructions for AI Components

## Overview

Vantiq R1.37 adds AI components to Vantiq installations: the AI Assistant which provides our core AI
features, and a vector database which provides the semantic indexes for the AI Assistant.

The extra steps for R1.37 upgrades of private clouds required for these new AI components are detailed
in this document. Please follow these additional instructions as part of the R1.37 upgrade process to
deploy the AI components properly.

Also note that a private cloud can choose to not run these AI components if desired, although features
that use them still appear in the UI and will error there if the components are not running. If you run
a private cloud and choose to not run the R1.37 AI components, follow the instructions in
[*Alternate Non-AI Config for R1.37 and Later Releases* doc in k8sdeploy_tools](https://github.com/Vantiq/k8sdeploy_tools/blob/master/docs/R1dot37AltNonAI.md)
instead of the instructions in this document.

&nbsp;

## Additional Steps for the R1.36 -> R1.37 upgrade process

### Summary of Steps

In addition to the normal upgrade steps, the R1.36 -> R1.37 upgrade process requires some extra steps
which can be summarized as:

 - Create two new secrets (vantiq-ai-assistant-env and vantiq-worker)
 - Upgrade MongoDB to 4.4.24 then to 5.0.18
 - Confirm proper operation of the new AI features

*Note*: in the example below, the installation name is `myvantiq`, you will need to change this to the
actual installation name(s) you are upgrading.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

#### 1. An `orgCompute` node for the AI Assistant pod is required

A node with the `vantiq.com/workload-preference=orgCompute` label is needed for the AI Assistant pod.
If you do not yet have an `orgCompute` node pool, you will need to create one and scale it to 1 node. If
you already have an `orgCompute` node pool, make sure one of the nodes has enough available CPU (1) and
memory (4GB) for the AI Assistant pod.

#### 2. Create a new vantiq worker Access Token

Create a new vantiq worker Access Token in the `system` namespace for use in the `vantiq-worker` secret
(prep step 3). This access token should be named something clear like `k8sWorker` and should use the
`system.federatedK8sWorker` profile. Note the value of this access token when you create it, since you
will need it for the next step.


#### 3. Create new AI and vantiq-worker secrets

In your `targetCluster` cluster branch, create new `vantiq-ai-assistant-env` and `vantiq-worker` secrets
either in the installation section (or the common section as shown) of secrets.yaml.

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
        token: TOKENVALUEFROMPREPSTEP2
```

Note that your vantiq-worker token value should be the access token from prep step 2.

Next, your `targetCluster/deploy/sensitive/vantiq-ai-assistant-env.txt` file should contain the
contents

```
OPENAI_API_KEY=XXXXXX
```

with the private cloud owner's actual OpenAI API key in place of the `XXXXXX`.

Finally, run `generateSecrets` to generate the YAML files for these secrets. After doing so you should
confirm that the two new YAML files have been created in `targetCluster/deploy/secrets/vantiq` as
expected. You should commit these YAML files to your `targetCluster` cluster branch along with your
modified `deploy.yaml` and `cluster.properties` files in prep step 6.

#### 4. Update deploy.yaml to R1.37 Values

Make the following changes to your `deploy.yaml` file, so they will be ready to apply with
`deployVantiq` at upgrade time:

##### 4a. Update the vantiq image tag `vantiq.installations.myvantiq.image.tag`

Update the vantiq image tag `vantiq.installations.myvantiq.image.tag` to `1.37.X` where `X` is the
desired patch release (currently `1.37.10`).

##### 4b. Set MongoDB version to 5.0.18 

Set MongoDB version to 5.0.18 (set `vantiq.installations.myvantiq.mongodb.image.tag` to `5.0.18`):

```
        mongodb:
          image:
            tag: 5.0.18
```

##### 4c. Enable the `vantiq-worker` and Qdrant vector db statefulsets

Enable the `vantiq-worker` and Qdrant vector db statefulsets by adding `vectordb` & `worker`
subsections to the `vantiq` section (`vantiq.installations.myvantiq`) as follows:

```
        vectordb:
          enabled: true
          persistence:
            size: 30Gi

        worker:
          enabled: true
```

##### 4d. Replace the `io.vantiq.modelmgr.ModelManager.json` subsection

Replace the `io.vantiq.modelmgr.ModelManager.json` subsection of the `vantiq` configuration
section (`vantiq.installations.myvantiq.configuration`) with:

```
          io.vantiq.modelmgr.ModelManager.json:
            config:
              collectionMonitorInterval: "3 hours"
              semanticIndexService:
                vectorDB:
                  host: "vantiq-myvantiq-vectordb.myvantiq.svc.cluster.local"
```

##### 4e. Update `vantiq_system_release` in `cluster.properties`

R1.37 requires a minimum `3.13.2` k8sdeploy release. As of this writing (27 Feb 2024) the
recommended release is `3.13.4`. Change the `vantiq_system_release` value in your
`cluster.properties` file to the desired k8sdeploy release.

#### 5. Optional: confirm that your shared nodes have enough memory for Grafana

If your installations have many namespaces, the current version (9.5.1) of Grafana may need to have a
resource block defined and the `shared` nodes must have enough memory to meet those resource requests.
If you notice the Grafana pod restarting during vantiq pod startup, it is likely due to this problem.
This in turn can cause vantiq pod startup problems, because the old Grafana pod takes some time to
stop so the new Grafana pod is stuck in `Pending` mode for several minutes which blocks vantiq pod
startup.

To fix this problem, add a resource block to the `grafana` section of `deploy.yaml` and make sure
that your shared nodes have enough memory to meet the memory request. For example, on the main Vantiq
public cloud (dev.vantiq.com etc) the `grafana` resource block is:

```
        resources:
          limits:
            cpu: 2
            memory: 6Gi
          requests:
            cpu: 1
            memory: 2Gi
```

This is run on shared nodes which have 2 vCPU / 8GB to ensure that this Grafana memory request is
met. This behavior of Grafana 9.5.1 varies by the number of namespaces, so if your private cloud
installations have a smaller number of namespaces then you may not see this problem.

#### 6. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `deploy.yaml`, `cluster.properties` and two new secrets YAML files in your
`targetCluster` cluster branch.

&nbsp;

### Upgrade Steps

#### 1. Scale down all Vantiq statefulsets

Scale down the vantiq and metrics-collector statefulsets with the commands

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=0
  kubectl scale sts vantiq -n myvantiq --replicas=0
```

Also scale down any Isolated Org Compute statefulsets, if you have any.

#### 2. Do the first (intermediate) manual upgrade of MongoDB to 4.4.24

Edit the mongodb statefulset with the command

```
  kubectl edit sts -n myvantiq mongodb
```

changing the image version to `mongo:4.4.24` in two places, the `mongodb` container section and
the `bootstrap` initcontainer section.

When you save this change, it should cause a rolling restart of all three mongodb pods.

Once the rolling restart is complete, exec onto the `mongodb-0` pod with

```
  kubectl exec -it mongodb-0 -n myvantiq -- bash
```

and run mongo as root with

```
  mongo -uroot -pADMINPASSWORD
```

(where `ADMINPASSWORD` is your admin password) then confirm the version with the command

```
  db.version()
```

which should now be `4.4.24`. Next, set the feature compatibility version to `4.4` with the command

```
  db.adminCommand( { setFeatureCompatibilityVersion: "4.4" } )
```

and confirm the feature compatibility version is 4.4 with the command

```
  db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } )
```

#### 3. Repeat the manual upgrade of MongoDB, this time to 5.0.18

Edit the mongodb statefulset with the command

```
  kubectl edit sts -n myvantiq mongodb
```

again changing the image version to `mongo:5.0.18` in two places, the `mongodb` container section
and the `bootstrap` initcontainer section.

When you save this change, it should again cause a rolling restart of all three mongodb pods.

Once the rolling restart is complete, exec onto the `mongodb-0` pod with

```
  kubectl exec -it mongodb-0 -n myvantiq -- bash
```

and run mongo as root with

```
  mongo -uroot -pADMINPASSWORD
```

where `ADMINPASSWORD` is your admin password. Also note, if your admin username is something other
than `root` then you will need to specify that username with the `-u` flag rather than the `root`
username.

Next, confirm the version with the command

```
  db.version()
```

which should now be `5.0.18`. Next, set the feature compatibility version to `5.0` with the command

```
  db.adminCommand( { setFeatureCompatibilityVersion: "5.0" } )
```

Confirm the feature compatibility version is `5.0` with the command

```
  db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } )
```

#### 4. Upgrade the installation with deployVantiq

Run `deployVantiq` to upgrade the installation components, and observe the R1.37 upgrade process
as usual (watch the log of the `load-model` init container as it runs to confirm the schema update
worked, then watch the log of the `vantiq` container to confirm it starts properly).

You should also notice the new AI Assistant and Qdrant vectordb pods starting and reaching a
`Running` state. If they do not reach a `Running` state you will need to investigate why.

Note that the MongoDB version will already be `5.0.18` so this step should not change the mongodb
statefulset and therefore not cause a rolling restart of the mongodb pods.

#### 5. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.

#### 6. Confirm network policy is working w/ test curls from AI Assistant pod

Exec onto the AI Assistant pod, then run these test curls to verify that the network policy is working:

```
  curl -v http://mongodb-0.vantiq-dev-mongodb.dev.svc.cluster.local:27017
  curl -v https://INSTALLATIONFQDN/
```

The first command should not work (the network policy should block it) and the second one should work
(the network policy should allow it).


#### 7. Confirm proper operation of the AI Assistant

A simple way to test the AI Assistant is to use the `AI Documentation Search` feature under the `Help`
menu. Type in some questions about Vantiq and it should give you answers from the docs, if the AI
Assistant is functioning properly.

You can also try some simple applications using the `submitPrompt` and `answerQuestion` activity
patterns, if you have them.
