# Centrally Managing Cluster Definitions by Vantiq

## Overview

This scenario describes how the Vantiq Ops team manages the cluster definitions for our public clouds, and for
all Vantiq-managed private clouds (PC-VMs) where Vantiq Ops is the sole maintainer of the cluster definition.
Each cluster definition is kept in its own branch in Vantiq's *k8sdeploy_clusters* Git repo.

The *k8sdeploy_clusters* repo is used by default because it is the value of the `clusterRepo` property in the tools.
If there is a different repo used for specific clusters (such as PC-VMs), the `clusterRepo` property must be
changed from the default for those clusters. This can be done via the command line by adding
`-PclusterRepo=<uri>` to every command. It can also be set globally using a `gradle.properties` file on the
deployment machine, but that will likely not be desired since
`‑PclusterRepo=https://github.com/Vantiq/k8sdeploy_clusters` would then need to be added to every command that was
using the normal Vantiq cluster definitions repo. The simplest approach would be to have an alternate copy of
*k8sdeploy_tools* with the `targetCluster` directory homed to a different repo, as described at the end of the
next section.

Each cluster definition contains the configuration definition for one or more Vantiq installations running on
that cluster, and the other installation components (Keycloak, Nginx & Grafana/InfluxDB) that are shared by those
Vantiq installations.


## Initial Bootstrap

If you are setting up a new deployment machine, these one-time bootstrap commands must be run to set up your
*k8sdeploy_tools* directory (a clone of this repo) and the *k8sdeploy_clusters* repo as the `targetCluster`
directory in *k8sdeploy_tools*:

```
git clone https://github.com/Vantiq/k8sdeploy_tools
cd k8sdeploy_tools
git clone https://github.com/Vantiq/k8sdeploy_clusters targetCluster
```

To bootstrap an alternate copy of *k8sdeploy_tools* with the `targetCluster` directory homed to a different
repo, repeat the above commands in a different directory and change the URI for `targetCluster` to match the
alternate cluster definitions repo.

<a name="new_cluster"></a>
## Creating a New Cluster Definition

To create a new cluster definition branch for a new cluster, do the following:

1) Change directory into the `targetCluster` sub-directory.
1) (Optional, but recommended if possible) Run the command `git checkout <protoclusterName>` where
`<protoclusterName>` is an existing cluster you wish to use as a starting point.
1) Run the command `git checkout -b <clusterName>` where `<clusterName>` is the name of the new cluster
definition branch you wish to create.
1) Run the command `git push -u origin` to push the new branch up to the cluster definitions repo.
1) Change directory back to the `k8sdeploy_tools` directory (which should be the immediate parent directory at
this point).
 
For Vantiq-managed clusters, we normally follow the best practice of naming the cluster branch the same as
the K8s cluster name, although that is not required. Whatever is chosen for the cluster branch name (e.g.
`foo`) will need to be used for the <code>&#8209;Pcluster=</code> arg (e.g. `-Pcluster=foo`).

<a name="git_workflow"></a>
## Vantiq Ops Git Workflow to Manage Changes

Git and its workflows are central to managing changes to the cluster definitions. If you are unfamiliar with
Git then you will want to gain a basic working knowledge in order to use the tools correctly.

To manage changes to the cluster definitions effectively, you should standardize on the same Git workflow
for your whole team. The workflow used by Vantiq Ops is:

1. Create a new GitHub issue for the changes. Note the issue number.
1. Check out the cluster branch with `git checkout <clusterBranch>`.
1. Create an issue branch from the cluster branch with `git checkout -b <issueBranch>` following the issue branch naming convention below.
1. Make the needed changes to config files you are planning to deploy.
1. Stage the changed file(s) for commit with `git add`, then commit the changes with `git commit`.
1. Push the changes in the issue branch up to GitHub with `git push -u origin <issueBranch>`.
1. Create a PR (pull request) from the newly pushed issue branch. If you visit the `Pull requests` tab on
GitHub right after pushing up the issue branch, you should see a link for the branch which will create the PR
with some items pre-filled. Make sure to select the cluster branch as the branch the PR will be merged into,
which should allow a simple squash-merge without additional steps.
1. Have someone review the PR, and approve it or note additional changes which need to be made (repeating
steps 4-6). Iterate this step until the PR is approved.
1. Squash-merge the PR into the cluster branch.
1. Check out the cluster branch with `git checkout <clusterBranch>`.
1. Pull down the newly merged changes to the cluster branch with `git pull` in the `targetCluster` directory.
1. Update k8sdeploy_tools with `git pull` in the `k8sdeploy_tools` root directory.
1. Apply the changes to the cluster while monitoring the installation for proper operation.

Note that steps 2-6 and 10-13 are run locally on your machine, and steps 1 and 7-9 are done in the GitHub
web UI.

Issue branch naming convention in step 3: in step 1 you noted the issue number. The issue branch is normally
named `<user>-<purpose>-#<issuenum>`. For example, the issue branch created by `fred` for issue `#782` to
update the Keycloak password would be named something like `fred-kcpassword-#782`. If the cluster definition
repo is in Github, the `#782` part of the branch name will cause Github to auto-connect the issue branch to
that issue and update its status when changes are made to the issue branch.

**Pro Tip**: it is always safe to run `git status` to confirm the result of commands like `git add` and to
confirm you have checked out the correct branch (it's only an informational command that makes no changes).

Note: this procedure can also be used for clusters whose definitions are managed locally as described in
[Managing Cluster Definitions Locally](LocallyManagedDefinition.md) by simplifying the steps of the Basic
Workflow above, doing only steps 2, 4-5 and 12-13. This is because it is recommended to still use Git
locally in `k8sdeploy_tools/targetCluster` to maintain the cluster branches even for temporary clusters. In
such cases, simply make the changes directly to the cluster branch that is local to your machine, skipping
steps 1, 3 & 6-11).

*Future note*: if/once we implement a Vantiq Controller which will implement automatic updates triggered by
changes to a cluster branch (ala [GitOps](https://www.weave.works/technologies/gitops/)), step 9 will
trigger step 13 automatically and steps 10-12 will not be needed. At that point, we will have to remember
to do the squash-merge (step 9) only once we are ready to push the changes to the live cluster.
