# Vantiq R1.43 Upgrade Instructions:

# Run QDrant Migration Tool to Update QDrant Collections to R1.43 Schema

## Overview

Vantiq R1.43 makes a change to the QDrant schema Vantiq uses, which requires additional upgrade steps
(see below).

The extra steps for R1.43 upgrades of private clouds are detailed in this document. Please follow these
additional instructions as part of the R1.43 upgrade process (along with the standard upgrade instructions)
to ensure the upgrade is done properly.

### Changes for R1.43

R1.42 requires k8sdeploy v3.17.5 which updates the QDrant migration tool which automates the update of
QDrant collections to the schema which Vantiq uses in R1.43.

&nbsp;

## Additional Steps for the R1.42 &rarr; R1.43 upgrade process

*Note*: in the example below, the cluster branch name is `myvantiq-cluster` and the 
installation name is `myvantiq`, you will need to change these to the actual names you
are upgrading.

As noted above, in addition to the normal upgrade steps, the R1.42 &rarr; R1.43 upgrade process
requires the extra step of running the current QDrant migration tool. To do this extra step, first
do the prep steps and once you are ready to upgrade then do the upgrade steps.

### Prep Steps

The following prep steps should be done shortly before doing the actual upgrade. None of them should
require downtime, so they can be done while the installation is still running.

Note that these prep steps are not extra steps, they are the standard upgrade prep steps.

#### 1. Update `vantiq_system_release` in `cluster.properties` to `3.17.5` or Later

R1.43 requires a minimum `3.17.5` k8sdeploy release. As of this writing (1 Dec 2025) this is
also the latest release. When in doubt, consult the
[*k8sdeploy* release map reference](https://github.com/Vantiq/k8sdeploy/blob/master/ReleaseMap.md).
Change the `vantiq_system_release` value in your `cluster.properties` file to the desired k8sdeploy
release, so it will be ready to apply with `deployVantiq` at upgrade time.

#### 2. Update `deploy.yaml` to R1.43 Values

As with any upgrade, you must update the vantiq image tag `vantiq.installations.myvantiq.image.tag`
to the desired R1.43 value, `1.43.X` where `X` is the desired patch release (currently `1.43.8`).


#### 3. Commit the changes in your `targetCluster` cluster branch.

Commit the updated `cluster.properties` and `deploy.yaml` in your `targetCluster` cluster
branch, then push the changes to your remote cluster repository.

&nbsp;

### Upgrade Steps Summary/Checklist

This is a summary of the upgrade steps, which can be used as checklist (these steps are detailed
below):

  1. Disable the `vantiq-worker` CronJob
  2. Scale down `vantiq` and `metrics-collector` statefulsets
  3. Upgrade Vantiq (and related components) with `deployVantiq`
  4. Once again scale down `vantiq` and `metrics-collector` statefulsets
  5. Run the QDrant migration job to update the QDrant schema
  6. Scale up the `vantiq` statefulset and monitor the upgrade process
  7. Re-enable the `vantiq-worker` CronJob
  8. Confirm proper operation of the installation (standard upgrade process)

Note that only upgrade steps 4 & 5 are extra steps, the other steps are the standard upgrade steps.

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

**Note**: this will start to scale up the `vantiq` and `metrics-collector` statefulsets.
You should immediately scale them down (repeat step 2) as noted in step 4, so you can
run step 5 without Vantiq running.

#### 4. Immediately, again scale down `vantiq` and `metrics-collector` statefulsets

Step 3 will start to scale up the `vantiq` and `metrics-collector` statefulsets. You should
immediately scale them down (repeat step 2) to defer the Vantiq part of the upgrade until step
6, to allow the QDrant migration (step 5) to proceed without Vantiq trying to modify the
collections during the migration.

#### 5. Run the QDrant Migration Job

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

Once you have completed the QDrant migrations so collections are updated, move on to the remaining
steps which are the rest of the standard upgrade process.

#### 6. Scale up the `vantiq` statefulset and monitor the upgrade process

Scale up the `vantiq` statefulset with the command:

```
  kubectl scale sts vantiq -n myvantiq --replicas=3
```

As the `vantiq-0` pod starts up, observe the R1.43 upgrade process as usual (watch the log of the
`load-model` init container as it runs to confirm the schema update worked, then watch the log of
the `vantiq` container to confirm it starts properly).

Once the `vantiq` statefulset is up, scale up the `metrics-collector` statefulset with the command:

```
  kubectl scale sts metrics-collector -n myvantiq --replicas=1
```

#### 7. Re-enable the `vantiq-worker` CronJob

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

#### 8. Confirm proper operation of the installation

Confirm proper operation of the installation as usual by checking the system dashboards in the
Vantiq web UI.

This is the standard upgrade "proper operation" confirmation.
