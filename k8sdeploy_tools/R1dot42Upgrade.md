# Vantiq R1.42 Upgrade Instructions:

# Migrate QDrant to Multi-Node, Replicated/Sharded Config

## Overview

Vantiq R1.42 makes a change to the QDrant component in Vantiq which requires additional upgrade steps
(see below).

The extra steps for R1.42 upgrades of private clouds are detailed in this document. Please follow these
additional instructions as part of the R1.42 upgrade process (along with the standard upgrade instructions)
to ensure the upgrade is done properly.

Please note that the elements of the R1.42-specific items detailed in this document have also been
integrated into docs such as the [Installing Vantiq](Installation.md) doc, so those docs are current with
info for the latest release.

### Changes for R1.42

R1.42 requires k8sdeploy v3.17.3 which makes the following changes:

  - QDrant changes & additions
    - Update to version 1.13.6
    - Client config (`vectorDbService.json`) added to `vantiq-config` configmap
    - QDrant migration tool added to automate migration to multi-node, replicated/sharded collections
    - Added QDrant backup/restore
  - Update nginx to `1.12.2` (chart `4.12.2`)

&nbsp;

## Additional Steps for the R1.41 &rarr; R1.42 upgrade process

*Note*: in the example below, the cluster branch name is `myvantiq-cluster` and the 
installation name is `myvantiq`, you will need to change these to the actual names you
are upgrading.

As noted above, in addition to the normal upgrade steps, the R1.41 -> R1.42 upgrade process requires
some extra steps and has some other changes you should be aware of. To do these extra steps, first
do the prep steps and once you are ready to upgrade then do the upgrade steps.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

Note that only prep steps 1 & 3 are extra steps. Prep steps 2 & 4 are the standard upgrade steps.

#### 1. Ensure Needed `database` Node Resources for Additional QDrant Pods

As noted below, step 3 of the added upgrade steps will update QDrant to a multi-node config
which will require 2 additional `database` nodes. As a prep step, you should scale up these
2 additional `database` nodes.

Once the new nodes have been scaled up, if they are not each in a unique zone (different from
the zone of the existing node running QDrant and in different zones from each other), you should
scale up one or more additional nodes until you have 2 new nodes which are each in a unique zone.

If you needed to scale up more than 2 new nodes to get 2 nodes which are each in a unique zone,
you should scale down the unneeded nodes. If you wish to defer scaling them down until after the
upgrade, you should at least taint the unneeded nodes with `NoSchedule` for now so the new
QDrant pods will not schedule onto them. Do that with the command

```
  kubectl taint node <NODELIST> key=value:NoSchedule
```

*Note*: each node should have a `topology.kubernetes.io/zone` label which shows the zone where
that node is located, see the output of `kubectl describe node` for that label.

#### 2. Update `vantiq_system_release` in `cluster.properties` to `3.17.3` or Later

R1.42 requires a minimum `3.17.3` k8sdeploy release. As of this writing (16 Jun 2025) this is
also the latest release. When in doubt, consult the
[*k8sdeploy* release map reference](https://github.com/Vantiq/k8sdeploy/blob/master/ReleaseMap.md).
Change the `vantiq_system_release` value in your `cluster.properties` file to the desired k8sdeploy
release, so it will be ready to apply with `deployVantiq` at upgrade time.

#### 3. Update `deploy.yaml` to R1.42 Values

Update the vantiq image tag `vantiq.installations.myvantiq.image.tag` in `deploy.yaml` to the current R1.42 Value

As with any upgrade, you must update the vantiq image tag `vantiq.installations.myvantiq.image.tag`
to the desired R1.42 value, `1.42.X` where `X` is the desired patch release (currently `1.42.2`).

In addition, you must add the `vantiq.installations.myvantiq.image.vectordb` section, which we normally
put just before the `vantiq.installations.myvantiq.image.worker` section. To do this, change


```
        worker:
          enabled: true
```

to

```
        vectordb:
          enabled: true
          replicaCount: 3
          persistence:
            size: 30Gi
          snapshotPersistence:
            enabled: true
          resources:
            limits:
              memory: 16Gi
            requests:
              memory: 16Gi
          readinessProbe:
            failureThreshold: 60
          backup:
            enabled: true
            persistentVolume:
              enabled: true
              size: 100Gi

        worker:
          enabled: true
```

#### 4. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `cluster.properties` and `deploy.yaml` in your `targetCluster` cluster
branch, then push the changes to your remote cluster repository.

&nbsp;

### Upgrade Steps Summary/Checklist

This is a summary of the upgrade steps, which can be used as checklist (these steps are detailed
below):

  1. Disable the `vantiq-worker` CronJob
  2. Scale down `vantiq` and `metrics-collector` statefulsets
  3. Upgrade Vantiq (and related components such as QDrant) with `deployVantiq`
  4. Once again scale down `vantiq` and `metrics-collector` statefulsets
  5. Confirm peer set on all 3 QDrant pods
  6. Run the QDrant migration job
  7. Upgrade nginx with `deployNginx`
  8. Scale up the `vantiq` statefulset and monitor the upgrade process
  9. Re-enable the `vantiq-worker` CronJob
  10. Confirm proper operation of the installation (standard upgrade process)

### Upgrade Steps

#### 1. Disable the `vantiq-worker` CronJob

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

#### 2. Scale down `vantiq` and `metrics-collector` statefulsets

Scale down the `vantiq` and `metrics-collector` statefulsets with

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=0
  kubectl scale sts vantiq -n myvantiq --replicas=0
```

Also scale down all Isolated Org Compute statefulsets, if you have any.

#### 3. Upgrade Vantiq (and related components such as QDrant) with `deployVantiq`

Run `deployVantiq` with

```
  ./gradlew -Pcluster=myvantiq-cluster deployVantiq
```

**Note**: this will upgrade QDrant to the multi-node config with new collections being replicated
and sharded, but it will also start to scale up the `vantiq` and `metrics-collector` statefulsets.
You should immediately scale them down (repeat step 2) as noted in step 4.

Once QDrant is updated to the new config and all 3 pods are running, the new config is implemented
but all collections will still be on the original pod and will not be replicated or sharded yet.
Once you scale down the `vantiq` and `metrics-collector` statefulsets in the next step, you will
confirm that all 3 peers of the new QDrant cluster show the same peer set. After that, you will
migrate all collections to be replicated/sharded and spread across all 3 pods.

#### 4. Immediately, again scale down `vantiq` and `metrics-collector` statefulsets

Step 3 will start to scale up the `vantiq` and `metrics-collector` statefulsets. You should
immediately scale them down (repeat step 2) to defer the Vantiq part of the upgrade until step
8, both to do defer the schema migration to step 8 where you will monitor it, and to allow the
QDrant migration (step 6) to proceed without Vantiq trying to modify the collections during
the migration.

As a final check before checking the peer set, confirm the new QDrant pods are running on the
2 additional `database` nodes (scaled up in prep step 1) as expected, with the command:

```
  kubectl get pod -n myvantiq -o wide
```

#### 5. Confirm Peer Set on All 3 QDrant Pods

Confirm the new QDrant cluster shows the same peer set on all 3 peers.

Start by checking the peer set on the `-0` pod with the commands:

```
  kubectl port-forward vantiq-myvantiq-vectordb-0 9000:6333 -n myvantiq
  curl http://localhost:9000/cluster | jq
  (terminate the kubectl command once you are done running curls)
```

*Note*: you will need to run these two commands in separate shell windows, since the `port-forward`
will continue to run until you terminate it.

Repeat for the other two pods (`-1` and `-2`) to confirm the peer set is the same on all three.

#### 6. Run the QDrant Migration Job

Create the QDrant migration job from the `qdrantmigration` CronJob with the command:

```
  kubectl create job myqdrantmigrate --from cronjob/qdrantmigration -n myvantiq
```

Monitor the output of the `myqdrantmigrate` pod with the command:

```
  kubectl logs myqdrantmigrate -n myvantiq -f
```

If the migration has problems with any of the collections, you can run the migration job again. It
will recognize any collections that have already been migrated and skip them, only migrating
collections that have not yet been migrated. You should confirm all collections have been migrated
by running one last migration job, which should show all collections being skipped because they
have already been migrated.

Once you have completed the QDrant migrations so all collections are replicated & sharded, move
on to the standard upgrade process.


#### 7. Upgrade nginx with `deployNginx`

Recall from the Changes section above that nginx was updated in the new k8sdeploy version you are
now using, so you need to implement that change by running `deployNginx` with the command:

```
  ./gradlew -Pcluster=myvantiq-cluster deployNginx`
```

Monitor the `shared` pods while this runs, and you will see the new nginx pods replace the old
ones.

#### 8. Scale up the `vantiq` statefulset and monitor the upgrade process

Scale up the `vantiq` statefulset with the command:

```
  kubectl scale sts vantiq -n myvantiq --replicas=3
```

As the `vantiq-0` pod starts up, observe the R1.42 upgrade process as usual (watch the log of the
`load-model` init container as it runs to confirm the schema update worked, then watch the log of
the `vantiq` container to confirm it starts properly).

One schema change unique to R1.42 is the deletion of the obsolete `Situation` resource. If your
Vantiq installation has a large number of orgs and/or `Situation` resource collections, this could
cause the `load-model` init container to take longer than normal to run. We do not expect most
customers to experience a much longer runtime for the `load-model` init container, but if yours
is taking longer than usual then please give it the time it needs to complete.

Once the `vantiq` statefulset is up, scale up the `metrics-collector` statefulset with the command:

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=1
```

#### 9. Re-enable the `vantiq-worker` CronJob

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

Note that, as described in step 20 (observe connector pods restarting once the `vantiq-worker`
CronJob runs) in the [Vantiq Installation Upgrade Procedure](VantiqInstallationUpgradeProcedure.md)
doc, Vantiq-provided connectors such as GenAI flow connectors are managed by the `vantiq-worker`
(k8sworker) function in Vantiq, and they should restart once the `vantiq-worker` CronJob is
running again. This is expected, and you should watch such pods restart and make sure they return
to a `Running` state.

#### 10. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.
