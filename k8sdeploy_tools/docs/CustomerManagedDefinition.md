# Centrally Managing Cluster Definitions by a Customer

This scenario allows a customer to manage the definition for a customer managed cloud in the same way that Vantiq
does, but using their own Git repo to store that definition.

This is a slight variant to the
[Vantiq-managed Cluster Definitions scenario](VantiqManagedDefinition.md) to address cases where the customer
wants to use our deployment tools (with the eventual ability to automate deployment) but does not want Vantiq to have
any access to the cluster definition. To support this scenario the customer must provide an alternative Git repo
to store the clusters branch. This repo can be any hosted Git solution (GitHub, Bitbucket, GitLab, etc.).   

Once this repo is established, its location must be provided to the tools via the “clusterRepo” property. This can be
done via the command line by adding `-PclusterRepo=<uri>` to every command, or it can be set globally using a
`gradle.properties` file on the deployment machine.  After that the overall install process is identical to what is
described in the Vantiq-managed scenario. 

<a name="clusterrepo"></a>
## Initializing and Using a Custom Cluster Repo by default for `targetCluster`

As noted above, setting a custom repo by default globally rather than adding `-PclusterRepo=<uri>` to every command
is a more user-friendly option. These are the steps required to do that, which you should do before proceeding to
the section below to create a new cluster definition (branch) in the repo you create in this section.

Assuming you have followed the
[*Installation and Configuration* section of the *k8sdeploy_tools Initial Setup and Configuration*](k8sdeploy_toolsBootstrap.md#installation-and-configuration)
doc (step 5 in particular), your `k8sdeploy_tools/.gradle/gradle.properties` file should look something like:

```
gitUsername=MYGITUSERNAME
gitPassword=MYGITTOKENPW
```

You should follow the additional instructions here to set the `clusterRepo` Gradle property in your
`gradle.properties` file and initialize your custom cluster repo (this is also listed in the
[*Installation and Configuration* section of the *k8sdeploy_tools Initial Setup and Configuration*](k8sdeploy_toolsBootstrap.md#installation-and-configuration)
doc as step 6). Do this by performing the following steps:

1) In step 5 of the bootstrapping doc, set the `clusterRepo` Gradle property in `.gradle/gradle.properties`
to the URI of what will be your custom cluster repo (at this point it does not yet exist)
1) Run the `configureVantiqSystem` task which will set up the local cluster repo rooted in `targetCluster`
(it will create it with a default branch of `master` and populate it with a generic `cluster.properties`
and `deploy.yaml` from the `bootstrap` dir)
1) Create the actual cluster repo (on GitHub or wherever you are storing it) as an empty repo

<ol start="4">
</li>
<li>Set the origin of the local cluster repo, then push the files up from the local repo to the origin with:
<ol>
<li> <code>cd targetCluster</code></li> 
<li> <code>git branch -M master</code></li> 
<li> <code>git remote add origin <i>ClusterRepoURI</i></code></li> 
<li> <code>git push -u origin master</code></li> 
<li> <code>git remote show origin</code>  <i>(check that the origin is properly set up)</i></li> 
</ol>
</li> 
</ol>

**Note:** the `clusterRepo` Gradle property in `.gradle/gradle.properties` and the actual value shown as
the `ClusterRepoURI` placeholder in 4.iii. above should be the same, a Git URI something like
`https://github.com/myorg/myclusterrepo.git`.

<a name="k8sdeployrepo"></a>
## Using a Custom `k8sdeploy` Repo

In most cases, you will use the default `k8sdeploy` repo (which is `https://github.com/Vantiq/k8sdeploy`)
so you can ignore this section. However, in rare cases you may need to use a custom `k8sdeploy` repo. In
such cases you can set the custom `k8sdeploy` repo location by setting the `vantiqSystemRepo` and
`helmChartRepo` Gradle properties in `.gradle/gradle.properties` the same way you set the `clusterRepo`
Gradle property above. Those lines should look something like:

```
vantiqSystemRepo=https://mygithub.somecompany.com/myorg/k8sdeploy.git
helmChartRepo=https://mygithub.somecompany.com/pages/myorg/k8sdeploy/charts/
```

Please note that the chart URI (the `helmChartRepo` property) must be publicly accessible for Helm to
access them.

Although you will not normally need to use a non-default `k8sdeploy` repo, you may need to do so in
some conditions. One example is if you are mirroring the `k8sdeploy` repo due to a company security
requirement. If you need help with such requirements, please contact
[Vantiq Support](mailto:support@vantiq.com).

If you are using a non-default `k8sdeploy` repo, you may also be using a custom image repo for your
container images. If you are, please see the
[*Using a Custom Image Repo* section of the *Installing Vantiq* doc](Installation.md#custom_image_repo)
for info on how to specify a custom image repo rather than the default `quay.io/vantiq` repo.

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
 
It is best practice to follow a naming standard for your cluster branches. For Vantiq-managed clusters, we
normally name the cluster branch the same as the K8s cluster name, although that is not required. Whatever is
chosen for the cluster branch name (e.g. `foo`) will need to be used for the <code>&#8209;Pcluster=</code> arg
(e.g. `-Pcluster=foo`).

## Standardize a Git Workflow to Manage Changes

Git and its workflows are central to managing changes to the cluster definitions. If you are unfamiliar with
Git then you will want to gain a basic working knowledge in order to use the tools correctly.

To manage changes to the cluster definitions effectively, you should standardize on the same Git workflow
for your whole team. The workflow used by Vantiq Ops can be found in the
[Git Workflow section of the Vantiq Managed Cluster Definitions doc](VantiqManagedDefinition.md#git_workflow).
You can use this same workflow, or create one of your own.

**Pro Tip**: it is always safe to run `git status` to confirm the result of commands like `git add` and to confirm you
have checked out the correct branch.

