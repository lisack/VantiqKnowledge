
# Introductory Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningClient](../assets/img/intro/RunningClient.png "Running Client")

## Objectives
Upon completion of this tutorial, a new developer will be able to:

* Easily navigate around the Vantiq IDE
* Create a simple real-world Vantiq application

## Tutorial Overview
This tutorial uses a practical example from the Internet of Things (IoT): processing data from engine temperature and speed sensors to detect and diagnose an overheating engine. The basic steps to creating this application are:

* Create a new Project
* Import an existing Vantiq Contributions project with some initial Project resources
* Create Sources to receive simulated sensor data
* Use the Service Builder's visual event handler to specify how the application reacts to asynchronous, real-time engine conditions
* Create a visual front-end with a Client
* Run the application in simulation

>Note: if needed, you can import a finished version of this project using the **Projects** button and select **Import**. Select _Tutorials_ for Import Type, then select _Introductory_ from the second drop-down, then click **Import**.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

### Namespace Privileges

<a name="namespace_privilege"></a>
In addition, when following the Tutorials, please make sure you are logged in as the administrator of the Vantiq namespace to which you are assigned. You can check your privilege level by clicking on your username in the title bar. If the bottom of the popup says, "Developer" or "Namespace Admin" at the bottom, you have the needed privileges. If it says, "User (Developer)," then you need to [change to a Developer namespace](./admin.md#change_namespace). You may need to first create your own Developer namespace, as described here: [Creating a Developer Namespace](./admin.md#create_dev_namespace).

## 1: Creating an Engine Monitoring Project
The first task in building the engine monitoring system is to create a Project in the Vantiq IDE.

>Note: You will be alerted if you do not have permission to create a project in the current namespace. You need to change to, or create, a namespace where you have Developer or Namespace Admin privilege ([see above](./tutorial.md#namespace_privilege)).

Use the **Project** menu to select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Existing** as the Project type and click **Continue**.

Next, select the **Import Projects** option and click **Go to Import Project Dialog**.

In the **Import Contributions** dialog, select *Contributions* as the **Select Import Type** and *IntroductoryStart* as the **Select From Contributions**, then click **Import**.

After the import process is complete, reload the *IntroductoryStart* project by clicking the **Reload** button:

&nbsp;&nbsp;&nbsp;&nbsp;![ImportStarter](../assets/img/intro/ImportStarter.png "Import Intro Starter")

After the project reload is complete, the _com.vantiq.engines.EngineMonitor_ Design Model pane is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![DesignModelInitial](../assets/img/intro/DesignModelInitial.png "Initial Design Model")

## 2: Understanding the Design Model
The Design Modeler is a visual IDE tool for building Vantiq systems. It allows the user to easily connect Services and Clients, which are the building blocks of a Vantiq system. The Design Model generated for the engine monitor Project contains six nodes:

- **Sensors**: this is an _External System_ Design Modeler node, which graphically represents the engine's temperature and speed sensors. External System nodes are used for documentation purposes only. They are meant to represent how the Vantiq system being built receives or transmits data external to the Vantiq system.
- **EngineMonitorSensors**: this is a _Service_ Design Modeler node, which represents an actual Vantiq Service. This Service has a limited purpose: to receive messages from the temperature and speeds sensors and to forward those events to the _EngineMonitor_ Service for processing.
- **EngineMonitor**: this is another _Service_ Design Modeler node which represents the Service that will use data from the sensors, determine if that data indicates possible problems with the engine, then forwards the sensor data and engine status to the _EngineMonitor_ Client for display. In this tutorial, the [Service Builder](../services.md) is used to modify both Services in this Design Model.
- **EngineMonitor**: this is a _Client_ Design Modeler node which represents the Client that will display engine status: speed, temperature and any error status. In this tutorial, the [Client Builder](../cbuser.md) is used to modify the Client in this Design Model.
- **DataWarehouse**: this is another _External System_ Design Modeler node. It could represent a database, either Vantiq's native database or an external database system, to store data received or calculated by the engine system. Since this is a real-time engine status system, this node won't be used and is deleted as this tutorial progresses.
- **OutsideWorld**: like the _DataWarehouse_ node and for the same reasons, this node is deleted later on.

This Design Model represents a flow of events in an IoT system. Here is how the data and events for the engine monitoring system will inform us to modify the Services and Clients to develop a working system:

1. Sensor data is captured from two [MQTT Sources](../sources/source.md). The speed and temperature data is simulated by a public MQTT server hosted by Vantiq.
2. The receipt of the Sensor data is handled by the _EngineMonitorSensors_ Service described above. This Service doesn't need to transform data for our engine monitor system but instead simply publishes it as [Outbound Event Types](../services.md#outbound-event-types) to the _EngineMonitor_ Service for processing. This example uses two Services to separate the receipt of raw sensor data from the processing of the data as Event Types. This architecture allows the _EngineMonitor_ Service to be reused in other Vantiq systems that process temperature and speed similarly.
3. The _EngineMonitor_ Service receives the temperature and speed Event Types in two separate Event Handlers.

    a. The speed Event Handler (_SpeedEvent_) simply saves the sensor data in a Service's _speed_ [Global State variable](../servicestatemgmt.md#global-state) then republishes that event to an Outbound Event Type for use by the _EngineMonitor_ Client. The _speed_ Global State variable is necessary so the temperature Event Handler may retrieve and use the speed data without having to store it in the Vantiq database. 
    
    b. The temperature Event Handler (_TemperatureEvent_) reads the temperature data to determine if there is an overheating condition (if the temperature reading is 210F or greater). If the engine is overheating, the handler reads the _speed_ Global State variable and constructs an alert message based on the combination of the temperature and speed sensor values. The handler then publishes an event that contains temperature and overheat status data to an Outbound Event Type for use by the _EngineMonitor_ Client.
    
4. The _EngineMonitor_ Client receives speed, temperature, and overheat status from the _EngineMonitor_ Service's two Outbound Event Types. These events are processed by two [Client Data Streams](../cbuser.md#data-streams_1), each of which are used to run [Client widgets](../cbuser.md#data-stream-widgets) (gauges, line charts, etc.) to display the data in a dashboard-like display.

>Please note this is a simple example of a working Vantiq system. It demonstrates basic event handling and filtering and works well for a system with a low rate of data receipt (the simulated speed and temperature MQTT messages are received at a rate of one per second). The _EngineMonitor_ Client can easily process the events produced by the _EngineMonitor_ Service, which are produced at no more than two per second.

<!-- -->
>The system demonstrates the basic architectural principles required to build scalable systems that process thousands of events each second. The core principle is to process the events in memory as they arrive, maintaining any state required for real-time processing in memory as Service Global State. The traditional approach of storing the events in a database when they arrive and then querying the database to process the events is too slow when processing thousands of events each second.

<!-- -->
>This simple example is not scalable to thousands or more events per second because it does not exploit the [flow control and filtering features](../apps.md#activity-patterns) that the Event Handler system provides to filter or combine data and reduce the overall number of events processed by the system and delivered to Clients.

<!-- -->
>Finally, this system also demonstrates a Client that does not have to retrieve data from a database and process it in order to display useful system status. It should be a goal of any scalable system to limit data transformation and modification operations to Service Event Handlers rather than delegating that work to Clients.

## 3: Create the Engine Sensor Sources
Two [MQTT Sources](../sources/source.md) must be created to simulate the speed and temperature data from a public MQTT server hosted by Vantiq.

Use the **Add** menu to select **Source...**:

&nbsp;&nbsp;&nbsp;&nbsp;![AddSource](../assets/img/intro/AddSource.png "Add Source")

Use the **New Source** button to display the _New Source_ pane. Enter the following values to configure the source:

1. **Source Name**: SpeedSensor
2. **Package**: com.vantiq.engines
3. **Source Type**: MQTT	
	
Add a Server URI from the **Server URI** tab: _tcp://public.vantiq.com:1883_
    
Add a Topic from the **Topic** tab: _com.vantiq.mqtt.enginespeed_

Save the Source then click the **Test Data Receipt** button from the pane's toolbar. The Source pane will switch to the Subscription pane to display data received from the MQTT server:

&nbsp;&nbsp;&nbsp;&nbsp;![SpeedData](../assets/img/intro/SpeedData.png "Speed Data")

Note the simulated data is sent approximately once per second and contains a JSON object with two properties: _systemId_ and _speed_.

Follow similar steps to create a second Source to receive simulated temperature events. Enter the following values to configure the source:

1. **Source Name**: TemperatureSensor
2. **Package**: com.vantiq.engines
3. **Source Type**: MQTT	
	
Add a Server URI from the **Server URI** tab: _tcp://public.vantiq.com:1883_
    
Add a Topic from the **Topic** tab: _com.vantiq.mqtt.enginetemp_

Save the Source.
    

## 4: Renaming the Design Model's Events
In [Lesson 2](#2-understanding-the-design-model) above, a four-step description described the flow of data and events for the engine monitoring system to be built. This lesson shows how to rename the Service Event Types and Client Data Streams to more accurately reflect that flow of data and events.

1. Right-click the _EngineMonitorSensors_ Service in the Design Model, then select _Edit in Service Builder_ menu item. The pane for that Service is displayed. Expand the _Outbound_ section under the _Interface_ tab, then select _Sensor0_, as shown below:

    ![RenameSensor0](../assets/img/intro/RenameExternalEvent0.png "Rename Sensor0")

    Change the **Name** of the Outbound Event to _SpeedEvent_. Save that change using the **Save Changes** button in the pane's title bar.
    
2. Select _Sensor1_ from the same _Outbound_ section. Change the **Name** of the Outbound Event to _TemperatureEvent_ and again save that change.

3. Right-click the _EngineMonitor_ Service (Service nodes have a green title bar) in the Design Model, then select _Edit in Service Builder_ menu item. The pane for that Service is displayed. Expand the _Inbound_ section under the _Interface_ tab, then select _SensorReading0_. Change the **Name** of the Inbound Event to _SpeedEvent_ and again save that change.

4. Select _SensorReading1_ from the same _Inbound_ section. Change the **Name** of the Inbound Event to _TemperatureEvent_ and again save the change.

5. Expand the _Outbound_ section under the _Interface_ tab, then select _AnomalyDetected0_. Change the **Name** of the Outbound Event to _EngineStatus_ and again save that change.

6. Select _AnomalyDetected1_ from the same _Outbound_ section. Change the **Name** of the Outbound Event to _EngineSpeed_ and again save that change.

7. Right-click the _EngineMonitor_ Client (Client nodes have a purple title bar) in the Design Model, then select _Edit in Client Builder_ menu item. The pane for that Client is displayed. Click the _Edit_ tab, expand the _Data Streams_ tree item, as shown below:

    ![RenameClientDataStream](../assets/img/intro/RenameClientDataStream.png "Rename Client DataStream")
    
	Click the _AnomalyDetected0_ Data Stream to display the _Edit Data Stream_ dialog. Make the following changes in that dialog:
	
    a. **Data Stream Name**: EngineStatus
    
    b. **Service**: com.vantiq.engines.EngineMonitor
    
    c. **Event**: EngineStatus
    
    Click **Save** to save the Data Stream.
    
7. Click the _AnomalyDetected1_ Data Stream to display the _Edit Data Stream_ dialog. Make the following changes in that dialog:
	
    a. **Data Stream Name**: EngineSpeed
    
    b. **Service**: com.vantiq.engines.EngineMonitor
    
    c. **Event**: EngineSpeed
    
    Click **Save** to save the Data Stream, then save the Client using the **Save Changes** icon in the pane's title bar.
	
Note after these changes, the Service and Client node in the Design Model pane changes to reflect the new Event Type and Data Stream names. Use the **Save Changes** button in the Design Model pane's title bar to save those changes.

## 5: Remove Unneeded External Systems
As explained in [Lesson 2](#2-understanding-the-design-model) above, this system doesn't require storing any event data in an External System. This means we can delete the _DataWarehouse_ and _OutsideWorld_ Design Model nodes. Click each of those nodes then use the **Delete** toolbar button to delete them from the Design Model, then save the Design Model. Even though those two nodes are used for documentation purposes only, deleting them more accurately reflects the system being developed. The Design Model pane should now look like this:

&nbsp;&nbsp;&nbsp;&nbsp;![RemoveExternalSystems](../assets/img/intro/RemoveExternalSystems.png "Remove External Systems")

## 6: Address the To Do List
Notice that in the screenshot from the previous lesson, there is a **To Do List** in the lower, left corner of the Design Model pane. The **To Do List** contains errors found in the two Services contained in the Design Model. At this point in the system development process, these errors are normal and are all associated with Inbound Event tasks in those Services that need to be configured for the engine system.

Clicking on a **To Do List** item in a Design Model causes the Service pane that contains the error to be displayed. Click on the first error in the list which will cause the _com.vantiq.engines.EngineMonitor_ Service to display and automatically navigate to the _Implement_ tab which contains the _SpeedEvent_ Inbound Event Handler that is associated with the error. After opening up the "Public" section of the palette and the items within in it, the Service pane should look like this:

&nbsp;&nbsp;&nbsp;&nbsp;![FirstError](../assets/img/intro/FirstError.png "First Error")

>Note that there were two "Public" Event Handlers generated which are called "SensorReading0" and "SensorReading1". These handlers listen for the Event Types called "SpeedEvent" and "TemperatureEvent".  (These are the ones we renamed above.) An Event Handler can listen for one or more Event Types. 


"SensorReading0" is the Event Handler which processes speed sensor data from the _EngineMonitorSensors_ Service. Recall from [Lesson 2](#2-understanding-the-design-model) that the _SpeedEvent_ Inbound Event Type Handler saves the sensor data in a Service's _speed_ [Global State variable](../servicestatemgmt.md#global-state) then republishes that event to an Outbound Event Type for use by the _EngineMonitor_ Client. This involves the following changes to the Visual Event Handler shown in the screenshot above (it contains the _SensorReading_ task (the orange rectangle contained in the _Ingest_ task context):

1. From the **Modifiers** section of the Event Handler palette, drag and drop an _AccumulateState_ task on the _SensorReading_ task. Then click on the _AccumulateState_ task and rename it _SaveSpeed_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **procedure** property. This allows you to write the code snippet for updating your Service’s state based on the incoming events. Select _VAIL Block_ in the _Edit union parameter_ dialog then replace the placeholder VAIL code with the following:

    ```
    var curSpeed = event.speed    
    state = curSpeed
    ```

    Click **OK** to return to the task configuration properties. Enter _speed_ as the **stateProperty** property. Click **OK** to complete editing the _SaveSpeed_ task. The _SaveSpeed_ task has now been configured to update the _speed_ Global State variable every time a sensor reading is received by the _SensorReading_ task. When the _EngineMonitor_ Service gets saved, the _SaveSpeed_ task will cause three Procedures to be generated: _com.vantiq.engines.EngineMonitor.speedGet()_, _com.vantiq.engines.EngineMonitor.speedReset()_, and _com.vantiq.engines.EngineMonitor.speedUpdate()_. These may be used to retrieve, reset and update the _speed_ Global State variable.
    
2. Right-click the _SaveSpeed_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _React_ as the **Task Name** and _event_ as the **Downstream Event**. Click **OK**. This will link the _SaveSpeed_ task to the _React_ task, which was the goal outlined in [Lesson 2](#2-understanding-the-design-model): save the speed sensor value then republish that data via the _React_ task.

3. Click the _React_ task and rename it to _PublishSpeed_. Click the **Click to Edit** link to edit the configuration for this task. The **service** property is correctly set (_com.vantiq.engines.EngineMonitor_). However, the **eventTypeName** property needs to reflect the renamed Outbound Event: replace _AnomalyDetected0_ with _EngineSpeed_. Click **OK**. The Event Handler graph should now look like this:

     ![EditSpeedEvent](../assets/img/intro/EditSpeedEvent.png "Edit Speed Event")
     
4. Since the speed sensor data will only be used when processing the temperature data to determine engine alert status, there are four tasks in the handler that are not needed. Click each of the following tasks and delete them using the Delete key or the Delete item in the pane's toolbar: _Analytics_, _GetStatistics_, _DetectAnomaly_, and _StoreAnalytics_. 
     
5. The blue rectangles in the graph are called "task contexts". These are created to show how tasks are related. Now that some of the tasks have been deleted, two of the task contexts, _Analysis_ and _DetectSituation_, are empty. Right-click each of those task contexts and select the _Remove Task Context_ menu item.

6. To more accurately document the running system, the _SaveSpeed_ task can be added to the _React_ task context. Right-click _React_ and select the _Add Task to Context_ menu item. Select _SaveSpeed_ from the **Task Name** menu, then click **OK**. The Event Handler graph should now look like this:

    ![FinishSpeedEvent](../assets/img/intro/FinishSpeedEvent.png "Finish Speed Event")
     
    Save the changes in the _EngineMonitor_ Service using the **Save Changes** titlebar icon. Notice how the Service's _SpeedEvent_ Event Handler now has no errors and the **To Do List** in the Design Model has fewer items.
    
Click on the next **To Do List** item in the Design Model. This will cause the same _com.vantiq.engines.EngineMonitor_ Service to display and automatically navigate to the Implement tab which contains the SensorReading1 Event Handler (which handles the _TemperatureEvent_ Inbound Event Type) that is associated with the error. The Service pane should look similar to the _SpeedEvent_ Event Handler above because they both processed sensor events in the same way. Here's how to restructure the _TemperatureEvent_ Event Handler for the engine monitoring system:

1. From the **Filters** section of the Event Handler palette, drag and drop a _Filter_ task on the _SensorReading_ task. Then click on the _Filter_ task and rename it _OverheatCheck_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then click the **Add Visual Condition** + button. Enter the following Visual Condition parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: temperature
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: >=
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 210     
    
    Click **OK**. This Visual Filter determines if the engine is overheating by checking if the temperature sensor reading is greater than or equal to 210 degrees. Click **OK** to save the configuration.
    
2. Drag and drop a second _Filter_ task on the _SensorReading_ task. Then click on the _Filter_ task and rename it _NoAlert_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then click the **Add Visual Condition** + button. Enter the following Visual Condition parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: temperature
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: <
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 210     
    
    Click **OK**. This Visual Filter determines if the engine is not overheating by checking if the temperature sensor reading is less than 210 degrees. Click **OK** to save the configuration.

3. From the **Modifiers** section of the Event Handler palette, drag and drop a _Transformation_ task on the _NoAlert_ task.

    Then click on the _Transformation_ task and rename it _ClearAlert_. Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;&#34; 
    
    Click **OK**. This Visual Transformation sets a new event property, _alertMsg_, to have a string value of _&#34;&#34;_ which effectively means there is no alert to be displayed in the engine dashboard. This is because the _NoAlert_ Filter task has determined that the engine is not overheating. Check the **transformInPlace** checkbox, which adds the new _alertMsg_ property to the temperature event. Click **OK** to save the _ClearAlert_ task configuration.
    
4. Right-click the _ClearAlert_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _React_ as the **Task Name**. Click **OK**. This will link the _ClearAlert_ task to the _React_ task, which was the goal outlined in [Lesson 2](#2-understanding-the-design-model): add the overheat status to the temperature then republish that data via the _React_ task.

5. Move the new _Filter_ and _Transformation_ tasks to their proper task context boxes:

	1. Right-click the _React_ task context and select the _Add Task to Context_ menu item. Select _ClearAlert_ from the **Task Name** menu, then click **OK**.
	
	2. Right-click the _DetectSituation_ task context and select the _Add Task to Context_ menu item. Select _NoAlert_ from the **Task Name** menu, then click **OK**.
	
    3. Right-click the _DetectSituation_ task context and select the _Add Task to Context_ menu item. Select _OverheatCheck_ from the **Task Name** menu, then click **OK**.
    
6. Since the temperature sensor data will only be used to determine engine alert status, there are four tasks in the handler that are not needed. Click each of the following tasks and delete them using the Delete key or the Delete item in the pane's toolbar: _Analytics_, _GetStatistics_, _DetectAnomaly_, and _StoreAnalytics_. 
     
7. Now that some of the tasks have been deleted, one of the task contexts, _Analysis_, is empty. Right-click that task context and select the _Remove Task Context_ menu item.

8. Click the _React_ task and rename it to _PublishStatus_. Click the **Click to Edit** link to edit the configuration for this task. The **service** property is correctly set (_com.vantiq.engines.EngineMonitor_). However, the **eventTypeName** property needs to reflect the renamed Outbound Event: replace _AnomalyDetected1_ with _EngineStatus_. Click **OK**. The Event Handler graph should now look like this:

     ![EditTempEvent](../assets/img/intro/EditTempEvent.png "Edit Temperature Event")
     
9. Drag and drop a _Transformation_ task on the _OverheatCheck_ task. Then click on the _Transformation_ task and rename it _RetrieveSpeed_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: speed
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: com.vantiq.engines.EngineMonitor.speedGet()
    
    Click **OK**. This Visual Transformation retrieves the _speed_ Global State variable so that it can be used to choose between one of two engine overheating alert messages in subsequent tasks. Check the **transformInPlace** checkbox, which adds the retrieved _speed_ property to the temperature event. Click **OK** to save the _RetrieveSpeed_ task configuration.
    
10. Drag and drop a _Filter_ task on the _RetrieveSpeed_ task. Then click on the _Filter_ task and rename it _SpeedOverheat_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then add the following two Visual Condition parameters, in this order:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: !=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: null
	
    and
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: >=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 45
    
    Click **OK**. This Visual Filter determines if the engine is overheating and the speed is not null and the speed is greater than or equal to 45. The speed can be null if a speed reading has not yet appeared. A subsequent task will set the overheat alert condition for use by the engine dashboard.
    
11. Drag and drop a _Transformation_ task on the _SpeedOverheat_ task. Then click on the _Transformation_ task and rename it _AddSpeedOverheat_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;Your engine is overheating: please reduce your speed.&#34;
    
    Click **OK**. This Visual Transformation sets the _alertMsg_ property to have a string value of _&#34;Your engine is overheating: please reduce your speed.&#34;_ which means there is an alert to be displayed in the engine dashboard. This is because the _SpeedOverheat_ Filter task has determined that the engine is overheating and the engine speed is above 45. Check the **transformInPlace** checkbox, which adds the new _alertMsg_ property to the temperature event. Click **OK** to save the _AddSpeedOverheat_ task configuration.
    
12. Drag and drop a second _Filter_ task on the _RetrieveSpeed_ task. Then click on the _Filter_ task and rename it _NonSpeedOverheat_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then add the following two Visual Condition parameters, in this order:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: !=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: null
	
    and
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: <
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 45
    
    Click **OK**. This Visual Filter determines if the engine is overheating and the speed is not null and less than 45. A subsequent task will set the overheat alert condition for use by the engine dashboard.
    
13. Drag and drop a second _Transformation_ task on the _NonSpeedOverheat_ task. Then click on the _Transformation_ task and rename it _AddNonSpeedOverheat_.

    Click the **Click to Edit** link to edit the configuration for this task. Click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;Your engine is overheating: check for a malfunctioning fan or a coolant leak.&#34;
        
    Click **OK**. This Visual Transformation sets the _alertMsg_ property to have a string value of _&#34;Your engine is overheating: check for a malfunctioning fan or a coolant leak.&#34;_ which means there is an alert to be displayed in the engine dashboard. This is because the _NonSpeedOverheat_ Filter task has determined that the engine is overheating and the engine speed is below 45. Check the **transformInPlace** checkbox, which adds the new _alertMsg_ property to the temperature event. Click **OK** to save the _AddNonSpeedOverheat_ task configuration.
    
14. Right-click the _AddSpeedOverheat_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _PublishStatus_ as the **Task Name**. Click **OK**. This will link the _AddSpeedOverheat_ task to the _PublishStatus_ task, which was the goal outlined in [Lesson 2](#2-understanding-the-design-model): add the overheat status to the temperature then republish that data via the _PublishStatus_ task.

14. Right-click the _AddNonSpeedOverheat_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _PublishStatus_ as the **Task Name**. Click **OK**. This will link the _AddNonSpeedOverheat_ task to the _PublishStatus_ task, which was the goal outlined in [Lesson 2](#2-understanding-the-design-model): add the overheat status to the temperature then republish that data via the _PublishStatus_ task.

15. Move the new _Filter_ and _Transformation_ tasks to their proper task context boxes:
	
	1. Right-click the _DetectSituation_ task context and select the _Add Task to Context_ menu item. Select _RetrieveSpeed_ from the **Task Name** menu, then click **OK**.
	
	2. Right-click the _DetectSituation_ task context and select the _Add Task to Context_ menu item. Select _SpeedOverheat_ from the **Task Name** menu, then click **OK**.
	
    3. Right-click the _DetectSituation_ task context and select the _Add Task to Context_ menu item. Select _NonSpeedOverheat_ from the **Task Name** menu, then click **OK**.
    
	4. Right-click the _React_ task context and select the _Add Task to Context_ menu item. Select _AddSpeedOverheat_ from the **Task Name** menu, then click **OK**.
	
	5. Right-click the _React_ task context and select the _Add Task to Context_ menu item. Select _AddNonSpeedOverheat_ from the **Task Name** menu, then click **OK**.
	
    Save the changes to the Service. The Event Handler graph should now look like this:

    ![FinishTempEvent](../assets/img/intro/FinishTempEvent.png "Finish Temperature Event")
    
Click on the next **To Do List** item in the Design Model. This will cause the same _com.vantiq.engines.EngineMonitorSensors_ Service to display and automatically navigate to the Implement tab which contains the _com.vantiq.engines.EngineMonitorSensors.IngestSensor0_ Internal Event Handler that is associated with the error. Here's how to address the errors in this Event Handler for the engine monitoring system:

1. Click on the _Ingest_ task and rename it _IngestSpeed_. Click the **Click to Edit** link to edit the configuration for this task. Select _sources_ for the **inboundResource** and _com.vantiq.engines.SpeedSensor_ for the **inboundResourceId**. Click **OK**. Click **OK** to save the _IngestSpeed_ task configuration.

2. Right-click the _IngestSpeed_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _PublishEvent_ as the **Task Name**. Click **OK**. This will link the _IngestSpeed_ task to the _PublishEvent_ task, which means the _Transform_ task may now be deleted.

3. Since the speed sensor data may be used as it is transmitted by the MQTT server, no data transformation needs to be done. Click the _Transform_ task and delete it using the Delete key or the Delete item in the pane's toolbar.

4. Now that the _Transform_ task has been deleted, one of the task contexts, _Transform_, is empty. Right-click that task context and select the _Remove Task Context_ menu item.

5. Click the _PublishEvent_ task and rename it to _PublishSpeed_. Click the **Click to Edit** link to edit the configuration for this task. The **service** property is correctly set (_com.vantiq.engines.EngineMonitorSensors_). However, the **eventTypeName** property needs to reflect the renamed Outbound Event: replace _Sensor0_ with _SpeedEvent_. Click **OK**.

    Save the Service changes and wait for several seconds. The Event Handler graph should now look like this:

    ![EditIngestSpeedEvent](../assets/img/intro/EditIngestSpeedEvent.png "Edit Ingest Speed Event")

    Note the rectangular badges with numbers that appear over the _IngestSpeed_ and _PublishSpeed_ tasks. These badges increment as each task event is received. This means that the Source is configured correctly and that the _EngineMonitorSensors_ service is successfully receiving those Source Events.
    
There should only be two remaining **To Do List** items in the Design Model. Click on one of them to automatically navigate to the Implement tab which contains the _com.vantiq.engines.EngineMonitorSensors.IngestSensor1_ Internal Event Handler that is associated with the error. Follow similar steps as above to receive temperature-related events:

1. Click on the _Ingest_ task and rename it _IngestTemperature_. Click the **Click to Edit** link to edit the configuration for this task. Select _sources_ for the **inboundResource** and _com.vantiq.engines.TemperatureSensor_ for the **inboundResourceId**. Click **OK**. Click **OK** to save the _IngestTemperature_ task configuration.

2. Right-click the _IngestTemperature_ task, select _Link Existing Task_ to display a dialog. In the dialog, select _PublishEvent_ as the **Task Name**. Click **OK**. This will link the _IngestTemperature_ task to the _PublishEvent_ task, which means the _Transform_ task may now be deleted.

3. Since the temperature sensor data may be used as it is transmitted by the MQTT server, no data transformation needs to be done. Click the _Transform_ task and delete it using the Delete key or the Delete item in the pane's toolbar.

4. Now that the _Transform_ task has been deleted, one of the task contexts, _Transform_, is empty. Right-click that task context and select the _Remove Task Context_ menu item.

5. Click the _PublishEvent_ task and rename it to _PublishTemperature_. Click the **Click to Edit** link to edit the configuration for this task. The **service** property is correctly set (_com.vantiq.engines.EngineMonitorSensors_). However, the **eventTypeName** property needs to reflect the renamed Outbound Event: replace _Sensor1_ with _TemperatureEvent_. Click **OK**.

Save the task changes by using the **Save Changes** icon in the pane's title bar.

Notice that the Design Model's **To Do List** is gone. This means Service-related all errors and missing task configurations have been addressed and the Service Event Handlers should be receiving and processing events. The next lesson will ensure their correct operation.

## 7: Create Event Schema Types
This lesson creates two schema Types based on the Service Event Handlers associated with the _EngineMonitor_ Service. Creating the schema types serves two purposes:

1. ensures the correct operation of the Event Handlers
2. makes it easier to build the engine dashboard using the _EngineMonitor_ Client, which happens in the next lesson.

Here's how to create the two schema Types:

1. Right-click the _EngineMonitor_ Service (Service nodes have a green title bar) in the Design Model, then select _Edit in Service Builder_ menu item. The pane for that Service is displayed. In the **Implement** tab, expand the "Public" section, then click the _SensorReading1_ Event Handler (which listens for the "TemperatureEvent" Event Type. The Event Handler graph should look like this (the layout has been adjusted a bit for readability):

    ![TemperatureEventHandler](../assets/img/intro/TemperatureEventHandler.png "Temperature Event Handler")

    Let the graph run for a minute so that the task badges are displayed as the simulated sensor data is received and processed. All ten tasks should eventually show incrementing badges. The sum of the _OverheatCheck_ and _NoAlert_ task badge counts should equal the _SensorReading_ task badge count since the filters check for temperature events above and below 210 degrees. The _PublishStatus_ task badge count should also equal the _SensorReading_ task badge count, which means every temperature reading is accounted for when creating engine status updates.
    
2. Click the _PublishStatus_ task then expand the **View Task Events** section of the task's configuration:

    ![TemperatureTaskEvents](../assets/img/intro/TemperatureTaskEvents.png "Temperature Task Events")
    
    An entry in the list should appear about one per second since temperature events from the MQTT source appear once per second. Click on one of the events to display the actual data being published on to the Outbound Event Type:
    
    ![TemperatureTaskEvent](../assets/img/intro/TemperatureTaskEvent.png "Temperature Task Event")
    
    Click the **Create Data Type** button, name the Type _StatusEvent_ with the _com.vantiq.engines_ package, then click **Save**. This creates the _StatusEvent_ Type that contains three properties: _alertMsg_, _systemId_, and _temperature_.

3. Switch to the _SpeedEvent_ Inbound Event as described in Step 1 above. Follow the similar instructions in Step 1 and 2 to create the _SpeedEvent_ Type. The _SpeedEvent_ Type contains two properties: _speed_ and _systemId_.

To associate the two new schema types with the Outbound Event handlers, switch to the Service's **Interface** tab, expand the **Outbound** section, then click the _EngineSpeed_ Event Handler. Use the **Event Schema** pull-down menu to select _com.vantiq.engines.SpeedEvent_, then save the Service using the **Save Changes** icon in the pane's title bar:

&nbsp;&nbsp;&nbsp;&nbsp;![EngineMonitorSchema](../assets/img/intro/EngineMonitorSchema.png "Engine Monitor Schema")

Click the _EngineStatus_ Event Handler. Use the **Event Schema** pull-down menu to select _com.vantiq.engines.StatusEvent_. Save the Service.

## 8: Visualizing a Running System
This section uses the IDE's Client Builder feature to create a visual interface for the engine simulation.

Right-click the _EngineMonitor_ Client (Client nodes have a purple title bar) in the Design Model, then select _Edit in Client Builder_ menu item. The pane for that Client is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;![EngineMonitorClient](../assets/img/intro/EngineMonitorClient.png "Engine Monitor Client")

From the **Data Display** menu, drag and drop one Line chart widget, one Column chart widget, two Gauge widgets,
one Pie chart widget and one Text widget to the canvas area below the widget palette to create a Client Builder layout similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;![128_IntroTut_FirstClient](../assets/img/intro/128_IntroTut_FirstClient.png "Client Builder")

We'll get to configuring each widget later so don't worry about the exact appearance of the widgets yet.

There are five display widgets and one text widget in the diagram above. What follows are the properties for each of those widgets.
Any property not mentioned is the default value for that widget. To display the property sheet for any widget, click on the widget. 
For example, here is the property sheet for a gauge, configured for tracking your engine speeds:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![129_IntroTut_GaugeProps](../assets/img/intro/129_IntroTut_GaugeProps.png "Speed Gauge Properties")

For the Engine Simulation text widget (top, center):
```text
 Specific -> Text: Engine Simulation
 Style -> Font Color: Dark Gray
```

For the Temperature line chart widget (top, left):
```text
 Specific -> Title: Temperature
 Data -> Data Stream: EngineStatus
 Data -> X-Axis Property: Timestamp
 Data -> Y-Axis Properties: temperature
```

For the Speed bar chart widget (bottom, left):
```text
 Specific -> Title: Speed
 Data -> Data Stream: EngineSpeed
 Data -> X-Axis Property: Timestamp
 Data -> Y-Axis Properties: speed
```

For the Speed gauge widget (top, left):
```text
 Specific -> Title: Speed
 Specific -> Minimum:0
 Specific -> Low Range Zones: 0:45
 Specific -> Medium Range Zones: 45:55
 Specific -> High Range Zones: 55:65
 Specific -> Maximum: 65
 Data -> Data Stream: EngineSpeed
 Data -> Data Stream Property: speed
```

For the Temperature gauge widget (top, right):
```text
 Specific -> Title: Temperature
 Specific -> Minimum: 180
 Specific -> Low Range Zones: 180:200
 Specific -> Medium Range Zones: 200:210
 Specific -> High Range Zones: 210:220
 Specific -> Maximum: 220
 Data -> Data Stream: EngineStatus
 Data -> Data Stream Property: temperature
```

For the Alert Status pie chart widget (bottom, right):
```text
 Specific -> Title: Alert Status
 Data -> Data Stream: EngineStatus
 Data -> Data Stream Property: alertMsg
```

When selecting the Data Stream Property value, the menu choices may be restricted to those properties appropriate to the 
type of the widget. For example, when configuring a bar or line chart, only numeric properties are available for selection. 
Other display elements, such as pie charts or lists, accept either numeric or string properties.

When you have finished adding and configuring your client widgets, save the client and return to the IDE. Save the project
in the IDE.

Use the **Run** icon button of the _Client: EngineMonitor_ pane (small triangle in a square at the top, right of the pane). This will start the Client running and the various widgets to display data from the Data Streams configured by the Design Modeler.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningClient](../assets/img/intro/RunningClient.png "Running Client")

    
## 9: Testing The App

Congratulations! You just built your first Vantiq application. However, there is an important piece missing.  How can you ensure your application works and will always work as you expect?

Learn how to test the application you just built by clicking here: [Testing the Intro Tutorial](testIntroTutorial.md)

## Conclusion

Users who have successfully completed this tutorial can comfortably: 

* Navigate through the Vantiq Integrated Development Environment (IDE) development phase
* Create and develop a Design Model
* Develop Design Model Services with visual Event Handlers 
* Configure simulated incoming events using Sources
* Configure a visual interface with a Client
