# Availability Monitoring - Monitor Provisioning

***Last updated 28 May 2024***

Availability Monitoring is composed of two distinct pieces acting together: a Vantiq monitor project installed
on a monitoring site and a Vantiq heartbeat project installed on the site to be monitored. This document is about
the monitor project, explaining how to add a monitor to a Vantiq monitoring site. A different document,
[`Heartbeat Provisioning`](AvailablityMonitoring_AsUser.md) explains how to install a heartbeat.

The reader of this document acts as *Vantiq Support*, below referred as *Support*. The person provisioning
a heartbeat is referred below as the *User*.

## Prerequisites

Acting as *Support*,

- decide on a `monitor name` and a `monitor friendly name`. `monitor name` is a short string value
characterizing the site to monitor while `monitor friendly name` - used in email notifications - can be more
descriptive. You might discuss these names with the *User* installing the heartbeat.
- you might discuss any additional person that should receive Availability email notifications
- decide on the `monitoring site` that will do the monitoring, typically `api.vantiq.com`
- log into the monitoring site namespace `vantiq_monitor` and create a new Token. Suffix the Token name with
the new monitor name, setting the Token to never expire (e.g., expiring decades from now)
- provide the *User* with,
  - `monitor name`
  - `monitoring site URL` (e.g., `https://api.vantiq.com`)
  - Token value. Token value must be provided out of band in a secure fashion
  
With this information, the *User* can follow the instructions from the `Heartbeat Provisioning` document to install
a heartbeat on the site to monitor. Note that the `monitor name` must be unique across all monitor names, 
uniquely identifying the site to be monitored.

## Monitor setup

The below instruction steps use the following name conventions,

- `<rule_name>` - name used to suffix the Monitor Rule name (e.g., AcmeDev for `monitorAcmeDev`)
- `<monitor_name>` - monitor name you decided on and provided to the user. This same name is also used as the Monitor
and Availability types name property (e.g., `acme-dev`)
- `<monitor_friendly_name>` - name you decided on with the user, used in emails and logs (e.g., "Acme Dev")

On the monitoring site,

- switch to `vantiq_monitor` namespace and select the Monitoring project
- create Rule `monitor<rule_name>` by copying the `monitorTemplate` Rule, or copying an existing `monitorXXX` Rule
(with a "/topics/heartbeat/signal" in the WHEN clause)
  - update the WHERE clause with the `<monitor_name>` value
  - update the `heartbeatReceived` and `heartbeatMissing` procedure parameters with the `<monitor_name>` and
  `<monitor_friendly_name>` values
- save the Rule, as non-activated
- use `addInstallation` procedure to add a `<monitor_name>` record to the Monitor type. When calling `addInstallation`
procedure, use the `<monitor_name>` value as the name parameter, specify the monitored site URL and change the start
parameter Value Type to Date Type.
- edit the added Monitor record to add the email addresses of the `operators`
- make sure that you receive the monitored site heartbeats (i.e., the *User* must have provisioned the site to monitor)
then activate the `monitor<rule_name>` Rule

Last but not least,

- Update the VCS `vantiqApps/Monitor` project with the newly added Monitor.

Note that if you are setting up a brand new monitoring system, you must also create a scheduled event named
`monitorEvent` that publishes to the `/monitor/monitor` topic. Make it active and set its interval to 1 minute.
If the monitoring system already exists and you are simply adding a new monitored system, the `monitorEvent` scheduled
event should already exist.

If you create a new monitoring system, the attached project [`MonitorTemplate.zip`](MonitorTemplate.zip) can be used
as a starting point.

## VCS

Whenever a new Monitor is added, or more generally whenever changes are made to the Vantiq `Monitor` project on `API`, changes should be checked in into GitHub.

- create an Issue in `k8sdeploy_tools` describing the project changes
- make sure that your master branch is up-to-date (e.g, `git pull`)
- create a branch for your changes,
  - `git checkout -b <user>-change-descriptive-branch-name-#<issue>`
    - for example for user `jcg` and issue `123`, `git checkout -b jcg-monitor-added-tdd-#123`
- start the local VCS server
  - `vantiq-cli VCSSERVER`
- within the `vantiq_monitor` namespace on `API`
  - ensure that the project is saved with your changes
  - select `Projects/Sync Project to VCS...`
  - enter the VCS Directory value, assuming `<repo_path>` is your local path for your GitHub repositories, you would enter:
    - `<repo_path>/k8sdeploy_tools/vantiqApps`
  - Click `Sync Project to Directory`, changed files are saved to your local repository
  - issue git commands to commit your changes (only files with changes should appear in the commit list)
    - `git add --all`, `git status`, `git commit -m "<commit message>"`
  - push branch to GitHub and create a PR
    - `git push -u origin <user>-change-descriptive-branch-name-#<issue>`
  - get approval and merge PR

## Example

A development Vantiq installation is deployed for the company Acme as a Vantiq Managed Private Cloud.
Alice is responsible to provision the heartbeat on the monitored site.

*Support* decided on the monitor name `acme-dev` and agreed with Alice to use `Acme Development` as the friendly name.
Alice also told *Support* that bob@dev.acme.org should receive availability notifications.

Monitoring will take place on `api.vantiq.com` so *Support* provided the url `https://api.vantiq.com` along
with a Token value (a newly created Token in the `vantiq_monitor` namespace, named `TokenAcmeDev`).

- `monitor name`: acme-dev
- `monitor friendly name`: Acme Development
- `monitoring URL`: https://api.vantiq.com
- `authentication token`: G8eSb5XF38uuaraVkn5E6IC0U4YXhEyAQ278cLHjd4E=  *(token example)*
- additional `operator`: bob@dev.acme.org

On the monitoring site, in API `vantiq_monitor` namespace, *Support* does the following:

- add a new Rule:
    // Acme Dev Private Cloud
    RULE monitorAcmeDev
    WHEN EVENT OCCURS ON "/topics/monitor/monitor" BEFORE EVENT OCCURS ON "/topics/heartbeat/signal" AS heartbeat
        WHERE heartbeat.value.name == "acme-dev" WITHIN 60 seconds
    heartbeatReceived("acme-dev", "Acme Development")
    TIMEOUT
    heartbeatMissing("acme-dev", "Acme Development")

- execute `addInstallation` with the monitored site URL (e.g., `https://dev.acme.org`) and `acme-dev`
for the name parameter
- edit the new `acme-dev` Monitor record to define the list of operators, including `bob@dev.acme.org`
- check that a heartbeat is received from the monitored site, then activate and save the `monitorAcmeDev` Rule.

## Template project

On `api.vantiq.com` in the `vantiq_monitor` namespace, a `monitorTemplate` Rule can be found in the Monitor project.
