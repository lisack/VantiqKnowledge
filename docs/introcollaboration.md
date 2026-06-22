# Collaboration Tutorial
![Heart Rate Monitoring App](../assets/img/introcollab/HeartRateApp.png "Heart Rate Monitoring App")

## Objectives

In this tutorial, developers will learn:

* How to initiate collaborations
* How to add and configure collaboration roles
* How to add and configure collaboration activity patterns
* How to close and verify closed collaborations

## Tutorial Overview:

This Tutorial imagines a scenario where an at-risk patient wears a heart rate monitor. If an unusual heart rate is detected
(either dangerously low or dangerously high), the patient is sent a notification to assess their status. If the patient
responds that they are in distress, or fails to respond within a predetermined amount of time, a first responder is
notified immediately.

All lessons assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new
developer completes the lessons in the [Introductory Tutorial](tutorial.md) before starting the lessons in this tutorial. 
In addition, please see the [Collaboration Overview](../servicestatemgmt.md#collaborations) guide for introductory information about the Vantiq collaboration system.

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item.  Just select _Tutorials_ for Import Type, then select _Introduction to Collaboration_ from the second drop-down, then click _Import_.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Creating a Patient Monitoring Project

The first task in building the heart rate monitor system is to create a project in the Vantiq IDE. A Project is a container
for your development resources.

Use the **Projects** button and select **New Project** to display the New Project Wizard. Either create a new Namespace
(recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project *PatientMonitor*.

![New Project](../assets/img/introcollab/NewProject.png "New Project")

The rest of the lessons take place inside this Project.

## 2: Creating a Patient Monitoring Service

Using the **Add** button, select **Service** and click **+ New Service**. Set the service name to *HeartRate* and the package
name to *patient.monitoring*.

![Create Service](../assets/img/introcollab/CreateService.png "Create Service")

Click **OK** to create the Service.

## 3: Defining an Inbound Event Type and Event Handler

In the *patient.monitoring.HeartRate* Service, navigate to the *Implement* tab. Click on the **+** button next to Public
and select **Add Visual Event Handler**. 

![Add Visual Event Handler](../assets/img/introcollab/AddVisualEventHandler.png "Add Visual Event Handler")

Set the Event Type Name to *MonitorReading*. (You can leave the Event Handler Name field blank and it will default to the same value). Click **OK**, which will
create an Inbound Event Type in the Service Interface and its Visual Event Handler in one step.

![Inbound Event Type Name](../assets/img/introcollab/InboundEventTypeName.png "Inbound Event Type Name")

Click **Save** in the title bar for the Service. 

Next, enhance the Event Type definition by defining an Event Schema. Click on the *Interface* tab and expand the Inbound
section. Click on **MonitorReading** to open the Event Type Interface definition.

Click on the *Event Schema* droplist and select *New Type*. Define the following properties as the event schema:

* _patientId_ (String)
* _name_ (String)
* _heartRate_ (Integer)
* _location_ (GeoJSON)


Click **Save** in the title bar for the Service. The Event Type should now look like this:

![Inbound Event Type Schema](../assets/img/introcollab/EventTypeSchema.png "Event Type Schema")



## 4: Filtering for Unusual Readings

Navigate back to the Event Handler by clicking on the *Implement* tab, expanding the Public section, and clicking on
**MonitorReading**. Drag and drop a Filter task from the Filters section of the palette over the EventStream.

Click on the Filter task and in the configuration slideout rename the task *isUnusualHeartRate*. 

![isUnusualHeartRate Filter Task](../assets/img/introcollab/isUnusualHeartRateTask.png "isUnusualHeartRate Filter Task")

Click **Click to Edit** next to the Configuration label. Click on **`<null>`** next to the condition property. Set the condition to:

`event.heartRate < 40 OR event.heartRate > 200`

![isUnusualHeartRate Filter Condition](../assets/img/introcollab/isUnusualHeartRateCond.png "isUnusualHeartRate Filter Condition")

Click **OK** twice to close the pop-ups.

Click **Save** in the title bar for the Service.

## 5: Simulating Monitor Readings

Before going any further, create a Procedure that simulates heart rate monitor readings to interactively test and debug
the App.

Click on the **+** button next to the Public item in the Procedure Section and click **Add Public Procedure**.

![Add Procedure](../assets/img/introcollab/AddProcedure.png "Add Procedure")

Set the procedure text to:

```js
package patient.monitoring
PROCEDURE HeartRate.generateHeartRate(heartRate Integer)

var event = {
    name: Context.preferredUsername(),
	patientId: Context.username(),
	heartRate: heartRate,
	location: {
        "type": "Point",
     	"coordinates": [
            -122.0651683957521,
            37.90793522730274
         ]
    }
}

PUBLISH event TO SERVICE EVENT "patient.monitoring.HeartRate/MonitorReading"
```

Click **Save** to save the Service with the new procedure. You will see a message slide in from the right that the Services's Interface has been repaired.

![GenerateHeartRateText](../assets/img/introcollab/GenerateHeartRateText.png "GenerateHeartRateText")

Right-click on the *generateHeartRate* Procedure entry and select **Open In New Pane**. 

![Open In New Pane](../assets/img/introcollab/OpenInNewPane.png "Open In New Pane")

Navigate back to the Event Handler by clicking on the *Implement* tab, expanding the Public section, and clicking on
**MonitorReading**.

Click the **Play** button in the Procedure pane to execute the procedure and pass 100 as the current heart rate. After clicking **Execute**, Click
**OK** to close the resulting pop-up. Notice that there is an event badge on the EventStream but *not* on the Filter task.
That is because the heart rate is in the "normal" range and therefore was filtered out. 

![Normal Heart Rate Event](../assets/img/introcollab/NormalHeartRateEvent.png "Normal Heart Rate Event")

Click the **Play** button in the Procedure pane again, but this time pass in 30 as the heart rate. Notice that this time
there are event badges on both the EventStream and Filter tasks since the event passed through the filter.

![Unusual Heart Rate Event](../assets/img/introcollab/UnusualHeartRateEvent.png "Unusual Heart Rate Event")

## 6: Defining Entity Role

Services may define certain roles to identify the responsibility of each participant in the collaborations it manages. _Collaborator roles_ represent actual users that are tasked with executing each activity while _entity roles_ are bound to objects that represent the entities impacted by each activity.

In this collaboration the patient whose heart rate is unusual represents the collaboration entity. To define a list of entity
roles, switch to the *Implement* tab and click on the State section in the palette. Open the "Collaboration State Properties" section - this 
is where you can edit various Service-wide properties that relate to Collaborations.

![State Section](../assets/img/introcollab/StateSection.png "State Section")


Click **Click to Edit** next to the Entity Roles label. Click **+** to add a new entity role definition. Set the variable reference to *patient*
and the type to *patient.monitoring.HeartRate.MonitoringReading*. Click **OK**.

![Configure Entity Role](../assets/img/introcollab/ConfigureEntityRole.png "Configure Entity Role")

Click **Save** to save the Service with the new entity role.

## 7: Entity Assignment

Now select the MonitorReading Event Handler in the Public section.

Once an event passes through the filter, we know the patient's heart rate is dangerously high or low, which means it 
is time to start a collaboration. 

First, assign the patient to the Entity Role. Drag and drop an *Assign* task from the 
*Collaboration* section of the palette onto the Filter task. Click on the new task and re-name it *AssignPatient*
in the right-hand slideout. 

![AssignPatient Task](../assets/img/introcollab/AssignPatientTask.png "AssignPatient task")

Click **Click to Edit** to configure the Assignment.

Set the roleType to *entity* and the Role Name to *patient* and click **OK**.

![AssignPatient Task](../assets/img/introcollab/ConfigureAssign.png "AssignPatient task")

Click **Save** to save the Service and Event Handler.

In Apps that contain [Collaboration Management Tasks](../apps.md#collaboration-management), a new collaboration is started when the first Collaboration Task is reached.
In the case of this App, events that are filtered out by *isUnusualHeartrate* will *not* start a new collaboration. However,
each event that passes through the filter to reach the *AssignPatient* task will create a new collaboration instance stored in the
Service state. Each of the Collaboration tasks downstream of this task will operate on that collaboration.

Notice that saving the Event Handler with a Collaboration task auto-generated several Procedures in the Service. These
Procedures are used to manage and update the Collaboration at each task. Some of these are "Public" and some are "Private". You
must toggle the "Generated" checkbox in order to see generated Procedures.

![Auto-Generated service procedures](../assets/img/introcollab/AutoGeneratedServiceProcs.png "Auto-Generated service procedures")

## 8: Send Patient Notification

Next, send a notification to the patient asking whether they require assistance.
Drag and drop a *Notify* task from the *Mobile* section of the palette onto the AssignPatient task. Click on the new
task and re-name it *NotifyPatient*. Click **Click to Edit** to configure the NotifyPatient task.

Set the title to: *&#34;Heart Rate Alert&#34;*  
Set the body to: *&#34;An unusual heart rate (&#34; + event.heartRate + &#34;) has been detected&#34;*  
Click **`<null>`** to configure the user to send the notification. Select *Literal Array* as the user type from the droplist. Click **+** to add an item to the list and set the
user to *event.patientId*. Click **OK** to close the pop-up.  
Select *Create Placeholder Client* next to the *clientName* configuration. Set the new Client name to *PatientResponse*
and click **OK**. This creates a placeholder client that you will configure in the next step of this tutorial.

Lastly, set the maxResponseTime to *90 seconds*. This allows you to alert a first responder if the patient does
not reply to the notification within the specified amount of time.

![Configure Notify Patient](../assets/img/introcollab/ConfigureNotifyPatient.png "Configure Notify Patient")

Click **OK** to close the pop-up.
Click **Save** to save the Service and event handler.

![NotifyPatient Task](../assets/img/introcollab/NotifyPatientTask.png "NotifyPatient task")

## 9: Creating the Patient Client

Using the **Add** button, select **Client** and click on **PatientResponse** to open the Client you created as a placeholder
in the previous section. 

For this tutorial, the patient is shown two buttons
in order to submit a response, one to indicate the unusual heart rate does not require help to resolve (perhaps the patient was exercising)
and the other to indicate that help is needed.

Drag and drop two Inline buttons from the widget palette to the Client Builder canvas. Tap on the top Inline button to display its properties. Change the following property values:

```text
 Specific -> Button Label: I'm OK
 Specific -> Value: 0
 Style -> Button Label Font Size: 16
 Style -> Button Label Color -> White
 Style -> Button Background Color -> Default
```

Tap on the bottom Inline button to display its properties. Change the following property values:

```text
 Specifc -> Button Label: Please Send Help
 Specifc ->  Value: 1
 Style -> Button Label Font Size: 22
 Style -> Button Label Color: White
 Style -> Button Background Color: Custom #ff0000
```

![Patient Response Client](../assets/img/introcollab/PatientResponseClient.png "Patient Response Client")

Then use the **Save** button to save the _PatientResponse_ Client. 

## 10: Handling Patient Response

There are three possible cases that need to be handled by this collaboration:

1. The patient replies: "I'm OK". In this case can terminate the collaboration 
2. The patient replies: "Please Send Help". In this case must dispatch a first response team
3. The patient does not reply within the specified amount of time. In this case must dispatch a first response team

### Patient is OK

To handle the first case, drag and drop a Filter task from the Filters section of the palette onto the NotifyPatient task. The Notify task
defines multiple *downstream events*: response, firstResponse, responseTimeout, and event. The first event to be handled
is when the patient responds with the "I'm OK" message. Select *response* from the droplist and click **OK**. Notice
that a *response* event triangle has been added between the Notify and Filter task. This represents the asynchronous
response event that triggers any downstream tasks. Rename the Filter task *OK*.

![Patient OK Filter](../assets/img/introcollab/PatientOKFilter.png "Patient OK Filter")

Click **Click to Edit** to edit the Filter configuration. Click **`<null>`** to configure
the filter condition and set the condition to `event.submitValue == 0`. Click **OK** twice to close the pop-ups. This
filters events such that only the event generated when the patient clicks "I'm OK" passes through.
If this is the case, the collaboration can be terminated.

![Patient OK Filter Condition](../assets/img/introcollab/PatientOKFilterCond.png "Patient OK Filter Condition")

Drag and drop a CloseCollaboration task from the Collaboration section of the palette to the "OK" Filter. Rename the task *PatientOK*.
Click **Click to Edit** to edit the CloseCollaboration configuration and set the status to *completed*. Click **OK** to close the pop-up.

![Patient OK Close Collaboration](../assets/img/introcollab/PatientOKCloseCollab.png "Patient OK Close Collaboration")

### Send Help Please

To handle the second case, drag and drop a Filter task from the Filters section of the palette onto the *response* triangle.
Rename the Filter task *HelpNeeded*. 

![Help Needed Filter Task](../assets/img/introcollab/HelpNeededFilterTask.png "Help Needed Filter Task")

Click **Click to Edit** to edit the Filter configuration. Click **`<null>`** to configure
the filter condition and set the condition to `event.submitValue == 1`. Click **OK** twice to close the pop-ups. This
filters events such that only the event generated when the patient clicks "Please Send Help" passes through.

![Help Needed Filter Task Conditino](../assets/img/introcollab/HelpNeededFilterTaskCond.png "Help Needed Filter Task Condition")

The third case, the patient does not respond in time, will be handled in section 12...

## 11: Notify the First Responder

Next, drag and drop a *GetCollaboration* task from the Collaboration section of the palette onto the *HelpNeeded* task.
Rename the task *GetPatient*.

![GetPatient Task](../assets/img/introcollab/GetPatient.png "GetPatient task")

Click **Click to Edit** to edit the task configuration and set the *taskName* to *patient*. This fetches the current definition of the 
patient entity from the collaboration and returns the value as the outbound event.

![GetPatient Task](../assets/img/introcollab/ConfigureGetPatient.png "GetPatient task")


Drag and drop a Notify task from the Mobile section of the palette onto the *GetPatient* task.  Click on the new
task and re-name it *NotifyFirstResponder*.

![NotifyFirstResponder Task](../assets/img/introcollab/NotifyFirstResponderTask.png "NotifyFirstResponder task")

Click **Click to Edit** to configure the NotifyFirstResponder task.  
Set the title to: `event.name + " Heart Rate Alert (" + event.heartRate + ")"`   
Set the body to: `"Are you available to assist " + event.name + "?"`    
Click **`<null>`** to configure the user to send the notification. Select *Literal Array* as the user type from the droplist.
Click **+** to add an item to the list and set the
user to *event.patientId*. Click **OK** to close the pop-up. 

For this tutorial, configure the patient and
first responder to be the same person. In the [Advanced Collaboration Tutorial](advancedcollaborations.md) you will find the nearby first responders
and loop through each available responder.    
Select *Create Placeholder Client* next to the *clientName* configuration. Set the new Client name to *FirstResponderResponse*
and click **OK**. This creates a placeholder client that you will configure in the next step of this tutorial.

![NotifyFirstResponder Task Config](../assets/img/introcollab/NotifyFirstResponderConf.png "NotifyFirstResponder task config")

Click **OK** to close the pop-up.
Click **Save** to save the Service and event handler.

Once the first responder has responded to the message, the collaboration is complete.
Drag and drop a CloseCollaboration task from the Collaboration section of the palette onto the NotifyFirstResponder task. Select *response* as the downstream
event and click **OK**. Rename the task *CollabComplete*.
Click **Click to Edit** to edit the CloseCollaboration configuration and set the status to *completed*. Click **OK** to close the pop-up.

Click **Save** to save the Service and event handler.

![Complete Collaboration](../assets/img/introcollab/CollabComplete.png "Complete Collaboration")

## 12: Handle the Response Timeout Case

In the scenarios listed in section 10, there are two scenarios which result in sending a Notification to a first responder.
You have already handled the second scenario: the patient responds "Please Send Help". Next,
you must handle the third scenario: the patient does not send a response within the required amount of time.
In this case, you need to get the current collaboration, send a notification to a first responder, and then
complete the collaboration when the first responder responds.

Instead of repeating the tasks in the section above, link the *NotifyPatient*'s *responseTimeout* event to the existing tasks.
Right-click on *NotifyPatient* and select **Link Existing Task**. 

![Link Existing Task](../assets/img/introcollab/LinkExistingTask.png "Link Existing Task")

Select *GetPatient* as the Task Name and *responseTimeout* as the Downstream Event and click **OK**.

![Link Existing Task Configuration](../assets/img/introcollab/LinkExistingTaskConfig.png "Link Existing Task configuration")

Click **Save** to save the Service and the Event Handler.

![Heart Rate Monitoring App](../assets/img/introcollab/HeartRateApp.png "Heart Rate Monitoring App")

## 13: Creating the First Responder Client

Using the **Add** button, select **Client** and click on **FirstResponderResponse** to open the Client you created as a placeholder
in section 11.
Drag and drop one Inline button from the widget palette to the Client Builder canvas. Tap on the Inline button to display its properties. Change the following property values:

````text
  Specific -> Button Label: On my way to ${patient.name}!
  Specific -> Value: 0
  Style -> Button Label Font Size: 22
  Style -> Button Label Color -> White
  Style -> Button Background Color -> Default
````

Click **Save** to Save the Client.

![FirstResponder Client](../assets/img/introcollab/FirstResponderClient.png "FirstResponder Client")

## 14: Testing the App

### Testing "I'm OK" Scenario

Log into this namespace in the Vantiq Mobile App. You may need to download the App if you have not yet done so.

<div style="height:120px;">
	<div style="float:left;">
		<a href="https://apps.apple.com/us/app/vantiq/id1137249724" target="_blank"><img src="../../assets/img/introcollab/iOS.png" style="border:0;padding-left:10px;margin:0;"/></a>
	</div>
	<div style="float:left;">
		<a href="http://play.google.com/store/apps/details?id=io.vantiq.rcs" target="_blank"><img src="../../assets/img/introcollab/Android.png" style="border:0;padding-left:10px;margin:0;"/></a>
	</div>
	<div style="float:left;">
		<img src="../../assets/img/introcollab/iOSQR.png" style="border:0;padding-left:10px;margin:-10px 0"/>
		<br><p style="text-align:center;font-weight:bold;">iOS App</p>
	</div>
	<div style="float:left;">
		<img src="../../assets/img/introcollab/AndroidQR.png" style="border:0;margin:-10px 0"/>
		<br><p style="text-align:center;font-weight:bold;">Android App</p>
	</div>
</div>
</br>

Right-click on the *generateHeartRate* Procedure entry and select **Open In New Pane**.
Navigate back to the Event Handler by clicking on the *Implement* tab, expanding the Inbound section, and click on
**MonitorReading**. Execute the Procedure passing in 210 as the heart rate.

You should receive a Notification in the Vantiq Mobile App with the following message:

<img src="../../assets/img/introcollab/PatientAlertNotification.png" width="360" height="640"></img>

Open the Notification and Click **I'm OK**. Notice that once you click the button, the badges in the App pick up again
starting with the Notification response task.

![Im OK App Badging](../assets/img/introcollab/ImOKAppBadging.png "Im OK App Badging")

### Testing "Please Send Help" Scenario

Execute the Procedure again passing in 220 as the heart rate.

You should receive a Patient Notification in the Vantiq Mobile App.
This time, open the Notification and Click **Please Send Help**. Notice that once you click the button, the badges in the App pick up again
starting with the Notification response task.

![Send Help App Badging](../assets/img/introcollab/SendHelpBadging.png "Send Help App Badging")

You'll then receive a second notification as the first responder.

<img src="../../assets/img/introcollab/FirstResponderNotification.png" width="360" height="640"></img>

Open the notification and click the "On my way..." button.

<img src="../../assets/img/introcollab/FirstResponderNotificationClient.png" width="360" height="640"></img>


![First Responder Notification](../assets/img/introcollab/SendHelpResponderBadging.png "First Responder Notification")

### Testing Response Timeout Scenario

Execute the Procedure again passing in 30 as the heart rate.

You should receive a Patient Notification in the Vantiq Mobile App. This time, do not open the notification or click on the buttons. Wait for 90 seconds and expect to receive 
a second notification as the first responder.

While you wait for the second notification, click on the **Properties** button in the top-right of the Event Handler toolbar and click **Run Query** next to Active Collaborations.
This will allow you to see your currently active collaborations. A new collaboration instance is created each time an event 
passes through the AssignPatient task. Click on the *Service State* radio button in the toolbar. This will allow you to 
see the collaborations currently stored in the Service State. You'll see one currently active collaboration. 

![Active Collaboration List](../assets/img/introcollab/ActiveCollabInState.png "Active Collaborations")

Click the **back** button in the titlebar and update the query to search for collaborations with any status. Click **Run Query**.

![Collaborations Any Status](../assets/img/introcollab/UpdateCollabQuery.png "Update Collaboration")

Now you'll notice the two collaborations you created in the previous scenarios are listed and are stored in the database. 

![Collaborations in DB](../assets/img/introcollab/CollaborationsInDB.png "Collaborations in DB")

Click on one of the completed collaborations. You'll notice that the collaboration contains a detailed log of the events that occurred. The patient is stored as the entity and each of the responses
to the notifications has been recorded as well.

![Completed Collaboration](../assets/img/introcollab/ClosedCollaboration.png "Close Collaboration")

Click **back** to return the list view.
Click on the *Service State* radio button in the toolbar. Notice that all three collaborations are still in the service state.
![Service State Collaborations](../assets/img/introcollab/CollaborationsInState.png "Collaborations in Memory")

Click on the active collaboration. You'll notice that the collaboration contains a detailed log of the events that occurred. Notice that
since the collaboration is still active, you can update the collaboration status directly from this pane if needed.

![Active Collaboration](../assets/img/introcollab/ActiveCollaboration.png "Active Collaboration")

Once you're finished exploring the collaborations list pane, you'll likely have received the First Responder notification in the Vantiq Mobile App.
Open the notification and click the button to confirm.

![Timeout Response Badging](../assets/img/introcollab/TimeoutResponseBadging.png "Timeout Response Badging")

Now if you click **refresh** in the collaborations list pane all three collaborations will be marked as completed.

## Conclusion

This simple App is a good example of multiple collaborators working together to solve a real world problem.

In the Tutorial you learned how to:

* Initiate a Collaboration
* Send Notifications to mobile Clients
* Complete the collaboration
