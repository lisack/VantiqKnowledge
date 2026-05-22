# Vantiq Installation Upgrade Procedure

<span style="font-size:9pt;">Last updated 17 Jun 2025</span>


## Overview

Use this procedure to perform a minor version upgrade (e.g. from `1.X.Y` to `1.{X+1}.0`) of a Vantiq
installation. The new release may include major feature improvements and/or bug fixes, and most importantly
will modify the database schema and therefore require a full scale-down then scale-up which involves downtime.

It is anticipated that this procedure will be identical when performing a major version upgrade (e.g. from
`1.X.Y` to `2.0.0`), but no major version changes have yet happened.

For Vantiq's own cloud installations, the main difference between this procedure and the one we use for patch
updates of Vantiq installations that are a patch version (`1.X.Y` to `1.X.{Y+1}`) update is the notice period
to customers and the field – we don’t provide notification for patches, but we do provide notice for these
since they involve at least minor downtime. For private clouds, you will need to determine your own notice
periods for patches and upgrades.

Before reading this document, you should be familiar with the other docs in this repo starting with the main
[README.md](https://github.com/Vantiq/k8sdeploy_tools/) and especially the details of how to run tasks such as
`deployVantiq` documented in the [Installation doc](Installation.md).

Also make sure you understand the purpose of the three k8sdeploy repos (k8sdeploy_tools, k8sdeploy and
k8sdeploy_clusters) and the relationship/anchor between them as documented in the
[*How the Repos are Connected* section of the background reference doc](BackgroundReference.md#repo-connections).

Note: this procedure can also be used for clusters whose definitions are managed locally as described in
[Managing Cluster Definitions Locally](LocallyManagedDefinition.md) by simplifying the steps of the
[current Vantiq Ops workflow referenced below](VantiqManagedDefinition.md#git_workflow), doing only steps 2,
4-5 and 12-20. This is because it is recommended to still use Git locally in `k8sdeploy_tools/targetCluster`
to maintain the cluster branches even for temporary clusters. In such cases, simply make the changes directly
to the cluster branch that is local to your machine, skipping steps 1, 3 & 6-11).

---

## Notice Period 

Minor and Major upgrades will need to be scheduled and announced, since they may involve downtime to apply
database schema changes or infrastructure work (unlike patch updates, which typically involve only a "rolling
restart" of the vantiq pods with little or no downtime).

As of this writing, the announcements follow the format of documents like
[R1.42 Rollout VANTIQ Ops Announcement.docx](https://vantiq.sharepoint.com/:w:/g/EQNzQbfwenZPrukAlSzfTDIBzVqTShlFkSToPqcqmYa-yg?e=5e58gV).

### Development Installations

For Vantiq's own cloud installations, customers should be notified at least two weeks in advance of the
upgrade via the standard Operations Announcements communication channels.

It is also standard practice to send an email to [Technical Team](mailto:technical@vantiq.com) at the
beginning of the actual upgrade process, and a matching email when the upgrade is complete.

### Production Installations

For Vantiq's own cloud installations, customers should be notified at least six weeks in advance of the
upgrade via the standard Operations Announcements communication channels. This gives the customer enough
time to prepare and to test their production applications on a dev installation before the apps need to be
ready for the new release.

It is also standard practice to send an email to [Technical Team](mailto:technical@vantiq.com) at the
beginning of the actual upgrade process, and a matching email when the upgrade is complete.

---

## Prerequisites

Before starting this procedure, you will need the following:

1. A system that is properly configured with the tools you need, as documented in the
[Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](k8sdeploy_toolsBootstrap.md) document.
2. A branch containing the cluster definition you will be updating, as documented in
[Configuring the Cluster Definition](Installation.md#configure_cluster_defn).
3. An account on the Vantiq installation being upgraded, with access to the `system` and `vantiq_monitor`
namespaces.

## Basic Workflow

The current Vantiq Ops workflow is defined in the
[Git Workflow section of the Vantiq Managed Definition doc](VantiqManagedDefinition.md#git_workflow).
It is used for the step-by-step process below.

If you use a different workflow, you will need to adjust the step-by-step process below to match.

*Note on example kubectl commands:* `kubectl` accesses multiple clusters by using the context for a given
cluster in your `~/.kube/config`, specified by the `--context <CONTEXTNAME>` option. Standard practice in
Vantiq Ops is to follow the [*Best Practice for Managing Multiple Kubernetes Clusters* section of the
*Vantiq Kubernetes Cheat Sheet* doc](VantiqK8sCheatSheet.md#manage-mult-clusters), so for this example we
are using the `kcus` command which is an alias for `kubectl --context prod-us`.

The workflow for this procedure consists of prep steps 1-11, and upgrade steps 12-19:

1. Create a new issue for the update and matching issue branch for the issue.
2. Check out the cluster branch.
3. Create an issue branch from the cluster branch.
4. Make needed changes to config files in your issue branch.
5. Commit the changes to config files in your issue branch.
6. Push the issue branch changes (commit) up to GitHub.
7. Generate a PR (pull request) for the pushed issue branch.
8. Get approval for the PR.
9. Squash-merge the issue branch into the cluster branch.
10. Switch to the cluster branch.
11. Update the cluster branch to get changes that were just merged in from the issue branch.
12. Disable the `vantiq-worker` CronJob.
13. Scale down all three Vantiq statefulsets to 0 (**the downtime clock is now ticking**).
14. Run a backup of MongoDB.
15. Update k8sdeploy_tools.
16. Apply the changes with `deployVantiq` while monitoring the installation for proper operation.
17. Scale up the remaining statefulsets while monitoring the installation for proper operation.
18. Verify proper load balancer operation, and the load balancer instance status in the cloud provider console or CLI.
19. Re-enable the `vantiq-worker` CronJob
20. Observe connector pods restarting once the `vantiq-worker` CronJob runs
21. Update the Availability Monitoring data to indicate the downtime was scheduled.

---

## Major or Minor Version Upgrade Process: Workflow + Commands Example - Step By Step

The workflow for this procedure and the commands to implement them are shown below, using the example of
`k8sdeploy_clusters` issue `#942` by `fred` to update the `dev` installation on the `prod-us` cluster to
patch release `1.42.0`. The matching issue branch `fred-produs-dev-#942` is created to contain the changes
for that issue, and changes to that branch result in PR `#943`. Once the PR is approved, the changes to the
`prod-us` cluster in the issue branch are merged into the cluster branch.

**Note**: in this example, the repo containing the cluster config is `k8sdeploy_clusters`. If you have a
private cloud with a different repo containing your cluster config branches that is anchored to your local
`targetCluster` directory, then you will need to substitute that repo for the `k8sdeploy_clusters` repo
described below. Likewise, if you are using a Git service other than GitHub you may need to adjust these
steps slightly.

1. Create a new GitHub issue describing the needed changes in `k8sdeploy_clusters`.

Create a new issue for the update in the `k8sdeploy_clusters` repo. Note the issue number for step 3.

In this example, the subject of the issue would be the typical *Upgrade dev on prod-us to 1.42.0* and the
body can be left blank since the subject covers everything. In cases where there is more detail to the
needed changes, that can be put in the issue body.

2. Check out the cluster branch with `git checkout <clusterBranch>`.

Check out the cluster branch matching the cluster you are updating, in your local copy of
`k8sdeploy_clusters` that is anchored to the `targetCluster` directory:

```
  cd targetCluster
  git checkout prod-us
```

3. Create an issue branch from the cluster branch with `git checkout -b <issueBranch>`.

Create an issue branch from the cluster branch for the issue from step 1. Typically the branch name has the
form `PERSON-PURPOSE-#ISSUENUM`, in this example the issue number was `#873` so we use the typical issue branch
name of `fred-produs-dev-#873`:

```
  (already in targetCluster in the prod-us branch from the previous step)
  git checkout -b fred-produs-dev-#873
```

*Note*: putting `#ISSUENUM` at the end of the branch name is a "helper" for GitHub that ensures the automation
in GitHub will link the branch to the issue.

4. Make needed changes to config files 

Edit config files (typically `deploy.yaml`, sometimes `cluster.properties`, rarely other files) to make the
needed changes.

5. Stage the changed file(s) for commit with `git add`, then commit the changes with `git commit`.

In your local copy of the issue branch, stage the changed file(s) for commit with `git add`, then commit the
changes with `git commit`. In this example we will only modify and commit `deploy.yaml`:

```
  (still in targetCluster in the fred-produs-dev-#873 issue branch from the previous steps)
  git add deploy.yaml
  git commit
```

The `git commit` command will put you into the editor to create the commit message. The typical commit
message for a change like this is:

```
  Updating dev on prod-us to 1.42.0

  Closes #873
```

The last line of the commit message is a "helper" for GitHub that ensures the automation in GitHub
will link the commit to the issue.

6. Push the contents of the issue branch up to GitHub with `git push -u origin <issueBranch>`.

Push the issue branch changes (commit) up to GitHub. Usually the issue branch only exists locally on your
machine at this point, so the `git push` will both create the issue branch on GitHub and push the content of
the branch to GitHub with a single command:

```
  git push -u origin fred-produs-dev-#873
```

7. Create a PR (pull request) on GitHub from the newly pushed issue branch.

Once the issue branch is pushed, generate a PR (pull request) for it:

- You should see a "PR helper" button in the Github UI as soon as you push the branch up, which can be used
to create the PR.
- In the PR, choose the cluster branch (not `master`, which is the default) as the branch into which you are
merging your issue branch. This will designate the issue branch as a sub-branch of the cluster branch, and
should result in the GitHub UI saying that the changes can be merged automatically.

In this example, `prod-us` is designated as the branch that `fred-produs-dev-#873` is being merged into, and
the PR created is `#874`.

8. Get approval for the PR on GitHub, making additional changes if needed.

Have someone review the PR, and either approve it or note additional changes which need to be made (which
will require repeating steps 4-6). Iterate this step until the PR is approved.

9. Squash-merge the issue branch into the cluster branch on GitHub.

Assuming the changes in the issue branch can cleanly merge into the cluster branch, do a squash-merge of the
`fred-produs-dev-#873` issue branch into the `prod-us` cluster branch on GitHub once the PR is approved.

Once that is done, you will normally want to "clean up" by deleting the issue branch on GitHub.

If GitHub cannot cleanly merge the changes in the issue branch into the cluster branch, you will need to run
`git merge` locally on your issue branch with the cluster branch and resolve any conflicts, then push the
result back to Github.

```
  git checkout prod-us
  git merge fred-produs-dev-#873    # this will put you into the editor where you will resolve any conflicts
  git push -u origin prod-us
```

10. Switch to the cluster branch with `git checkout <clusterBranch>`.

Switch to the cluster branch in your `targetCluster` directory:

```
  git checkout prod-us
```

11. Update the cluster branch to get changes that were just merged in from the issue branch

Update the `prod-us` cluster branch in your `targetCluster` directory with `git pull` to pull down the changes
that were just merged into it on GitHub from the issue branch.

```
  (still in targetCluster in the prod-us branch from the previous step)
  git pull
```

If you like, at this point you can examine the changed files to confirm they contain the expected changes.

12. Disable the `vantiq-worker` CronJob

Edit the `vantiq-worker` CronJob in the installation being upgraded, so the `vantiq-worker` pods
won't keep trying to contact Vantiq while it's down. To do this, edit the CronJob with

```
  kcus edit cronjob vantiq-worker -n dev
```

and at the bottom change

```
  suspend: false
```
to

```
  suspend: true
```

13. Scale down all the Vantiq statefulsets to 0.

*Note: the upgrade procedure requires this step of scaling all Vantiq statefulsets down to 0 to provide total
Vantiq server quiescence (i.e. system downtime) to ensure that the MongoDB database is not being updated while
the backup is done in the next step.*

Prior to running mongodump, note the number of running pods for each of the Vantiq statefulsets (`vantiq`,
`metrics-collector` and any others such as Isolated Org Compute or `vision-analytics`), then scale all of
them down to 0.

```
  kcus get pods -n dev
  kcus scale sts vantiq -n dev --replicas=0
  kcus scale sts metrics-collector -n dev --replicas=0
  kcus scale sts vision-analytics -n dev --replicas=0
```

The Vantiq installation will be down at this point, so **the downtime clock is now ticking.**

14. Run a backup of MongoDB.

Run a backup of MongoDB by creating a new Job from the `mongobackup` CronJob. Monitor the backup job while
it runs.

```
  kcus create job --from=CronJob/mongobackup -n dev
  kcus get job -n dev
  kcus logs MONGODUMPJOBPOD -n dev -f
```

This backup is for upgrade disaster recovery protection (in case something bad happens during the run of the
`load-model` init container of `vantiq-0` in the next step) and you have to restore from the backup to
recover the installation. Normally this backup will not be needed.

**Pro tip**: this is typically the longest part of the upgrade downtime. In order to properly estimate the
length of the downtime, check the runtime of your `mongobackup` pods that have been doing the normal backups.
You can also start the backup ahead of the upgrade scale-down, if you are comfortable with the upgrade
backup being the same as a DR backup (losing the small amount of data changed while the backup is running).
If you do run the backup ahead of time, you can use the estimate to start the backup at a time where it
should finish right when you want to scale down the the `vantiq` statefulset.

15. Update k8sdeploy_tools.

You should always use the current version of k8sdeploy_tools unless you are certain you need to use an older
version. Update to the current version with:

```
  cd ..    (up to k8sdeploy_tools)
  git checkout master
  git pull
```

16. Apply the changes with `deployVantiq` while monitoring the installation for proper operation.

To start the upgrade process, apply the changes to the cluster with `deployVantiq` which will scale up the
`vantiq`, `metrics-collector` statefulsets (and the `vision-analytics` statefulset if used). Allow the
`vantiq` statefulset to scale up, but scale down the `metrics-collector` and `vision-analytics` statefulsets
until the `vantiq-0` pod has completed running the `load-model` init container and the other `vantiq`
pods have scaled up. As all pods scale up, you should monitoring the installation for proper operation as
described below in
[Monitoring An Installation For Proper Operation During & After An Update](#monitoring):

a. Prepare your monitoring windows as described below.

b. In shell window #1, apply the changes to the cluster:

```
  (already in k8sdeploy_tools from the previous step)
  ./gradlew -Pcluster=prod-us deployVantiq
```

c. Scale down the `metrics-collector` statefulset (and the `vision-analytics` statefulset if used)

You should scale down the `metrics-collector` and `vision-analytics` statefulsets while the the `vantiq-0`
pod starts up:

```
  kcus scale metrics-collector -n dev --replicas=0
  kcus scale vision-analytics -n dev --replicas=0
```

d. Monitor the run of the `load-model` init container of the `vantiq-0` pod as described below.

Before moving on to the standard monitoring of the installation pod startups as described below, you must
first the monitor the progress of the `load-model` init container (the third and final one) of the `vantiq-0`
pod. Depending on the extent of schema changes in the new release, the `load-model` container may run quickly
or it may run for a substantial amount of time. Monitor the progress of the `load-model` container (in your
shell window #3 as described below) with:

```
  kcus logs vantiq-0 -n dev -c load-model -f
```

Once the `load-model` container of the `vantiq-0` pod completes, the `vantiq` container should start normally
and you can follow the standard pod startup monitoring process below.

**At this point, the downtime clock has stopped ticking.**

Once the `vantiq-0` pod is fully up and running properly, the Vantiq installation should be up and usable.
The `vantiq` statefulset should continue to scale up to the number of pods defined in the configuration
(typically 3), and you should monitor each pod as it starts using the process described below.

17. Scale up the remaining statefulsets while monitoring the installation for proper operation.

the `metrics-collector` statefulset (and the `vision-analytics` statefulset if used)

```
  kcus scale metrics-collector -n dev --replicas=1
  kcus scale vision-analytics -n dev --replicas=2
```

18. Verify proper load balancer operation, and the load balancer instance status in the cloud provider console or CLI.

First, verify proper load balancer operation with the command

```
  curl -H "Authorization: Bearer MYTOKEN" https://api.vantiq.com/api/v1/_status python -m json.tool | egrep '"host":|memberId' -A 1
```

where MYTOKEN is a long-lived access token you created in the `system` namespace.

Run this command multiple times. You should see that the load balancer cycles through each of the Vantiq
server pods, and that the other servers have the status `started` (not `starting`). If a pod is totally down,
it will not be in the output at all. The host entry should have 1 peer if 2 pods are up, 2 peers if 3 pods are
up and so on. With 3 Vantiq pods and 1 metrics-collector pod, there are 4 pods total so there should be 3 peers.

Next, verify proper load balancer status and functioning using kubectl and the cloud provider console or CLI.

For example, on AWS this can be done by comparing the health of the load balancer instances with the list of
nodes running the nginx controller pods, using kubectl and the AWS CLI.

Determine which nodes are running nginx ingress controller pods (there should be 3):

```
  kcus get pod -n shared -o wide | grep nginx
```

Get the load balancer name, then determine which load balancer instances are healthy (State = InService) and
then get their hostnames. In AWS this is done with AWS CLI commands:

```
  aws elb describe-load-balancers | grep LoadBalancerName
  aws elb describe-instance-health --load-balancer-name LBNAMEFROMPREVCMD | grep -B 1 InService
  aws ec2 describe-instances --instance-ids ID1FROMPREVCMD ID2FROMPREVCMD ID3FROMPREVCMD --query "Reservations[*].Instances[*].[PrivateDnsName,InstanceId]"
```

Compare the hostnames from the kubectl command that show running nginx controller pods with the hostnames
from the final AWS CLI command. The two hostname lists should match. If there is a mismatch or there are not
three nginx ingress controller pods, determine why and fix any problems.

Note that if the installation is not in the account & region pointed to by your default profile, you will
need to add `--profile PROFILENAME` to the above `aws` commands.

Other cloud providers should have similar CLI commands to output the details of a load balancer to perform
this check. The AWS example is provided here only for convenience.

19. Re-enable the `vantiq-worker` CronJob

Edit the `vantiq-worker` CronJob in the installation being upgraded, to re-enable it. First edit the
CronJob with

```
  kcus edit cronjob vantiq-worker -n dev
```

and at the bottom change

```
  suspend: true
```
to

```
  suspend: false
```

20. Observe connector pods restarting once the `vantiq-worker` CronJob runs

Vantiq-provided connectors such as GenAI flow connectors are managed by the `vantiq-worker` (k8sworker)
function in Vantiq, and their versions must stay in sync with the Vantiq version. As a result, you
should observe such connector pods restarting once the `vantiq-worker` CronJob is running again. This
is expected, and you should watch such pods restart and make sure they return to a `Running` state.

To ensure proper operation of these connectors, you can exercise the part of Vantiq that uses them.
A few examples:

  - To confirm the AI Assistant pod is working, use the AI help function (`Help` &rarr; `AI
Documentation Search`)
  - To confirm the GenAI GenAI flow connector for an org is working, use the `GenAI Builder` in a
namespace in that org.

21. Update the Availability Monitoring data to indicate the downtime was scheduled. 

Update the Availability Monitoring data to indicate the downtime was scheduled and keep our uptime stats
accurate. That data is kept in the `vantiq_monitor` namespace on `api.vantiq.com`.

- Log onto `api.vantiq.com` and open `vantiq_monitor` namespace &rarr; `Monitor` project
- Select `Show` &rarr; `Find Records` and query the `Availability` type
- Select `Edit` from the `...` menu on the right for the record for this downtime to edit it
- Select `True` in the `scheduled` dropdown and click `Update Record` to save

*Note*: this step only applies to the Vantiq Ops team, for Vantiq public clouds and Vantiq-managed
private clouds. If you are running a customer-managed private cloud, you may have your own availability
monitor (if so, you will need to update your availability data in a similar way).

---

<a name="monitoring"></a>
## Monitoring An Installation For Proper Operation During & After An Update

*Note on example commands:* as noted above, `kubectl` accesses multiple clusters by using the context for a
given cluster in your `~/.kube/config`, specified by the `--context <CONTEXTNAME>` option. Standard practice
in Vantiq Ops is to follow the [*Best Practice for Managing Multiple Kubernetes Clusters* section of the
*Vantiq Kubernetes Cheat Sheet* doc](VantiqK8sCheatSheet.md#manage-mult-clusters), so for this example we
are using the `kcus` command which is an alias for `kubectl --context prod-us`.


### Prep: Additional Shell Windows for Monitoring Vantiq Pods

You should have three shell windows to fully monitor the patching process.

As noted above, in shell window #1 you will apply the changes to the cluster with `deployVantiq`.

In shell window #2, begin monitoring the status of all pods in the cluster (including the `vantiq` pods
in the installation namespace) with:

```
  kcus get pod -n dev -w
```

In shell window #3, get ready to watch the logs of the vantiq pods as they start. You should run each of
these when you see in shell window #2 that the pod in question has completed its init containers and is
starting the main container, indicated by the status of the pod changing to `PodInitializing` and then
`Running`. At that point you can run the command which matches the pod you wish to monitor:

```
  kcus logs metrics-collector-0 -n dev -f
  kcus logs vantiq-2 -n dev -c vantiq -f
  kcus logs vantiq-1 -n dev -c vantiq -f
  kcus logs vantiq-0 -n dev -c vantiq -f
```

### As Soon As Possible: Web Browsers to Monitor Vantiq Via the UI

#### Open `system` namespace &rarr; Administer &rarr; Grafana &rarr; Vantiq Resources

In your primary web browser, as soon as the `vantiq-0` pod is up log onto the Vantiq installation and switch
to the `system` namespace. Select `Grafana` from the `Administer` menu to start Grafana, then select the
`Vantiq Resources` dashboard.

#### Open `vantiq_monitor` namespace &rarr; TimerTest project

In a separate web browser (or a private window in the same browser), log onto the same Vantiq installation
and switch to the `vantiq_monitor` namespace, then open the `TimerTest` project.

Turn on the `on_quicktest` rule and save it.

Monitor the `Log Messages` output in the `Log Messages` pane. You should see one `QUICKTEST WAS HERE`
message per second at almost all times (some may get dropped as the Vantiq pods restart). If you see a lot of
messages missing, there is a problem which you should diagnose.

Note: if you have not yet imported the *TimerTest* and *Heartbeat* projects into the `vantiq_monitor`
namespace, they can be imported from the `vantiqApps` directory. Details about these apps can be found in
INSERT REF

### Apply Changes While Monitoring for Proper Operation

Apply the change to the cluster (step 16 above).

You will immediately see the pods in the `vantiq` statefulset start, one by one, starting with `vantiq-0`
and going up to the highest-numbered pod last.

**Note:** remember from above for the `vantiq-0` pod you must first montitor the progress of the `load-model`
init container (the third and final one) with the command:

```
  kcus logs vantiq-0 -n dev -c load-model -f
```

Once the `load-model` container of the `vantiq-0` pod completes, you can then move on to monitoring the main
`vantiq` container of each `vantiq` pod as described here.

1. Run the log output command in window #3 as shown above when you see the `Running` state of `0/1` (0
containers ready out of 1) for the pod status in window #2. Watch the log output, when you see the usual boot
completion message `Succeeded in deploying verticle` the pod is running. About 30 seconds later the
readinessProbe for the pod should succeed and you should see the status for the pod in window #2 change to a
`Running`state of `1/1`, and Kubernetes will start the next statefulset member. At this point you can ctrl-c
your current window #3 `logs -f` command and get ready to run the next one.

2. In parallel with observing the pod states and log output, observe both your web browser windows (the
`Vantiq Resources` Grafana dashboard and `TimerTest` application) to confirm you are seeing normal behavior.
Note that normal behavior for the `CPU Utilization` pane in the `Vantiq Resources` Grafana dashboard is that
the pod will use most of the available CPU during startup (for example, nearly 400% on a 4-vCPU pod). It
should then drop back to pre-restart levels after the CPU-intensive startup and post-startup phases, which
can take up to 5 minutes.

After all pods have restarted, you should look through other Grafana system dashboards such as
`Metric Collection Resources` and `MongoDB Monitoring Dashboard` to look for abnormal behavior.

### Cleanup: Stop TimerTest and Clear Logs

Once you are all done, clean up after yourself by first turning off the `on_quicktest` rule in TimerTest,
then clearing the log data in the `Log Messages` pane.

---

## Rollback Procedure

As of this writing, there is not a true rollback procedure for a major or minor version upgrade, since it
includes database schema changes. If something went wrong with the upgrade that requires a rollback, the
backup from step 13 must be used to restore the MongoDB database to its pre-upgrade state as would be done
in a DR situation. Follow the process in
[Vantiq Disaster Recovery Procedure](VantiqDisasterRecoveryProcedure.md) to roll back the installation to
the pre-upgrade state.

In short, the process is:

1. Scale down all Vantiq statefulsets to 0.
2. Restore MongoDB to its pre-upgrade state using the backup file from upgrade step 10.
3. Roll back the Vantiq image to the previous version in the cluster config (in deploy.yaml).
4. Repeat upgrade steps 15-20.
