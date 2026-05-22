# Vantiq Catalog Security Guide

[Vantiq Catalog](broker.md) is an Advanced Event Broker, and every Advanced Event Broker needs to offer security
mechanisms to control and monitor the access of applications connected to the broker. The key security capabilities 
offered with the Vantiq Catalog include:

* Limit which Publishers and Subscribers can see which Event Types in the catalog.
* Audit the events produced by Producers and consumed by Subscribers.
* Manage and remove connected publishers and subscribers.
* Revoke catalog access from a connected namespace.

## Catalog Connections Overview
Before diving into the Catalog Security Model, it's important to first familiarize yourself with the core security model 
of the Vantiq Platform, primarily [Profiles](resourceguide.md#profiles) and [Groups](resourceguide.md#groups).

Profiles are used to govern the authorizations between namespaces in a brokered environment. Every namespace that connects
to the catalog does so through a node, and that node uses an access token to gain access to the Catalog Namespace. That
token has a specific profile associated with it, and that profile determines which resources in the Catalog Namespace
the connected namespace can access. These nodes and tokens are automatically generated as part of the connection process
so the only thing necessary at the time of connection is a token from the Catalog Namespace (referred to as the Catalog 
Token) with Broker Member or Admin profiles. 

Once the Catalog Token is submitted through the IDE or to the **Broker.makeNodes** procedure to connect to the Catalog,
new tokens are generated in both namespaces that uniquely identify the connection and have the minimum necessary profiles.
The Catalog namespace will generate a token with the name of the form `dev_vantiq_com_<memberNamespace>_to_dev_vantiq_com_<catalogNamespace>`
and with a system profile of _brokerManager_. The token name indicates the token will be used by the memberNamespace on 
_dev.vantiq.com_ to connect to the catalogNamespace on _dev.vantiq.com_. The brokerManager profile associated with this token allows the 
Catalog namespace to access just enough resources in the member namespace to remove the member as a publisher or subscriber,
to remove their access entirely from the catalog, and to read the contents of the namespace for deployment purposes.

The connected namespace will generate a token named `dev_vantiq_com_<catalogNamespace>_to_dev_vantiq_com_<memberNamespace>`,
indicating the token is used to grant the catalog namespace access to the member namespace. This token will have the
_brokerMember_ profile, which offers lower authorizations than the brokerManager profile. The member only has enough 
access to the catalog namespace to execute existing procedures, create Event Types, and register as a publisher or 
subscriber of an existing Event Type. 

These generated tokens last forever, and are used to generate a node in the Catalog Namespace that points to the newly
connected namespace and a node in newly connected namespace that points to the Catalog Namespace. All interactions
with the catalog will be performed through these nodes. Even when the Catalog Namespace accesses its own catalog, the
operations are done through nodes. Because each node uses a uniquely generated token, all interactions between namespaces 
that are audited can be uniquely traced to the node and namespace that made the request.


## Catalog Access
By default, all namespaces connected to an Event Catalog can see all Event Types defined in the Catalog. If a namespace
can see an Event Type in the Catalog, then that namespace can register as a publisher or as a subscriber of the Event
Type. All connected namespaces can create new Event Types in the Catalog, and those Event Types are by default visible
to all connected members. 

To restrict access to specific Event Types in a Catalog, use Groups. The Catalog Namespace (and no other connected
namespace) has the ability to define and update Event Types with a Group value. The value
should be the name of a group that already exists in the Catalog Namespace. Once the Event Type has an Group value,
only members of that group will be able to see the Event Type. 

View existing Groups in the [Vantiq IDE](ide.md) under **Administer** > **Advanced** > **Groups**,
and create a new Group by clicking the plus icon in the title bar of the Group List pane. When creating a Group for 
the purposes of restricting access to Event Types in the Catalog, be sure to check the _For Catalog_ box, which will
automatically grant the Catalog Namespace access to the group. Add nodes to the group to grant the corresponding member
namespace access to Event Types in the group.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Create Group](assets/img/brokersecurity/createGroup.png "Create Group")

When editing an existing Event Type or creating a new Event Type from the Catalog Namespace there is an option to select
a group for the Event Type:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Add Event To Group](assets/img/brokersecurity/addEventToGroup.png "Add Event To Group")

After saving the Event Type with a group value, all members of the group will continue to see the Event Type and can
interact with it exactly as before. Broker members that were not added to the group will no longer be able to see the 
Event Type in the catalog.  But if they were already registered as a publisher or subscriber of the Event Type, that
relationship will not be broken by placing the Event Type in a group. To view all publishers or subscribers of an Event
Type from the Catalog Namespace, click on the name of the Event Type in question in the catalog and use the _Click To View_
links. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Manage Publishers](assets/img/brokersecurity/managePublishers.png "Manage Publishers")

From this popup, use the trash cans to remove any registered publishers (or subscribers on the corresponding subscriber 
list popup). Note that the option to remove publishers or subscribers other than yourself is only available to the 
Catalog Namespace. All other namespaces can only remove themselves.

To completely remove a members access to the catalog from the Catalog Namespace, open the Namespaces list in Operations
mode, click on the Catalog Namespace, and click the _Edit Event Catalogs_ link, which will open a popup listing all of
the connected members:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Manage Connections](assets/img/brokersecurity/manageConnections.png "Manage Connections")

From here, click the revoke button next to any connected member to remove that members access to the catalog. This will
immediately stop the member from publishing events to the catalog and also unsubscribe the member from any previously
subscribed to Event Types.

## Using The Event Ledger
Events in Vantiq are generally ephemeral. They arrive, they trigger any associated rules or apps, and then after those 
behaviors execute the event disappears. When a persistent record of all events is needed, the Event Ledger makes it easy
to record those events from a [Vantiq App](apps.md). 

The [Catalog Tutorial](tutorials/eventbroker.md) demonstrates how to use an Event Type in a catalog as the triggering
condition for an Event Stream in an App, and also shows how to register a task in App as a publisher of an Event Type.

Attach a _RecordEvent_ task to an Event Stream that is triggered by an Event Type in the catalog and the result is an app
that will record all events of an Event Type across all publishers. To record only the events produced by a single 
publisher, attach a _RecordEvent_ to a task configured to publish events to the catalog. This will only record events
produced by this one publisher, but many publishers could be registered for the Event Type. By choosing where to place
the _RecordEvent_ task, it's possible to use it to either record a single publishers activity, or record all publishers 
activity. 

It's important to note here that the Event Ledger is isolated to a single namespace, and it is not centrally managed by 
the Catalog Namespace. What events to record in the ledger is entirely up to the builders of the applications that
produce and consume events. To record all events of an Event Type as the administrator of the Catalog Namespace, create
a simple app that has a single event stream that uses the Event Type as the inbound source of events and attach a 
_RecordEvent_ task to the output like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Record Event Example](assets/img/brokersecurity/simpleLedgerApp.png "Record Event Example")

To view the Event Ledger, click the book icon next to the Event Type in question in the catalog pane. This will open a 
new pane containing all entries in the ledger, sorted by the time when the event was recorded from most recent to least
recent.
