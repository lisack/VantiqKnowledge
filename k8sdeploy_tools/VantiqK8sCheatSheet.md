# Vantiq Kubernetes Cheat Sheet

## Overview

This document is the Vantiq Kubernetes cheat sheet. Before continuing to read this document, you should first
read [the canonical Kubernetes cheat sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) which
contains most of the information you will need.

We also use [Helm](https://helm.sh/) to deploy the components of a Vantiq installation, so you should be
familiar with basic Helm commands. Consult the [Helm documentation](https://helm.sh/docs/helm/) for a reference
of Helm commands.

Some of the sections below ([Useful Basic `kubectl` Commands](#kubectl_cmds) and
[Useful Basic `helm` Commands](#helm_cmds)) duplicate commands from the above references, but customized to
match the K8s resources found in a Vantiq installation.

The remaining sections contain commands and patterns that are more complex or specialized and only found here.

---

## Table of Contents

* [Useful Basic `kubectl` Commands](#kubectl_cmds)
* [Useful Basic `helm` Commands](#helm_cmds)
* [Useful Advanced `kubectl` Commands](#kubectl_advancedcmds)
    * [Extract Certificate from `vantiq-ssl-cert` Secret](#extract_vantiqcert)
    * [Use Selected Output from `kubectl describe nodes` to See Pod Distribution on Nodes](#show_nodes_pods)
    * [Forcing Pods Onto the Correct Nodes](#force_pods)
* [Tips for Managing Contexts in Your `kubeconfig` Files](#manage-kube-contexts)
    * [Best Practice for Managing Multiple Kubernetes Clusters](#manage-mult-clusters)
    * [Managing `kubeconfig` Files in `k8sdeploy_tools/targetCluster](#tc_kubeconfig)
        * [Remember `k8sdeploy_tools` Uses  `targetCluster/kubeconfig` Not  `~/.kube/config`](#tc_kubeconfig_in_tc)
        * [Best Practice for Managing Multiple `targetCluster/kubeconfig` Files](#tc_mult_kubeconfigs)

---

<a name="kubectl_cmds"></a>
## Useful Basic `kubectl` Commands

The following basic commands are the ones we use most often:

```sh
# List all pods in all namespaces and watch for changes - useful for monitoring "kubectl rollout restart" etc
kubectl get pods -A -w

# List pods with "-o wide" to include pod IP and node, in this case for pods in the "dev" namespace
kubectl get pods -n dev -o wide

# Display the log output including `-f` to live-tail it, in this example of the vantiq-2 pod in the "dev" namespace
kubectl logs vantiq-2 -n dev -f

# Scale a deployment or statefulset, in this example scale the mongdb statefulset in the "dev" namespace to 0 pods
kubectl scale sts mongdb -n dev --replicas=0 

# Do a rolling restart (one pod at a time), in this example restart the vantiq statefulset pods in the "dev" namespace
kubectl rollout restart sts vantiq -n dev

# Delete a pod, in this example the vantiq-2 pod in the "dev" namespace so the K8s scheduler will start a new one
kubectl delete pod vantiq-2 -n dev 

# Display all events
kubectl events -A

# Display all events for pod vantiq-0 in all namespaces
kubectl events -A --for pod/vantiq-0

# Display all events of type "Warning" in all namespaces
kubectl events -A --types=Warning
```

One note about `kubectl rollout restart` vs. `kubectl delete pod`: if you run `kubectl delete pod` for each pod
in a statefulset, waiting for each new pod to become ready before deleting the next, you would have the same
functional equivalent as if you ran `kubectl rollout restart`. In general, `kubectl rollout restart` is easier
since you only need to run one command, and  `kubectl delete pod` useful mainly to terminate then recreate a
single pod or two.


<a name="helm_cmds"></a>
## Useful Basic `helm` Commands

As noted above, you should consult the [Helm documentation](https://helm.sh/docs/helm/) for a reference of
Helm commands.

There are only a few Helm commands you are likely to use, since most Helm commands will be called for you by
the tools tasks like `deployVantiq` and `deployShared`. Those commands are:

```sh
# List the Helm repos installed on your local machine
helm repo ls

# Update the Helm repos installed on your local machine
helm repo update

# List deployed Helm releases / charts - not that useful without a context and namespace
helm ls

# List the Helm releases / charts deployed to the "dev" namespace in the "prod-us" cluster
helm --kube-context prod-us -n dev ls
```

<a name="kubectl_advancedcmds"></a>
## Useful Advanced `kubectl` Commands

The following more complex `kubectl` commands are useful for managing Vantiq installations.

<a name="extract_vantiqcert"></a>
### Extract Certificate from `vantiq-ssl-cert` Secret

The `vantiq-ssl-cert` secret in each Vantiq installation namespace contains the certificate for the Vantiq
installation in that namespace, in the `tls.crt` key value, Base64-encoded. To extract the certificate and
have `openssl` decode it into human-readable form with a single command, run

```sh
kubectl get secret -n dev vantiq-ssl-cert -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout 
```

<a name="show_nodes_pods"></a>
### Use Selected Output from `kubectl describe nodes` to See Pod Distribution on Nodes

It can be useful to see more info about pods and nodes than is provided by the
`kubectl get pods -n dev -o wide` command above, especially to get a listing of all pods by node that are
part of a Vantiq installation. In addition to pods, it is also useful to see node info such as instance
(VM) type, region & zone, and taints. This info can be listed all at once with the command:

```sh
kubectl describe nodes | egrep "^Name:|instance|mongo|userdb|vantiq|metrics|vision|influx|grafana|coredns|keycloak|nginx|telegraf|domain|Taint"
```

If you want this info for only a subset of nodes, you can limit the output to only nodes with a specific label.
For example, to only describe nodes with the `node.kubernetes.io/instance-type` label set to `t3.medium` and
output the same info as before, run the command:

```sh
kubectl describe nodes -l node.kubernetes.io/instance-type=t3.medium | egrep "^Name:|instance|mongo|userdb|vantiq|metrics|vision|influx|grafana|coredns|keycloak|nginx|telegraf|domain|Taint"
```

<a name="force_pods"></a>
### Forcing Pods Onto the Correct Nodes

Most of the time the affinity settings in the deployments and statefulsets of a Vantiq installation are
sufficient for the K8s scheduler to place them on the correct node. However, there are times when that does
not happen and you must force pods onto the correct nodes.

For example, let's say you have one node of type `c6i.large` intended to run the `metrics-collector-0` pod
and three nodes of type `c6i.xlarge` intended to run the three `vantiq` pods, and all four nodes have the
`vantiq.com/workload-preference=compute` label to guide the K8s scheduler to place these pods via affinity
settings. If the `metrics-collector-0` pod came up before the final `vantiq` pod, `metrics-collector-0`
could get scheduled onto a `c6i.xlarge` node, causing `vantiq-2` to have nowhere to be scheduled and be
stuck in `Pending` status.

The resulting problem would look like this:

```sh
$ kubectl get pod -n dev
NAME                         READY   STATUS      RESTARTS   AGE
metrics-collector-0          1/1     Running     0          2h
mongodb-0                    2/2     Running     0          2h
mongodb-1                    2/2     Running     0          2h
mongodb-2                    2/2     Running     0          2h
vantiq-0                     1/1     Running     0          2h
vantiq-1                     1/1     Running     0          2h
vantiq-2                     0/1     Pending     0          2h

$ kubectl describe nodes -l vantiq.com/workload-preference=compute | egrep "^Name:|instance|mongo|userdb|vantiq|metrics|vision|influx|grafana|coredns|keycloak|nginx|telegraf|domain|Taint"
Name:               ip-10-10-153-36.us-west-2.compute.internal
                    failure-domain.beta.kubernetes.io/region=us-west-2
                    failure-domain.beta.kubernetes.io/zone=us-west-2a
                    node.kubernetes.io/instance-type=c6i.xlarge
                    vantiq.com/workload-preference=compute
Taints:             <none>
  dev                         vantiq-0                                          2 (51%)       8 (204%)    4Gi (60%)        8Gi (120%)     2h
  shared                      telegraf-ds-hq9g7                                 100m (2%)     1 (25%)     256Mi (3%)       1Gi (15%)      3h
Name:               ip-10-10-156-87.us-west-2.compute.internal
                    failure-domain.beta.kubernetes.io/region=us-west-2
                    failure-domain.beta.kubernetes.io/zone=us-west-2a
                    node.kubernetes.io/instance-type=c6i.large
                    vantiq.com/workload-preference=compute
Taints:             <none>
  shared                      telegraf-ds-hq9g7                                 100m (4%)     1 (50%)     256Mi (6%)       1Gi (30%)      3h
Name:               ip-10-10-168-101.us-west-2.compute.internal
                    failure-domain.beta.kubernetes.io/region=us-west-2
                    failure-domain.beta.kubernetes.io/zone=us-west-2b
                    node.kubernetes.io/instance-type=c6i.xlarge
                    vantiq.com/workload-preference=compute
Taints:             <none>
  dev                         vantiq-1                                          2 (51%)       8 (204%)    4Gi (60%)        8Gi (120%)     2h
  shared                      telegraf-ds-7dhj5                                 100m (2%)     1 (25%)     256Mi (3%)       1Gi (15%)      3h
Name:               ip-10-10-180-145.us-west-2.compute.internal
                    failure-domain.beta.kubernetes.io/region=us-west-2
                    failure-domain.beta.kubernetes.io/zone=us-west-2c
                    node.kubernetes.io/instance-type=c6i.xlarge
                    vantiq.com/workload-preference=compute
Taints:             <none>
  dev                         metrics-collector-0                               2 (51%)       4 (102%)    5Gi (75%)        8Gi (120%)     2h
  shared                      telegraf-ds-vqpf8                                 100m (2%)     1 (25%)     256Mi (3%)       1Gi (15%)      3h
```

To fix this by forcing the `metrics-collector-0` pod onto the correct node
(ip-10-10-156-87.us-west-2.compute.internal), you can taint all nodes with `NoSchedule`, then untaint
ip-10-10-156-87.us-west-2.compute.internal, then delete `metrics-collector-0` so the K8s scheduler will create
a new one (this time on the correct node). Once `metrics-collector-0` is running on the correct node, you can
untaint all nodes which should allow `vantiq-2` to be scheduled onto the node where `metrics-collector-0` used
to be running.

You would run the following commands to do this:

```sh
kubectl taint nodes --all key=value:NoSchedule
kubectl taint nodes ip-10-10-156-87.us-west-2.compute.internal key:NoSchedule-
kubectl delete pod metrics-collector-0 -n dev
kubectl get pod -n dev -o wide        # Confirm that metrics-collector-0 is starting on ip-10-10-156-87
kubectl taint nodes --all key:NoSchedule-
kubectl get pod -n dev -o wide        # Confirm that vantiq-2 is starting on ip-10-10-180-145
```

Of course this example is somewhat contrived, since it would be simpler to temporarily scale down the
metrics-collector statefulset to allow `vantiq-2` to start:

```sh
kubectl scale sts metrics-collector -n dev --replicas=0
kubectl get pod -n dev -o wide        # Once metrics-collector-0 is down, confirm that vantiq-2 is starting on ip-10-10-180-145
kubectl scale sts metrics-collector -n dev --replicas=1
kubectl get pod -n dev -o wide        # Confirm that metrics-collector-0 is starting on ip-10-10-156-87
```

However, there can be times when you will need to force pods onto the correct nodes with the above "taint node
then delete pod" process. You may even need to move multiple pods, which you can do by repeating the process
with a new node and pod: retainting the node you just moved a pod to, then untainting another node to force a
different pod onto it, then deleting the new pod you wish to move, and so on until all pods are on the correct
nodes.

**Important:** don't forget the `kubectl taint nodes --all key=value:NoSchedule` step at the end to remove the
`NoSchedule` taint from all nodes. If you don't then you will still have nodes with that taint applied, so
the K8s scheduler will not be able to schedule new pods onto those nodes and the pods will be stuck in
`Pending` state. This includes new pods from a `kubectl rollout restart`, or if you replace a pod by deleting
it with `kubectl delete pod` so the K8s scheduler will create a new one.

---

<a name="manage-kube-contexts"></a>
## Tips for Managing Contexts in Your `kubeconfig` Files

<a name="manage-mult-clusters"></a>
### Best Practice for Managing Multiple Kubernetes Clusters


If you only ever manage a single Kubernetes cluster, it is simplest to have that cluster be the current
context in your `~/.kube/context` file (in fact it may be the only context). In such cases, you can just use
the `kubectl` command as-is, knowing that the context it will be using (and therefore the Kubernetes cluster
it will be interacting with) will always be the same one.

However, if you manage more than one Kubernetes cluster you will have multiple contexts in your
`~/.kube/config` file and need some way of using each of those contexts when you need to work on the cluster
it matches.

The standard way of doing this is to use the `kubectl config use-context` command to change the current
context, then run `kubectl` commands as usual. In our experience this is a **bad idea**, since you must rely
on your memory to know which context you are using at any given moment, unless you run the
`kubectl config current-context` command before each real `kubectl` command (or embed the
`kubectl config current-context` command into your prompt). This in turn makes it far too easy to run a
command on one cluster that you meant to run on another cluster. Picture yourself thinking you are running
the command `kubectl delete statefulset vantiq` on a sandbox cluster on which you were doing practice
installs, but instead mistakenly running it on a production cluster with disastrous consequences. No one
ever wants to do this, so it's best to put a practice in place that is more likely to avoid it ever
happening.


Our best practice for managing more than one Kubernetes cluster (and the multiple contexts in 
`~/.kube/config` that go with them) is to set up an alias for `kubectl` for each cluster and use that alias
for all commands. That way, you are always clear which cluster you are running a command on, because the
cluster is embedded in the command you are using.

Our current practice is to use 4-letter aliases, which all have `kc` as the first two letters and have the
last two letters be a representation of the context name.

For example, let's say the 4 clusters and contexts you have are the production clusters in the US, EU and
Asia Pacific with contexts `prod-us`, `prod-eu` and `prod-ap` as well as a non-production cluster
`nonprod-us`. The `kubectl` aliases for these could be:

```
alias kcus='kubectl --context prod-us'
alias kceu='kubectl --context prod-eu'
alias kcap='kubectl --context prod-ap'
alias kcnp='kubectl --context nonprod-us'
```

To run the ``kubectl get node` command for each of these clusters, you would run:

```
kcus get node
kceu get node
kcap get node
kcnp get node
```

You may wish to use this pattern or come up with your own. No matter which pattern you follow, it is highly
recommended that it embeds the cluster context into the commands you type so you are clear which cluster
you are accessing with every command. Aliases are ideal for this purpose.

<a name="tc_kubeconfig"></a>
### Managing `kubeconfig` Files in `k8sdeploy_tools/targetCluster`

<a name="tc_kubeconfig_in_tc"></a>
#### Remember `k8sdeploy_tools` Uses  `targetCluster/kubeconfig` Not  `~/.kube/config`

It is important to note that `k8sdeploy_tools` does not use the contexts in your
`~/.kube/config` file. Instead, it uses the `targetCluster/kubeconfig` file which
should only have a single context in it (which should also be set to be the default
context).

The actual `targetCluster/kubeconfig` file will change depending on which branch you
switch to in the repo that is rooted to the `targetCluster` subdirectory. Each branch's
`kubeconfig` contents should match the cluster which the branch is the config for. The
branch name is used in the `-Pcluster` arg for the `gradlew` command. Example: for the
`prod-us` cluster mentioned in the previous section which uses the `prod-us` branch in
the `k8sdeploy_clusters` repo (or whatever repo is rooted to the `targetCluster`
subdirectory), the `deployVantiq` task would be:

```
./gradlew -Pcluster=prod-us deployVantiq
```

This would switch the `targetCluster` repo to the `prod-us` branch in the process of running the task. Note
in this case that the cluster name and the context in `targetCluster/kubeconfig` are also  `prod-us`. This is
common practice since it makes everything more clear, but it is only the `targetCluster` repo branch name that
must match the `-Pcluster` arg. The branch name does not need to match the cluster name or kubeconfig context
name, it's just clearer if they do.

<a name="tc_mult_kubeconfigs"></a>
#### Best Practice for Managing Multiple `targetCluster/kubeconfig` Files

Note that if the `kubeconfig` in the `targetCluster` repo branches are actual files containing actual
kubeconfig credentials, it is likely you will not want to check them into SCM since they contain credentials
you should keep secure.

Our best practice to avoid this is to create a `targetCluster/sensitive` subdirectory to contain the actual
kubeconfig files, then have the `targetCluster/kubeconfig` in each branch be a symlink pointing to the
matching (real) kubeconfig file in `targetCluster/sensitive`. Any files in `targetCluster/sensitive` will not
be checked into Git due to the `.gitignore` file.

Let's use the `prod-us` cluster above as an example. If the `prod-us` branch in the `targetCluster` repo has
a normal `kubeconfig` file, its credentials would be checked into SCM which is a security problem you don't
want. To convert this to the secure practice where `targetCluster/kubeconfig` is only a symlink and the real
`kubeconfig` (and the credentials it contains) is only in the `targetCluster/sensitive` subdirectory on your
local machine, run the commands:

```
git checkout prod-us
mv kubeconfig sensitive/kubeconfig.prod-us
ln -s sensitive/kubeconfig.prod-us kubeconfig
git add kubeconfig
git commit
git push -u origin prod-us
```

This will require each person using this `targetCluster` repo to have all the the real
`sensitive/kubeconfig.xxxxx` files (which the `kubeconfig` symlinks in the branches point to) in the
`targetCluster/sensitive` subdirectory on their local machine. Since each person most likely already has the
contexts for these in their `~/.kube/config` file, it is straighforward for them to create each
`sensitive/kubeconfig.xxxxx` file from a copy of their `~/.kube/config`, which they then edit to reduce it to
only the single context needed.

When they create their `sensitive/kubeconfig.xxxxx` files, they must remember to set the default context in
each file to the correct context (which should be the only context left in the file).

While you can convert the kubeconfig files in the branches of the `targetCluster` repo to symlinks later as
described above, it is of course simpler to set things up this way in the first place (each time you create
a new branch for a new cluster).








