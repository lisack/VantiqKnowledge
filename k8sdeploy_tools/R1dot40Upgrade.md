# Vantiq R1.40 Upgrade Instructions:

# Update Qdrant & Vantiq Volumes, Add `unstructured-api`

## Overview

Vantiq R1.40 makes several changes to components in Vantiq installations which require additional
upgrade steps (see below).

The extra steps for R1.40 upgrades of private clouds are detailed in this document. Please follow these
additional instructions as part of the R1.40 upgrade process (along with the standard upgrade instructions)
to ensure the upgrade is done properly.

Please note that the elements of the R1.40-specific items detailed in this document have also been
integrated into docs such as the [Installing Vantiq](Installation.md) doc, so those docs are current with
info for the latest release.

### Changes for R1.40

R1.40 requires k8sdeploy v3.15.5 which makes the following changes:

  - Contains fixes to match the k8sdeploy_tools upgrade of Gradle to 8.10.2
  - Adds the new Unstructured API server to the deployed shared components with affinity to `shared` nodes
  - Adds an optional `snapshotVolume` PVC to the `vantiq` statefulset (for temp storage of files being loaded into semantic indexes)
  - Affinities Qdrant pods to `database` nodes
  - Adds pod security settings & explicit resource settings for Qdrant
  - Adds volume to Qdrant for collection snapshots
  - Adds `firebase.json` file to vantiq-push secret
  - Changes default username for Keycloak admin user from `keycloak` to `admin`

&nbsp;

## Additional Steps for the R1.39 -> R1.40 upgrade process

*Note*: in the example below, the cluster branch name is `myvantiq-cluster` and the
installation name is `myvantiq`, you will need to change these to the actual names you
are upgrading.

As noted above, in addition to the normal upgrade steps, the R1.39 -> R1.40 upgrade process requires
some extra steps and has some other changes you should be aware of. To do these extra steps, first
do the prep steps and once you are ready to upgrade then do the upgrade steps.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

#### 1. Ensure Needed `database` Node Resources for Qdrant Pod (optional)

As noted below, step 4 of the upgrade steps below will update Qdrant to affinity its pods to the
`database` nodes, and they will require 8Gi of memory. As a prep step, you can determine if there
is a database node where the Qdrant pod can run, and if not, scale one up.

Note that the node in question will not only need CPU and memory resources for the Qdrant pod, it
will also need to be in the same availability zone as the existing Qdrant volume (the details of
this requirement varies by cloud provider, consult with your infrastructure team if you are not
sure of the behavior on your infrastructure).

This step is optional, the alternative is to wait until upgrade step 4 below and see if the Qdrant
pod schedules onto a node. If it doesn't, you will need to be prepared to quickly scale one up.

#### 2. Update `vantiq_system_release` in `cluster.properties` to `3.15.5` or Later

R1.40 requires a minimum `3.15.5` k8sdeploy release. As of this writing (4 Feb 2025) the latest
release is `3.16.1`, and it has been verified to work for R1.40.10 and later so you should use
`3.16.1`. When in doubt, consult the
[*k8sdeploy* release map reference](https://github.com/Vantiq/k8sdeploy/blob/master/ReleaseMap.md).
Change the `vantiq_system_release` value in your `cluster.properties` file to the desired k8sdeploy
release, so it will be ready to apply with `deployVantiq` at upgrade time.

#### 3. Update `deploy.yaml` to R1.40 Values

Make the following changes to your `deploy.yaml` file so they will be ready to apply with
`deployVantiq` at upgrade time:

##### 3a. Add the `unstructured-api` section

This release adds `unstructured-api` to the shared components, so you will need to add the new
`unstructured-api` section. The suggested location is just after the `keycloak` section, which is
just before the `vantiq` section.

The new `unstructured-api` section should be:

```
unstructured-api:
  replicaCount: 2
  parallelMode:
    enabled: true
  downloadStorage:
    enabled: true
    storageClass: vantiq-sc
```

The default `replicaCount` value for `unstructured-api` in k8sdeploy is `1`, and if that will be
sufficient for your needs you can leave that line out of your `deploy.yaml`. The example shows
setting this to `2` which will scale the `unstructured-api` statefulset to `2`.

##### 3b. Update the vantiq image tag `vantiq.installations.myvantiq.image.tag`

Update the vantiq image tag `vantiq.installations.myvantiq.image.tag` to `1.40.X` where `X` is the
desired patch release (currently `1.40.16`).

##### 3c. Add `genAIFlowService.unstructuredApiUrl` to `io.vantiq.aimanager.AiManager.json` Config Override if Using AI

If you are using AI features you will have an existing config override to `io.vantiq.aimanager.AiManager`
in your `deploy.yaml` like this:

```
vantiq:
  installations:
    - myvantiq
        configuration:
          io.vantiq.aimanager.AiManager.json:
            config:
              semanticIndexService:
                vectorDB:
                  host: "vantiq-myvantiq-vectordb.myvantiq.svc.cluster.local"
```

If you do, then you will need to add `genAIFlowService.unstructuredApiUrl` to that config block like this:

```
vantiq:
  installations:
    - myvantiq
        configuration:
          io.vantiq.aimanager.AiManager.json:
            config:
              semanticIndexService:
                vectorDB:
                  host: "vantiq-myvantiq-vectordb.myvantiq.svc.cluster.local"
              genAIFlowService:
                unstructuredApiUrl: "http://unstructured-api.shared.svc.cluster.local"
```

If you are not using AI features, you will not have an existing config override to
`io.vantiq.aimanager.AiManager`and you can ignore this item.

Note that each config file content block in `deploy.yaml` must be complete: for config file
content you can't have partial data that is merged with k8sdeploy and chart data by Helm. See
https://github.com/helm/helm/issues/3486 for details about this bug in Helm that will hopefully
get fixed eventually.

#### 4. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `cluster.properties` and `deploy.yaml` in your `targetCluster` cluster
branch, then push the changes to your remote cluster repository.

&nbsp;

### Upgrade Steps Summary/Checklist

This is a summary of the upgrade steps, which can be used as checklist (these steps are detailed
below):

  1. Run `deployShared` to deploy `unstructured-api` pods
  2. Disable the `vantiq-worker` CronJob
  3. Scale down `vantiq` and `metrics-collector` statefulsets
  4. Delete the Qdrant (`vantiq-xxx-vectordb`) statefulset using `—cascade=orphan`
  5. Upgrade Qdrant with `deployVantiq` (targeting only the installation being upgraded, if you have multiple installations)
  6. Delete the `vantiq` statefulset in the target installation (no `—cascade=orphan` needed)
  7. Upgrade Vantiq with `deployVantiq` targeting only the installation being upgraded
  8. Confirm proper operation of the installation (standard upgrade process)

Note that at step 5 Qdrant will be updated to affinity to the `database` nodes and request 8Gi of
memory. If you did not do prep step 1 and are instead waiting until this point to determine if you
need a new database node where the Qdrant pod can run, you will need to be prepared to quickly scale
one up if you need to.

### Upgrade Steps

#### 1. Run `deployShared` to deploy `unstructured-api` pods

Run `deployShared` to deploy the `unstructured-api` pods with

```
  ./gradlew -Pcluster=myvantiq-cluster deployShared
```

Note: you should confirm the new `unstructured-api` pods are in a `Running` state before starting
step 3.

#### 2. Disable the `vantiq-worker` CronJob

Edit the `vantiq-worker` CronJob in the installation being upgraded, so the `vantiq-worker` pods
won't keep trying to contact Vantiq while it's down. To do this, edit the CronJob with

```
  kubectl edit cronjob vantiq-worker -n myvantiq
```

and at the bottom change

```
  suspend: false
```
to

```
  suspend: true
```

#### 3. Scale down `vantiq` and `metrics-collector` statefulsets

Scale down the `vantiq` and `metrics-collector` statefulsets with

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=0
  kubectl scale sts vantiq -n myvantiq --replicas=0
```

Also scale down all Isolated Org Compute statefulsets, if you have any.

#### 4. Delete the Qdrant statefulset using <code style="white-space:nowrap;">--cascade=orphan</code>

Delete the Qdrant statefulset (in this example, `vantiq-myvantiq-vectordb`) using
<code style="white-space:nowrap;">--cascade=orphan</code>:

```
  kubectl delete sts vantiq-myvantiq-vectordb -n myvantiq —-cascade=orphan
```

This will delete the Qdrant statefulset without deleting the volumes which contain the Qdrant
data. For details on how <code style="white-space:nowrap;">--cascade=orphan</code> works, see the
[*Delete owner objects and orphan dependents* section of the *Use Cascading Deletion in a Cluster* Kubernetes doc](https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/#set-orphan-deletion-policy).

#### 5. Upgrade Qdrant with `deployVantiq` targeting only the installation being upgraded

Run `deployVantiq` (targeting only the installation being upgraded which is `myvantiq` in this
example, if you have multiple installations) with

```
  ./gradlew -Pcluster=myvantiq-cluster -Pinstallation=myvantiq deployVantiq
```

When you run `deployVantiq` it will update Qdrant, but fail when it attempts to update the
`vantiq` statefulset due to the addition of volumes to it. This is to allow Qdrant a chance to
fully start before Vantiq itself updates.

Keep in mind the earlier note that at this point Qdrant will be updated to affinity to the
`database` nodes and request 8Gi of memory. If you did not do prep step 1 and are instead waiting
until this point to determine if you need a new database node where the Qdrant pod can run, you
should be prepared to quickly scale one up if you need to. The indication of this is that your
`vantiq-xxx-vectordb` pod will be stuck in `Pending` status.

At this point you should also scale down the just-scaled-up `metrics-collector` statefulset with

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=0
```
so it's not trying to start up until the next run of `deployVantiq`.

#### 6. Delete the `vantiq` statefulset in the target installation (no `—cascade=orphan` needed)

Delete the `vantiq` statefulset with

```
  kubectl delete sts vantiq -n myvantiq
```

so it can be re-created with the addition of volumes to it in step 7.

#### 7. Upgrade Vantiq with `deployVantiq` targeting only the installation being upgraded

Run `deployVantiq` again (targeting only the installation being upgraded which is `myvantiq` in this
example, if you have multiple installations) with:

```
  ./gradlew -Pcluster=myvantiq-cluster -Pinstallation=myvantiq deployVantiq
```

This should re-create the `vantiq` statefulset with the addition of volumes. As the `vantiq-0` pod
starts up, observe the R1.40 upgrade process as usual (watch the log of the `load-model` init
container as it runs to confirm the schema update worked, then watch the log of the `vantiq` container
to confirm it starts properly).

#### 8. Re-enable the `vantiq-worker` CronJob

Edit the `vantiq-worker` CronJob in the installation being upgraded, to re-enable it so
`vantiq-worker` jobs will resume running. To do this, edit the CronJob with

```
  kubectl edit cronjob vantiq-worker -n myvantiq
```

and at the bottom change

```
  suspend: true
```
to

```
  suspend: false
```

#### 9. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.
