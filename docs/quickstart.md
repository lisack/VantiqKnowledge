# Quickstart Tutorial

## Objectives
Create a simple running temperature alerting application using Vantiq's [Generative AI](https://en.wikipedia.org/wiki/Generative_artificial_intelligence) capabilities.

## Tutorial Overview
This tutorial demonstrates the Design Modeler, a visual IDE tool for building Vantiq systems. It uses [Claude Code](https://claude.com/product/claude-code), a Generative AI product that allows the user to enter a text description of the system to be built then turns that description into the beginnings of the running application. The basic steps to create this application are:

* Create a new Project, including a Claude Code configuration to interact with the Vantiq server
* Use the Claude Code command line interface (CLI) to turn a simple application description into a Vantiq Project, including a Design Model that displays an overview of the application
* Configure a Source to receive simulated sensor data
* Run the application in simulation

>Note: if needed, you can import a finished version of this Project using the **Projects** button and select **Import**. Select _Tutorials_ for Import Type, then select _Quickstart_ from the second drop-down, then click **Import**.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.


### Namespace Privileges

<a name="namespace_privilege"></a>
In addition, when following the Tutorials, please make sure you are logged in as the administrator of the Vantiq namespace to which you are assigned. You can check your privilege level by clicking on your username in the title bar. If the bottom of the popup says, "Developer" or "Namespace Admin" at the bottom, you have the needed privileges. If it says, "User (Developer)," then you need to [change to a Developer namespace](./admin.md#change_namespace). You may need to first create your own Developer namespace, as described here: [Creating a Developer Namespace](./admin.md#create_dev_namespace).

## 1: Creating a Temperature Alert Project
The first task in building the temperature alerting system is to create a Project in the Vantiq IDE.

>Note: You will be alerted if you do not have permission to create a Project in the current namespace. You need to change to, or create, a namespace where you have Developer or Namespace Admin privilege ([see above](./quickstart.md#namespace_privilege)).

Use the **Project** menu to select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new Project to the current Namespace, select **AI Development** as the Project type and click **Continue**.

&nbsp;&nbsp;&nbsp;&nbsp;![133_IntroTut_CreateProjScreen](../assets/img/intro/133_IntroTut_CreateProjScreen.png "Create Temperature Alert Project")

Set the Project name to *TemperatureAlert* and click **Continue**. The **Create Claude Code Access** dialog is displayed with information similar to the following:

&nbsp;&nbsp;&nbsp;&nbsp;![ClaudeCodeAccess](../assets/img/quickstart/ClaudeCodeAccess.png "New Design Model")

As part of setting up the new Vantiq Project, an access token is created. Follow the instructions in the dialog to use that access token to link a Claude Code CLI session to the Vantiq server.

Click **Finish** to confirm.

## 2: Using Claude Code
For this tutorial, we'll use the [CLI version of Claude](https://code.claude.com/docs/en/quickstart#step-1-install-claude-code) to build the temperature alerting application. Open a new command line interface on your local machine (e.g. Terminal on macOS), then navigate to the directory that contains the .mcp.json file referenced in the **Create Claude Code Access** dialog from Step 1 above.

Start a new session by starting the claude CLI:

&nbsp;&nbsp;&nbsp;&nbsp;![CCStart](../assets/img/quickstart/CCStart.png "Start Claude CLI Session")

At the Claude CLI prompt, use the text entry field to enter the following text:

```text
Create an application to receive temperature events from MQTT
source 'TempMQTT'. If the temperature crosses a threshold of 200
degrees, notify user 'maintenance' via the 'Maintenance' Client.
Place all resources created in project 'TemperatureAlert'.
```
This short text describes a simple temperature sensing application, reading from an MQTT Source and notifying a user when a high temperature threshold is crossed. Once the text has been entered, Claude will start building the application, prompting for information it needs to build. For example, it will ask for a package name: use one of the suggested package names or enter one of your own. It may ask for a MQTT broker URI and topic. If so, use *tcp://public.vantiq.com:1883* and *com.vantiq.mqtt.enginetemp*.

Claude will update the display as it makes progress:

&nbsp;&nbsp;&nbsp;&nbsp;![CCProgress](../assets/img/quickstart/CCProgress.png "Create Claude Session Progress")

Please note the Claude response may take several minutes or more depending on the complexity of the description entered. Once Claude completes the application, it will display a summary of the work that it did:

&nbsp;&nbsp;&nbsp;&nbsp;![CCFinish](../assets/img/quickstart/CCFinish.png "Create Claude Session Finished")

It is important to remember the output of Generative AI systems such as Claude can vary even when entering the same prompt in a different session. The names of resources and their contents in the steps that follow may be different than what is produced by Claude. Please be prepared to apply the concepts in the following steps to resources that might not have exactly the same names and/or properties.

## 3: Opening the Design Model
Claude transfers the resources it creates to the Namespace specified in Step 1 above via the Vantiq server's [MCP server](https://modelcontextprotocol.io/docs/getting-started/intro). Open the Design Model it created, *TemperatureAlertApp*, by using the **Add** menu to select **Design Model**, then select **TemperatureAlertApp**.

The Design Model pane will look similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;![Design Model](../assets/img/quickstart/DesignModel.png "Initial Design Model")

The graph contains three nodes:

1. _TempMQTT_: the white-titled node represents an External System. In this case, it's a placeholder for the MQTT server that's delivering the temperature sensor readings.
2. _TemperatureMonitorService_: the green-titled node represents the Service that implements the sensor reading Event Handler.
3. _Maintenance_: the purple-titled node that represents the Client that receives the temperature threshold notification.

For more detailed information about the Design Modeler, please consult its [Reference Guide](../designmodeler.md#understanding-the-design-model-pane).

## 4: Configure the TempMQTT Source
The application description sent to Claude specified an MQTT sensor data Source called _TempMQTT_. This Claude-created [Vantiq Source](../sources/source.md) should be reviewed in order to run the _TempEventStream_ Event Stream task described in the preceding sections. This Source will receive simulated temperature readings from a public Vantiq MQTT server.

Use the **Add** menu to select **Source...**:

&nbsp;&nbsp;&nbsp;&nbsp;![AddSource](../assets/img/quickstart/AddSource.png "Add Source")

Select *com.vantiq.temp.TempMQTT* to display the Source pane. Ensure the following two values are present:

1. In the **Server UI** tab, an item with the value _tcp://public.vantiq.com:1883_
2. In the **Topic** tab, an item with the value _com.vantiq.mqtt.enginetemp_

If changes needed to be made, save the Source.

## 5: Address the Design Model To Do List
The lower left of the Design Model may contain the **To Do List**. The **To Do List** contains errors found in the _TemperatureMonitorService_ Service created for the Design Modeler. Errors are normal and are associated with Event Handler tasks that need to be configured in order to have a completely running application, although not all Design Models will contain errors.

Clicking on any **To Do List** item causes the Service pane that contains the error to be displayed. The pane will display the nature of the error that needs to be corrected.

## 6: Adjust Event Handler Properties
The description of the application given to Claude didn't contain a lot of details so Claude either prompted you for details or made assumptions when building the application. In order to have a fully functional application, you should review the resources Claude produced. An example of this review was done in Step 4: checking the configuration of the *TempMQTT* Source.

Other changes will likely have to be made to the Event Handler in the *com.vantiq.temp.TemperatureMonitorService*. Using the Design Model, right-click the *TemperatureMonitorService* and select **Edit in Service Builder**.

&nbsp;&nbsp;&nbsp;&nbsp;![Review Properties](../assets/img/quickstart/ReviewProperties.png "Review Properties")

In the **Event Handlers** section on the right, open the **Source** section, then click the *TemperatureReceived* Event Handler. The Event Handler will display as shown above but may have slightly different contents.

Click the *ThresholdCheck* task, then click the **Click to Edit** link in the _'Filter' Activity_ slide out on the right side of the pane. The *condition* property may read *event.value.temperature > 200*. This is an assumption made by Claude as to the format of data returned by the *TempMQTT* Source. However, the actual temperature property returned by the Vantiq MQTT example Source is *event.temperature*. If necessary, edit the *condition* property to use this actual property. Click **OK** to save the configuration.

Click the *NotifyMaintenance* task, then click the **Click to Edit** link in the _'Notify' Activity_ slide out on the right side of the pane. The *body* property may contain a similar reference to *event.value.temperature* so edit that value to *event.temperature*. Click **OK** to save the configuration.

Save any changes to this *TemperatureMonitorService* Service.

## 7: Running the Application

By correcting any errors and ensuring the values of various resource properties, the Design Modeler **To Do List** should be empty and the application should start running. If it is running correctly, the _TemperatureReceived_ Event Handler graph should look similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;![Running Application](../assets/img/quickstart/RunningTempStream.png "Running Application")

Note the rectangular badges with numbers that appear over the tasks. These badges increment as each task event is received. This means the Source is configured correctly and the _TemperatureMonitorService_ Service is successfully receiving and processing those events.

## 8: Create A Session Summary

Optionally, you may ask Claude to produce a session summary: enter _'Please produce a session summary.'_ in the **Type / for commands** field at the bottom of the Claude CLI. Claude will produce a summary of the resources created. To view the summary, click the **VIA Session Summaries** button at the top right of the Vantiq IDE:

&nbsp;&nbsp;&nbsp;&nbsp;![VIA Session Summary](../assets/img/quickstart/VIASS.png "VIA Session Summary")

## 9: Example Claude Descriptions
Claude uses a Generative AI engine to translate natural language descriptions of a desired system into skeletons of Design Models. Those descriptions are generally referred to as _prompts_. Writing effective prompts is referred to as [prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering). In order to make effective use of Claude, it's helpful to have some examples of prompts that are good starting points to describe business processes. Below are a few examples of such prompts that translate to terms understood by the Vantiq system.

### Patient Care Example
Patient vital sign events are received from the '/vitals' Topic and are of type Vitals. If a vital sign property is above or below a threshold value, the vital signs are saved in the database using the Patient type and the patient's doctor is notified using the PatientCare Client. The patient's doctor receives the notification and interviews the patient using the PatientCare Client. Patient interview text events are received and the Patient type is updated with the new interview text. The interview text is also sent to a Procedure which generates suggestions for a diagnosis and treatment plan. The treatment plan is sent as a new notification to the doctor using the PatientCare Client.

### Pump Monitoring Example
There is a pump with a temperature and pressure sensor. Join the two events together and notify a technician when the pressure is over 150. Track the technician’s location and send a notification to the factory manager when they are close. Send a notification to the factory manager when the technician has resolved the issue.

### Image Processing Example
Source "imageSrc" produces an event when a person is passing through the building entrance. The event can be described as type "com.alertcalifornia.cameras". Count the number of people entering and leaving the building. Then use those numbers to calculate the number of people remaining in the building. Generate an alert if there are more than 300 people in the building.