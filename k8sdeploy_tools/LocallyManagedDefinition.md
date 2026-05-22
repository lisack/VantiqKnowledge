# Managing Cluster Definitions Locally

This scenario is targeted at 2 primary use cases:

* Deployment of a customer managed installation where the customer either can’t or doesn’t want to provide a way to store 
the cluster definition in a hosted manner.
* Deployment of a less permanent installation where long term management of the cluster definition isn’t required.

Use of this scenario precludes leveraging any future work we will do to automate the deployment process. The user 
will always be required to make updates to the installation via the command line tools run from a deployment machine 
external to the cluster.

## Creating a New Cluster Definition

1) Change directory into the `targetCluster` sub-directory 
1) Run the command `git checkout -b <clusterName>`.  Even though this is locally managed, it is still a good idea to 
give the cluster branch a meaningful name. Often this is the same as the K8s cluster name, although that is not
required.
1) Edit the `cluster.properties` file and uncomment the line that reads `#requireRemote=false` by
removing the leading `#`.
1) Change directory back to the `k8sdeploy_tools` directory (which should be the immediate parent directory at this
point).

## Utilizing Git to Manage Changes

Even though locally managed cluster definitions will never be pushed to a central Git repository, you can still
benefit from the fact that the definition is managed by Git locally.  The goal should be that the cluster's current
definition should be checked in to its branch. As you make changes Git will automatically track those, so you can:

a) Know exactly what has been changed and get a comparison between the current state and the cluster's current state.  
b) Revert what you've changed if it doesn't work out.

If you are unfamiliar with Git then you will want to gain a basic working knowledge.  Of particular interest will
be the *checkout*, *add*, and *commit* commands.  The basic workflow when making changes to the cluster definition should 
be something like:

1) Checkout the cluster's branch.
1) Make the changes you are planning to deploy.
1) Deploy/test the changes on the target cluster.
1) Once you are satisfied use `git add` and `git commit` to save your changes as the current cluster state.

**Pro Tip**: it is always safe to run `git status` to confirm the result of commands like `git add` and to confirm you
have checked out the correct branch.

