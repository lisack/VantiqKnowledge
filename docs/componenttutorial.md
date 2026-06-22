# App Component Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;![FullComponentDefinition](../assets/img/components/Overview.png "FullComponentDefinition")

## Overview

In this tutorial, you will learn how to create App Components as reusable technical solutions.
You will gain experience using and composing Components to quickly create and improve Visual Event Handlers,
reducing duplicative tasks.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## Part 1: Creating a Component

### 1: Import the Introductory Tutorial

Use the **Project** menu to select **Import**. Select *Tutorials* as the Import Type. Select the *Introductory* Tutorial
and click **Import**.

&nbsp;&nbsp;&nbsp;&nbsp;![Import Intro Tutorial](../assets/img/components/ImportIntroTutorial.png "Import Intro Tutorial")

Click **Refresh** once the import is completed.

Click the _com.vantiq.engines.EngineMonitor_ Service from the Project Contents tree or use the **Add** menu to select **Service** and open the *com.vantiq.engines.EngineMonitor* Service. For more details or information
on how the *com.vantiq.engines.EngineMonitor* Service works, refer to the [Introductory Tutorial](tutorial.md).

Navigate to the *Implement* tab in the Service and click on the *Public* section header to view the inbound
Event Handlers. Select the *SensorReading1* Event Handler (which handles the *TemperatureEvent* Event Type). Recall that this event handler receives
temperature events, retrieves the current speed value if necessary, then generates an alert message for the event.
Notice that there are three similar patterns in this Event Type handler: a Filter task (i.e., _NoAlert_, _NonSpeedOverheat_, _SpeedOverheat_) each followed by a Transformation task (i.e., _ClearAlert_, _AddNonSpeedOverheat_, _AddSpeedOverheat_).

&nbsp;&nbsp;&nbsp;&nbsp;![TemperatureEventHandler](../assets/img/components/TemperatureEventHandler.png "Temperature Event Handler")

Duplicative tasks are tedious to configure and cumbersome to maintain. To solve this, create a reusable component for filtering and transforming using differing temperature and speed values. The _TemperatureEvent_ Event Handler will use this Component to produce the proper engine alert message based on the sensor data it receives.

### 2: Create a Component From an Existing Handler

App Components may either be created from scratch or copied from an existing event handler. Use the existing definition
of the _TemperatureEvent_ Event Handler to copy the duplicated tasks and create a new App Component.

Hold the shift key and drag your mouse to select the _NoAlert_ and _ClearAlert_ tasks. Notice that the
tasks show a green border when they are selected.

&nbsp;&nbsp;&nbsp;&nbsp;![HighlightComponentTasks](../assets/img/components/HighlightComponentTasks.png "Highlight component tasks")

Click **Save Component** in the upper right-hand corner of the pane.
Enter *FilterAndDiagnose* as the App Component name and click **OK**.

&nbsp;&nbsp;&nbsp;&nbsp;![CreateComponent](../assets/img/components/CreateComponent.png "Create component")

A new App Component has been created with an exact copy of the tasks you selected from the Event Handler. 

&nbsp;&nbsp;&nbsp;&nbsp;![NewComponent](../assets/img/components/NewComponent.png "New Component")

### 3: Rename Component Tasks

Notice that an oval bubble called *Downstream* has been added beneath the Filter task.
As the creator of the Component, you may decide how users of the Component will
attach tasks beneath the Component.
When a Component is used, it appears as a single black box for all the functionality and tasks contained within. For a user
to connect another task as a child of the Component, the Component creator must expose *downstream connection points*
to one or more tasks within the Component. 

Click on the _Downstream_ bubble and rename it *Diagnosis*. 
When this Component is used, if a task is added
as a child of the Component using this connection point, it is effectively a child of the _Diagnosis_ task. Rename the _NoAlert_ task to _Diagnose_ and the _ClearAlert_ task to _AddDiagnosis_.

&nbsp;&nbsp;&nbsp;&nbsp;![RenameDownstream](../assets/img/components/RenameDownstream.png "Rename Downstream")

**Save** the Component.

### 4: Expose Component Properties
Components are sections of Visual Event Handlers that are configurable and reusable to solve a wide range of problems. Components
serve as a black box and are represented as a single Task.
The user of a Component may treat it like any other Task, configuring a small set of properties to achieve the desired
functionality.

The _FilterAndDiagnose_ Component contains two tasks, the _Diagnose_ Filter task and the _AddDiagnosis_ Transformation task. Event Handlers that use _FilterAndDiagnose_ will need to specify the filtering condition and the transformation properties for those tasks. The **Expose Property** feature of the component editor allows task parameters to be designated as "exposed".

Click the _Diagnose_ task then click the **Click to Edit** link. Click the **Expose Property +** button to the right of the _condition_ property.

&nbsp;&nbsp;&nbsp;&nbsp;![ExposeConditionParameter](../assets/img/components/ExposeConditionParameter.png "Expose Condition Parameter")

Leave the name of the configuration property as the default _condition_, then click **OK**. Click **OK** again to save the single configuration property for the _Diagnose_ task.

Click the _AddDiagnosis_ task then click the **Click to Edit** link. Click the **Expose Property +** button to the right of the _transformation_ property. Leave the name of the configuration property as the default _transformation_, then click **OK**. Click **OK** again to save the single configuration property for the _AddDiagnosis_ task.

Click **OK** and then **Save** the Component.

## Part 2: Use the FilterAndDiagnose Component

Now that you have created the _FilterAndDiagnose_ Component, it is time to plug it into the Event Handler.

### 1: Replace Repeated Tasks 

Open the Service by using the **Add** button, click **Services** and then select *com.vantiq.engines.EngineMonitor* from the list.

Click on the *Implement* tab and open the *SensorReading1* Event Handler (for the *TemperatureEvent* Event Type) in the *Public* section.

Expand the **Components** section of the Task palette in the Event Handler. Notice
that the _FilterAndDiagnose_ Component is in the palette. Your component is now available to be used in your Visual Event Handlers. 

Delete the *NoAlert* and *ClearAlert* tasks by clicking on each task and then clicking the **Delete** button in the pane's toolbar.

&nbsp;&nbsp;&nbsp;&nbsp;![DeletedTasks](../assets/img/components/DeletedTasks.png "delete duplicated tasks")

Drag in the _FilterAndDiagnose_ Component and drop it on the _SensorReading_ Task. 

Notice that the Component appears as a single task called _FilterAndDiagnose_. Also notice a
downstream _Diagnosis_ task appears as a triangular node beneath the Component representing a connection
point for the component.

&nbsp;&nbsp;&nbsp;&nbsp;![ComponentedAdded](../assets/img/components/ComponentedAdded.png "Component Added")

Rename the _FilterAndDiagnose_ task to _NoAlert_ then right-click the _Diagnosis_ downstream task connected to the _NoAlert_ task and select _Link Existing Task_. Select _PublishStatus_ from the **Task Name** menu, then click **OK**.

&nbsp;&nbsp;&nbsp;&nbsp;![ConnectPublishStatus](../assets/img/components/ConnectPublishStatus.png "Connect PublishStatus")

Delete the *NonSpeedOverheat* and *AddNonSpeedOverheat* tasks by clicking on the task and then clicking the **Delete** button in the pane's toolbar.

Drag in the _FilterAndDiagnose_ Component and drop it on the _RetrieveSpeed_ Task. 

Rename the _FilterAndDiagnose_ task to _NonSpeedOverheat_ then right-click the _Diagnosis_ downstream task connected to the _NonSpeedOverheat_ task and select _Link Existing Task_. Select _PublishStatus_ from the **Task Name** menu, then click **OK**.

Delete the *SpeedOverheat* and *AddSpeedOverheat* tasks by clicking on each task and then clicking the **Delete** button in the pane's toolbar.

Drag in the _FilterAndDiagnose_ Component and drop it on the _RetrieveSpeed_ Task. 

Rename the _FilterAndDiagnose_ task to _SpeedOverheat_ then right-click the _Diagnosis_ downstream task connected to the  _SpeedOverheat_ task and select _Link Existing Task_. Select _PublishStatus_ from the **Task Name** menu, then click **OK**.

Click **Save** to save the _com.vantiq.engines.EngineMonitor_ Service.

You have now replaced your duplicated tasks with your reusable component. Please note there will be errors displayed after saving the Service. These are expected and will be corrected in subsequent steps.

&nbsp;&nbsp;&nbsp;&nbsp;![ReplaceTempEventsHandler](../assets/img/components/ReplaceTempEventsHandler.png "Add Components to TemperatureEvents handler")

### 2: Configure the New Component Tasks
Now that three instances of the _FilterAndDiagnose_ component have replaced six tasks in the _TemperatureEvent_ Event Handler, it's time to configure each of those component properties.

1. Click the _NoAlert_ task then click the **Click to Edit** link. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then click the **Add Visual Condition** + button. Enter the following Visual Condition parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: temperature
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: <
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 210     
    
    Click **OK**. As for the original _NoAlert_ task, this Visual Filter determines if the engine is not overheating by checking if the temperature sensor reading is less than 210 degrees.
    
    Now click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;&#34;    
    
    Click **OK**. As for the original _NoAlert_ task, this Visual Transformation sets a new event property, _alertMsg_, to have a string value of _&#34;&#34;_ which effectively means there is no alert to be displayed in the engine dashboard. This is because the _NoAlert_ Filter task has determined that the engine is not overheating. Click **OK** to save the configuration.
    
2. Click the _NonSpeedOverheat_ task then click the **Click to Edit** link. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then add the following two Visual Condition parameters, in this order:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: !=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: null
	
    and
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: <
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 45
    
    Click **OK**. As for the original _NonSpeedOverheat_ task, this Visual Filter determines if the engine is overheating and the speed is not null and less than 45. The speed can be null if a speed reading has not yet appeared.
        
    Now click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;Your engine is overheating: check for a malfunctioning fan or a coolant leak.&#34;    
    
    Click **OK**. Click **OK** again to save the configuration.
    
3. Click the _SpeedOverheat_ task then click the **Click to Edit** link. Click on the link next to the **condition** property. Choose _Visual Filter_ as the **condition Type** then add the following two Visual Condition parameters, in this order:

    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: !=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: null
	
    and
    
    &nbsp;&nbsp;&nbsp;&nbsp;**Property Name**: speed
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Comparator**: >=
    
	&nbsp;&nbsp;&nbsp;&nbsp;**Filter Expression**: 45
    
    Click **OK**. As for the original _SpeedOverheat_ task, this Visual Filter determines if the engine is overheating and the speed is not null and greater than or equal to 45.
        
    Now click on the link next to the **transformation** property. Choose _Visual Transformation_ as the **transformation Type** then click the **Add a Transformation** + button. Enter the following Visual Transformation parameters:

    &nbsp;&nbsp;&nbsp;&nbsp;**Outbound Property**: alertMsg
        
    &nbsp;&nbsp;&nbsp;&nbsp;**Transformation Expression**: &#34;Your engine is overheating: please reduce your speed.&#34;    
    
    Click **OK**. Click **OK** again to save the configuration.

Click **Save** to save the _com.vantiq.engines.EngineMonitor_ Service.

### 3: Run Events through the Component

Now it is time to test that the Component works as expected.

If you've imported the [Introductory Tutorial](tutorial.md) or the App Components completed tutorial, you will need to enable the two Sources, _com.vantiq.engines.SpeedSensor_ and _com.vantiq.engines.TemperatureSensor_ in order to begin the flow of simulated sensor events.

Click the _Active Resource Control Center_ (lightning bolt) icon in the IDE Navigation Bar to display the _Active Resource Control Center_ pane:

&nbsp;&nbsp;&nbsp;&nbsp;![ActiveResourceControlCenter](../assets/img/components/ActiveResourceControlCenter.png "Active Resource Control Center")

Activate the _SpeedSensor_ and _TemperatureSensor_ Sources by clicking their Active Slider.


Click the _com.vantiq.engines.EngineMonitor_ Client from the Project Contents tree or use the **Add** menu to select **Clients** and open the *com.vantiq.engines.EngineMonitor* Client.

Notice that even though the implementation of the _com.vantiq.engines.EngineMonitor_ Service changed, the Client did not need to be updated because the Data Streams in the Client use the Outbound Service Event Types and the Interface remained unchanged.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningClient](../assets/img/intro/RunningClient.png "Running Client")

## Conclusion

Congratulations, you have just created your first App Component!

In this Tutorial you have:

- Created a Component from an existing Event Handler
- Added Configurable Properties to the Component
- Replaced duplicated code by using the same App Component in an Event Handler

In the [next tutorial](statefulservices.md), you will update this App Component to use Stateful Services to store and persist engine data while
maintaining scalability and performance.


