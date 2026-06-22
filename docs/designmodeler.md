# Design Modeler Reference Guide

## Introduction
The Design Modeler is the visual IDE tool for building Vantiq systems. It allows the user to easily connect Services and Clients, which are the building blocks of a Vantiq system. It also allows for the graphical visualization of how the events flow through a Vantiq system.

## Tutorials
For an introduction to the use of the Design Modeler, follow the [Introductory Tutorial](tutorials/tutorial.md). This tutorial introduces the basics of creating a new Design Model to implement a simple engine monitoring system. In addition, the [System Model Tutorial](tutorials/systemmod.md) shows how to model business process requirements and then produce a Design Model based on those requirements.

## Creating a New Design Model
New Design Models are created using **Add>Design Model** and clicking the **New Design Model** button. For the remainder of this guide, we'll instead use an example Vantiq project using an import process.

Use the **Project** menu to select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Existing** as the Project type and click **Continue**.

Next, select the **Import Projects** option and click **Go to Import Project Dialog**.

In the **Import Contributions** dialog, select *Contributions* as the **Select Import Type** and *IntroductoryStart* as the **Select From Contributions**, then click **Import**.

After the import process is complete, reload the *IntroductoryStart* project by clicking the **Reload** button:

&nbsp;&nbsp;&nbsp;&nbsp;![ImportStarter](../assets/img/intro/ImportStarter.png "Import Intro Starter")

After the project reload is complete, the _com.vantiq.engines.EngineMonitor_ Design Model pane is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![DesignModelInitial](assets/img/intro/DesignModelInitial.png "Initial Design Model")

## Understanding the Design Model Pane
The right side of the Design Model pane contains the graphical representation of the model. In the example shown above, there are six nodes in the graph:

- **Sensors**: this is an _External System_ Design Modeler node, which graphically represents the engine's temperature and speed sensors. External System nodes are used for documentation purposes only. They are meant to represent how the Vantiq system being built receives or transmits data external to the Vantiq system.
- **EngineMonitorSensors**: this is a _Service_ Design Modeler node, which represents an actual Vantiq Service. This Service has a limited purpose: to receive messages from the temperature and speeds sensors and to forward those events to the _EngineMonitor_ Service for processing.
- **EngineMonitor**: this is another _Service_ Design Modeler node which represents the Service that will use data from the sensors, determine if that data indicates possible problems with the engine, then forwards the sensor data and engine status to the _EngineMonitor_ Client for display. In this tutorial, the [Service Builder](services.md) is used to modify both Services in this Design Model.
- **EngineMonitor**: this is a _Client_ Design Modeler node which represents the Client that will display engine status: speed, temperature and any error status. In this tutorial, the [Client Builder](cbuser.md) is used to modify the Client in this Design Model.
- **DataWarehouse**: this is another _External System_ Design Modeler node. It could represent a database, either Vantiq's native database or an external database system, to store data received or calculated by the engine system. Since this is a real-time engine status system, this node won't be used and is deleted as this tutorial progresses.
- **OutsideWorld**: like the _DataWarehouse_ node, it could represent, for example, a REST API or MQTT server, that might consume data from this Vantiq system.

The left side of the Design Model pane contains two sections. The upper section is the Design Modeler palette. The palette contains five drag-and-droppable items that are used to create new nodes (External Systems, Services, and Clients) in the Design Model:

- **New Service**: add a placeholder Service. Placeholder Services are used to represent Services that are in development but have not been created as an actual Service. Using the graph, new Inbound and Outbound Event Types may be created between placeholder Services and other Services and Clients. New connections may also be created between placeholder Services and External Systems. See the [next section](#converting-placeholder-services-and-clients) for how to convert a placeholder Service to an actual Service.

- **Service**: add an existing Service. The developer must select a Service in the current Namespace or subscribe to or install one from a Catalog, if available. As with a placeholder Service, new Inbound and Outbound Event Types may be created using the graph between placeholder Services and other Services and Clients. New connections may also be created between placeholder Services and External Systems.

- **New Client**: add a placeholder Client. As with placeholder Services, placeholder Clients are used to represent Clients that are in development but have not been created as an actual Client. Using the graph, new [Client Data Streams](cbuser.md#data-streams_1) may be created between Service Outbound Event Types and placeholder Clients. See the [next section](#converting-placeholder-services-and-clients) for how to convert a placeholder Client to an actual Client.

- **Client**: add an existing Client. The developer must select a Client in the current Namespace or subscribe to or install one from a Catalog, if available. As with a placeholder Client, new Client Data Streams may be created using the graph between Service Outbound Event Types and placeholder Clients.

- **External System**: add a new External System node to represent data external to a Vantiq system.

The lower section of the left side of the Design Model pane is the **To Do List**. The **To Do List** contains errors found in any of the Services contained in the Design Model. When a Design Model is initially generated, these errors are normal and are all associated with Inbound Event tasks in those Services that need to be configured for the specific needs of the system being developed.

Clicking on a **To Do List** item causes the Service pane that contains the error to be displayed. An example from the [Introductory Tutorial](tutorials/tutorial.md) is shown below:

&nbsp;&nbsp;&nbsp;&nbsp;![FirstError](assets/img/intro/FirstError.png "First Error")

Use the **To Do List** to find and clear each error until the **To Do List** is empty and disappears. This indicates there are no Service configuration errors.

Click the **Show Flow View** checkbox in the toolbar to split the Design Modeler canvas into two sections: the Design Model graph and the Flow View:

&nbsp;&nbsp;&nbsp;&nbsp;![Flow View](assets/img/designmodeler/FlowView.png "Flow View")

The Flow View shows an event-processing view of the tasks in the Design Model. The majority of the nodes in the Flow View are related to Inbound Event Handlers found in Services (e.g. the _Ingest_ and _Transform_ nodes) but will also contain nodes representing Clients (e.g. _EngineMonitor_). The reason why there so many disconnected nodes in the Flow View shown above is that there are unconfigured tasks in this Design Model. Once the **To Do List** items are addressed, the Flow View graph should be highly connected.

## Converting Placeholder Services and Clients
When the developer is ready to create an actual Service based on the placeholder Service, they double-click the Service's node to display the _Editing Service_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;![EditService](assets/img/designmodeler/EditService.png "Edit Service")

Use the **Service** pull-down menu to select _Create New Service_. The **Label** text will change to reflect a suggested name (including a package prefix). Use the **Label** text to modify the name of the Service, if desired. As the dialog indicates, the new Service will be created when the Design Model is saved.

Creating an actual Client based on a placeholder Client follows the same pattern as for placeholder Services as described above.

## Creating New Connections
The Design Model graph handles simple user gestures for creating new links between Services, Clients, and External Systems.

> Please note that the Design Modeler is the **only** way to create working connections between Services to ensure that data produced by an Outbound Event Type is delivered to another Service's Inbound Event Type.

### New Service Connections
Consider the Design Model shown below, which represents a simple IoT system:

&nbsp;&nbsp;&nbsp;&nbsp;![IoTStart](assets/img/designmodeler/IoTStart.png "IoT System")

The _IoTExample_ node represents a Service that is receiving IoT sensor data from the _IngestExternalSensorEventsService_ Service. The _DeviceManager_ node is a placeholder Service that is being developed to receive status update data based on sensor readings. To create a new connection between _IoTExample_ and _DeviceManager_ to allow those status updates, click and drag from the small blue circle next to the _Add Outbound Event_ label of _IoTExample_ to the small blue circle next to the _Add Inbound Event_ label of _DeviceManager_:

&nbsp;&nbsp;&nbsp;&nbsp;![NewServiceConnection](assets/img/designmodeler/NewServiceConnection.png "New Service Connection")

When the mouse is released, a dialog is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![NameServiceConnection](assets/img/designmodeler/NameServiceConnection.png "Name Service Connection")

Since the connection is supposed to represent status updates, we'll name both Service Event Types _UpdateStatus_. Click **OK** to create the connection. The Design Model graph updates to show the new connection:

&nbsp;&nbsp;&nbsp;&nbsp;![CompleteServiceConnection](assets/img/designmodeler/CompleteServiceConnection.png "Complete Service Connection")

Save the Design Model using the **Save Changes** icon in the Design Model pane's titlebar. Once the Design Model is saved, the _IoTExample_ Service is updated with a new Outbound Event Type called _UpdateStatus_. To see that update, right-click the _IoTExample_ Service node on the graph and select _Open in Service Builder_. The _Service: com.vantiq.example.IoTExample_ pane is displayed. Click the _Outbound_ tab to display the Outbound Events of the Service. Note there are now two Outbound Event Types: the preexisting _AnomalyDetected0_ Event Type and the newly-created _UpdateStatus_ Event Type:

&nbsp;&nbsp;&nbsp;&nbsp;![ServiceService](assets/img/designmodeler/ServiceService.png "Service to Service Connection")

Since the _DeviceManager_ Service in the Design Model is a placeholder Service, its _UpdateStatus_ Inbound Event Type is also a placeholder for an Inbound Event Type. That Inbound Event Type will be created when the Service is [converted to a real Service](#converting-placeholder-services-and-clients).

### New Client Connections
Using the example from above, to create a new connection between the _IoTExample_ Service (with the green node titlebar) and the _IoTExample_ Client (with the purple titlebar), click and drag from the small blue circle next to the _UpdateStatus_ label of the the Service to the small blue circle next to the _Add Data Stream_ label of the Client:

&nbsp;&nbsp;&nbsp;&nbsp;![NewClientConnection](assets/img/designmodeler/NewClientConnection.png "New Client Connection")

When the mouse is release, a dialog is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![NewDataStream](assets/img/designmodeler/NewDataStream.png "New Data Stream")

Since the connection is supposed to represent the display of status updates, we'll name the Client's Data Stream _DisplayStatus_. Click **OK** to create the connection. The Design Model graph updates to show the new connection:

&nbsp;&nbsp;&nbsp;&nbsp;![ServiceClient](assets/img/designmodeler/ServiceClient.png "Complete Client Connection")

Once the Design Model is saved, the _IoTExample_ Client is updated with a new Data Stream called _DisplayStatus_. Data sent via the _IoTExample_ Service's _UpdateStatus_ Outbound Event Type can then be used in the Client by selecting its _DisplayStatus_ Data Stream.

## Bridge Services
Continuing to use the simple IoT system described above, consider the changes shown in this updated Design Model:

&nbsp;&nbsp;&nbsp;&nbsp;![BridgeServiceSetup](assets/img/designmodeler/BridgeServiceSetup.png "Bridge Service Intro")

The placeholder _DeviceManager_ Service has been [converted to a real Service](#converting-placeholder-services-and-clients) and defines a new Inbound Event Stream called _UpdateDefect_. To specify the format of the data received by the Service, the _UpdateDefect_ Event Stream has been assigned an Event Schema _com.vantiq.example.DefectiveDevice_.

Next, we want to feed events published on the _IoTExample_ Service's _AnomalyDetected0_ Outbound Event Type to the new _UpdateDefect_ Inbound Event Stream of _DeviceManager_. Click and drag from the small blue circle next to the _AnomalyDetected0_ label to the small blue circle next to the _UpdateDefect_ label. When the mouse is released, a dialog is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![NewBridgeService](assets/img/designmodeler/NewBridgeService.png "New Bridge Service")

This dialog appears when a new connection between existing Service Event Types is created but the Event Type schemas do not match. This means the outbound data has a different format than the Inbound Event Type expects. A "Bridge Service" is necessary in this case to transform the outbound data into the specified format expected by the Inbound Event Type. We'll name the Bridge Service _BridgeDefect_. Click **OK** to create the _BridgeDefect_ Service node, then save the Design Model. You must save the Design Model in order for the _BridgeDefect_ Service to be created. The Design Model will now look similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;![BridgeComplete](assets/img/designmodeler/BridgeComplete.png "Bridge In Place")

The only purpose of the _BridgeDefect_ Service is to implement a Transformation task in a Visual Event Handler that looks like this:

&nbsp;&nbsp;&nbsp;&nbsp;![BridgeTransform](assets/img/designmodeler/BridgeTransform.png "New Bridge Transform")

Configure the _Transformation_ task to convert the data format from the schema associated with the _AnomalyDetected0_ Outbound Event Type into the data format for the schema associated with the _UpdateDefect_ Inbound Event Type.

## System Model Requirements
Design Models can be created from System Models using the [System Modeler's Generate feature](tutorials/systemmod.md#4-generating-a-design-model). Design Models generated via the System Modeler will have an additional section on the left side of the Design Model pane called the Requirements List:

&nbsp;&nbsp;&nbsp;&nbsp;![DesignModel](assets/img/systemmod/DesignModel.png "Design Model")

The Requirements List is the list of all of the System Model notes. As the Design Model is developed, check off each of the Requirements List items as they are developed in the Design Model. You can drag and drop list items to change the order of list items.
