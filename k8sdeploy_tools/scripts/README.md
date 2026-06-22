# Utility scripts

This directory conains a number of utility scripts designed to make it easier to perform the common
cluster maintenance tasks.  They are all based on `kubectl` and the ability to access the K8s cluster 
(you'll need the right `KUBECONFIG` set up).

## Server Heap Dump

The script `heap_dump.sh` is provided here to facilitate grabbing the java heap of 
the VANTIQ server from a running Kubernetes deployment. The usage is:

    heap_dump.sh [ -f <filename> ] [ -n <namespace> ] [ -c <context> ] pod

* `pod` is the name of the Kubernetes pod for the server
* optional `filename` is the path for storing the resulting hprof file on your local
machine. if not specified, the default is `/tmp/vantiq_heap.hprof`
* optional `namespace` corresponds to the Kubernetes namespace for the pod. if not 
specified, the script defaults to the namespace setting in the `current-context` in
KUBECONFIG.
* optional `context` enables you to choose the context to use in your KUBECONFIG file. If
unset, the script defaults to the `current-context`

_EXAMPLES_

    $ heap_dump.sh vantiq-0
    
    $ heap_dump.sh -f /tmp/foo.hprof -n vantiq-keycloak vantiq-2
    
    $ heap_dump.sh -f /tmp/foo.hprof -c nonprod vantiq-0
    
    $ heap_dump.sh -n staging -c nonprod vantiq-1

Future refinements will likely move this tool into a K8s job, but this should be good
enough to get started.
---
## Restart Vantiq Pods

The script `restart_vantiq.sh` is provided here to facilitate performing a rolling restart of the Vantiq server
statefulsets.  This can be used whenever there is a need to perform a controlled restart of all pods in a given
statefulset without introducing any substantive changes.  Unlike `kubectl scale` this script triggers a restart
governed by the Update Policy of the target statefulset.  For the Vantiq servers this means that it will perform
a rolling restart, during which time the system will always be available (since at no point will the set contain
fewer than N-1 pods, where N is the current replication count).  The usage is:

    restart_vantiq.sh [ -n <namespace> ] [ -c <context> ] [<target statefulset>]

* optional `target statefulset` is the name of the Kubernetes statefulset to be restarted.  If not 
specified, the default is `vantiq` (aka the primary Vantiq server).
* optional `namespace` corresponds to the Kubernetes namespace for the pod. If not specified, the script 
defaults to the namespace setting in the `current-context` in KUBECONFIG.
* optional `context` enables you to choose the context to use in your KUBECONFIG file. If
unset, the script defaults to the `current-context`

_EXAMPLES_

    $ restart.sh
    
    $ restart.sh vantiq-vision-analytics
    
    $ restart.sh -n staging -c nonprod

---
## Mongodb Restore From Backup
The script mongo_restore.sh is provided here to facilitate restoration of the Vantiq database
from a backup. When deployed the Vantiq helm chart knows the details for creating and storing
backups to an object store (e.g. AWS S3). mongo restore will work from the LATEST back up file
recreating the ars02 database. The usage is:

    mongo_restore.sh [ -n <namespace> ] [ -c <context> ]
    mongo_restore.sh [ -n <namespace> ] [ -c <context> ] delete

* optional `namespace` corresponds to the Kubernetes namespace for the pod. if not 
specified, the script defaults to the namespace setting in the `current-context` in
KUBECONFIG.
* optional `context` enables you to choose the context to use in your KUBECONFIG file. If
unset, the script defaults to the `current-context`

* once a job is created it cannot be recreated until it is first deleted. running mongo_restore with
the `delete` parameter removes a previously created mongorestore job and its associated pod regardless of its state
(failed, in-progress or completed).

_EXAMPLES_

    $ mongorestore.sh

    $ mongorestore.sh -n staging -c nonprod

    $ mongorestore.sh -n staging delete
    $ mongorestore.sh -n staging
    
## Helper Script for Air Gap Deployments
The script airgap_deploy.sh is intended for use performing Vantiq deployments in air gapped private cloud infrastructure
(i.e. infrastructure that does not allow connections to the internet. It knows the right docker volume mounts to help
you load the saved `airgapdeploy` docker image and import the associated docker volume. It can then be run to exec a
bash shell in the container so that deployment may proceed more or less normally.

_EXAMPLES_

    $ airgap_deploy.sh -d /path/to/saved/image/and/volume/exports
    
    # get a bash shell in the container to perform deployment
    $ airgap_deploy.sh

---
Was this page helpful?<br/>
[[Yes](https://giphy.com/search/yesss)] [[No](https://giphy.com/explore/no-no-no)]
