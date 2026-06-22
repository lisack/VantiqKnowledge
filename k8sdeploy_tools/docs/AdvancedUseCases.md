# k8sdeploy_tools Advanced Use Cases

## Overview

This document contains a collection of advanced use cases which are only relevant in specific conditions so they do
not belong with the main info in places like the [main Installation doc](Installation.md). If one of these specific
advanced use cases applies to your Vantiq installation, the info you need should be found in one of the sections
below.

&nbsp;

## Table of Contents
* [Networking Advanced Use Cases](#networking)
    * [Dealing with missing DNS entries](#missing_dns_entries)
    * [Ingress Controller Options](#ingress_controller_options)
        * [Deploying Vantiq Using a Preexisting Nginx Ingress Controller](#existing_nginx_controller)
        * [Deploying Vantiq Using a Preexisting Non-Nginx Ingress Controller](#existing_nonnginx_controller)
        * [Deploying the Vantiq Nginx Alongside an Existing Nginx Ingress Controller](#multiple_nginx_controllers)
    * [Installing Vantiq Without Virtual Host Routing](#no_virtual_host_routing)
* [Other Advanced Use Cases](#other)
    * [More Complex Configuration Overrides](#complex_overrides)
    * [Branding / White-Labeling](#whitelabeling)
        * [Branding / White-Labeling the Web UI](#whitelabeling_webui)
        * [Branding / White-Labeling Keycloak](#whitelabeling_keycloak)
            * [Prepared Custom Theme Files &rarr; tar File &rarr; configmap](#whitelabeling_kc_prep)
            * [Generate Base Resource for `kustomize`](#whitelabeling_kc_base)
            * [Create Overlay Patch for `kustomize`](#whitelabeling_kc_createpatch)
            * [Create `kustomization.yaml` File and Apply Patch](#whitelabeling_kc_applypatch)
    * [Deploying Vantiq into Air-Gapped Infrastructure](#airgapped)
        * [Prepare a Docker Volume](#airgapped_init)
        * [Export the Docker Volume and Image](#airgapped_export)
        * [Performing the Airgap Deploy](#airgapped_deploy)
        * [Helm Chart Docker Images Not Included](#airgapped_imagesneeded)
        * [Dealing with DNS and SSL in an Air-Gapped Deployment](#airgapped_dnsssl)        
    * [Support for Isolated Organization Compute](#ioc)
        * [Enabling the Worker](#ioc_enableworker)
        * [Vantiq-Worker Secret](#ioc_workersecret)

&nbsp;

<a name="networking"></a>
## Networking Advanced Use Cases

There are a number of networking corner cases that can be handled using the info in this section.

<a name="missing_dns_entries"></a>
### Dealing with missing DNS entries

As described in the [Updating DNS section of the Installation doc](Installation.md#updating_dns), complete
deployment of the Vantiq system requires the creation of an entry (usually a `CNAME` record but sometimes an `A`
record) in the target domain's DNS server. While this step must be completed before Vantiq is ready for general
use, it is possible to work around the lack of these DNS entries on a short term basis. To do this you need to
add an entry to your local "hosts" file. This entry should map the installation's FQDN to the IP address of the
cloud provider's load balancer. The location of the hosts file is platform dependent:

* Windows -- `C:\Windows\System32\drivers\etc\hosts`
* MacOS -- `/etc/hosts`

Please note -- this is a **TEMPORARY** workaround and should not be used for any purpose other than to enable basic
validation of the deployment.  Due to the way OAuth/Keycloak works you will be unable to log into Vantiq until the
actual DNS entry is available.

### Ingress Controller Options

The default method of providing an ingress controller for Vantiq is to use the Nginx controller deployed as one of
the shared components by this repo via the `deployNginx` task. The standard Vantiq Nginx controller uses an
*ingress class* of `vantiq`. The Vantiq ingress in each installation namespace also has its *ingress class* set to
`vantiq` which causes it to use the standard Vantiq Nginx Controller.

This also limits the Vantiq-deployed Nginx ingress controller to only own the Vantiq Ingress instances, which has
been the default since Vantiq System (k8sdeploy) 3.6.1. Prior to that, the ingress class was `nginx` which could
conflict with non-Vantiq components using a default-configured generic Nginx Ingress controller, and in those cases
what is now the default had to be configured via overrides. To accomplish that, the following had to be added to
`deploy.yaml`:

```yaml
# Set the ingress class to use under the "nginx" section.
nginx:
  controller:
    ingressClass: vantiq

# Set the ingress class for Vantiq in that section:
vantiq:
  ingress:
    annotations:
      kubernetes.io/ingress.class: vantiq
```

This now-default behavior only needs to be adjusted if you want the Vantiq Ingress to be managed by a
preexisting ingress controller as described in one of the ingress controller subsections below.

<a name="existing_nginx_controller"></a>
#### Deploying Vantiq Using a Preexisting Nginx Ingress Controller

If the preexisting ingress controller is also Nginx like the Vantiq-deployed one, then it is possible to use it to
route for the Vantiq installations and eliminate the need for the Vantiq-deployed Nginx ingress controller. In this
case you would skip the steps relating to deploying the Nginx controller via the Vantiq tools and just move on to
deploying the rest of the Vantiq system. You will however need one small config change via `deploy.yaml`.

You will first need to determine the ingress class being used by the preexisting Nginx controller. You can then set
the vantiq `kubernetes.io/ingress.class` annotation to match. For example, if the preexisting Nginx controller is
using the ingress class `mynginx`, then you must set the vantiq `kubernetes.io/ingress.class` annotation in
`deploy.yaml` to match as follows:

```yaml
# Set the ingress class for Vantiq in the vantiq.ingress section:
vantiq:
  ingress:
    annotations:
      kubernetes.io/ingress.class: mynginx
```

For example, Rancher RKE2 deploys a generic Nginx ingress controller as part of the standard RKE2 cluster which uses
the default ingress class of `nginx`. To use that existing Nginx controller instead of the one deployed by our tools,
simply skip the `deployNginx` step of the install process, and set the vantiq `kubernetes.io/ingress.class`
annotation in `deploy.yaml` to `nginx`.


<a name="existing_nonnginx_controller"></a>
#### Deploying Vantiq Using a Preexisting Non-Nginx Ingress Controller

If you wish to use a preexisting non-Nginx ingress controller as described in the previous section, the process is
most likely identical but may not be. This option is beyond the scope of this document so you must implement and
maintain it on your own.

<a name="multiple_nginx_controllers"></a>
#### Deploying the Vantiq Nginx Alongside an Existing Nginx Ingress Controller

In some private cloud environments you may need to deploy the Vantiq Nginx controller alongside an existing Nginx
controller. In such cases you may run into a conflict between the `ingressclass` resource deployed by the existing
Nginx controller and the one the Vantiq-deployed Nginx ingress controller is attempting to deploy. This is because
the `ingressclass` resource type is a global (not namespaced) resource type, and the default name of the
`ingressclass` resource in the Nginx Helm chart is simply `nginx`. Most Nginx deployments do not change this
default (k8sdeploy does not, either) so the second `ingressclass` with the name `nginx` attempting to deploy to
the cluster will conflict with the first.

To fix this problem in the Vantiq-deployed Nginx ingress controller and avoid this conflict, set the
`ingressclass` resource name in `deploy.yaml` to something else, such as `vantiq-nginx` as shown here:

```
nginx:
  controller:
    ingressClassResource:
      name: vantiq-nginx
```

Again, let's use Rancher RKE2 which deploys a generic Nginx ingress controller as part of the standard RKE2 cluster.
It uses the default Nginx Helm chart which uses the `ingressclass` resource name of `nginx`. To deploy the Vantiq
Nginx controller alongside this preexisting Nginx controller, you would need to set the `ingressclass` resource
name in `deploy.yaml` to something else as shown above.


<a name="no_virtual_host_routing"></a>
### Installing Vantiq Without Virtual Host Routing

Normally when you install Vantiq we make use of virtual host routing to direct traffic from the Ingress controller
to the deployed Vantiq server. This allows us to support multiple Vantiq installations in the same cluster without
the need to deploy multiple Ingress controllers (and create their associated load balancers).

While this is the preferred configuration, it is possible to turn off v-host routing and deploy Vantiq so that it can
be accessed through the default routes of the Ingress controller. The primary use case for this is when you are
deploying in an installation where Vantiq must be accessed using a raw IP address and not an actual host name. Note
that in this configuration Vantiq must still be known by a single, fixed name/IP (otherwise authentication will not
work).

To enable this option you should set the following keys in your `deploy.yaml` file (an example of this
configuration can be found in
[`no-vhost.deploy.yaml`](https://github.com/Vantiq/k8sdeploy_clusters/blob/master/samples/no-vhost.deploy.yaml)):

| Key | Value | Description |
|-------|---------|-------------|
| vantiq.ingress.useHost | `false` | Disables virtual host routing in the Vantiq ingress resource. |
| vantiq.externalAddress |  | Configures the external address of Vantiq server.  This name/IP address must be visible from both inside and outside the cluster. |

Sometimes in this configuration it is necessary to use self-signed certificates (though that should be avoided if at
all possible). In this case the server must disable its trust checking when communicating with the Keycloak server. To
do this set the `vantiq.ingress.tls.selfSigned` key to `true`.  This will _not_ disable host name verification, so it
is necessary for the certificate to be properly associated with the server's external address (through the use of a
subject alternative name).  Creation of such a certificate is outside the scope of this documentation.

&nbsp;

<a name="other"></a>
## Other Advanced Use Cases

<a name="complex_overrides"></a>
### More Complex Configuration Overrides

The configuration associated with each component of the Vantiq deployment can be overridden in two ways. The first
approach is to add the desired configuration to the `deploy.yaml` file under the `configuration` key for whichever
component you wish to reconfigure. For example, if you want to adjust the configuration of the primary Vantiq
server, you would add the desired settings under the `vantiq.configuration` key. If you wanted to update the
configuration for the Vision Analytics server, you would add your settings under the 
`vantiq.visionAnalytics.configuration` key. This approach works well when you only have a few changes to make and
the configuration being changed is JSON or text. However, sometimes it is necessary to add very large files and/or
binary files to the configuration. For example, localizing the Vantiq server requires the addition of a 500+ line
properties file. Deploying a "white label" version of Vantiq requires the addition of binary icon files (and may
also involve localization). To handle these cases the deployment tools allow configuration files to be placed in
the `deploy/vantiq/config` directory of the target cluster repository. Configuration files for a given component
of the Vantiq deployment are placed in its associated sub-directory:

* `vantiq` -- the primary Vantiq server
* `visionAnalytics` -- the Vision Analytics server
* `metricsCollector` -- the Metrics Collector server

Any binary files are placed in the sub-directory `binary` (so a binary file for the Vantiq server would go in the
`vantiq/binary` sub-directory).

<a name="whitelabeling"></a>
### Branding / White-Labeling

One example of using the more complex configuration overrides in the previous section is for branding (aka
white-labeling) the Vantiq web UI. The details for doing that are found in the next subsection.

This is often accompanied by applying a custom Keycloak theme to the login screen to white-label that too. The
custom theme is applied to Keycloak directly at the K8s level (not by k8sdeploy_tools), details for doing that
are found in the subsection after next. Although this does not precisely belong here since it's not done by
*k8sdeploy_tools*, it is documented here for convenience.

<a name="whitelabeling_webui"></a>
#### Branding / White-Labeling the Web UI

White-labeling the Vantiq web UI allows you to change certain labels and icons to make a private cloud
installation appear the way you want it to look. This is commonly desired if you are using Vantiq to provide
a product platform of your own, so you want it to display your own brand and not the Vantiq brand (see
[White Labeling Vantiq](https://dev.vantiq.com/docs/system/idebranding/index.html) for details on exactly
what can be changed and how). As part of this process you will likely have a properties override file and
some new icons. To reference these you would add the following to your `deploy.yaml` (under the
`vantiq.configuration` section):

```yaml
vantiq:
  configuration:
    webUIConfig.json:
      brandedProperties: override.properties
      navbarDefaults:
        appicon: my-appicon.png
        icon: my-icon.png
```

This references 3 files -- a properties file called `override.properties` and 2 PNG files called
`my-appicon.png` and `my-icon.png`. You would then create/place these files under
`deploy/vantiq/config/vantiq` in your `targetCluster` directory. So you'd have:

* `deploy/vantiq/config/vantiq/override.properties`
* `deploy/vantiq/config/vantiq/binary/my-appicon.png`
* `deploy/vantiq/config/vantiq/binary/my-icon.png`

<a name="whitelabeling_keycloak"></a>
#### Branding / White-Labeling Keycloak

This section describes how to apply a customized theme to KeyCloak using Kustomize which is often done
together with the web UI white-labeling documented in the previous section. As noted above, since the
custom theme is applied to Keycloak directly at the K8s level and not by *k8sdeploy_tools*, these
instructions do not precisely belong here but are included for convenience.

Kustomize is Kubernetes native configuration management tool. Kustomize introduces a template-free way to
customize application configuration that simplifies the use of off-the-shelf applications. Kustomize is
built into `kubectl` via the `-k` option which is how it is used below. For further info on Kustomize,
please see the [Kustomize web site](https://kustomize.io/).

**Note:** Instructions for the creation of custom Keycloak themes are not included here, but are something
you will need to learn before you can create the custom theme files used in these instructions. Please see the
[Creating a Theme section of the Keycloak Server Development Guide](https://www.keycloak.org/docs/15.1/server_development/#creating-a-theme)
for this info. You may also wish to read the [Apache Freemarker](https://freemarker.apache.org/) docs since
Freemarker is the template engine used by Keycloak themes, as well as involve someone on your team who is
familiar with CSS (such as a web designer) since Keycloak themes also use CSS.

<a name="whitelabeling_kc_prep"></a>
##### Prepared Custom Theme Files &rarr; tar File &rarr; configmap

Let's say you work for MyCoolCompany Inc. and you have created the `MyCoolCompany_login_theme1` custom login
theme to white-label your Vantiq private cloud installation. You are now ready to apply this custom theme to
your Keycloak deployment using Kustomize. The first step in the process is to prepare the customized theme
property files for Kustomize by putting them in a tar file, then creating a configmap from that tar file.

We start with the theme files in the directory `MyCoolCompany_login_theme1`:

```sh
$ tree MyCoolCompany_login_theme1
MyCoolCompany_login_theme1
└── login
    ├── login.ftl
    ├── messages
    │   └── messages_en.properties
    ├── resources
    │   ├── css
    │   │   ├── login.css
    │   └── img
    │       ├── favicon.ico
    │       ├── feedback-error-arrow-down.png
    │       ├── feedback-error-sign.png
    │       ├── feedback-success-arrow-down.png
    │       ├── feedback-success-sign.png
    │       ├── feedback-warning-arrow-down.png
    │       ├── feedback-warning-sign.png
    │       ├── MyCoolCompany_Background.png
    │       └── MyCoolCompany_logo.png
    └── theme.properties

5 directories, 13 files
```

(This is only an example, your theme may contain different files. Also, if you don't have the `tree`
command you can list the directory tree in another way such as `ls -lR`.)

Next, create a tar file from the directory:

```sh
tar -cvf MyCoolCompany_login_theme1.tar ./MyCoolCompany_login_theme1
```

Next, create a configmap from the tar file:

```sh
kubectl -n shared create configmap keycloak-mcc-theme1 --from-file=./MyCoolCompany_login_theme1.tar
```
<a name="whitelabeling_kc_base"></a>
##### Generate Base Resource for `kustomize`

The next step in the process is to generate the base resource for Kustomize, in this case the `keycloak`
statefulset. Extract the `keycloak` statefulset into `keycloak-sts.yaml`, then edit it to remove all
runtime specification, such as `creationTimestamp`, `softLink`, `uid`, and `status`.

The files for this and later steps need to be in the same directory, we recommend calling it `kustomize`:

```sh
$ mkdir kustomize
$ cd kustomize
$ kubectl -n shared get statefulset keycloak -o yaml | kubectl neat > keycloak-sts.yaml
```

Note: `kubectl neat` is a kubectl plugin, see the
[installation section of the `kubectl neat` plugin page](https://github.com/itaysk/kubectl-neat#installation)
for details on the plugin and its installation. You can also leave off the `| kubectl neat` part of the
above command and hand-edit the output file to remove the runtime specification lines.

<a name="whitelabeling_kc_createpatch"></a>
##### Create Overlay Patch for `kustomize`

Next you must create the overlay patch file of the `keycloak` statefulset for Kustomize. In this example you
will put the patch in the file `keycloak-sts-patch.yaml`. The patch will mount the `keycloak-mcc-theme1`
configmap as the `mcctheme` volume mounted at `/mnt`, and extract the theme tar file into the
`/opt/jboss/keycloak/themes` directory immediately after starting. The `keycloak-sts-patch.yaml` contents
to do that should be:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: keycloak
  namespace: shared
spec:
  template:
    spec:
      volumes:
        - name: mcctheme
          configMap:
            name: keycloak-mcc-theme1
      containers:
      - name: keycloak
        volumeMounts:
        - name: mcctheme
          mountPath: "/mnt"
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "tar -xvf /mnt/MyCoolCompany_login_theme1.tar -C /opt/jboss/keycloak/themes/"]
```

<a name="whitelabeling_kc_applypatch"></a>
##### Create `kustomization.yaml` File and Apply Patch

Finally, you must create the `kustomization.yaml` file for Kustomize. This specifies the contents of
`keycloak-sts.yaml` as the base resource, and `keycloak-sts-patch.yaml` as the patch to it. The
`kustomization.yaml` contents to do that should be:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - keycloak-sts.yaml
namespace: shared
patchesStrategicMerge:
  - keycloak-sts-patch.yaml
```      

You can now apply the patch via the built-in Kustomize feature of `kubectl`:

```sh
kubectl apply -k .
```

Once the Keycloak pods cycle to pick up the new config, you should be able to log into the Keycloak admin
UI and select the new login theme to begin using it.

**Note:** you will need to reapply this Kustomize patch to your Keycloak deployment any time you run the
`deployShared` task. This is because `deployShared` will reset the configuration of your Keycloak to whatever
the Keycloak deployment is defined as by the k8sdeploy version you set in `cluster.properties` combined with
any custom Keycloak definitions in `deploy.yaml`. If anything has changed with the base definition of your
`keycloak` statefulset, you will also need to repeat the step to regenerate the `keycloak-sts.yaml` file
before reapplying the Kustomize patch.

Also keep in mind that as k8sdeploy versions move forward they will sometimes involve new Keycloak versions,
and that your theme may need to be updated to match the new Keycloak version when you upgrade it.

&nbsp;

<a name="airgapped"></a>
### Deploying Vantiq into Air-Gapped Infrastructure

Some private cloud environments are highly restrictive about access to the Internet, and in some cases are
completely isolated (aka air-gapped). Vantiq deployment relies on tools like Helm which depend on the
ability to connect to chart and docker image repositories. We added the `initAirgapped` and `exportAirgapped`
tasks to *k8sdeploy_tools* to make deployment into these restricted environments easier. The following steps
describe how to use the `initAirgapped` and `exportAirgapped` tasks.

<a name="airgapped_init"></a>
#### Prepare a Docker Volume 

There is a specialized docker image (airgapedeploy) to help with installation into air-gapped infrastructure.
The image is preloaded with many of the pieces required (bash, java, git, helm, kubectl, a helm chart server,
etc). It works with a docker volume that you must prepare ahead of time. This first step in the process _must
occur while you are connected to the Internet_ and involves loading up the docker volume with Gradle, clones
of the git repos for the `targetCluster` (k8sdeploy_clusters) and `vantiqSystem` (k8sdeploy) subdirectories,
a copy of all the vantiq charts, and a download of Gradle.

This should be done in a clone of the master branch from the *k8sdeploy_tools* repo as though you were
setting up to do a normal deployment. We need to take the first two steps in the normal deployment process:

```
./gradlew configureClient
```

This will set up `gradle.properies` under `.gradle` where you should add your Git credentials. Then run:
      
```
./gradlew configureVantiqSystem
```

The repos that underpin the `targetCluster` and `vantiqSystem` directories will be cloned (if necessary).
Once complete you should edit the `cluster.properties` and `deploy.yaml` files under `targetCluster` to
tailor the deployment to your needs. These can be updated later during the actual deploy if necessary, but
changes in the air-gapped environment will obviously not be propagated back into the `targetClusters` repo
branch unless you do so by hand.

Once settings and configuration are ready, run:

```
./gradlew initAirgapped
```

This task will do a fair amount of work. Among the steps are:
1. Mount a docker volume named `k8sdeploy_tools` onto /home/vantiq/k8sdeploy_tools in the running container.
   This should be an empty volume to start. If you have run initAirgapped previously and are running it
   again, it is a good idea remove the existing volume first with `docker volume rm k8sdeploy_tools`.
2. Verify git credentials and clone the `k8sdeploy_tools` repo master branch into /home/vantiq/k8sdeploy_tools.
3. Clone the vantiq charts from the `k8sdeploy` repo's gh-pages branch into /home/vantiq/k8sdeploy_tools/vantiqCharts.
4. Copy `targetCluster` from a volume bind mount into `targetCluster` under k8sdeploy_tools/. The tool does
   not require that the targetCluster branch be pushed to GitHub. Whatever state your local copy of the
   branch has will be used to configure the air-gapped deployment.
5. Clone the vantiq system based on the release specified in cluster.properties
6. Init the air-gapped deploy's Helm client. We need only the locally running chart server to respond to
   requests for charts from the `vantiq` chart repo. We remove the stable repo since it won't be available.

Once `initAirgapped` completes successfully the `k8sdeploy_tools` docker volume should be ready to go.

<a name="airgapped_export"></a>
#### Export the Docker Volume and Image

To run the deployment tools in the air gapped environment, we first need to save the image and export the
volume to the local disk. Run the `exportAirgapped` task for this:

```
./gradlew exportAirgapped
```

Once `exportAirgapped` completes there will be two `tar` files in the k8sdeploy_tools/.gradle/ directory:

```
airgapdeploy.tar    - the saved docker image
k8sdeploy_tools.tar - the exported docker volume
```

These both need to be copied into the airgap deployment infrastructure. In addition, there is a helper
script, `scripts/airgap_deploy.sh`, to assist in setting up the deployment tools. Copy it as well.

**Pro Tip**: the `exportAirgapped` target lists `initAirgapped` as a dependency. You can run it first
directly, and skip running it as part of `exportAirgapped`.

<a name="airgapped_import"></a>
#### Load the Docker Image and Import the Volume

Once you are working on the air-gapped infrastructure, you first need to load the image and import the
`k8sdeploy_tools` volume. Run the helper script:

```
airgap_deploy.sh -d /path/to/directory/containing/tar/files
```

This creates a docker image: `vantiq/airgapdeploy:latest` and imports the `k8sdeploy_tools` volume from
the `k8sdeploy_tools.tar` file.

<a name="airgapped_deploy"></a>
#### Performing the Airgap Deploy

Once the docker image and volume are loaded up in the air-gapped environment you are ready to perform the
actual deployment. You can use docker run to mount the `k8sdeploy_tools` volume and get a bash shell. You
can then proceed with deployment as normal. Run the helper script with no arguments:

```
$ airgap_deploy.sh 

waiting for chartmusuem to start....started
$ ./gradlew -Pcluster=prod_cluster deploy
```

<a name="airgapped_imagesneeded"></a>
#### Helm Chart Docker Images Not Included

The charts involved in a full deployment of Vantiq depend on a number of Docker images. There are images
for Nginx, Grafana, InfluxDB, MySQL, Vantiq Server, etc. These images must be saved when you are connected
and copied onto the worker nodes where they will run, and loaded there. At present, *k8sdeploy_tools*
does not provide help with this set of steps.

<a name="airgapped_dnsssl"></a>
#### Dealing with DNS and SSL in an Air-Gapped Deployment

As noted elsewhere, Vantiq will not function properly without correct DNS and SSL certificates. This is
not always possible in an air-gapped environment.

Ideally the air-gapped environment will at least have its own fully functional DNS. If this is the case
then adding the FQDN for the installation to the air-gapped DNS can be done as normal, it's just that it
will only be resolvable within the air-gapped environment. However, if there is no DNS within the
air-gapped environment then the raw IP of the load balancer can be used, but that means the SSL
certificates also must use IP addresses.

Since you cannot obtain IP-address-based SSL certificates from a third party, you must create your own
CA certificate then generate the needed IP-address-based certificates from that CA certificate. This is
typically done using `openssl`. You must also deploy the CA certificate you created to all the browsers
and operating systems in the air-gapped environment that will use the air-gapped Vantiq installation, so
they will properly trust the CA certificate as authoritative and therefore trust any child certificates
of it.

The same will be true if you have DNS so you can use a FQDN and not a raw IP, but you are not purchasing
an SSL certificate from a real CA. In that case you will need to generate your own CA certificate then
generate the needed FQDN certificates from that CA certificate. Also, direct use of cert-manager to
obtain SSL certificates from Let's Encrypt is not an option here since by definition an air-gapped
environment cannot reach the Let's Encrypt servers. You can work around this if you have a connected
server and control of the (real) domain used within the air-gapped environment: obtain the certificates
from Let's Encrypt using any software that is able to do so (certbot, cert-manager) then copy the
certificates and private keys to the air-gapped environment for use.

The *k8sdeploy_tools* tasks do not provide help with any of the scenarios described in this section. You
must have your infrastructure team handle them, and/or engage with Vantiq Consulting.

&nbsp;

<a name="ioc"></a>
### Support for Isolated Organization Compute

Starting with Vantiq System (k8sdeploy) 3.8.0 (and Vantiq release 1.31) *k8sdeploy_tools* provides support
for isolated organization compute (IOC). This deploys dedicated vantiq pods that run the rules and
procedures for a specific org (the remaining vantiq server processing remains on the multi-tenant vantiq
pods). While the tools do not actually deploy the IOC statefulsets themselves, they do enable the vantiq
server to deploy them dynamically when an org is "IOC-enabled" in the Vantiq web UI at the system admin
level (in the system namespace). 

In terms of Kubernetes resources, the tools create a CronJob (with associated RoleBinding and
ServiceAccount), ConfigMap and Secret. The CronJob kicks off the `vantiq-worker` job (a.k.a. the worker)
to poll the server runtime for any requested changes to the Kubernetes environment. The worker leverages
the Kubernetes API to create and delete IOC StatefulSets as needed.

<a name="ioc_enableworker"></a>
#### Enabling the Worker

By default, the Vantiq system chart disables the worker:

```yaml
worker:
  enabled: false
  schedule: "*/1 * * * *"
  clusterName: self
  image:
    repository: quay.io/vantiq/vantiq-k8sworker
    pullPolicy: IfNotPresent
    pullSecrets: registry-creds
```

The chart allows you to enable and adjust its run schedule. The schedule format is 
[based on BSD crontab](https://www.freebsd.org/cgi/man.cgi?crontab) and by default runs the job once
per minute. The other settings should not normally require any overrides.

Normally, the only addition you need to make to `deploy.yaml` to enable the IOC worker is to change
the CronJob `enabled:` parameter from `false` to `true`. Here is an example of that snippet of
`deploy.yaml` for the `coolprod` Vantiq installation:

```yaml
vantiq:
  installations:
    - coolprod:
        worker:
          enabled: true
```

<a name="ioc_workersecret"></a>
#### Vantiq-Worker Secret

The worker requires a Vantiq _system namespace_ access token with the `system.k8sWorker__system`
profile. It uses this token to poll the vantiq system for Kubernetes requests. Once the token is set up,
use it to create the `vantiq-worker` secret via the normal `generateSecrets` and `deployVantiq` tasks.
The `k8sWorker__system` profile contains the minimum permissions needed for the worker task to do its
processing, so using it is preferable to using the `system.admin` profile for this token.

Here is an example of the setting in `secrets.yaml` for the `coolprod` Vantiq installation:

```yaml
vantiq:
  coolprod:
    #
    # vantiq worker access token. This cannot be known until the post-deployment steps. Once a long-lived access token
    # is generated it can be added here and secrets regenerated / redeployed
    #
    vantiq-worker:
      data:
        token: "MA0ZNNblm_C40RAr-yoeL7joUCcG-dlkA_3xWxSpZ5K="
```

For brand-new installations it will be necessary to do the deployment in two steps. First, bring the
system up without Isolated Organization Compute support, create the access token and secret, then
deploy a second time with the worker enabled.





