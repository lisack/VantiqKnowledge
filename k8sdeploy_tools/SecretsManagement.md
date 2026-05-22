# Managing Sensitive Configuration for Vantiq in Kubernetes

## Overview

This document contains the details of managing sensitive configuration (aka secrets) in a Vantiq cloud installation
running on a Kubernetes (K8s) cluster, using the Vantiq *k8sdeploy_tools* deployment utilities. Such secrets include
passwords for MongoDB, Keycloak and other components, as well as credentials to access container image repositories
and backup buckets.

This sensitive configuration is ultimately stored in Kubernetes *secrets* (the resource used by K8s to hold
sensitive information). The data in each *secret* is
[Base64-encoded](https://www.redhat.com/sysadmin/base64-encoding), not encrypted, which is trivial to
decode and therefore not secure to store in places like source code management systems.

Since sensitive configuration contains information which should be protected and which cannot be safely stored
without some form of encryption, one important choice you must make when deploying a new installation is whether
to encrypt the secrets configuration stored in the YAML files in `targetCluster/deploy/secrets`. It is optional but
**strongly** recommended you do encrypt the content in secrets configuration files by setting

```
enableSealedSecrets=true
```

in your `cluster.properties` file. If you do not, the secrets configuration files will contain the same
Base64-encoded data as the output of the command `kubectl get secret <secretname> -n <namespace>`. For details
see the [Using Sealed Secrets to Manage Sensitive Configuration](#using_sealedsecrets) section below.

We recommend using non-sealed secrets only for short-term Vantiq installations, or if there is some type of
technical barrier to using sealed secrets. For details see the
[Using Non-Sealed Secrets to Manage Sensitive Configuration](#using_nonsealedsecrets) section below.

You may also use alternatives to sealed secrets to encrypt your secrets, but you must implement and maintain such
alternatives on your own (the tools only support sealed secrets to encrypt secrets).

It is possible to convert from non-sealed secrets to sealed secrets by following the procedure in the
[Converting To Sealed Secrets](#converting_to_sealed) section below, but it is simpler to just start by
using them when you first create the new Vantiq installation rather than converting later.

See the [Sealed Secrets repo](https://github.com/bitnami-labs/sealed-secrets) for broader details on how sealed
secrets work, and why they are a good idea when storing K8s configuration in a SCM repo like `k8sdeploy_clusters`.

&nbsp;

## Table of Contents

* [Overview](#overview)
* [`secrets.yaml`](#secretsdotyaml)
    * [Overview of `secrets.yaml`](#secretsdotyaml-overview)
    * [`secrets.yaml` Basics](#secretsdotyaml-basics)
    * [`secrets.yaml` Key Details](#secretsdotyaml-keys)
        * [Details of multiple options for Vantiq installation secrets](#vantiq-key-options)
    * [Running the `generateSecrets` Task](#run_generatesecrets)
* [Step-By-Step References](#sbs-references)
    * [Using Sealed Secrets - Step-By-Step Reference](#using_sealedsecrets)
        * [You Need to Maintain the Sealed Secrets Controller](#maintain_sealedsecrets_controller)
    * [Using Non-Sealed Secrets - Step-By-Step Reference](#using_nonsealedsecrets)
    * [Converting To Sealed Secrets - Step-By-Step Reference](#converting_to_sealed)

&nbsp;

<a name="secretsdotyaml"></a>
## `secrets.yaml`

<a name="secretsdotyaml-overview"></a>
### Overview of `secrets.yaml`

As noted above, the use of [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets/) to encrypt the
configuration of secrets is optional but recommended. Regardless of whether you use sealed secrets or non-sealed
secrets, the sensitive configuration is managed independently from its non-sensitive counterpart in `deploy.yaml`.
The `secrets.yaml` file is where the sensitive configuration is defined.

The general process is as follows:

* Enter the sensitive configuration values in the `secrets.yaml` file.
* Run the `generateSecrets` task to consume the information in `secrets.yaml` and create the secrets YAML config
files in `targetCluster/deploy/secrets`. Later, the config in these files will be pushed to the cluster to create
the actual secrets as part of the `deployShared` and `deployVantiq` tasks described below.
* Delete the initial input files as they are no longer needed. This last step is not strictly necessary, but it is
a good practice since retaining the information is not necessary and only creates a potential risk.

Note that the YAML files which the `generateSecrets` task creates in `targetCluster/deploy/secrets` will contain
different data for sealed secrets vs. non-sealed secrets:

* If you **are not using** sealed secrets, these files will be plain *secrets* definitions, containing
[Base64 encoded](https://www.redhat.com/sysadmin/base64-encoding) values of the plaintext values in `secrets.yaml`.
This is the same data you should see if you later run `kubectl get secret XXXXX -o yaml` to output the contents
of a secret in the cluster.
* If you **are using** sealed secrets, these files will be encrypted *sealedsecrets* definitions created by `kubeseal`
interacting with the sealed secrets controller running on the cluster. When the `deployShared` and `deployVantiq`
tasks push the config in these files to the cluster, that will create *sealedsecrets* which will cause the sealed
secrets controller to create a matching *secret* for each *sealedsecret*.

<a name="secretsdotyaml-basics"></a>
### `secrets.yaml` Basics

When you run the `setupCluster` task, a template for `secrets.yaml` is copied to your `targetCluster` directory.
The primary copy of this template lives in the `bootstrap` directory of this repo, so you can get a fresh copy
from there at any point. This file has 3 main sections, one for each sub-system. Under each section there are
keys for the expected *secrets*. Under that you will find keys used to actually provide the credentials. See
the next section for details on all the keys that can currently be defined in `secrets.yaml`.

Most of these are defined as the actual credentials themselves directly in `secrets.yaml`, but in some cases they
instead refer to files that must be placed under the `targetCluster` directory. For example, when dealing with SSL
certificates we need both the cert and its associated key. These are typically distributed as files, so that is
how we consume them. We provide a default location `targetCluster/deploy/certificates` for certificates. That
directory comes pre-configured with a `.gitignore` file so the files do not get merged into your cluster
definition (since they should not be exposed directly).

There are other secrets that use files as their source such as `dbbackup-creds` and `vantiq-push`. The source
files for these secrets are typically stored in the `targetCluster/deploy/sensitive` directory (which likewise
should contain a `.gitignore` file so the files do not get merged into your cluster definition). The important
thing to remember is that the reference to these files in `secrets.yaml` must match the directory and be
relative to `targetCluster`, such as setting the value for the `vantiq-push.files.vantiqConfig.json` key to
something like `deploy/sensitive/vantiq-push.txt`.

**Pro tip:** As is true for the rest of the deployment process, it is possible to specify credentials
incrementally instead of all at once. The main requirement is that before you can deploy a given subsystem, you
must have generated all of the secrets used by that subsystem. The `generateSecrets` task however can be used to
generate any number of secrets at one time. This allows you to update individual secrets as needed when their
values change, for example to update the SSL certificate or Vantiq license secrets. In such cases, you only put
the new or changed secrets `secrets.yaml`. Then when you run `generateSecrets` it will only generate new files
in `targetCluster/deploy/secrets` for the secrets defined in `secrets.yaml` and leave the others untouched. When
you then run `deployShared` or `deployVantiq` you will notice in the task output that only the updated secrets
will be updated on the cluster and the remaining ones will be unchanged.

<a name="secretsdotyaml-keys"></a>
### `secrets.yaml` Key Details

The following secrets keys should be entered in the matching location in `secrets.yaml`, following the template
data already in place as described above.

In the table below each key is referenced by its path, and notice that multiple keys can go into a secret. The
first part of a path is either `shared` for the `shared` namespace, or `vantiq` which can map to either all
Vantiq namespaces (`vantiq.common`) or specific Vantiq namespaces which match the installations (`vantiq.ins1`,
`vantiq.ins2` etc., see the note below the table for details).

For example, the keys with paths `shared.keycloakdb.data.username` and `shared.keycloakdb.data.password` go
into the `keycloakdb` secret in the `shared` namespace, and the relevant part of `secrets.yaml` for these
would look like this::

```yaml
shared:
  keycloakdb:
    data:
      username: myKCUsernameValue
      password: myKCPasswordValue
```

The following secrets keys can be entered in `secrets.yaml`:

| Secret | Namespace | Key Path | Purpose |
|--------|-----------|----------|---------|
| grafanadb | shared | shared.grafanadb.data.mysql-root-password | The root password for the MySQL database used by Grafana to store its config data. |
| grafanadb | shared | shared.grafanadb.data.mysql-password | The password for the user account used by Grafana to access the MySQL database used to store Grafana config data. This is applied to the MySQL instance itself. |
| grafanadb | shared | shared.grafanadb.data.GF_DATABASE_PASSWORD | The password for the user account used by Grafana to access the MySQL database used to store Grafana config data. This is applied to the Grafana deployment and must match the value of `shared.grafanadb.data.mysql-password`. |
| influxdb | shared | shared.influxdb.data.influxdb-user | The username for the admin account for InfluxDB. |
| influxdb | shared | shared.influxdb.data.influxdb-password | The password for the admin account for InfluxDB. |
| keycloak | shared | shared.keycloak.data.username | The admin username for Keycloak itself (not the username to access the Postgres database used by Keycloak). This is set to `keycloak` by default and normally does not need to be set in `secrets.yaml`. |
| keycloak | shared | shared.keycloak.data.password | The admin password for Keycloak itself (not the password to access the Postgres database used by Keycloak). |
| keycloakdb | shared | shared.keycloakdb.data.username | The username for the user account used by Keycloak to access the Postgres database used to store Keycloak data. This is set to `keycloak` by default and normally does not need to be set in `secrets.yaml`. |
| keycloakdb | shared | shared.keycloakdb.data.password | The password for the user account used by Keycloak to access the Postgres database used to store Keycloak data. |
| dbbackup-creds | *installation namespace(s)* | vantiq.common.dbbackup-creds.files.credentials | The credentials file used to access the backups bucket. The contents of the file varies by cloud provider. |
| influxdb | *installation namespace(s)* | vantiq.common.influxdb.data.influxdb-user | The username for the admin account for InfluxDB. Must match `shared.influxdb.data.influxdb-user`. |
| influxdb | *installation namespace(s)* | vantiq.common.influxdb.data.influxdb-password | The username for the admin account for InfluxDB. Must match `shared.influxdb.data.influxdb-password`. |
| keycloak | *installation namespace(s)* | vantiq.common.keycloak.data.username | The admin username of Keycloak, used by Vantiq to access Keycloak. Must match `shared.keycloak.data.username`. This is set to `keycloak` by default and normally does not need to be set in `secrets.yaml`. |
| keycloak | *installation namespace(s)* | vantiq.common.keycloak.data.password | The admin password of Keycloak, used by Vantiq to access Keycloak. Must match `shared.keycloak.data.password`. |
| keycloak | *installation namespace(s)* | vantiq.common.keycloak.data.stmp.password | The password for the SMTP account used by Keycloak to send email. |
| mongodb | *installation namespace(s)* | vantiq.common.mongodb.data.user | The admin username of MongoDB for this installation. Normally set only at the installation level. |
| mongodb | *installation namespace(s)* | vantiq.common.mongodb.data.password | The admin password of MongoDB for this installation. Normally set only at the installation level. |
| registry-creds | *installation namespace(s)* | vantiq.common.registry-creds.registry.server | The server URL for image registry used to store the container images we use for the installation pods. |
| registry-creds | *installation namespace(s)* | vantiq.common.registry-creds.registry.username | The username for the account used to access the container image registry. |
| registry-creds | *installation namespace(s)* | vantiq.common.registry-creds.registry.password | The password for the account used to access the container image registry. |
| vantiq-license | *installation namespace(s)* | vantiq.common.vantiq-license.files.public.pem | The `public.pem` file of the Vantiq license for this installation. Should only be set at the `vantiq.common` level if the license contains all FQDNs for all installations in the cluster. |
| vantiq-license | *installation namespace(s)* | vantiq.common.vantiq-license.files.license.key | The `license.key` file of the Vantiq license for this installation. Should only be set at the `vantiq.common` level if the license contains all FQDNs for all installations in the cluster. |
| vantiq-push | *installation namespace(s)* | vantiq.common.vantiq-push.files.vantiqConfig.json | The files used to create the `vantiqConfig.json` and `firebase.json` files used by Vantiq, containing all of the push notification secrets used by push sources such as APNS and Firebase. |
| vantiq-ssl-cert | *installation namespace(s)* | vantiq.common.vantiq-ssl-cert.files.tls.crt | The certificate chain file for the SSL certificate for the installation. This needs to contain the certificate for the installation FQDN(s), as well as any intermediate certificates in the chain up to the CA that issued the certificate. Should only be set at the `vantiq.common` level if the certificate contains all FQDNs as SANs for all installations in the cluster. This is required if not using cert-manager to obtain free SSL certificates from Let's Encrypt (if using cert-manager, note that cert-manager controls this secret not `secrets.yaml`). |
| vantiq-ssl-cert | *installation namespace(s)* | vantiq.common.vantiq-ssl-cert.files.tls.key | The private key file for the SSL certificate for the installation. Should only be set at the `vantiq.common` level if the matching `vantiq.common.vantiq-ssl-cert.files.tls.crt` certificate contains all FQDNs as SANs for all installations in the cluster. This is required if not using cert-manager to obtain free SSL certificates from Let's Encrypt (if using cert-manager, note that cert-manager controls this secret not `secrets.yaml`). |
| vantiq-worker | *installation namespace(s)* | vantiq.common.vantiq-worker.data.token | The Vantiq token used by the `vantiq-worker` pod to access the Vantiq installation to check if there are changes which need to be made to the Kubernetes cluster from Vantiq. This will need to be set if the installation uses IOC, service connectors (for AI or otherwise) or anything else being deployed to Kubernetes from Vantiq. |

<a name="vantiq-key-options"></a>
#### Details of multiple options for Vantiq installation secrets

In a cluster containing multiple installations, there are multiple options for specifying the Vantiq
installation secrets. Note that all such keys are shown in the table above with a path starting with
`vantiq.common` meaning they can be set at that level, but they can also be set at the installation level.

Any secrets that are set at the `vantiq.common` level will set the value the same for all installations.
Setting it instead at the `vantiq.<installation>` level (`vantiq.<installation>.xxx.yyy.zzz` instead of
`vantiq.common.xxx.yyy.zzz`) will set the value just for that installation. These can also be mixed: if a
secret is set at the `vantiq.common` level its value will be used for all installations, except ones that
also have that same value set at the installation level (the installation level takes precedence over
the common level).

For example, let's say we have the `dev`, `test` and `prod` installations in a cluster. We want to set the
`registry-creds` secret values the same for all installations, the `mongodb` secret the same for `dev` and
`test` but have a different one for `prod`, and have the `mongodb-keyfile` secret be different for all three
installations. The relevant part of `secrets.yaml` to accomplish this would look like:

```yaml
vantiq:
  common:
    registry-creds:
      registry:
        server: quay.io
        username: myQuayIOUsername
        password: 1I70NJG0Z9DKNIR3LAZSKTREKGVL22GWXN03TXS1VEZHHRWJLT5U247D9NCVSXQP
    mongodb:
      data:
        user: root
        password: mySecretSharedMdbPW
  dev:
    mongodb-keyfile: 
      data:
        key.txt: chmz9j8hISuV7HVFlLEy23FNQiUruuO
  test:
    mongodb-keyfile: 
      data:
        key.txt: 2P6IHsUMoVjZElYEuhwA2of3nzIxmkh
  prod:
    mongodb:
      data:
        user: root
        password: mySecretProdMdbPW
    mongodb-keyfile: 
      data:
        key.txt: X3fcqmG0Z1JAzyDNOjveUZoe5DcSrDr
```

<a name="run_generatesecrets"></a>
### Running the `generateSecrets` Task

Once the credentials have been provided in `secrets.yaml`, the next step is to run the `generateSecrets` task as
described in the
[Managing Sensitive Configuration section of the Installation doc](Installation.md#managing_sensitive).
This will use the data you provided to generate the YAML files required by K8s under the
`targetCluster/deploy/secrets` directory as described above.

Once the `generateSecrets` task is done generating these files, you should check them into the repo associated with
the `targetCluster` directory (along with the `deploy.yaml` file and other configuration files).

Again, if you **are not using** sealed secrets, the secrets YAML files will be plain *secrets* definitions,
containing [Base64 encoded](https://www.redhat.com/sysadmin/base64-encoding) values of the plaintext values in
`secrets.yaml`. This is not secure, and is why you should use sealed secrets so the secrets YAML files will be
encrypted.

&nbsp;

<a name="sbs-references"></a>
## Step-By-Step References

<a name="using_sealedsecrets"></a>
### Using Sealed Secrets - Step-By-Step Reference

The detailed steps to use sealed secrets to manage sensitive configuration in a Vantiq installation as you deploy it:

1) Set the `enableSealedSecrets` property in `cluster.properties` to `true` as noted in the
[the Setting Cluster Properties section of the Installation doc](Installation.md#setting-cluster-properties).
1) Run the `setupCluster` task as noted in the
[the One-time Setup of Cluster section of the Installation doc](Installation.md#onetime_setup). This will update
the cluster to add the [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) controller, and create several
files under `targetClusters` including a template version of `secrets.yaml`.
1) Confirm that the sealed secrets controller is deployed (in the `kube-system` namespace) and that its pod is running.
Once the pod is running, run the `configureSealedSecrets` task.
1) [Extract the cluster's private sealing key](https://github.com/bitnami-labs/sealed-secrets#how-can-i-do-a-backup-of-my-sealedsecrets)
and store it somewhere secure. The private sealing key is required if you ever need to reconstruct the cluster,
but exposure of the key puts your sealed secrets at risk so store it in a secure manner similar to your cloud
admin credentials.
1) Enter all of the sensitive configuration to the appropriate location in `secrets.yaml` as described above in the
[`secrets.yaml` Basics](#secretsdotyaml-basics) and [`secrets.yaml` Key Details](#secretsdotyaml-keys) sections.
1) Run the `generateSecrets` task. This will create the necessary sealedsecrets YAML files in
`targetCluster/deploy/secrets` using the provided sensitive configuration.


<a name="maintain_sealedsecrets_controller"></a>
#### You Need to Maintain the Sealed Secrets Controller

Please note that, while the `setupCluster` task will do the initial deployment of the sealed secrets controller
if you have the `enableSealedSecrets` property set to `true` in `cluster.properties` when that task is run, the
tools will not make any further changes to the sealed secrets controller.

Maintaining the sealed secrets controller is a task that you must do yourself, the tools will not do that for
you. You should periodically update the sealed secrets controller to the current version, and keep track of
any changes to it that may be needed when you do Kubernetes upgrades.


<a name="using_nonsealedsecrets"></a>
### Using Non-Sealed Secrets - Step-By-Step Reference

The detailed steps to use non-sealed secrets to manage sensitive configuration in a Vantiq installation as you deploy
it:

1) Set the `enableSealedSecrets` property in `cluster.properties` to `false` (or just leave the `enableSealedSecrets`
line commented out since `false` is the default) as noted in the
[the Setting Cluster Properties section of the Installation doc](Installation.md#setting-cluster-properties).
1) Run the `setupCluster` task as noted in the
[the One-time Setup of Cluster section of the Installation doc](Installation.md#onetime_setup). This will create
several files under `targetClusters`, including a template version of `secrets.yaml`.
1) Enter all of the sensitive configuration to the appropriate location in `secrets.yaml` as described above in the
[`secrets.yaml` Basics](#secretsdotyaml-basics) and [`secrets.yaml` Key Details](#secretsdotyaml-keys) sections.
1) Run the `generateSecrets` task. This will create the necessary secrets YAML files in
`targetCluster/deploy/secrets` using the provided sensitive configuration.

<a name="converting_to_sealed"></a>
### Converting To Sealed Secrets - Step-By-Step Reference

To switch from using non-sealed secrets to sealed secrets to manage sensitive configuration in a cluster, do the
following:

1) Set the `enableSealedSecrets` property in `cluster.properties` to `true` and run the `setupCluster` task. This
will update the cluster to add the [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) controller.
1) Confirm that the sealed secrets controller is deployed (in the `kube-system` namespace) and that its pod is running.
Once the pod is running, run the `configureSealedSecrets` task.
1) If you don't still have a copy of your original `secrets.yaml` file, recreate it by combining the `secrets.yaml`
template file from the `bootstrap` directory and the Base64-decoded secrets from the installation.
1) Set the `enableSealedSecrets` property in `cluster.properties` to `false` and run the `generateSecrets` task.
This will generate non-sealed versions of the secrets under `targetCluster/deploy/secrets`.
1) Run the `removeSecrets` task.
1) Set the `enableSealedSecrets` property in `cluster.properties` to `true` and re-run the `generateSecrets` task.
This will replace the non-sealed secrets with sealed versions specific to your cluster.

At this point you have the correct, fully secure definition of your cluster. You should add all changes to a
commit and merge that into your cluster's central definition, after appropriate code review.

### Historical Note: Non-sealed Secrets in `deploy.yaml`

The above secrets management options using `secrets.yaml` require Vantiq System (k8sdeploy) version 3.3 or greater.
If you were to use a version prior to 3.3 you would need to manage the credentials directly in the `deploy.yaml`
file. To our knowledge, as of this writing in 2023 there is no one using such an old k8sdeploy version (nor should
they). The fact that secrets used to be contained in `deploy.yaml` instead of `secrets.yaml` is only noted here for
historical purposes, and in case anyone decides to use a k8sdeploy version < 3.3 which is not recommended.

