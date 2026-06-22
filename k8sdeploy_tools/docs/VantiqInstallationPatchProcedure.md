# Vantiq Installation Patch Procedure

<span style="font-size:9pt;">Last updated 17 Jun 2025</span>

## Overview

Use this procedure to perform a patch version update (e.g. from `1.X.Y` to `1.X.{Y+1}`) of a Vantiq installation
with a release that will include minor feature improvements and/or bug fixes but will not modify the database
schema.

For Vantiq's own cloud installations, the main difference between this patch procedure and the one we use for
upgrades of Vantiq installations that are a minor version (`1.X.Y` to `1.{X+1}.0`) update is the notice period
to customers and the field – we don’t provide notification for patches. For private clouds, you will need to
determine your own notice periods for patches and upgrades.

This procedure does not require any downtime, since the primary vantiq statefulset pods are updated
automatically one at a time by Kubernetes via a "rolling restart", which leaves the remaining pods up.

Before reading this document, you should be familiar with the other docs in this repo starting with the main
[README.md](https://github.com/Vantiq/k8sdeploy_tools/) and especially the details of how to run tasks such as
`deployVantiq` documented in the [Installation doc](Installation.md).

Also make sure you understand the purpose of the three k8sdeploy repos (k8sdeploy_tools, k8sdeploy and
k8sdeploy_clusters) and the relationship/anchor between them as documented in the
[*How the Repos are Connected* section of the background reference doc](BackgroundReference.md#repo-connections).

Note: this procedure can also be used for clusters whose definitions are managed locally as described in
[Managing Cluster Definitions Locally](LocallyManagedDefinition.md) by simplifying the steps of the
[current Vantiq Ops workflow referenced below](VantiqManagedDefinition.md#git_workflow), doing only steps 2,
4-5 and 12-13. This is because it is recommended to still use Git locally in `k8sdeploy_tools/targetCluster`
to maintain the cluster branches even for temporary clusters. In such cases, simply make the changes directly
to the cluster branch that is local to your machine, skipping steps 1, 3 & 6-11).

---

## Notice Period 

### Development Installations 

No advance notice needed. However, for Vantiq's own cloud installations it is standard practice to send an
email to [Technical Team](mailto:technical@vantiq.com) at the beginning of the actual update process, and a
matching email when the update is complete.

### Production Installations 

No advance notice needed. However, for Vantiq's own cloud installations it is standard practice to send an
email to [Technical Team](mailto:technical@vantiq.com) at the beginning of the actual update process, and a
matching email when the update is complete.

---

## Prerequisites

Before starting this procedure, you will need the following:

1. A system that is properly configured with the tools you need, as documented in the
[Vantiq Kubernetes deployment tools (k8sdeploy_tools) bootstrap](k8sdeploy_toolsBootstrap.md) document.
2. A branch containing the cluster definition you will be updating, as documented in
[Configuring the Cluster Definition](Installation.md#configure_cluster_defn).
3. An account on the Vantiq installation being upgraded, with access to the `system` and `vantiq_monitor`
namespaces.

---

## Basic Workflow

The current Vantiq Ops workflow is defined in the
[Git Workflow section of the Vantiq Managed Definition doc](VantiqManagedDefinition.md#git_workflow).
It is used for the step-by-step process below.

If you use a different workflow, you will need to adjust the step-by-step process below to match.

---

## Patch Upgrade Process: Workflow + Commands Example - Step By Step

The workflow for this procedure and the commands to implement them are shown below, using the example of
`k8sdeploy_clusters` issue `#873` by `fred` to update the `dev` installation on the `prod-us` cluster to
patch release `1.42.5`. The matching issue branch `fred-produs-dev-#873` is created to contain the changes
for that issue, and changes to that branch result in PR `#874`. Once the PR is approved, the changes to the
`prod-us` cluster in the issue branch are merged into the cluster branch.

**Note**: in this example, the repo containing the cluster config is `k8sdeploy_clusters`. If you have a
private cloud with a different repo containing your cluster config branches that is anchored to your local
`targetCluster` directory, then you will need to substitute that repo for the `k8sdeploy_clusters` repo
described below. Likewise, if you are using a Git service other than GitHub you may need to adjust these
steps slightly.

1. Create a new GitHub issue describing the needed changes in `k8sdeploy_clusters`.

Create a new issue for the update in the `k8sdeploy_clusters` repo. Note the issue number for step 3.

In this example, the subject of the issue would be the typical *Update dev on prod-us to 1.42.5* and the
body can be left blank since the subject covers everything. In cases where there is more detail to the
needed changes, that can be put in the issue body.

2. Check out the cluster branch with `git checkout <clusterBranch>`.

Check out the cluster branch matching the cluster you are updating, in your local copy of
`k8sdeploy_clusters` that is anchored to the `targetCluster` directory, and do a `git pull` to make sure
your local copy is up to date:

```
  cd targetCluster
  git checkout prod-us
  git pull
```

3. Create an issue branch from the cluster branch with `git checkout -b <issueBranch>`.

Create an issue branch from the cluster branch for the issue from step 1. Typically the branch name has the
form `PERSON-PURPOSE-#ISSUENUM`, in this example the issue number was `#873` so we use the typical issue branch
name of `fred-produs-dev-#873`:

```
  (already in targetCluster in the prod-us branch from the previous step)
  git checkout -b fred-produs-dev-#873
```

Putting `#ISSUENUM` at the end of the branch name is a "helper" for GitHub that ensures the automation in
GitHub will link the branch to the issue.

4. Make needed changes to config files 

Edit config files (typically `deploy.yaml`, sometimes `cluster.properties`, rarely to other files) to make
the needed changes.

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
  Updating dev on prod-us to 1.42.5

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
should result in the GitHub UI saying that the changes can be merged cleanly and automatically.

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
  git pull
```

If you like, at this point you can examine the changed files to confirm they contain the expected changes.
If you do not plan to examine the changed files, you can skip steps 10 & 11 since the `deployVantiq` task will
do those steps too.

12. Update k8sdeploy_tools.

You should always use the current version of k8sdeploy_tools unless you are certain you need to use an older
version. Update to the current version with:

```
  cd ..    (up to k8sdeploy_tools)
  git checkout master
  git pull
```

13. Apply the changes to the cluster while monitoring the installation for proper operation.

To start the patch update process, apply the changes to the cluster with `deployVantiq` while monitoring the
installation for proper operation as described below in
[Monitoring An Installation For Proper Operation During & After An Update](#monitoring):

a. Prepare your monitoring windows as described below.

b. In shell window #1, apply the changes to the cluster:

```
  (already in k8sdeploy_tools from the previous step)
  ./gradlew -Pcluster=prod-us deployVantiq
```

c. Monitor the changes as described below.

---

<a name="monitoring"></a>
## Monitoring An Installation For Proper Operation During & After An Update

*Note on example commands:* `kubectl` accesses multiple clusters by using the context for a given cluster in
your `~/.kube/config`, specified by the `--context <CONTEXTNAME>` option. Standard practice in Vantiq Ops is
to follow the [*Best Practice for Managing Multiple Kubernetes Clusters* section of the *Vantiq Kubernetes
Cheat Sheet* doc](VantiqK8sCheatSheet.md#manage-mult-clusters), so for this example we are using the `kcus`
command which is an alias for `kubectl --context prod-us`.

### Prep: Web Browsers to Monitor Vantiq Via the UI

#### Open `system` namespace &rarr; Administer &rarr; Grafana &rarr; Vantiq Resources

In your primary web browser, log onto the Vantiq installation you are about to modify and switch to the
`system` namespace. Select `Grafana` from the `Administer` menu to start Grafana, then select the
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

### Prep: Additional Shell Windows for Monitoring Vantiq Pods

You should have three shell windows to fully monitor the patching process.

As noted above, in shell window #1 you will apply the changes to the cluster with `deployVantiq`.

In shell window #2, begin monitoring the status of all pods in the cluster (including the Vantiq pods in
the installation namespace) with:

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

### Apply Changes While Monitoring for Proper Operation

Apply the change to the cluster (step 13 above).

You will immediately see the pods in each Vantiq statefulset terminate and a matching new pod start, one
by one, starting with the highest-numbered pod N and going down to pod 0 last.

1. Run the log output command in window #3 as shown above when you see the `Running` state of `0/1` (0
containers ready out of 1) for the pod status in window #2. Watch the log output, when you see the usual boot
completion message `Succeeded in deploying verticle` the pod is running. About 30 seconds later the
readinessProbe for the pod should succeed and you should see the status for the pod in window #2 change to a
`Running`state of `1/1`, and Kubernetes will terminate the next statefulset member. At this point you can
ctrl-c your current window #3 `logs -f` command and get ready to run the next one.

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

If the update procedure fails or there is any question as to whether the new release is running correctly,
roll back to the previous release (`1.X.Y`).

Simply repeat steps 4 and 13 of the update process, but in step 4 change the image version back to `1.X.Y`
before repeating step 13.

---

## Restarting (AKA Rolling) the Vantiq Pods Without Updating

Sometimes the Vantiq pods need to be restarted to resolve an installation health issue or for some other reason,
without updating the Vantiq version. The `kubectl rollout restart` command should be used for this purpose.

Using the above example of the `dev` installation on the `prod-us` cluster which uses the `kcus` alias for
`kubectl`, the command to do a rolling restart of the `vantiq` statefulset would be:

```
  kcus rollout restart sts vantiq -n dev
```

During the restart process, you should follow the
[Monitoring An Installation For Proper Operation During & After An Update](#monitoring) process above, as
follows:

1. Perform the prep steps to get your monitoring windows ready.

2. Run the `kubectl rollout restart` command to initiate the statefulset restart.

3. Monitor the installation for proper operation as each pod restarts.

Please see the
[*Useful Basic `kubectl` Commands* section of the *Vantiq Kubernetes Cheat Sheet* doc](VantiqK8sCheatSheet.md#kubectl_cmds)
for details on `kubectl rollout restart` vs. `kubectl delete pod` for restarting pods.