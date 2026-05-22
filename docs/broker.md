# Vantiq Catalog Reference Guide

## Overview
The Vantiq Catalog connects Namespaces across a distributed Application to quickly and easily execute operations and copy resources between Namespaces. It has three sub-catalogs that focus on different features: the Event Catalog, the Service Catalog, and the Assembly Catalog.

The Event Catalog offers a sophisticated event ledger for recording events as they are published and/or delivered to subscribers. The event ledger takes advantage of the powerful transformation and augmentation facilities available in the Vantiq system to record precisely the desired information in the ledger.

The Service Catalog allows a Namespace to publish a set of high level Procedures and Service Events to the Catalog. Subscribers may treat the Service as an interface, calling Catalog Service Procedures as if they exist in their own Namespace. The Service Catalog provides logical and functional connectivity between Namespaces operating on analogous Applications.

The Assembly Catalog lets users install resources from a central location, and keep those resources up-to-date with any fixes or changes. Subscribers have a full, read-only copy of all the resources published by the publisher namespace.

The Vantiq Catalog provides a full set of security features for fine grained control of publishers and subscribers.

For a more structured walk-through of building an application with the Vantiq Catalog, please review the [Vantiq Catalog Tutorial](tutorials/eventbroker.md).

## Terminology
There are some core concepts in the Catalog that need to be defined to avoid confusion.

* Namespace - a Namespace is the unit of isolation within Vantiq. Each Catalog resides in a single Namespace that 
is isolated from all publishers and subscribers. Namespaces connected to the Catalog can act as publishers and 
subscribers. Applications that wish to publish and/or subscribe to Event Types or Services authenticate into a Namespace
that is connected to a Catalog.
* Event Catalog - The list of Event Types that are managed by the Catalog. Event Types are identified by a name which is also 
known as a Topic in the Catalog.
* Service Catalog - The list of Services that are managed by the Catalog. Services are identified by their name, which is 
also the prefix for the Procedures used. 
* Catalog Namespace - A Namespace that hosts a Catalog. This stores information on every entry in the Catalog, such as
Event Types or Services.
* Event Type - An entry in the Event Catalog that defines an identifier for the Event Type, a schema which the events 
should conform to, and metadata for identifying the Event Type in the Catalog.
* Service - An entry in the Service Catalog that holds information on the Service's publisher and the Procedures that
are part of the Catalog.
* Publisher - A Namespace connected to a Catalog that produces events or holds the Procedures for a Service.
* Subscriber - A Namespace that has requested receipt of all events of an Event Type or use of a Service in the Catalog.
* User - a user authorized to access the Catalog. A user authenticates with their provisioned access credentials or with an 
access token supplied to the user by a user with sufficient privileges to create an access token. An application that 
publishes or subscribes to Catalog events must be associated with a User either through an access token or by having the 
user using the application supply their credentials to authenticate with the Catalog.
* Manager Namespace - A Namespace with sufficient authorizations in the Catalog Namespace to administer the Event 
Catalog.
* Member Namespace - A user with sufficient authorizations in the Catalog Namespace to use the Catalog to 
subscribe, publish or create new Event Types and Services.

## Configuring the Vantiq Catalog

### Provisioning Vantiq Catalog Users
Catalog users are created and managed using the [Vantiq User Editor](namespaces.md#adding-a-new-user-to-an-organization)

### Provisioning Catalogs
The Catalog is a central location where Event Types are 
defined and Services published. The Catalog is hosted in the Catalog Namespace, but can be viewed by any Namespace 
connected to the Catalog Namespace. An Organization can host many Catalogs, but each Namespace can only host
at most one Catalog. Individual Namespaces can be connected to many Catalogs.

Vantiq recommends starting with a single Catalog so that all Catalog users will have access to a complete, global 
view of the available Catalog entries within the organization. Once additional experience is gained, it may make 
sense to define more specialized Catalogs.

At least one Catalog must be created. The Catalog is created by first creating a Namespace to hold the Catalog. 
The Namespace name will serve as the Catalog name. A Catalog is created by using the Administer>Advanced>Catalog menu item.
To create a Catalog in this Namespace, click the **Create Catalog** button.

#### Enabling Edge Connections

Catalogs can accept connections from edge nodes. This is not enabled when created through the UI, but the setting can be changed at any time by navigating to Administer>Advanced>Catalog and toggling the "Allow Edge" box for the catalog namespace. Disabling it will forcibly disconnect all edge members.

Note that this may force the catalog namespace to perform work on the connections. Since edge nodes cannot directly talk to each other, the catalog namespace will act as a bridge for any Services and Event Types that have edge members as both publishers and subscribers.

### Connecting To A Catalog
A Namespace must be connected to the Catalog to be able to search the entries as well as to publish or subscribe to
events and Services.

When a Namespace needs to be connected to an existing Catalog in a different Namespace, use the **Show>Catalogs** menu item to display the _Catalogs_ pane. Click the **New** button to create a new Catalog connection.

To connect to the Catalog Namespace, you will need an Access Token that was created in the Catalog Namespace, which 
must be generated by the Catalog Namespace administrator. The Catalog administrator must deliver this token to the 
user desiring to gain access to the Catalog. This token will be used to make the initial connection between the
Broker Member Namespace and Catalog Namespace. During this initial connection, new Access Tokens and Nodes are 
generated in both Namespaces in order to create a permanent connection that can be uniquely identified. The token used 
to make the initial connection between Namespaces is not reused, so the Catalog Namespace administrator should make 
those tokens relatively short lived.

#### Connecting From an Edge Installation

If you are connecting from an edge installation, you must check the "Connect using VQS" box if using the UI or set the `useVQS` value to true when connecting to the catalog. Not all catalogs will allow edge connections. If you need to connect from an edge installation and the catalog does not allow it, you will need to contact the catalog owner and ask them to enable it.

#### Repairing Catalog Connections

There are some situations in which tokens or nodes used by the catalog can break or disappear. You can repair the connections using [this operation](brokerapi.md#repair-catalog).

This can be done through the UI as well. When selecting Show>Catalogs, you can right-click on a catalog and select Repair. This will reconnect you to the catalog and any other members as necessary, and will also update any services or event types the namespace is using. Both the URI and the token are optional, but if neither is provided then it requires the catalog connection to be working, and if only the token is provided then the catalog node must still exist and have the correct URI.

### Public Catalogs

In some cases it may be more convenient to make a catalog available to an entire Organization or installation, instead of providing credentials to each namespace individually. In these cases, the Catalog administrator may provide a longer-lived access token to an Organization administrator. The Org admin can then, in the Organization namespace, go to **Administer>Advanced>Catalog**, click **New**, and fill in the Catalog token and url.

![createPublicCatalog](assets/img/brokerref/createPublicCatalog.png)

Once this is done, an administrator in any of the Org's namespaces can connect to the catalog by navigating to **Show>Catalogs**, clicking **Connect**, selecting "Public Catalog", and picking the catalog.

![connectPublicCatalog](assets/img/brokerref/connectToPublicCatalog.png)

### Viewing The Catalog
To browse the contents of a Catalog, use the **Show>Catalogs** menu item, then click the name of the catalog in the list. Here's an example view of what the
Catalog looks like in the IDE:

![eventCatalog](assets/img/brokerref/catalog.png "Event Catalog Example")

The screenshot illustrates a collection of entries in the Event Catalog for Acme Industries. Note
the name in the title bar of the Catalog pane is "AcmeIndustries". This is because the Catalog Namespace for this 
Catalog is the AcmeIndustries Namespace. 


#### Searching The Catalog
The example Catalog shown above uses a hierarchical naming scheme where events are organized by resource (e.g. employee, 
machine, and sensor). Hierarchical names make the Catalog easier to search along the dimensions represented by the 
hierarchy. This is just an example convention. Any hierarchical naming convention can be used.

Searches are specified using the search bar at the top of the Catalog. The search term
is checked against the entry name, description, schema type name, and the tags for any partial matches.

#### Catalog Actions
Entries in the Catalog have the following Actions available. 

**View Ledger** - looks like a closed book, and runs a query for all entries in the ledger. The results 
are displayed in a newly opened pane. 

**Subscribe** - looks like a play button in a circle, subscribes the current Namespace to 
the entry.
 
* Subscribing to an Event Type through the Catalog adds a topic to the current Namespace, which will 
receive all events of that Event Type. To view a live stream of the events, click on the topic in the project resource
graph and click the play button in the topic pane's title bar. 
* Subscribing to a Service adds Procedures to the current
Namespace. To view information on the Procedures, select **Add** > **Services** in the top of the Development bar.

**Unsubscribe** - looks like a pause button, terminates the current subscription to the entry. The unsubscribe
button will only show up under actions if there is an active subscription to the entry in the current Namespace. 

**Delete** - removes the entry from the Catalog and removes all publishers and subscribers. 
* For Event Types they
are no longer visible across the Catalog environment. The events may still be generated in the publisher Namespace, but
no applications that consume the events through the AEB will see the event. Only admins in the Catalog Namespace
can remove Event Types from the Catalog. Removing Event Types may impact running production apps and so permission to 
remove Event Types is restricted from every other Namespace.
* For Services only the publisher or the Catalog Namespace admin can remove the entry, and doing so will remove the 
subscribed Procedures from each subscriber.

**<entry name\>** - clicking the entry name navigates to the detail pane for the Event Type or Service.

**Graph** - Visualize publishers and subscribers of entries in a graph.  
 - If this action is performed in a Catalog member Namespace, only Event Types used by this Namespace are displayed in 
 the graph.
 - If this action is performed in the Catalog Namespace, selected entries are displayed in the graph. All publishers
  and subscribers of each entry are also displayed in graph.  If no entry is selected, users are given the option to 
  graph all entries within the Catalog.  For example, after completing the  [Vantiq Catalog Tutorial](tutorials/eventbroker.md),
  the Event Type graph looks like the following:
  ![eventGraph](assets/img/brokerref/eventTypeGraph.png "Event Type Graph")

### Setting Permissions

Permissions can be set for each operation available in a catalog. If a member tries to perform an operation it does not have permission to do, the system will throw an error.
The default permissions can be set in the host's Catalog resource, and per-member permissions can be set in the relevant Member resource. The Catalog resource must have a value for each operation, but the Member resource only requires a value where it will override the Catalog's default permissions. It is suggested that the default permissions are set to the most restrictive settings you will use, and then expanded on a per-member basis.

In the Vantiq IDE, this is managed through the _Manage Catalogs_ pane in the Catalog Namespace, accessed through **Administer\>Advanced\>Catalogs**. Select **Edit Permissions** for the catalog namespace to change the defaults or for a member namespace to change its specific permissions.

Note that changing permissions only affects *future* registrations, not existing ones. E.g. if a member publishes a service and then you remove service publishing permissions for that member, the service will still be published and other members can still subscribe to it.

![Manage Catalogs Pane](assets/img/brokerref/manageCatalog.png "Manage Catalogs Pane")

#### Format

The permissions are stored as an Object in the *catalogPermissions* field of Members and Catalogs. The value `true` gives permission for the operation, `false` denies permission. The format and default values are below.

```json
{
	"service": {
		"publish": true,
		"subscribe": true,
		"createEntry": true,
		"removeEntry": true
	},
	"event": {
		"publish": true,
		"subscribe": true,
		"createEntry": true,
		"removeEntry": false
	},
	"assembly": {
		"publish": true,
		"install": true,
		"createEntry": true,
		"removeEntry": true
	},
	"semanticindex": {
		"publish": true,
		"subscribe": true,
		"createEntry": false,
		"removeEntry": false
	}
}
```

### Types in the Catalog

Both Event Types and Services may have types associated with them. If an entry uses a type, that type must exist in the catalog namespace as well as any publishing and subscribing namespaces. When such a type does not exist in the relevant namespace, it is created there with its role set to "schema".

Types are created in the catalog namespace when:

* An Event Type is created or updated.
* A Service is published and has a typed parameter, return type, or event type using a user-defined type.
* A published Service is updated and has a typed parameter, return type, or event type using a user-defined type.

Types are created in a member namespace when:

* It publishes or subscribes to an Event Type.
* It subscribes to a Service that has a typed parameter, return type, or event type using a user-defined type.
* It updates a subscribed Service that has a typed parameter, return type, or event type using a user-defined type.

#### Type Compatibility

When a catalog action would create a new type, it may conflict with an existing type in the namespace. In this case the types are compared, and if they are compatible the existing type has its fields updated. Types are compatible if:

* The new type has all the fields of the existing type, and the sub-properties of each field match.
* Any fields that are in the new type but not the existing type are not required.

Put simply, types are compatible if the only changes are new, non-required fields. 

### Import and Export of Catalog Connections
Catalogs are a Vantiq resource and Catalog connections may be exported and imported to move them between Namespaces. When importing projects or Namespaces that include Catalog connections, those connections must be reestablished by providing a current connection Access Token and URL. Use the **Show>Catalogs** menu item to reestablish Catalog connections.

## Event Catalog

### Using the Event Catalog
#### Events
The Event Catalog manages a collection of Event Types, which describe what events will look like. For those familiar with pub/sub messaging systems, Event Types can be thought of as similar to topics to which messages are published and subscriptions are requested.

Event Types are created by users with sufficient permissions to create Event Types. When an Event Type is
first created, there are no publishers or subscribers.

Publishers are registered to define the producers of instances of the Event Type.

Subscribers are registered to indicate their desire to receive instances of the Event Type published by the publishers. 
A subscriber that subscribes before any publisher is registered will receive no event instances since there is no 
publisher producing such events. Once a publisher is registered and starts publishing event instances, existing 
subscribers will receive the published event instances.

The connections for Event Types look like this:

![Connections Between Event Publishers and their Subscribers](assets/img/brokerref/eventCatalogArchitecture2Subscribers.png)

#### Adding Event Types 
Create a new Event Type by clicking the plus icon in the title bar.
A new pane opens in which you type 
the name, description and schema for the new event.

The name of an Event Type must begin with a `/` character. The names use a hierarchical naming convention with each 
level in the hierarchy delimited by a `/` (in a fashion similar to Linux filenames). This is necessary because Event 
Type names must be valid topic names.

When a Namespace subscribes to an Event Type in the Catalog all of the events will be delivered to the subscriber on a 
topic in the subscriber Namespace, and unless overridden, the topic in the subscriber Namespace will be the same as the 
Event Type name.

##### Reliable Events

When adding an Event Type to the Catalog, check the `Is Reliable?` box to indicate that publishers of the event must be
reliable and that the Catalog must retry forwarding of events from a reliable publisher until successfully delivered to all 
subscribers. Note that in some failure scenarios this means a particular subscriber might see the same event more than
once.


#### Registering Event Publishers
In the Event Catalog find the existing Event Type or create a new one if the desired Event Type does not exist.
Click on the name of the Event Type to open the Event Type detail pane, resulting in a display similar to the following:

![eventDetail](assets/img/brokerref/eventDetail.png "Event Detail Pane")

Click on the "Click to View" link next to "Publishers" to open the list of known publishers and a form to register as a 
publisher:

![publisherList](assets/img/brokerref/publisherList.png "Publisher List Popup")

The top half of the popup registers the local topic or source that represents the stream of events to bind to the 
Event Type. In the example there is an existing publisher, FactorySensors, of `/machine/offline`. The local events that 
are bound to `/machine/offline` are produced by the topic: `/sensors/offline`. 

Note that if you choose an existing persistent topic to be a publisher of an Event Type, it must have a message type that matches
the message type expected by the Catalog. If the message types are not compatible, the Catalog will reject the registration of
the publisher.

Instances of Event Types in the Catalog are generally published by Vantiq sources or by applications using the Vantiq SDKs to 
publish event instances to the Advanced Event Broker. Use of the Vantiq SDKs is detailed in a separate [API reference guide](brokerapi.md).

#### Removing Event Publishers
To remove the FactorySensors Namespace as a publisher of the Event Type, click the remove button in the right-most 
column. Only administrators of the Catalog Namespace and of the FactorySensors Namespace can remove FactorySensors
as a publisher of the Event Type. Other connected Namespaces can see that FactorySensors is a publisher, but do not have
the authority to remove the publisher.

#### Registering Subscribers
As described in the [Catalog Actions](#catalog-actions) Section, it is possible to subscribe to an Event Type in the 
Catalog using the play button in the Actions column of the Event Catalog. Doing so will use the Event Type name as the 
local topic on which published events will be delivered to the subscribed Namespace.

If the default topic will not work, it is possible to subscribe to an Event Type and specify a different local topic on 
which published events will be delivered.  To do so, use the "Click to View" link next to "Subscribers" in the Event Type detail
pane. The subscribers popup should look like this:

![subscriberList](assets/img/brokerref/subscriberList.png "Subscriber List Popup")

To register as a subscriber of the Event Type and use a different topic name, simply enter the topic in the input field
and click the "Subscribe" button. Events will immediately start being delivered to the Namespace on the specified topic
as soon as they are published. 

Note that if you choose an existing persistent topic to be a subscriber of an Event Type, it must have a message type that matches
the message type expected by the Catalog. If the message types are not compatible, the Catalog will reject the registration of
the subscriber.

#### Removing Subscribers From Event Types
In the screenshot above, note that there is a single subscriber listed. The Namespace OperationalManagement has
subscribed to the `/machine/offline` events, and has requested those events are delivered locally on the topic
`/m/offline`. From this subscribers list, it's possible to unsubscribe to events as well using the remove button in the 
right-most column. Similar to publishing, only the Catalog Namespace and the Subscribing Namespace can remove a 
subscriber.

### Augmenting Brokered Events
#### App Builder Integrations
Many of the features of an Event Catalog are enabled through the [App Builder](apps.md). These 
integrations take a few different forms:

* Subscribe to Event Types directly in app Event Stream tasks
* Publish the output of an app task to an Event Type
* Record the output of an app task in the Event Ledger

All of these integrations are demonstrated in the [Catalog Tutorial](tutorials/eventbroker.md).

### Publishing Events

Instances of Event Types in the Catalog are generally published by Vantiq sources or by applications using the Vantiq SDKs to 
publish event instances to the Catalog. Use of the Vantiq SDKs is detailed in a separate [API reference guide](brokerapi.md).

### Receiving Events
Instances of Event Types in the Catalog are generally subscribed to and delivered to applications built using the Vantiq SDKs. 
Use of the Vantiq SDKs is detailed in a separate [API reference guide](brokerapi.md).

### Source Integrations
In addition to supporting applications that produce event instances through the Vantiq SDKs, the Catalog contains 
pre-integrated support for popular platforms that produce event streams. These platforms are represented in Vantiq as a 
[Source](sources/source.md). To avoid putting extra load on that external system, it's a good idea to create 
only one source to receive the inbound stream of events from the external system. The source can then publish those 
events to the Event Catalog so they can be consumed by any number of subscribers.

Once you've created a source, there are a few easy steps you can take to create an Event Type in the Catalog and begin 
publishing source events directly to that Event Type. The first step is to test the source and receive a sample event, 
which can be inspected to determine the schema of the inbound events. From the source pane, click the **Test Data Receipt** button.

![clickSubscribeSource](assets/img/brokerref/clickSubscribeSource.png "Click Subscribe Source")

Clicking the **Test Data Receipt** button opens a live subscription pane that shows the events streaming in from the source in real 
time. Once an event arrives, you can click on that event and then use the **Create Data Type** button to generate a
schema type using the format of the received event as a model. 

![clickCreateType](assets/img/brokerref/clickCreateType.png "Click Create Type")

This should open a popup to confirm the type name and role, and after clicking **OK** the schema type is created. 

Once the schema type has been created, go back to the source pane, scroll to the bottom and click **Publish To 
Event Catalog**, which opens the following popup:
 
![publishFromSourcePopup](assets/img/brokerref/publishFromSourcePopup.png "Publish From Source")

It's possible to publish to an existing Event Type chosen from the drop list, or to create a new Event Type and register
as a publisher using the **Create New Event** button, which opens a new dialog box to complete the Event Type definition 
like this:

![createNewEventTypeFromSource](assets/img/brokerref/createNewEventTypeFromSource.png "Create New Event Type From Source")

After that, all events produced by the external system will be published to the Event Catalog.

## Service Catalog

### Using the Service Catalog

#### Services
The Service Catalog handles [Services](./resourceguide.md#Services), which are collections of 
[Procedures](./resourceguide.md#Procedures) that the Service Catalog allows to be run from any subscriber.

Services do not exist in the Catalog until published by a Catalog member. Once published, no other Namespace can publish
a Service with the same name to the same Catalog until the publisher removes the Service.

Subscribers register for use of a Service once it has been published. Local Procedures are generated in the subscriber 
Namespace that will call the Procedures of the same name in the publisher.

Note that the Service Procedures are run in the publishing Namespace, so they cannot directly affect anything in the
subscriber's Namespace. Any development that occurs after publishing the Service will affect subscribers' use of the Service.
If significant changes are expected to occur while a 
Service is published, it may be useful to note that in the Service's description.

The connections for Services look like this:

![Connections Between Service Publishers and their Subscribers](assets/img/brokerref/serviceCatalogArchitecture2Subscribers.png)

#### Subscriber Permissions

Subscribers will only have user-level permissions in the publisher Namespace. If any Procedures in a published Service
require higher permissions than the default user-level permissions, you will need to define
[explicit profiles](./rules.md#with-clause-options) on the Procedure for the Service to function properly.

### Creating and Editing Service Procedures

Use the **Add>Service** menu item to create and edit Services. Users may create
and view Service Procedure Signatures through the Service pane. 

The Interface tab of the Service pane shows all of the Procedure signatures contained by the Service.
Users may add, edit, and remove Procedures from this pane. When the Service is saved, the changes made in the Service Pane
must be applied to the Procedures in the Implement tab, otherwise the Service will be in error.

![Interface tab](assets/img/brokerref/publisherInterfaceTab.png "Procedures tab of the Services pane")

Procedures in the Interface are added to the Catalog when the Service is published. Private Procedures
are never published to the Catalog. When creating or editing a Procedure, the user may define the Procedure name and parameters.
Procedures in the Interface may also specify the Procedure description and return type.
The return type may be set to either a Built-in Type (ex: String, Boolean, Integer...) or to a Schema 
Type defined in the Namespace.

By clicking on the pencil icon next to a parameter, you may define a parameter description as well as set the type of the parameter.

![Procedures tab](assets/img/brokerref/editParameterPopup.png "Edit parameter popup of the Services pane")

### Publishing Services

All local Services are publishable. To publish a service through the IDE,
go to **Add** > **Services** to open the Services pane which looks as below. 

![ServicesPane](assets/img/brokerref/allServicesPane.png "Services pane in Modelo")

Find the desired Service and click on it to open its Service pane. Navigate to the `Interface` tab. Here is where you
can see and set the interface for procedures.
You can give a description for the Procedure, add a return type,
and fill in some details for the parameters. See above for more details.

Click the up arrow in the `Publish` column for the Catalog you want to publish to. This will attempt to publish the 
Service to that Catalog and, if successful, the Publish symbol will turn into an `x` for that Catalog.

![Service pane](assets/img/brokerref/publisherServiceGeneralTab.png "Pane for the Service testSvc")

Services may also be published directly from the Catalog Pane. Clicking on the "+ New" button will give the user the option
to Publish a new Service to the Catalog. 

![Service pane](assets/img/brokerref/publishServiceFromCatalog.png "Publish from Catalog pane")

The user may select which Services to Publish. Clicking "OK" will complete the Publishing
process.

![Service pane](assets/img/brokerref/publishFromCatalogPopup.png "Select Catalogs to publish")


If you cannot use the IDE, then you can publish the Service through the 
[Catalog API](./brokerapi.md#publisher-service).

#### Updating Published Services

Services can change in the publisher Namespace. This can be the addition or removal of a Procedure, an update in 
parameters for a Procedure, a new schema, or an updated description. However, it _cannot_ be a change to a schema
already given to a Catalog.

To perform an update, navigate to the Service's `General` subtab in the `Interface` tab and click the refresh icon in the `Update` column for each
Catalog that you would like to send the update to.

![Updating a Service](assets/img/brokerref/updatePublishedService.png "Updating the Service")

Note that updating a Service as a publisher will not update all subscribers. Each subscriber will have to individually
update their own subscriptions in order to ensure they have the most recent version.

If you cannot use the IDE, then you can update a published Service through the 
[Catalog API](./brokerapi.md#publisher-service).

#### Removing Services

Services can be removed from the Catalog by the publisher. Doing so will also stop all subscribers from running
the Service, causing an error when they try.

To remove a Service, navigate to the `General` subtab of its Service pane and click the `x` in the Publish column for each 
Catalog.

![Removing a Service](assets/img/brokerref/updatePublishedService.png "Removing the Service from a Catalog")

If you cannot use the IDE, then you can remove a published Service through the 
[Catalog API](./brokerapi.md#publisher-service).

### Using Published Services

Subscribing to a published Service allows you to use the publisher's Procedures. To subscribe
through the IDE, find the desired Service in **Show** > **Catalog** and click the play button.

![Subscribing to Service in Catalog](assets/img/brokerref/subscribeToServiceInCatalog.png "Service Catalog Subscribing")

You can also subscribe by clicking on the Service in the Catalog to open its Catalog Service pane, then clicking
`Subscribe` in the `General` subtab.

![Subscribing to Service in Service](assets/img/brokerref/subscribeToServiceInService.png "Service Catalog Subscribing")

Services may also be Subscribed to directly through the Test input and output pop-ups as well as the App Builder and Collaboration Builder.
Wherever there is a droplist to select Procedures, there may be a Search icon which allows you to look at a list of all Services, including those in Catalogs.
 
![Subscribing to Service in Service](assets/img/brokerref/subscribeFromApp.png "Subscribe to Service from App")

Clicking on the Search icon
will open a pop-up that will allow the user to select which Service they would like to use.
Selecting a Service with the book next to it gives the option to subscribe to it. Clicking "OK" 
will subscribe to the Service and make the Procedures in the Service immediately available in the Procedure droplist.

![Subscribing to Service in Service](assets/img/brokerref/subscribeFromAppPopup.png "Subscribe to Service from App popup")

To use the subscribed Service, simply call the subscribed Procedures as normal, and they will be run in the publisher
Namespace.

If you cannot use the IDE, then you can subscribe through the [Catalog API](./brokerapi.md#subscriber-service).

#### Updating Subscribed Services

In order to keep Procedures from unexpectedly appearing or disappearing, subscribed Services are not updated when a
publisher updates that Service in the Catalog. Instead, a subscriber must update themselves in order to obtain the most
recent versions. 

To update through the IDE, click on the Service in the Catalog then click on the refresh icon in the `General` subtab of the `Interface` tab. If
there are no changes to update, the icon will be greyed out and you cannot click it.

![Updating Service](assets/img/brokerref/updateServiceSubscription.png "Updating a subscribed Service")

If you cannot use the IDE, then you can update subscriptions through the 
[Catalog API](./brokerapi.md#subscriber-service).

#### Unsubscribing from a Service

Unsubscribing from a Service deletes it locally and deletes all associated Procedures, though it leaves any schema
that the Service added. To unsubscribe, find the desired Service in **Show** > **Catalog** and click the pause button.

![Unsubscribing from Service in Catalog](assets/img/brokerref/unsubscribeServiceThroughCatalog.png "Service Catalog Unsubscribing")

You can also unsubscribe in the Catalog Service's window by clicking `Unsubscribe` in the `General` subtab.

![Unsubscribing from Service in Service](assets/img/brokerref/unsubscribeThroughService.png "Service Catalog Unsubscribing")

If you cannot use the IDE, then you can unsubscribe through the [Catalog API](./brokerapi.md#subscriber-service).

## Assembly Catalog

### Using the Assembly Catalog

#### Assemblies

The Assembly Catalog handles Assemblies, which are configurable [Projects](resourceguide.md#projects) intended to be reused multiple times.

Assemblies do not exist in the Catalog until published by a Catalog member. Once published, no other Namespace can publish an Assembly with the same name to the same Catalog until the publisher removes the Assembly.

Consumers register for use of an Assembly once it has been published. The Assembly's resources are installed to the consumer namespace, and all resources not intended to be directly used will be marked hidden.

The connections for Assemblies look like this:

![Connections Between Assembly Publishers and their Subscribers](assets/img/brokerref/assemblyCatalogArchitecture2Subscribers.png)

### Publishing Assemblies

All local Assemblies are publishable. To publish an Assembly through the IDE, navigate to the Assembly Project with **Projects><Assembly name\>** then **Show\>Assembly** to open the Assembly pane which looks as below.

![assemblyPane](assets/img/brokerref/assemblyPubPane.png "Assembly pane in Modelo")

Navigate to the `Configuration` pane to set the configurable values for the assembly. Clicking on **New Property** or the pencil icon for a property will allow you to give a description for the property, set the type, and specify what resources it will configure.

![Configuration tab](assets/img/brokerref/assemblyConfigTab.png "Configuration tab of the Assembly pane")

In the `Visible Resources` pane you can decide what resources will be visible to consumers. Dragging resources from the left to the right means that consumers will be able to see them, and selecting a resource on the right then clicking the trash can reverses this. Not all resources can be made visible. See the [Assembly Reference Guide](assemblies.md#visible-resources) for more details

![Visible Resources tab](assets/img/brokerref/assemblyVisibleResources.png "Visible Resources tab of the Assembly pane")

Once you have set up the properties and visible resources you wish to be published and saved the Assembly, navigate to the `General` tab.

Back in the `General` tab, select the catalog you wish to publish to then click the **Publish** button. If the publish is successful, the button will be placed with an `X`.

![Assembly pane](assets/img/brokerref/assemblyUpdatePub.png "Pane for the Assembly")

If you cannot use the IDE, then you can publish the Assembly through the [Catalog API](./brokerapi.md#publisher-service).

### Using Published Assemblies

Installing a published Assembly allows you to use and configure the resources in the Assembly. To install through the IDE, find the desired Assembly in **Show>Catalog**, right-click it, and click the play button.

![Installing Assembly in Catalog](assets/img/brokerref/assemblyCatalog.png "Assembly Catalog Installing")

This will open a dialog that will allow you to set configuration properties for the Assembly, so that it will be fully configured and ready to go when installed. 

![Configuring Assembly in Catalog](assets/img/brokerref/installConfig.png "Assembly Configuration")

Once an Assembly is installed, it can be used in the local namespace. All the visible resources are available to be used as well as the events and procedures in the Assembly's interface.

If you cannot use the IDE, then you can install through the [Catalog API](./brokerapi.md#subscriber-service).

#### Updating Installed Assemblies

In order to keep resources and functionality from unexpectedly appearing or disappearing, installed Assemblies are not updated when a publisher updates that Assembly in the Catalog. Instead, an installer must update themselves in order to obtain the most recent versions.

To update through the IDE, click on the Assembly in the Catalog then click on the refresh icon in the General tab. If there are no changes to update, the icon will be greyed out and you cannot click it.

![Updating Assembly](assets/img/brokerref/updateInstalledAssembly.png "Updating an installed Assembly")

If you cannot use the IDE, then you can update installations through the [Catalog API](./brokerapi.md#subscriber-service).

#### Uninstalling an Assembly

Uninstalling an Assembly deletes the Assembly and all its resources. To uninstall, find the desired Assembly in **Show>Catalog**, right-click it, and click the pause button.

![Uninstalling Assembly in Catalog](assets/img/brokerref/uninstallAssemblyCatalog.png "Assembly Catalog Uninstalling")

You can also uninstall in the Assembly pane by clicking `Uninstall` in the `General` tab.

![Uninstalling Assembly in Assembly](assets/img/brokerref/updateInstalledAssembly.png "Assembly Catalog Uninstall")

If you cannot use the IDE, then you can uninstall through the [Catalog API](./brokerapi.md#subscriber-service).

## Semantic Index Catalog

### Using the Semantic Index Catalog

#### Semantic Indexes
The Semantic Index Catalog handles [Semantic Indexes](./resourceguide.md#semantic-indexes), which are collections of various data that can be easily referenced and fed to LLMs. The Catalog allows you to upload that data to a single location and then use it in any connected namespace.

Semantic Indexes do not exist in the Catalog until published by a Catalog member. Once published, no other Namespace can publish a Semantic Index with the same name to the same Catalog until the publisher removes the Semantic Index.

Subscribers register for use of a Semantic Index once it has been published. A [Remote Semantic Index](semanticsearch.md#remote-semantic-indexes) is then generated in the local namespace, connected to the publisher namespace. The available Semantic Index Entries will thus be fully up-to-date with the index in the publisher namespace.

### Publishing Semantic Indexes

All local Semantic Indexes are publishable. To publish a Semantic Index through the IDE, go to **Add** > **Semantic Indexes** to open the Semantic Indexes pane which looks as below.

![Semantic Indexes Pane](assets/img/brokerref/allSemanticIndexesPane.png "Semantic Indexes pane in Modelo")

Find the desired Semantic Index and click on it to open its Semantic Index pane. Here is where you can manage entries and various connection properties.

Click the up arrow in the `Publish` column for the Catalog you want to publish to. You'll likely need to scroll down to see this option. This will attempt to publish the Semantic Index to that Catalog and, if successful, the Publish symbol will turn into an `x` for that Catalog.

![Semantic Index pane](assets/img/brokerref/publisherSemanticIndex.png "Pane for the Semantic Index")

If you cannot use the IDE, then you can publish the Semantic Index through the [Catalog API](./brokerapi.md#publisher-service).

#### Updating Published Semantic Indexes

Changes to a Semantic Index typically do not require updates in the catalog. Because the subscriber Semantic Indexes access the Index in the publisher namespace, changes to the publisher's entries will effectively propagate immediately. Only changes to the description require an update.

To perform an update, navigate to the bottom of the Semantic Index's pane and click the refresh icon in the `Update` column for each Catalog that you would like to send the update to.

![Updating a Semantic Index](assets/img/brokerref/updatePublishedSemanticIndex.png "Pane for the Semantic Index")

Note that updating a Semantic Index as a publisher will not update all subscribers. Each subscriber will have to individually update their own subscriptions in order to ensure they have the most recent version.

If you cannot use the IDE, then you can update a published Semantic Index through the [Catalog API](./brokerapi.md#publisher-service).

#### Removing Semantic Indexes

Semantic Indexes can be removed from the Catalog by the publisher. Doing so will also unsubscribe all subscribers of the index.

To remove a Semantic Index, navigate to the bottom of its pane and click the `x` in the Publish column for each Catalog.

![Removing a Semantic Index](assets/img/brokerref/updatePublishedSemanticIndex.png "Removing the Semantic Index from a Catalog")

If you cannot use the IDE, then you can remove a published Semantic Index through the [Catalog API](./brokerapi.md#publisher-service).

### Using Published Semantic Indexes

Subscribing to a published Semantic Index allows you to use the entries in the publisher's Semantic Index. To subscribe
through the IDE, find the desired Semantic Index in **Show** > **Catalog**, and click on its name.

![Subscribing to Semantic Index in Catalog](assets/img/brokerref/subscribeToSemanticIndex.png "Semantic Index Catalog Subscribing")

To use the subscribed Semantic Index in a GenAI Procedure, simply reference it as you would a local Semantic Index.

To use the Semantic Index for AnswerQuestion, you must create a GenAI Procedure that handles the request. A single [RAG component](genaibuilder.md#rag) mostly emulates the standard AnswerQuestion functionality. See the [AnswerQuestion Procedure section of External Semantic Indexes](semanticsearch.md#external-semantic-indexes) for more details.

You cannot manage entries for subscribed Semantic Indexes. That can only be done in the publisher namespace.

If you cannot use the IDE, then you can subscribe through the [Catalog API](./brokerapi.md#subscriber-service).

#### Updating Subscribed Semantic Indexes

Currently, Semantic Indexes have no significant updates that are done through the catalog. Changes in entries are done by the publisher and immediately affect all subscribers. The only property that a publisher may update is the description.

To update through the IDE, click on the Semantic Index in the Catalog then click on the refresh icon at the bottom of the pane. If
there are no changes to update, the icon will be greyed out and you cannot click it.

![Updating Semantic Index](assets/img/brokerref/updateSemanticIndexSubscription.png "Updating a subscribed Semantic Index")

If you cannot use the IDE, then you can update subscriptions through the [Catalog API](./brokerapi.md#subscriber-service).

#### Unsubscribing from a Semantic Index

Unsubscribing from a Semantic Index deletes it locally, though it doesn't affect the Answer Question procedure or default LLM. To unsubscribe, find the desired Semantic Index in **Show** > **Catalog**, right-click it, and click Unsubscribe.

![Unsubscribing from Semantic Index in Catalog](assets/img/brokerref/unsubscribeSemanticIndexThroughCatalog.png "Semantic Index Catalog Unsubscribing")

You can also unsubscribe in the Catalog Semantic Index's window by clicking `Unsubscribe` at the bottom of the pane.

![Unsubscribing from Semantic Index in Semantic Index](assets/img/brokerref/updateSemanticIndexSubscription.png "Semantic Index Catalog Unsubscribing")

If you cannot use the IDE, then you can unsubscribe through the [Catalog API](./brokerapi.md#subscriber-service).
