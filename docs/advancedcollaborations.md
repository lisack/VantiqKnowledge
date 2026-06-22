# Advanced Collaboration Tutorial

## Overview

In the [Introductory Collaboration Tutorial](introcollaboration.md) you created an App that detects whether a patient is in distress
and sends a notification to a first responder. However, the complexity of finding and notifying the correct first responder
was overlooked.

In this tutorial you will compute a list of available first responders sorted by their proximity to the patient. You'll send a message to a responder, 
waiting a specified amount of time before retracting the message and trying the next closest responder. Once a responder
confirms that they are on their way, you will track the first responder's location until they arrive at the patient.

## Import Intro Collaboration Tutorial

This Tutorial will start where the [Introductory Collaboration Tutorial](advancedcollaborations.md) left off. It is highly recommended that you
complete the Introductory Collaboration Tutorial before starting this one. To import the final result of the
Introductory Collaboration Tutorial use the **Projects** button and click **Import**. Select *Tutorials* as the 
Import Type and select *Introduction to Collaboration* from the droplist. Click **OK** to complete the import and then
click **Reload** once the import completes.

## Create First Responder Instances

Start by creating a FirstResponder persistent Type. Use the **Add** button to select **Type** and click **+ New Type**.
Set the name to *FirstResponder* and the Role to *standard*. Click **OK**. 

![Create new type](../assets/img/advcollaborations/CreateNewType.png "Create new type")

Click on the **Properties** tab in the *FirstResponder* Type pane and click **+ Add Property**. Set the following properties
on the type: 

* *name* (String)
* *username* (String) 
* *location* (GeoJSON)

Click **OK** to close the add property pop-up and then **Save** the Type.

![first responder type](../assets/img/advcollaborations/FirstResponderType.png "first responder type")

Next, create a few instances of the *FirstResponder* Type. The username property is be used
to send Notifications to first responders later in this tutorial. This means that the usernames must point to valid, existing, Vantiq
users. For the sake of this Tutorial, set the username on each instance to *your* username so that the messages will
be sent to your mobile phone.
However, we'll give each first responder a unique name as if they are actually separate people. To get your username, click on the
*user* icon in the Vantiq banner. Hover your mouse over the username until a green plus
icon appears. Clicking on the username copies it to your clickboard. 

![copy username](../assets/img/advcollaborations/CopyUsername.png "copy username")

Click **Add New Record** at the top of the Type pane. Set the name to *John Smith*. Paste your username as the username.
Click onto the link to specify the GeoJSON location. Set the location type to *Point*. Set the longitude to -122.4194 and
latitude 37.7749 Click **Add Record**. 

![add first responder](../assets/img/advcollaborations/AddFirstResponder.png "add first responder")

Add the following additional instances:

```json
"name": "Sarah Brown",
"username": "<your username>",
"location": longitude: -122.27304, latitude: 37.8715
```

```json
"name": "Robert Johnson",
"username": "<your username>",
"location": longitude: -122.2892 latitude: 37.8395
```

## Recommend First Responder

Drag a *Recommend* task from the Collaboration section of the palette over the link between *GetPatient* and *NotifyFirstResponder* and then drop it.
Rename the Recommend task *FindResponders*.

![find responders](../assets/img/advcollaborations/FindResponders.png "find responders")

Double-click on the new task to open its configuration. Set the *Candidate Type* to *FirstResponder*.
Set the *returnBehavior* to *Attach Return value to returnProperty* and then set returnProperty to *recommendedResponders*.
Click **OK**.

![find responders config](../assets/img/advcollaborations/FindRespondersConfig.png "find responders config")

## Notify First Responder and wait

Use the results from the Recommend task to Notify first responders one at a time, starting with the closest responder. 
If the first responder does not accept the notification within 1 minute, retract the message and notify the next 
closest responder.

### LoopWhile
Drag a *LoopWhile* task from the Flow Control section of the palette over the link between *FindResponders* and *NotifyFirstResponder* and then drop it.
Select *whileTrue* as the downstream event. The LoopWhile task is the App Builder's version of a while loop. It 
repeatedly executes the tasks in the *whileTrue* branch of the task from the *whileTrue* event to the branch leaf until the condition is false.
For more details on the Loop While activity pattern reference the [Loop While](../apps.md#loop-while) documentation.

![loop while](../assets/img/advcollaborations/LoopWhile.png "loop while")

Click on the new task and open its configuration. Set the condition to *counter < length(event.recommendedResponders)*. 
Set the *counterProperty* to *counter*. The counter property is attached to the outbound event so that any tasks
in the *whileTrue* branch have access to the loop counter. Click **OK**.

![loop while config](../assets/img/advcollaborations/LoopWhileConfig.png "loop while config")

Next click on the *NotifyFirstResponder* task to update the configuration.  
Update the body to: `event.recommendedResponders[event.counter].name + ": Are you available to assist " + event.name + "?"`.
Click on the *users* property and update the user to `event.recommendedResponders[event.counter].username`. This will index 
into the recommendedResponders array and return the `event.counter`th username. Click **OK** to close the pop-up.

![first responder updated config](../assets/img/advcollaborations/NotifyFirstResonderUpdatedConfig.png "first responder updated config")

### Wait For Response

Drag and drop a Delay task from the Flow Control section of the palette onto the NotifyFirstResponder task. Select *event* as the
downstream event. Notice that the Delay task is directly connected to the NotifyFirstResponder task rather than an asynchronous
downstream event triangle. This means that it is executed as part of the loop root to leaf path. Rename the task *AwaitResponse*.

![await response](../assets/img/advcollaborations/AwaitResponse.png "await response")

Click **Click to Edit** to configure the Delay task and set the *delay* to *1 minute*. 

![delay config](../assets/img/advcollaborations/DelayConfig.png "delay config")

### Retract Notification

If the Delay expires, we must retract the notification from the first responder before sending a notification to the next one.
Drag and drop a *GetCollaboration* task from the Collaboration section of the palette
onto the *AwaitResponse* task. Rename the activity *GetPayloadId*. 

![get payloadId](../assets/img/advcollaborations/GetPayloadId.png "get payloadId")


In the configuration, set the *taskName* to *NotifyFirstResponder*. This will return the collaboration state specific to the NotifyFirstResponder task which
includes the payloadId for the Notification message and any responses received.
Click **OK**.

![get payloadId](../assets/img/advcollaborations/GetPayloadIdConfig.png "get payloadId")

We only want to retract the notification if no responses have been received. Drag and drop a Filter task from the *Filters* 
section of the palette onto the *getPayloadId* task. Rename the task *NoResponse*. Double-click to edit the next
task. Set the filter condition to `event.responses == null || event.responses.size() == 0`. Click **OK** twice to close
the pop-ups.

![no response](../assets/img/advcollaborations/NoResponse.png "no response")

Drag and drop a *retractPayload* from the *Notification* section of the *Services* section of the palette onto the
*GetPayloadId* task. Rename the task *RetractMsg*.

![retract](../assets/img/advcollaborations/RetractMsg.png "retract task")

Double-click the new task to edit its configuration. Click **`<null>`** next to *parameters* to edit the Procedure parameters. Set the payloadId to *event.payloadId*
and leave the exclusionList empty. This retracts the notification associated with the payloadId returned by the upstream task.
Click **OK** twice to close the pop-ups.

![retract config](../assets/img/advcollaborations/RetractConfig.png "retract config")

The Loop follows the *event stream* path from the *whileTrue* event to leaf. This means it follows the direct arrows
from task to task. Asychronous downstream events (such as Notification response) are not considered part of this loop path.
The Loop flows from the *whileTrue* event -> *NotifyFirstResponder* -> *AwaitResponse* -> *GetPayloadId* -> *NoResponse* -> *RetractMsg* and then repeats.

Click **Save** to save the Service and Event Handler. 

## Assign First Responder

### Add Collaborator Role

The first responder is an active collaborator in this Collaboration and should be assigned to a distinct collaborator role. Click on the **State** section of the service implementation tab and open up **Collaboration State Properties**.  Now click **Click to Edit** next to *Collaborator Roles*. Click **+ Add an Item** and name the collaboratorRole *firstResponder*. Then click **OK**.

![first responder collaborator role](../assets/img/advcollaborations/FirstResponderCollaboratorRole.png "first responder collaborator role")

### Assign Collaborator
Drag and drop an Assign task from the Collaboration section of the palette onto the link between the *NotifyFirstResponder* response
event and *CollabComplete* task. Rename the task *AssignCollaborator*. 

![assign collaborator](../assets/img/advcollaborations/AssignCollaborator.png "assign collaborator")

Double-click on the new task to edit the configuration. Set the roleType to *collaborator* and the roleName to *firstResponder*. Click **OK**.

![assign collaborator config](../assets/img/advcollaborations/AssignCollaboratorConfig.png "assign collaborator config")

Click **Save** to save the Service and Event Handler.

### Add Assignment Filter

We only want to repeat the Loop tasks if the assignment has not yet occurred.
Click on the LoopWhile task to edit the configuration
and update the condition to: `counter < event.recommendedResponders.size() && (HeartRate.ActiveCollabsGetById(collaborationId, "firstResponder") == null)`.
This means the loop will end either when there are no more first responders to notify OR if a first responder has already been
notified and assigned to the firstResponder collaborator role.

![update loop while config](../assets/img/advcollaborations/LoopWhileUpdateConfig.png "update loop while config")

Click **Save** to save the Service and Event Handler.

## Loop Ends

So far, you've written the logic to loop through each of the recommended first responders until either one responds to the
notification or you run out of first responders to message. Next, you must handle what happens when the loop completes.
If the firstResponder collaborator role has not been set the collaboration has failed. Note that if the collaborator role
was set, the collaboration was marked as 'completed'.

Drag and drop a *GetCollaboration* task from the *Collaboration* section of the palette onto the *LoopWhile* task.
Select *onceFalse* as the downstream event and click **OK**. Rename the task *GetFirstResponder*.

![getFirstResponder task](../assets/img/advcollaborations/GetResponder.png "getFirstResponder task")

Double-click the GetFirstResponder task to edit the configurations. Set the taskName to *firstResponder*. Select *Attach Return Value
to returnProperty* as the return behavior. Lastly, set *firstResponder* as the returnProperty. 

![getFirstResponder task](../assets/img/advcollaborations/GetResponderConfig.png "getFirstResponder task")

Drag and drop a Filter task from the Filters section of the palette
onto the *getFirstResponder* task. Rename the filter *NoResponder*. Click **Click to Edit** to edit the Filter configuration.
Set the condition to *event.firstResponder == null* and click **OK** twice to close the pop-ups.

![no responder found](../assets/img/advcollaborations/NoResponder.png "no responder found")

Drag and drop a *CollaborationStatus* task from the Collaboration section of the palette onto the *NoResponder* task.
Rename the task *CollabFailed*. Click **Click to Edit** to edit the task's configuration and set *status* to *failed*. Click **OK**.

![collaboration failed](../assets/img/advcollaborations/CollabFailed.png "collaboration failed")

## Track the First Responder

### Track the First Responder
Track the first responder from their current location until they reach the patient. Drag a *Track* activity pattern
from the Mobile section of the palette over the link between *AssignCollaborator* and *CollabComplete* and drop it there.
Select *update* as the Downstream Event name and click **OK**.
Rename the task *TrackResponder*.

![track responder](../assets/img/advcollaborations/TrackResponder.png "track responder")

Double-click on the *TrackResponder* to edit its configuration. The *TrackResponder* task will receive the event produced
by the notification response. This means that the event will include the first responder's username. Click to open the pop-up
to configure the task's users property.Select *Literal Array* as the user type from the droplist.
Click **Add an item** and set the value to *event.username*. Click **OK** twice to close the
pop-ups.

![track responder config](../assets/img/advcollaborations/TrackResponderConfig.png "track responder config")

### Get Patient location

The Track task will produce a location update event as the first responder moves towards the patient. As each location update
event is received, check whether the first responder has arrived at the patient's location. To do this, get the patient's 
location by retrieving the *patient* information from the collaboration entities.
Drag and drop a *GetCollaboration* task from the Collaboration section of the palette
onto between the *update* event and the *CollabComplete* task. Rename the activity *GetPatientLocation*.

![get patient location](../assets/img/advcollaborations/GetPatientLocation.png "get patient location")

Click **Click to Edit** to edit the task configuration. Set the taskName to *patient*.
Set the *returnBehavior* to *Attach Return value to returnProperty* and then set returnProperty to *patient*.

![get patient location config](../assets/img/advcollaborations/GetPatientLocationConfig.png "get patient location config")

### Check if responder arrived

Drag a Filter task from the *Filters* section of the palette over the link between *GetPatientLocation* and *CollabComplete*
and drop it there. Rename the task *ResponderArrived*.

![responder arrived](../assets/img/advcollaborations/ResponderArrived.png "responder arrived")

Click **Click to Edit** to edit the Filter's configuration. Set the condition to `geoDistance(event.location, event.patient.location) < 50`.
This will return true if the first responder is within 50 meters of the patient. Click **OK** twice to close the pop-ups and 
**Save** Service Event Handler.

![responder arrived config](../assets/img/advcollaborations/ResponderArrivedConfig.png "responder arrived config")

Click **Save** to save the Service and Event Handler.

## Testing the App

Before you can begin testing your App, log into this Namespace in your Vantiq Mobile App. You may have to download the App
if you have not done so already.

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

### Collaboration Fails

First, test the case in which none of the first responders accept the notification which leads to the collaboration failing.
Note that for the purposes of testing you may choose to shorten the intervals for the *NotifyPatient* maxResponseTime
and *AwaitResponse* Delay tasks from 1 minute to 10 seconds.

Right click on the *generateHeartRate* Procedure in the *Procedures* section of the implement tab and click **Open in New Pane**.
Click the blue **Execute** play button. Pass *30* as the heartRate and click **Execute**. 

At this point, expect to receive the *PatientResponse* message. Do not respond to this message. Next, notice 3 messages arrive
one at a time for each first responder. Do not respond to these either. Notice that once the delay expires, the notification is removed
from the Vantiq App's notification center. Once all three first responders have been tried, the loop will end and the collaboration is marked
as *failed*.

![collaboration failed with badging](../assets/img/advcollaborations/CollaborationFailedWithBadging.png "collaboration failed with badging")

Click the **Clear Badges** icon at the top of the service pane.

![clear runtime status](../assets/img/advcollaborations/ClearRuntimeStatus.png "clear runtime status")

### Collaboration Success

To test the successful case where a first responder is tracked to the patient's location. Click [here](https://www.latlong.net/) 
and enter your address to discover your current latitude and longitude. In the *generateHeartRate* Procedure pane,
update the event location to *your* location. 
Click the blue **Execute** play button. Pass *240* as the heartRate and click **Execute**.

At this point, expect to receive the *PatientResponse* message. Do not respond to this message.
![notification sent](../assets/img/advcollaborations/NotificationSent.png "notification sent")

Next, when you receive the *FirstResponderNotification*, open the notification and click **On my way!**.


Notice when you respond to the notification, badges will appear on the *response* event. The Vantiq mobile App will then
start tracking your location. Since your location is the same as the patient's, the Filter should be *true* at the first
location update event and the collaboration will complete. 

![collab complete](../assets/img/advcollaborations/CollaborationComplete.png "collab complete")

## Conclusion

In this tutorial you learned how to:

* Use the Recommend activity pattern to compute a list of nearby first responders
* Use the LoopWhile activity pattern to notify first responders one at a time
* Retract notification messages when a response is not received
* Use the Track activity pattern to track a first responder's location