# Using the Vantiq Catalog

## Purpose

To familiarize developers with the powerful features of the Vantiq [Catalog](../broker.md).

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## Objectives
By the end of this tutorial, the developer should be able to:

* Access and configure a Catalog
* Link subscribers and publishers to the Catalog
* Set up access tokens to the Catalog for maximum security
* Subscribe to events from the Vantiq IDE
* Create and publish simulated events with VAIL Rules, Scheduled Events, and Event Generators
* Be able to verify event receipt to subscribers
* Create and publish a Service to the Catalog
* Subscribe to a Catalog Service and execute Service Procedures in an Application

## Tutorial Overview

In this tutorial, we will create a simple service event handler that publishes "overheat" events when a simulated machine sensor reports a temperature that is too high. Our Catalog set-up will allow such events and related "reaction" events to communicate across different Namespaces.

The basic steps involved to accomplish this are:

* Create separate Namespaces for the Catalog, publisher, and subscriber
* Register the publisher and subscriber to the Catalog
* Define Event Types
* Define a Catalog Service
* Receive events
* Generate and publish events
* Execute Procedures from a Catalog Service

## Part 1: Setup Catalog Infrastructure

### Step 1: Create Catalog Namespaces

This tutorial requires three Namespaces, which means you should first familiarize yourself with creating and managing
Namespaces in the [User and Namespace Administration Tutorial](./admin.md#task-2-adding-a-new-developer). 

The first step is to sign into a Namespace in which you have developer or higher privileges. From there, you will create
Namespaces to act as each of the three Catalog roles: Catalog, Subscriber and Publisher.

Use the **Administer** button to select **Namespaces**, then use the **New** button in the Namespaces list to create three Namespaces with the following names: _catalog_, _publisher_ and _subscriber_. You should be the administrator of each of these Namespaces.

![1228_EventsTut_NewNamespace](../assets/img/brokertutorial/128_EventsTut_NewNamespace.png "Namespace List")

Once you've created the three Namespaces, switch into the _catalog_ Namespace using the Current Namespace button at the top right of the IDE Navigation Bar and selecting _catalog_ from the list of available Namespaces.

### Step 2: Configure Catalog

Now that all of the Namespaces have been created and you're in the _catalog_ Namespace, it's time to configure each Namespace for its respective role. The _catalog_ Namespace is currently just a standard developer Namespace. To allow this Namespace to host a Catalog of events and Services, use the **Administer** button to select **Advanced>Catalog** which displays the _Manage Catalog_ pane. Click the **Create Catalog** button and confirm that you want to create a Catalog. (Leave the optional
"Catalog Name" blank.)

![becomeEventCatalog](../assets/img/brokertutorial/becomeEventManager.png "Become Catalog Namespace")

This Namespace is now ready to host events and Services in the Catalog. Other Namespaces that connect to the _catalog_ Namespace can read the Catalog of events and Services and register as publishers and subscribers of events and Services.

Of course, we'll be publishing important information through this catalog. We don't want just anyone to be able to send out messages. To avoid this, we can change the default permissions for connected namespaces.

In the _Manage Catalog_ pane, find the catalog namespace (it should be the only one present right now) and click on **Edit Permissions**. Toggle off the box for **publish** under **Event Types** then click **OK**. Now no members of the catalog will be allowed to publish to Event Types unless we explicitly let them.

![Host Catalog Default Permissions](../assets/img/brokertutorial/hostCatalogPermissions.png "Catalog Default Permissions")

### Step 3: Connect Publisher and Subscriber to Catalog

The next step is to connect the _publisher_ and _subscriber_ Namespaces to the _catalog_ Namespace.

To connect the _publisher_ and _subscriber_ Namespaces to the _catalog_ Namespace, we need to get credentials that can be used by those Namespaces to communicate with the _catalog_ Namespace. To that end, we create an access token by clicking the **New Token** button in the _Manage Catalog_ pane. Name the access token "CatalogToken" then click **Create**. This creates a new token and copies it to the browser clipboard. Save this token string somewhere readily accessible as we'll need it to configure the _subscriber_ and _publisher_ Namespace Catalog connections.

![createCatalogToken](../assets/img/brokertutorial/createCatalogToken.png "Create Catalog Token")

Switch into the _publisher_ Namespace using the Current Namespace button at the top right of the IDE Navigation Bar and selecting _publisher_ from the list of available Namespaces. You will see the page reload and you will now be in the _publisher_ Namespace. Verify this by checking that the Namespace name in the Navigation Bar has changed from _catalog_ to _publisher_. 

Once in the _publisher_ Namespace, we must connect to the _catalog_ Namespace using the access token we just created. Use the **Show** button to select **Catalogs** to display the _Catalogs_ pane. Use the **Connect** button to display the _Connect to Catalog_ dialog. Paste the token string into the **New Catalog Access Token** field, verify the URL in the **URL to Connect to Catalog Namespace** field, and click the **Connect** button.

![connectToCatalog](../assets/img/brokertutorial/connectToCatalog.png "Connect to Catalog")

Switch to the _subscriber_ Namespace and repeat the process of connecting to the _catalog_. Afterwards, both the _publisher_ and _subscriber_ Namespaces are now able to view the Catalog of Event Types and Services hosted by the Catalog Namespace. To view the Catalog of Event Types and Services from any connected Namespace, use the **Show** button to select **Catalogs** to display the _Catalogs_ pane. Click on any listed Catalog Namespace to display its list of known Event Types and Services. 

Both the _publisher_ and the _subscriber_ namespace need to perform publishes as part of this tutorial. Because we changed the default catalog permissions to disallow publishing, we must now override the default permissions for both namespaces. To do this, return to the _catalog_ namespace and open the _Manage Catalog_ pane. For the _publisher_ and _subscriber_ namespaces in the list, click **Edit Permissions**. Select "Event Types" and "publish" in the dropdowns, then click **Add Override**. Make sure the box is checked, then click **Save**.

![Member Override Permissions](../assets/img/brokertutorial/memberCatalogPermissions.png "Member Override Permissions")

## Part 2: Creating Events

### Step 1: Create Event Schema

To get started on creating the machine temperature and overheat Event Types, switch back to the _catalog_ Namespace.  

Before we can create the Event Types, we first need to define a schema type which defines the schema for the machine temperature and overheat events. Use the **Add** button to select **Type** and create a new type. In the resulting dialog, name the type _MachineData_, verify the role is set to _schema_ then click **Create**. From the _Type: MachineData_ pane, add the following properties, making sure to check them all as _required_:

* _machineId_ (String) - A unique identifier that associates a reading with a specific machine.
* _temperature_ (Integer) - The sensor reading in degrees fahrenheit.
* _timestamp_ (DateTime) - The time at which the sensor reading was recorded.

![createMachineDataType](../assets/img/brokertutorial/createMachineDataType.png "Create MachineData Type")

Click **Save** to save the Type definition.

### Step 2: Define Event Types

Now we finally get to add events to the Catalog. While still in the _catalog_ Namespace, open the Catalogs pane by using the **Show** button to select **Catalogs**. Select the _catalog_ Catalog Namespace from the list, then use the **New** button to select **Create New Event Type**. The _Event Type_ pane is displayed in which we create our first Event Type. Configure this Event Type with the following values:

* _Event Name_: /machine/temp
* _Description_: A new machine temperature sensor reading.
* _Schema_: Select _MachineData_ from the droplist

![128_EventsTut_NewEventType](../assets/img/brokertutorial/128_EventsTut_NewEventType.png "Create /machine/temp Event Type")

Note that the Event Type name is a Topic. Topics must contain a leading slash but often contain additional slashes, which is a good practice for organizing events in a hierarchical manner. The prefix _/machine_ indicates this is an event on a machine and the suffix _/temp_ indicates this is a temperature event. In the future, we will add another event with the same _/machine_ event prefix. Giving events common prefixes makes it easier to find them in the Catalog and helps users looking at the Catalog get a sense for how different events are related.

Once you've completed the new Event Type pane, click the **Save** icon and you'll see a list of suggested keywords found by parsing the specified description. Leave _machine_ and _temperature_, delete the rest, then click **OK**. This will add some keyword tags to the newly created Event Type, which offers users a different way to query for interesting Event Types.

Follow the same process to create an Event Type for the overheating event. Use the following configuration:

* _Event Name_: /machine/overheat
* _Description_: The temperature of a machine has risen above the normal operating range.
* _Schema_: Select _MachineData_ from the droplist

Save the Event Type, then delete any unhelpful suggested keywords. (In this case, everything except machine and temperature.) Click **OK**. You should now see two Event Types listed in the Catalog pane. 

![View Catalog](../assets/img/brokertutorial/128_EventsTut_EventCatalog.png "View Catalog")

### Step 3: Register a Publisher

Now that we have the necessary events in the Catalog, it's time to switch to the _publisher_ Namespace and start producing temperature events. Create a project called "MachineData". (Changes in the Project will be saved automatically if you have the "Project Autosave Enabled" options set. Otherwise save the project by clicking the **Save** button in the navbar again after each step.)

Next, open the Catalog by using the **Show** button to select **Catalogs**. Select the _catalog_ Catalog Namespace from the list, then click on the _/machine/temp_ event in the list. In the resulting _Event Type_ pane, click on _Click to View_ next to **Publishers**. In the _Publishers of /machine/temp_ dialog, specify a "Local topic for events", _/my/machine/temp/event_, for the _/machine/temp_ event. Click **+ Become Publisher**.

The local name of an Event Type is the Topic on which the events will occur in this Namespace. For this tutorial, we set the local name to _/my/machine/temp/event_. This means that when an event occurs on _/my/machine/temp/event_, it will be forwarded to all of the subscribers of _/machine/temp_.

![becomePublisher](../assets/img/brokertutorial/becomePublisher.png "Become Publisher")

### Step 4: Publish Events

We now need to generate events in this _publisher_ Namespace that will be published to _/my/machine/temp/event_ so the _subscriber_ Namespace will have some data to consume. To generate random data, we create a rule that runs every five seconds and publishes the data to _/my/machine/temp/event_. To create a rule, use the **Add>Advanced** button to select **Rule** then click the **New Rule** button.

Create a rule with the following text:

```js
RULE tempEventTrigger
WHEN PUBLISH OCCURS ON "/random"
// Publish one random temperature event each for 3 machineIds
PUBLISH {temperature: random(0, 100), machineId: "Machine1", timestamp: now()} TO TOPIC "/my/machine/temp/event"
PUBLISH {temperature: random(0, 100), machineId: "Machine2", timestamp: now()} TO TOPIC "/my/machine/temp/event"
PUBLISH {temperature: random(0, 100), machineId: "Machine3", timestamp: now()} TO TOPIC "/my/machine/temp/event"
```

Click **Save** to save the Rule. This rule will run every time an event publishes to the _/random_ Topic. Next we need to create a Scheduled Event that will publish to _/random_ once every five seconds. To create the Scheduled Event, use the **Add** button to select **Advanced>Scheduled Event** then click the **New Scheduled Event** button.

Create a new Scheduled Event with the following properties:
````text
   Name: "RandomTempGenerator"
   Topic: /random
   Periodic?: True
   Active?: True
   Scheduling Type: Periodically, starting now
   Interval: 5 seconds
````
![128_EventsTut_NewScheduledEvent](../assets/img/brokertutorial/128_EventsTut_NewScheduledEvent.png "Create Scheduled Event")

Click **Save** to save the Scheduled Event. If you want to verify that the events are being published as you expect, use the **Show** button to select **Resource Graph** then find and click on the Topic _/my/machine/temp/event_. Click the **Test Data Receipt** button in the top left of the resulting pane. This displays a subscription pane that streams all of the events in real time that occur on that Topic, all of which are forwarded to all subscribers of the Event Type _/machine/temp_. Wait five seconds and you should see an event like this:

![134_EventsTut_StreamSubscription](../assets/img/brokertutorial/134_EventsTut_StreamSubscription.png "Live Temperature Events")

### Step 5: Register a Subscriber

Now that the publisher is generating _/machine/temp_ events, it's time to switch to the _subscriber_ Namespace and register a subscriber. In the subscriber Namespace, give the project a name such as "OverheatDetector" and click the **Save** button in the Navigation Bar. 

Once you've created the project, open the Catalog by using the **Show** button to select **Catalogs**. Select the _catalog_ Catalog Namespace from the list, then right-click on the _/machine/temp_ entry in the list. Select **Subscribe** to confirm that you want to subscribe to _/machine/temp_ events.

At this point, all events published to _/my/machine/temp/event_ in the _publisher_ Namespace should be forwarded to the _subscriber_ Namespace on the Topic _/machine/temp_. You may verify this by clicking the **Test Data Receipt** button from the _/machine/temp_ Topic pane.

## Part 3: Building Apps in Services

### Step 1: Trigger an Event Handler on /machine/temp Events

While still in the _subscriber_ Namespace, create a new Vantiq Service by using the **Add** button to select **Service** then clicking the **New Service** button. Name the service _OverheatDetector_, and set the package to _machine.maint_. This Service will process the _/machine/temp_ events to identify when a machine overheats. When the Service identifies a machine that is overheating, it will produce a _/machine/overheat_ event and publish that event to the Catalog. We define overheating to mean the temperature has risen above 100 degrees. Below 100 degrees, the machine is deemed to be operating within the normal operating temperature range.

With the new Service pane open, switch to the _Implement_ tab.  Under _Event Handlers_, click the plus button next to  _Service_ and add a Service Visual Event Handler. Name the Event Handler _OverheatMonitor_.

![ServiceEventHandler](../assets/img/brokertutorial/serviceVisualEventHandler.png "Add Service Event Handler")

Now that the App Builder for the Service Event Handler is open, we can create an application to handle incoming events. Every Service Event Handler starts with an unconfigured orange _Initiate_ activity representing an initial stream of events. Click on the orange box and name the task _TempStream_. Next, click _Click to Edit_ next to Configuration label to edit the _TempStream_ configuration. The _inboundResource_ for the event stream is _topics_, and the _inboundResourceId_ (_/machine/temp_) can be selected from the dropdown next to the input field:

![dropdownSelectMachineTemp](../assets/img/brokertutorial/dropdownSelectMachineTemp.png "Select Machine Temp Event From Dropdown")

Note that once you select _/machine/temp_ from the droplist, the schema property at the bottom of the configuration dialog is automatically updated to show _MachineData_. This is because the _/machine/temp_ event in the Catalog has an associated schema type so subscribing to the event through the Catalog added a copy of the schema type to this Namespace. 

It's also possible to subscribe to events in the Catalog directly from the Service Handler's configuration dialog. Click the magnifying glass button next to the dropdown for the _inboundResourceId_ property and you will see a dialog where you could subscribe to any event from the Catalog. This would have the same effect as subscribing from the _Catalogs_ pane displayed by using the **Show** button and selecting **Catalogs**.

After clicking OK and exiting the configuration, you'll notice that the TempStream task is now yellow. This signifies that the task is now a topic event stream.

To verify the event stream is working, save the Service, right click on the _TempStream_ task and click **View Task Events**. This opens a subscription pane which shows events as they arrive.

![viewTaskEvents](../assets/img/brokertutorial/viewTaskEvents.png "View Task Events")

![128)EventsTut_ViewTaskEvents](../assets/img/brokertutorial/128_EventsTut_ViewTaskEvents.png "View Task Events")

### Step 2: Split by MachineId

The random temperature readings published to _/machine/temp_ from the _publisher_ Namespace each contain a machineId. We want all downstream processing to be separated for each machine to ensure that temperature readings from one machine are not matched against readings from a different machine. To do this, we must add a _SplitByGroup_ task below the _TempStream_ task. Drag and drop _SplitByGroup_ from the Activity Pattern palette on the left side of the App Builder (found in the _Flow Control_ palette section) on top of the _TempStream_ task. Rename the task _SplitByMachineId_ by clicking on the newly added task. Then click _Click to Edit_ next to Configuration label to edit the _SplitByMachineId_ configuration.

![splitByGroupConfiguration](../assets/img/brokertutorial/splitByGroupConfiguration.png "SplitByGroup Configuration")

The property we want to split by is machineId. Click on the downward arrow next to the _groupBy_ parameter and select _event.machineId_ from the property menu. Click **OK** to close the configuration dialog and then save the Service again.

![appWithSplitByGroup](../assets/img/brokertutorial/appWithSplitByGroup.png "App With SplitByMachineId")

### Step 3: Detect Machine Overheating

The random temperature readings published to _/machine/temp_ from the _publisher_ Namespace range from 0 to 100, so we'll say the machine is overheating whenever the temperature rises above 100 degrees. To detect when the temperature crosses from under 100 to over 100, we must add a threshold task below the _SplitByMachineId_ task. Drag and drop _Threshold_ from the Activity Pattern palette on the left side of the App Builder (found in the _Filters_ palette section) on top of the _SplitByMachineId_ task. Rename the task _DetectOverheat_ by clicking on the newly added task. Then click _Click to Edit_ next to Configuration label to edit the _DetectOverheat_ configuration. 

![128_EventsTut_ThresholdActivity](../assets/img/brokertutorial/128_EventsTut_ThresholdActivity.png "Threshold Configuration")

The condition we want to check is `event.temperature>100`, so enter that in the _condition_ input field.
 
The _direction_ property should be set to _true_ because we only care when the condition changes from false to true, meaning the temperature was under 100 degrees and is now over 100 degrees. Click **OK** to close the configuration dialog and then save the Service again. 

![appWithUncrossedThreshold](../assets/img/brokertutorial/appWithUncrossedThreshold.png "App With Uncrossed Threshold")

### Step 4: Test Threshold Crossing

You'll notice while the _OverheatDetector_ Event Handler is running that the threshold task is never triggered. That's because the data generated in the _publisher_ Namespace is always below the threshold. To check that the threshold task is properly configured, we can simulate an overheating event in this Namespace by publishing an event to the _/machine/temp_ Topic with a temperature outside the normal range. This published event won't go through the Catalog, but it will behave as if it came from the Catalog within the _subscriber_ Namespace. To publish this event, click on
the _/machine/temp_ Topic in the Project Contents list (found at the left of the IDE) to open the Topic detail pane. Edit the **Publish Message**
field to use _Machine1_ as the _machineId_ and set the temperature to any number greater than 100:

![publishThresholdCrossingEvent](../assets/img/brokertutorial/publishThresholdCrossingEvent.png "Publish Threshold Crossing Event")

Click the **Publish** button to publish the event. After you publish the event, you should see the counter next to the _DetectOverheat_ task display the number 1. Change the _machineId_ value in the Topic detail pane to _Machine2_ and publish the event again and you'll see the counter increment to 2.

One important note is that after a threshold is crossed, no other event will be produced by the threshold task until the boundary is crossed again. If the generator in the _publisher_ Namespace is producing data below the threshold and
the threshold is crossed by a manual publish in this Namespace, publishing a second event with a temperature over 100 will not produce more output from the threshold until the generator generates another temperature below 100. 

### Step 5: Publish Overheat Events

Now that we can detect when a machine is overheating, the last step is to publish the overheat events back to the Catalog.
To do this, we must add a _PublishToTopic_ task below the _DetectOverheat_ task. Drag and drop _PublishToTopic_ from the Activity Pattern palette on the left side of the App Builder (found in the _Actions_ palette section) on top of the _DetectOverheat_ task. 
Rename the task _PublishToCatalog_ by clicking on the newly added task. Then click _Click to Edit_ next to Configuration label to edit the _PublishToCatalog_ configuration.

In the resulting dialog, type _/local/machine/overheat_ as the topic. Select the name of the catalog from the **catalog** droplist.
Finally, select _/machine/overheat_ as the **event** and click **OK**.
Now, all events that flow through this task will be published to the topic _/local/machine/overheat_ which will be registered as a publisher
for the _/machine/overheat_ in the Catalog. All _/machine/overheat_ subscribers will receive the event.

![publishToCatalog](../assets/img/brokertutorial/PublishToCatalogConfig.png "Publish to Catalog")

Now, save the Service and you will see an extra node appear in the graph below the **PublishToCatalog** task marking the task as a catalog publisher for the _/machine/overheat_ event type.

![publishToCatalog](../assets/img/brokertutorial/PublishToCatalogSyntheticNodeAdded.png "Full TempStream App")

### Step 6: Create Overheat Type
In addition to using the Catalog for events, the Catalog may also be used to host Vantiq [Services](../resourceguide.md#services). Services are containers for Procedures which can be used to organize a collection of related Procedures into a common package. In the next few steps, we will create and host a Service, _machineTemperatureService_. However, before we can create _machineTemperatureService_, we first need to define a data type which represents an instance of a machine overheat event.

Use the **Add** button to select **Type** and create a new Standard type. In the resulting dialog, name the type _OverheatedMachine_ and assign it the following properties:

* _machineId_ (String) - A unique identifier that associates a reading with a specific machine.
* _temperature_ (Integer) - The sensor reading in degrees fahrenheit.
* _timestamp_ (DateTime) - The time at which the sensor reading was recorded.
* _hasBeenMaintenanced_ (Boolean) - If the machine has been subject to maintenance since it last malfunctioned

![overheatType](../assets/img/brokertutorial/OverheatMachineType.png "Overheat type")

### Step 7: Save to Overheat Type

When a machine overheats, we want to document the occurrence for historical purposes by inserting an instance of the _OverheatedMachine_ type. Drag and drop _SaveToType_ from the Activity Pattern palette on the left side of the App Builder (found in the _Actions_ palette section) on top of the _DetectOverheat_ task.

Click on the _SaveToType_ Task and name the task _RecordOverheat_. Next, click _Click to Edit_ next to Configuration label to edit the _RecordOverheat_ configuration. Select _OverheatedMachine_ as the type. Click **OK** and then save the Service.

![SubscriberApp](../assets/img/brokertutorial/subscriberApp.png "Subscriber App")

### Step 8: Create the _machineTemperatureService_ Service

Next, you will create a Service which will be published to the Catalog. This Service will be used by subscribers of the _/machine/overheat_ event to determine whether or not the overheating machine requires maintenance.

Use the **Add** button to select **Services** and click **+ New** to create a new Service. Create a new Service named **machineTemperatureService** with a package of machine.maint and click **OK**.

In the Service pane add the following description: _Service to keep track of machine status_.

![machineTemperatureService](../assets/img/brokertutorial/machineTemperatureServiceWithDesc.png "machineTemperatureService")

Navigate to the Interface tab in the Service pane and click the Add button next to Procedures to add a new Procedure interface to the service.

Define a new Procedure Signature with the following properties:

* _Name_: doesMachineNeedMaint
* _Description_: Returns true if a machine has overheated three times this week
* _Return Type_: Boolean

![machineServiceParameter](../assets/img/brokertutorial/addSignaturePopup.png "machine Service parameter")

Click __+ New Parameter__ then on the pencil icon next to it, and add a parameter with the following properties:

* _Name_: _machineDef_
* _Description_: machine descriptor
* _Type_: Type _MachineData_

![machineServiceParameter](../assets/img/brokertutorial/machineServiceParameter.png "machine Service parameter")

To generate the Procedure stub, go to the Implement tab, right-click on the unbound procedure, and select _Add Procedure_. Save the Service.

![machineServiceProceduresTab](../assets/img/brokertutorial/machineProceduresTab.png "machine Service procedures tab")

Next, we need to fill in the _machineTemperatureService.doesMachineNeedMaint_ Procedure. Add the following Procedure text that returns true if the machine has overheated three times in the past week.

```
/* Returns true if a machine has overheated three times this week */
package machine.maint
import type OverheatedMachine
import type MachineData
PROCEDURE machineTemperatureService.doesMachineNeedMaint(machineDef MachineData):Boolean
var oneWeekAgo = now().minusMillis(1 week)
var overheatedMachines = SELECT * FROM OverheatedMachine WHERE timestamp > oneWeekAgo  and machineId == machineDef.machineId and hasBeenMaintenanced == null
return overheatedMachines.size() > 3
```

Save the Service. Return to the **Interface** tab, click General, then click the **Publish** button. After publishing the Service to the Catalog, the Service is now available to all Namespaces that have access to the Catalog.


### Step 9: Subscribe to Overheat Events

Now we will subscribe to _/machine/overheat_ events in the _publisher_ Namespace. First, switch into the _publisher_ Namespace.

We will create an Service Event Handler which reacts to _/machine/overheat_ events and detects whether or not the overheating machine requires maintenance. If maintenance is required, the event handler will trigger another
App with collaboration tasks.

Use the **Add** button to select **Service** then click the **New Service** button. Name the Service _OverheatService_ with a package of machine.overheat. Add a Service Event Handler to the Service by clicking the plus button next to _Service_ in the _Implement_ tab and adding a Service Visual Event Handler. Name the Event Handler _OverheatHandler_.
 
 Click on the orange EventStream box. Name the EventStream _overheatEventStream_. Click _Click to Edit_ to configure the EventStream. Select _topics_
 as the inboundResource. Click on the magnifying glass button to the left of the _inboundResourceId_ box. This will allow you to subscribe directly to the
 _/machine/overheat/_ event from the Catalog. 
![subscribeFromAppPlus](../assets/img/brokertutorial/clickOnPlusBtn.png "subscribeFromApp Plus button")

 Select  _/machine/overheat/_, then subscribe, and then _/machine/overheat_ again.
 ![subscribeToEventInApp](../assets/img/brokertutorial/subscribeToEventInApp.png "subscribe to event from app")

 Notice that the _MachineData_ type was automatically set as the _schema_ for this EventStream. 
 
 ![EventStreamConfig](../assets/img/brokertutorial/configureEventStream.png "Event Stream configuration")

Click **OK** to close the dialog.

Drag and drop _Procedure_ from the Activity Pattern palette on the left side of the App Builder (found in the _Actions_ palette section) on top of the _overheatEventStream_ task. Rename the task _doesMachineNeedMaintenance_ by clicking on the newly added task then clicking _Click to Edit_ next to Configuration label to edit the _doesMachineNeedMaintenance_ configuration.
  
Click on the Search icon next to the Procedure droplist to subscribe to a Service in the Catalog.
 
![clickOnBook](../assets/img/brokertutorial/clickOnBook.png "Click on book")

Select _machineTemperatureService_ as the Service. Click subscribe, then click **OK** to subscribe to the Service. When the dialog closes, select _machineTemperatureService.doesMachineNeedMaint_ from the Procedure droplist and click **OK**.
 
This App is now using the Procedure defined in the Service that was published to the Catalog by the _subscriber_ Namespace. By subscribing to the Service through the Catalog, this Namespace invokes the Procedure as if it were defined locally.
 
![procedureTaskConfig](../assets/img/brokertutorial/configureProcedureCall.png "procedureTaskConfig")
  
Close out of the procedure configuration and add a _Filter_ task below the _doesMachineNeedMaintenance_ task, by dragging and dropping _Filter_ on top of the _doesMachineNeedMaintenance_ task. Keep the downstream event as "event". Click **OK** to close the dialog.
 
Click on the Filter task, name this task _machineNeedsMaintenance_. Then click _Click to Edit_ to configure the task. Set the condition to `event == true`. The Procedure we called above will return a Boolean so we only want to continue downstream when the Procedure returns true.
 
![filterTaskConfig](../assets/img/brokertutorial/setFilter.png "filter task config")

 Click **OK**. 
 
 ![filterAddedToApp](../assets/img/brokertutorial/filterAddedToApp.png "filter added")

Finally, drag a _PublishToTopic_ task onto the _machineNeedsMaintenance_ filter Task and keep "event" as the downstream event. Click on the new _PublishToTopic_ Task and name the task _maintenanceCollab_. Then click _Click to Edit_ to configure the task.
Set the topic to */start/maintenanceCollab* and click **OK** to close the pop-up.

![startCollabConfig](../assets/img/brokertutorial/nameStartCollab.png "nameStartCollab")

In a fully complete system, this PublishToTopic would trigger another App which would likely find and request a repair person to fix the overheating machine. 
For brevity, this step has been removed from this tutorial. For more information on Collaborations, see the [Collaboration Tutorial](./introcollaboration.md).
 
Click the **Save** button to save the Service.

### Step 10: Catalog Round Trip

The last step in this tutorial is to test the complete round trip by:

* Publishing a temperature event from the _publisher_ Namespace with a temperature over 100
* Identifying the overheating machine in the _subscriber_ Namespace
* Publishing the overheat event from the _subscriber_ Namespace
* Verifying the overheat event shows back up in the _publisher_ Namespace
* Calling a Service Procedure in the publisher Namespace which was defined in the subscriber Namespace
* Detecting whether the machine requires maintenance

We already have a rule running in the _publisher_ Namespace that produces "good" temperature readings, so all we need to do to trigger an overheat event is publish a single "bad" temperature reading. 

We will do this using an Event Generator, so it is easily repeatable. Use the **Test** button to select **Event Generator** then click **New Event Generator**. Name the event generator _GenBadEvents_ and click the OK button. 
Add a new Generator by clicking the small plus button at the top of the Event Generator Pane. 

![newEventGen](../assets/img/brokertutorial/newEventGen.png "New Event Generator")

Give it the following properties:

* _Resource_: Topics
* _ResourceId_: /my/machine/temp/event
* _Repeat_: Iterations, 3
* _Interval_: 1 second

In the _Properties_ section, set the following properties:

* _machineId_: 
  * _Variation_: Constant
  * _Value_: Machine1
* _temperature_:
  * _Variation_: Range
  * _Random_: True
  * _Min_: 101
  * _Max_: 200
* _timestamp_:
  * _Variation_: Current Time

![eventDescriptor](../assets/img/brokertutorial/eventDescriptor.png "Event Descriptor")

Click Create.

Save the Event Generator and run it. The blue _Run Generator_ button should change into a red _Stop Generator_ button, indicating that the event generator is running.


You should see three events show up in the _OverheatDetector_ Event Handler. The event will stop at the _doesMachineNeedMaintenance_ task because the machine has not overheated more than three times this week.

![App received event](../assets/img/brokertutorial/appReceivedEvent.png "App received event")

Execute the Event Generator a second time. The fourth event will travel all the way down the Event Handler and trigger the next handler with its collaboration.

![CollabTriggered](../assets/img/brokertutorial/collabTriggered.png "Collaboration triggered")

## Conclusion ##

At the completion of this tutorial, a developer should be familiar with:

* The relationship between Catalogs, Event Subscribers and Event Producers
* The concept that Subscribers can also be producers and producers can also be subscribers
* How to register Namespaces with Catalogs
* Proper Topic nomenclature
* Populating Catalogs with events
* Subscribing to events from other Namespaces
* Ways to publish simulated events
* Creating a Service
* Publishing a Service to the Catalog
* Subscribing to a Service and using Service Procedures in a subscriber Namespace

For more details on the **Vantiq Catalog**, please refer to the [Catalog documentation](../broker.md).

