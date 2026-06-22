# Assembly Tutorial

![consumer Assembly Project](../assets/img/assemblytutorial/consumerAssemblyProject.png "consumer Assembly Project")

## Overview

In this tutorial, you will learn how to build Assemblies as reusable and configurable projects.
You will gain experience composing Assemblies and integrating them into existing Projects to quickly create fully customized Applications.

In this tutorial you will:

- Import an existing Project which detects "dangerous" weather conditions and either warns residents or orders an evacuation  
- Convert the imported Project into an Assembly and generalize it such that any data source and conditions may be used  
to trigger warning and evacuation alerts
- Publish the Assembly to the Catalog  
- Install the Assembly from the Catalog as a consumer and configure it to meet the consumer's requirements  

A brief note on terminology:

- An Assembly author is the creator of the Assembly and usually the person who published the Assembly to the Vantiq Catalog.  
- An Assembly consumer is a user who has installed the Assembly from the Catalog and is configuring the Assembly to integrate
it into their Application.

## Part 1: Setting up the Catalog

This tutorial assumes you are already familiar with the Vantiq Catalog. To learn about the Catalog, follow the full
[Catalog Tutorial](eventbroker.md).

If you're already familiar with the Catalog, follow [Part 1 of the Catalog Tutorial](eventbroker.md#part-1-setup-catalog-infrastructure)
to set up a Catalog host namespace, a publisher namespace, and a subscribing (consuming) Namespace for the Assembly.

## Part 2: Creating the Assembly

### Import the Project

To begin creating an Assembly, start by importing a fully functioning Project. The goal is to generalize this Project such 
that it can be customized to report warnings and evacuation alerts for any
type of data using the conditions specified by the Assembly consumer.

In the publisher Namespace created in Part 1, using the **Projects** button, select **Import**.

Select *Contributions* as the Import Type and *com.vantiq.weatherEmergencies.WeatherEmergencyProject* as the Contribution. Click **Import**.

![Project import](../assets/img/assemblytutorial/AssemblyProjectImport.png "Import project")

Click **Reload** once the import is completed. You have just imported a project that you will convert into an Assembly.

As an overview, the key resources in this Project are all in the `com.vantiq.weatherEmergencies` package:

* The `weather` Source which sends data to the `DetectWeatherEmergency` Service. 
* The `DetectWeatherEmergency` Service uses the `isDangerousWeather` App Component to detect whether there are dangerous weather conditions and triggers corresponding Collaboration Types
* The Collaborations send warning or evacuation notifications to be displayed by the `ResidentNotificationSystem` Client.


![Project overview](../assets/img/assemblytutorial/ProjectOverview.png "Project overview")

### Convert the Project into an Assembly

Using the **Projects** button, select **Convert To Assembly** and then click **Convert to Assembly** in the confirmation dialog.
This converts the Project from a static definition to a configurable, reusable, and shareable Assembly.

Set the description for the Assembly to: 

*Detects whether unhealthy weather conditions are present and notifies residents with a warning or evacuation alert.*

Click **Save** to save the Assembly.

![Assembly Pane](../assets/img/assemblytutorial/AssemblyPane.png "Assembly Pane")


### Creating the Assembly Interface

When Assemblies are installed by consumers, they act as black boxes to provide high level, reusable tools. Consumers can only 
interact with the Assembly through the Assembly Interface. 

The Assembly Interface is defined by the Event Driven Services
the author chooses to expose. Event Driven Services contain inbound and outbound Event Types which provide a layer
of abstraction between the implementation of the Assembly's asynchronous behavior and its consumers. Event Driven Services also define
Procedures that may be invoked by consumers. 

In this Project, the *com.vantiq.weatherEmergencies.DetectWeatherEmergency* Service exposes Event Types from the
_com.vantiq.weatherEmergencies.DetectWeatherEmergency_ Service which is the core event processing logic in the Assembly. This allows consumers to send events
to the Assembly and react to events produced by the Assembly.
The *com.vantiq.weatherEmergencies.WeatherService* Service provides some common
Procedures for transforming weather events such as *convertToFahrenheit*.

Navigate to the *Interface* tab of the Assembly Pane and click **Manage Services** to expose existing Services to the
Assembly Interface.

![Manage Services](../assets/img/assemblytutorial/ManageServices.png "Manage Services")

Select **com.vantiq.weatherEmergencies.WeatherService** and **com.vantiq.weatherEmergencies.DetectWeatherEmergency** and click **OK**. 

![Select Services](../assets/img/assemblytutorial/AddServices.png "Select Services")

![Services Added](../assets/img/assemblytutorial/ServicesAdded.png "Services Added")

Notice that each Event Type and Procedure from the two Services described above is now visible as part of the Assembly Interface.

The *WeatherEvents* Event Type represents the inbound events that triggers the Visual event handler in the *com.vantiq.weatherEmergencies.DetectWeatherEmergency* Service.  

The *WarningEvent* Event Type represents the outbound event produced by the *com.vantiq.weatherEmergencies.DetectWeatherEmergency* Service when
a warning notification is produced.

The *EvacuationEvent* Event Type is the outbound event produced by the *com.vantiq.weatherEmergencies.DetectWeatherEmergency* Service when
an evacuation notification is produced.

### Creating the Assembly Configuration Properties

The Assembly author may add Configuration Properties to the Assembly to define how the Assembly can be configured by
consumers. Configuration Properties describe how they are applied to specific properties for each project resource.

Assembly authors must thoughtfully define the Configuration properties to create an easy-to-use
experience for the consumers that still provides sufficient degrees of freedom to configure the Assembly to their requirements.

Navigate to the *Configuration* tab of the Assembly Pane. 

![Configuration Tab](../assets/img/assemblytutorial/ConfigurationTab.png "Configuration Tab")

First, add a configuration property that allows the consumer of the Assembly to customize
the *com.vantiq.weatherEmergencies.ResidentNotificationSystem* Client to a theme of their choice such 
that it matches their branding or style requirements. 

Click **New Property** and set the following properties:

* **Name**: *clientTheme*   
* **Description**: *The theme applied to the com.vantiq.weatherEmergencies.ResidentNotificationSystem Client*
* **Type**: *Client Theme*. 
* **Default**: *Light*

Under the Usage section click **Add Reference** and set the following properties.

* **Resource**: *Client*
* **ResourceId**: *com.vantiq.weatherEmergencies.ResidentNotificationSystem* 
* **Property**: *options.themeName*

Click **Add**.

![Client Config Property](../assets/img/assemblytutorial/AddClientConfiguration.png "Client Config Property")

Next, create a configuration property that allows the consumer of the Assembly to deactivate
the *com.vantiq.weatherEmergencies.weather*  Source and instead use custom local events which are rerouted to the Assembly. 

Click **New Property** and set the following properties:

* **Name**: *useBuiltInSource*
* **Description**: *Boolean property used to activate the provided "com.vantiq.weatherEmergencies.weather" source* 
* **Type**: *Boolean*
* **Default**: *true*. This sets the Source to *active* by default. The consumer must explicitly de-activate the Source
if that's the desired behavior.

Under the Usage section click **Add Reference** and set the following properties:

* **Resource**: *Source*
* **ResourceId**: *com.vantiq.weatherEmergencies.weather*
* **Property**: *active*

Click **Add**.

Lastly, create a property that allows consumers of the Assembly to swap out the App Component used in the
_com.vantiq.weatherEmergencies.DetectWeatherEmergency_ App such that they may set custom conditions for warning and evacuation alerts.

Click **New Property** and set the following properties:

* **Name**: *detectDangerousWeather*
* **Description**: *Component used to determine whether there is a warning or emergency. The events, WarnResidents and Evacuation Required, must emit a warning message object*.
* **Type**: *App Component*
* **Default**: *com.vantiq.weatherEmergencies.isDangerousWeather*. You'll set the default to the current Component used by the App to maintain
  the current default behavior.

Under the Usage section click **Add Reference** and set the following properties:

* **Resource**: *App*
* **ResourceId**: *com.vantiq.weatherEmergencies.DetectWeatherEmergency.WeatherEvents*
* **Property**: *Component Used by Task com_vantiq_weatherEmergencies_isDangerousWeather*

Click **Add**.

![Configuration Properties](../assets/img/assemblytutorial/ConfigurationProperties.png "Configuration Properties")


### Creating the Visible Resources

All of the Assembly resources are copied into the consumer's Namespace when they install the Assembly, however
Consumers are only able to see and interact with resources enumerated
either in the Interface or in the Visible Resources tab.

While the Interface defines connection points for interacting with and integrating the Assembly, the Visible Resources
enumerate the Assembly resources which are re-usable and can be used throughout a consumer's application.

The *com.vantiq.weatherEmergencies.ResidentNotificationSystem* is a Client which displays the weather alerts. This is the user-facing
element of this Assembly. Therefore, it is useful to make visible so that Assembly consumers may launch the
Client and include it in their Project to alert users. 

The *com.vantiq.weatherEmergencies.isDangerousWeather* is an App Component which may be useful for the Assembly consumer to reuse in other parts of their
Application.

Navigate to the *Visible Resources* Tab of the Assembly Pane and drag the *com.vantiq.weatherEmergencies.isDangerousWeather* App Component and
*com.vantiq.weatherEmergencies.ResidentNotificationSystem* Client into the Visible Resources column.

![Visible Resources](../assets/img/assemblytutorial/VisibleResources.png "Visible Resources")


### Testing the Assembly

Congratulations, you have just authored your first Assembly! 

You have exposed the activation status 
for the *com.vantiq.weatherEmergencies.weather* Source, the App Component to be used by the *com.vantiq.weatherEmergencies.DetectWeatherEmergency* Service, and the Client Theme as configuration
properties for this Assembly.

Before publishing the Assembly to the Catalog, you should test the Assembly locally to ensure that it works and is configurable
as you expect.

Test the Assembly by overriding the Source's activation status.

Navigate to the Assembly Pane and click **Configure As Consumer**. 

![Configure as consumer](../assets/img/assemblytutorial/ConfigureAsConsumerBtn.png "Configure As consumer")

This places you in a *Consumer State* that allows you to configure the Assembly as if you were a consumer. Navigate to the
*Configuration* tab.

Locate the droplist next to the *useBuiltInSource* property and select *false*. This disables the *com.vantiq.weatherEmergencies.weather* Source.

Click **Save** to save the Assembly.

![Configure as consumer](../assets/img/assemblytutorial/ConfigureAsConsumer.png "Configure As consumer")

Open the *com.vantiq.weatherEmergencies.weather* Source by navigating to the Assembly Contents tree and selecting the Source.

Click **Test Data Receipt**. The Source is currently configured as inactive and therefore is not receiving any data.

![Waiting For Data](../assets/img/assemblytutorial/WaitingForData.png "Waiting for data")

Now set **useBuiltInSource** back to *Use Default Value* to activate the configured Source. Click **Save** in the Assembly pane.
Now expect to see weather data populate the *com.vantiq.weatherEmergencies.weather* Source viewer. Note: weather events are only produced every 10 seconds
so you may need to wait a few seconds before seeing data.

![Waiting For Data](../assets/img/assemblytutorial/WeatherData.png "Waiting for data")

Click **Edit as Author** in the Assembly pane. This toggles back to author mode and removes the configuration.

![Edit as author](../assets/img/assemblytutorial/EditAsAuthor.png "Edit as author")

### Publishing the Assembly

Now that you have tested the Assembly and it works as expected, it is time to publish it to the Catalog so that
other Vantiq developers can take advantage of it.

Navigate to the *General* tab of the Assembly pane and click **Publish** cloud icon.

![Assembly Pane](../assets/img/assemblytutorial/AssemblyPane.png "Assembly Pane")

## Part 3: Consuming the Assembly

### Install the Assembly

Switch to the subscriber namespace you created in Part 1. Name the current Project *AirQualityAlerts* and click **Save**
to save the Project.

The Assembly was originally designed to provide weather alerts if the temperature was too hot.
You are going to use the WeatherEmergency Assembly to create an Application that notifies residents when the local
air quality is unsafe, and alert them to evacuate when it reaches toxic levels.

To accomplish this, you will replace the App Component used by the Assembly with one you create that detects
unhealthy air quality. You will reroute local events to the Assembly using the Assembly's Interface.
Finally, you will retheme the Notification Client to use a theme that matches your company's branding.

Open the Catalog Pane by using the **Show** button and selecting **Catalogs**.
Select the Catalog that you published the Assembly to and then click **Assemblies**.

![Assembly Catalog](../assets/img/assemblytutorial/AssemblyCatalog.png "Assembly Catalog")

Right click on **com.vantiq.weatherEmergencies.WeatherEmergencyProject** and click **Install**, then click **Install** on the confirmation dialog.
You will be prompted to provide Assembly Configuration. This allows you to install the Assembly in the 
your desired state. For now, install the Assembly using the current defaults. Click **OK** to install the Assembly.

![Assembly Install Properties](../assets/img/assemblytutorial/AssemblyInstallProperties.png "Assembly Install Properties")


Open the *com.vantiq.weatherEmergencies.ResidentNotificationSystem* Client by navigating to the Project Contents tree and selecting the *com.vantiq.weatherEmergencies.ResidentNotificationSystem* Client.

![Client has been installed](../assets/img/assemblytutorial/ClientInstalled.png "Client has been installed")

Launch the Client by clicking the **Run** button in the titlebar. Expect to start to see Weather emergency
notifications within 10 seconds.

![Weather warning message](../assets/img/assemblytutorial/WeatherWarningMessage.png "Weather warning message")


### Create a Custom Source

To configure the Assembly to use AQI (Air Quality Index) events,
we will use a public Vantiq Source that produces artificial MQTT data to simulate air quality readings
from a city with poor air quality.

First, create a new AQI Source for that MQTT server.

Use the *Add* menu button and select *Source*. Click **New Source**.

Name the Source *AQIReadings* and set the Source Type to *MQTT*.

![AQI Source](../assets/img/assemblytutorial/NewAQISource.png "AQI Source")

In the *Server URI* tab of the Source pane, add the uri: *tcp://public.vantiq.com:1883*

In the *Topic* tab of the Source pane, add the topic: *com.vantiq.mqtt.aqi*

Save the Source. Click **Test Data Receipt** to verify that your Source is receiving AQI data.

![AQI Source events](../assets/img/assemblytutorial/AQISourceEvents.png "AQI Source events")

### Transform Local Events into Assembly Events

Now that you have a new Source of events, you must disable the existing Assembly Source and instead route the AQI events
to the Assembly.

Navigate to the *com.vantiq.weatherEmergencies.WeatherEmergencyProject* Assembly pane and under the *Configuration* tab set *useBuiltInSource* to
*False* and click **Save**. This disables the *com.vantiq.weatherEmergencies.weather* Source.

![Disable the weather source](../assets/img/assemblytutorial/DisableSourceConfig.png "Disable the weather source")

Now you must transform *AQIReadings* events into events that the Assembly can ingest. Navigate to the *Interface* Tab
of the Assembly Pane. Notice that there is one inbound Event Type defined: *com.vantiq.weatherEmergencies.DetectWeatherEmergency/WeatherEvents*. You can use
the inbound Event Type to send events to the Assembly. Right-click on the *com.vantiq.weatherEmergencies.DetectWeatherEmergency/WeatherEvents* Event Type and click **Transform Local Events**.

![Right click to transform local events](../assets/img/assemblytutorial/TransformLocalEvents.png "Right click to transform local events")

Set the Service name to *TransformAQIEvents*, the Package to *com.vantiq.aqi*, and click **OK**.

The *com.vantiq.aqi.TransformAQIEvents* Service opens to display the _WeatherEvents_ Event Handler which contains an empty Event Stream, a Transformation task, and a PublishToEventType task. By configuring the
EventStream, this Event Handler automatically routes events from the specified event path to the inbound Event Type for the Assembly.

![Initial TransformAQIEvents App](../assets/img/assemblytutorial/InitialTransformationApp.png "Initial TransformAQIEvents App")

Click on the EventStream task outlined in red.

Name the EventStream *AQIEvents* and click *Click to Edit* in the slide out to configure the App Task.  

Set the inboundResource to *sources*.  
Set the inboundResourceId to *AQIReadings*.  
Click **OK**.

The Transformation task is needed when your local events do not match the format or schema of the  Event Type.
Since your local events match the schema, you can delete the Transformation task by clicking on the Transformation task
and clicking **Delete**.

Right-click on the AQIEvents Task and select *Link Existing Task*. Select *PublishToEventType*
and click **OK**.

Disable the Event Handler (and Service) for now by clicking Toggle Keep Active Off button in the titlebar. We will re-enable it when we have fully configured the Assembly.

Click **Save** to save the Service.

![TransformAQIEvents App](../assets/img/assemblytutorial/TransformAQIEventsApp.png "TransformAQIEvents App")

### Replacing the App Component

The Assembly currently uses an App Component to determine if the weather is dangerously hot. You want to replace the
Component to instead detect whether the air quality is unhealthy. When replacing one App Component with another through
Assembly Configuration, the replacing Component must have the exact same configuration properties and downstream events
as the original component. To guarantee that the replacing Component has the correct definition, you can use the shortcut 
provided in the Assembly Pane.

Navigate to the *Configuration* tab in the Assembly Pane. In the *Actions* column next to the *detectDangerousWeather* 
property, click the Lightning icon to create a Component stub. 
Set the Component Name to *isDangerousAirQuality*, the Package to *com.vantiq.aqi*, and click **OK**.

![Create Component Stub](../assets/img/assemblytutorial/CreateComponentStub.png "Create Component Stub")

An App Component skeleton will appear with the downstream events: WarnResidents and EvacuationRequired defined.

![Component Stub](../assets/img/assemblytutorial/InitialAirQualityComponent.png "Component Stub")

Click to configure the Transformation task. Set the following properties on the transformation:

* **outboundProperty**: *aqi*
* **Transformation Expression**: `toInteger(toReal(event.data.aqi))`

This transforms the string AQI value into an integer and
unnest the value so that it may be referenced downstream directly instead of as a nested property of the data object.

Click **OK**.

![AQI transformation](../assets/img/assemblytutorial/AQITransformation.png "AQI transformation")

Drag a Filter task between the Transformation task and the WarnResidents downstream. Name the task *UnhealthyForSensitiveGroups*.
Configure the Filter task to have the **condition** *event.aqi > 100 && event.aqi < 150*.

Drag a Transformation Task between *UnhealthyForSensitiveGroups* and the *WarnResidents* downstream. Name the task 
*WarnMessage*. Click to configure the Transformation task. Set the values to :

* **outboundProperty**: *message*
* **Transformation Expression**: `now().toString() + ": The AQI is " + toDecimal(event.aqi, 1).toString() + ". This is unhealthy for sensitive groups. Limit outdoor activity"`.

**Save** the Component.

![warn message transformation](../assets/img/assemblytutorial/warnMessageTransformation.png "warn message transformation")

Drag a Filter task between the Transformation task and the EvacuationRequired downstream. Name the task *Unhealthy*.
Configure the Filter task to have the **condition** *event.aqi >= 150*.

Drag a Transformation Task between *Unhealthy* and the *EvacuationRequired* downstream. Name the task
*EvacuationMessage*. Click to configure the Transformation task. Set the values to :

* **outboundProperty**: *message*
* **Transformation Expression**: `now().toString() + ": The AQI is " + toDecimal(event.aqi, 1).toString() + ". This is unhealthy for all citizens and outdoor activity should be limited as much as possible"`.

**Save** the Component.

![AQI component](../assets/img/assemblytutorial/AQIComponent.png "AQI component")

### Configuring the Assembly

Navigate back to the Assembly Pane and go to the *Configuration* tab with the following configuration:

* **detectDangerousWeather**:  *com.vantiq.aqi.isDangerousAirQuality*
* **useBuiltInSource**: *False*. 
* **clientTheme**: *Cheetah*.

Click **Save** to save the Assembly.

![AQI component](../assets/img/assemblytutorial/FullConfiguration.png "AQI component")

Open the *com.vantiq.weatherEmergencies.ResidentNotificationSystem* Client and click the Run button in the titlebar to run the Client. 
Notice that the background of the Client
is orange to reflect the configured theme. 

Navigate back to the **TransformAQIEvents** Service and click the Toggle Keep Active On button in the titlebar to activate the *WeatherEvents* Event Handler. Click
**Save** to save the Service.

Expect AQI warning events populate the Client instead of weather events. Note: AQI events only occur every 10 seconds
so you may need to wait a few seconds before seeing warnings arrive.

![AQI client warning events](../assets/img/assemblytutorial/AQIWarningEvents.png "AQI client warning events")

## Conclusion

Congratulations! You have authored and consumed your first Assembly! 

* You took an existing project and turned into a configurable and reusable business solution. 
* Installed an Assembly and customized it to fit your requirements.
* Swapped out an App Component to customize the core decision-making
functionality
* Rerouted local events to trigger the Assembly's asynchronous processing
* Applied a custom theme to a Client.
