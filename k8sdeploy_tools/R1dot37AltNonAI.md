## Alternate Non-AI Config for R1.37 and Later Releases

### Overview

Vantiq R1.37 adds AI components to Vantiq installations: the AI Assistant which provides our core AI
features, and a vector database which provides the semantic indexes for the AI Assistant.

However, a private cloud can choose to not run these AI components if desired, although features that
use them still appear in the UI and will get an error if used when the components are not running. If
you run a private cloud and choose to not run the R1.37 AI components, follow the instruction in this
document.

If instead you choose to run these AI components, you should follow the additional instructions in
[*R1.37 Upgrade Instructions for AI Components* doc in k8sdeploy_tools](https://github.com/Vantiq/k8sdeploy_tools/blob/master/docs/R1dot37Upgrade.md).
as part of your R1.37 upgrade instead of the instructions in this document.

The instructions in this document are similar to that other document, but instead of the steps to
enable the AI components there is a step to disable them. The MongoDB upgrade steps are the same
in both documents.

&nbsp;

## Additional Steps for the R1.36 -> R1.37 upgrade process - Alternate Non-AI Config

### Summary of Steps

In addition to the normal upgrade steps, the R1.36 -> R1.37 upgrade process requires some extra steps
to upgrade MongoDB to 4.4.24 then to 5.0.18, and to disable the `vantiq-worker` CronJob.

*Note*: in the example below, the installation name is `myvantiq`, you will need to change this to the
actual installation name(s) you are upgrading.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

#### 1. Update deploy.yaml to R1.37 Values

Make the following changes to your `deploy.yaml` file, so they will be ready to apply with
`deployVantiq` at upgrade time:

##### 1a. Update the vantiq image tag `vantiq.installations.myvantiq.image.tag`

Update the vantiq image tag `vantiq.installations.myvantiq.image.tag` to `1.37.X` where `X` is the
desired patch release (currently `1.37.10`).

##### 1b. Set MongoDB version to 5.0.18 

Set MongoDB version to 5.0.18 (set `vantiq.installations.myvantiq.mongodb.image.tag` to `5.0.18`):

```
        mongodb:
          image:
            tag: 5.0.18
```

##### 1c. Disable the `vantiq-worker`

Disable the `vantiq-worker` in the `worker` subsection of the `vantiq` section:

```
vantiq:
  worker:
    enabled: false
```

**Note:** if you have any Isolated Compute Orgs, then you can't disable the `vantiq-worker`
CronJob and you must skip this section.

##### 1d. Update `vantiq_system_release` in `cluster.properties`

R1.37 requires a minimum `3.13.2` k8sdeploy release. As of this writing (27 Feb 2024) the
recommended release is `3.13.4`. Change the `vantiq_system_release` value in your
`cluster.properties` file to the desired k8sdeploy release.

#### 2. Optional: confirm that your shared nodes have enough memory for Grafana

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

#### 3. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `deploy.yaml` and `cluster.properties` files in your `targetCluster` cluster branch.

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

(where `ADMINPASSWORD` is your admin password) then confirm the version with the command

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

Note that the MongoDB version will already be `5.0.18` so this step should not change the mongodb
statefulset and therefore not cause a rolling restart of the mongodb pods.

#### 5. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.
