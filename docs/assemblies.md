# Assembly Guide

## Introduction

Vantiq constantly strives to make developers successful as quickly and easily as possible. 
Assemblies allow developers to construct reusable solutions that can be easily integrated and applied in many contexts. 
This powerful tool
allows developers to raise the level of abstraction and complete full scale applications faster than ever before.

Assemblies are Vantiq Projects that are configurable and customizable to each
user's individual requirements. Assemblies provide higher level functionality than any individual Vantiq resource. They
work as a black box, abstracting away any implementation details and only exposing what will be directly used by
its consumers.

Developers can now build full scale Applications by composing existing Assemblies, weaving them together through 
general interfaces, to create custom solutions. 

## Tutorial

To walk through building your first assembly, check out the [tutorial](tutorials/assemblytutorial.md).

## Assembly Terminology

Below is a brief glossary of terms used to define Assemblies and how they are used:

- **Assembly**: A reusable, shareable, and configurable Vantiq Project
- **Project**: A Vantiq Project is a named collection of resources defined in a Namespace
- **Author**: The creator of an Assembly is known as its *author*. This is the person who either built the Project from scratch, 
or otherwise took an existing project and generalized it into a configurable, reusable Assembly.
- **Publisher**: The publisher of an Assembly is the person who publishes an Assembly to the Vantiq Catalog. This is usually the Assembly Author.
- **Consumer**: A Consumer is a Vantiq user who *installs* an Assembly from the Catalog. Consumers configure installed Assemblies and integrate them into their own Projects.

## Authoring an Assembly

Assemblies are special instances of Projects (_system.projects_) with the following properties:

- **name** (*String*): the unique name for the assembly
- **resources** (*Array of Objects*): An array of objects each of the form `{resourceReference: </resource>/<resourceId>}` defining each of the resources contained by the Assembly.
- **isAssembly** (*boolean*): a boolean flag that must be set to true if the project is an Assembly
- **configurationProperties** (*Object*): A map where each key is the name of the configuration property and the value is the property description. See the [Configuration Properties](#configuration-properties) section for more details.
- **configurationMappings** (*Object*): An object describing how each configuration property is applied to the Assembly resources. See the [Using Configuration Properties to Customize Resources](#using-configuration-properties-to-customize-resources) section for more details.
- **visibleResources** (*Array of Strings*): A list of resource references describing which of the Assembly resources are visible to Assembly Consumers. 
The Services in this list are considered the Assembly Interface.
- **dependentAssemblies** (*Array of Objects*): A list of Assemblies that will be installed alongside this Assembly when a Consumer installs it. Each entry is of the form `{name: <assembly name>, catalog: <catalog name>}`. See the [Dependent Assemblies](#dependent-assemblies) section for more details.

![Assembly Pane](assets/img/assemblies/AssemblyPane.png "Assembly Pane")

**Note**: It is _highly_ recommended that Assemblies and all of their resources are contained in Packages. This 
significantly decreases the likelihood that the Assembly resource names collide with resource names in the consumer's namespace. 

### Assembly Interface

An Assembly author's goal must be to abstract away as many *implementation details* of the Assembly as possible. While all
Assembly resources are always copied into the consumer's Namespace on Assembly install, by default all resources within the Assembly
are hidden from the Consumer. The author must explicitly select which resources to make *visible* or available for the Consumer.

The resources consumers directly interact with within an Assembly come in two flavors: the Interface and other Visible Resources.

The Interface for the Assembly is a list of [Event Driven Services](rules.md#services) that the author exposes. Event Driven Services contain
Event Types and Procedures. The Event Types, either inbound or outbound, define how the Consumer communicates with the asynchronous 
pieces of the Assembly. Consumers send events to the Assembly by publishing to any inbound Event Type. Consumers use Outbound events
to trigger any local Rules, Apps, or Collaboration Types. Consumers can also invoke Procedures defined in any of the exposed Services.

Because the Interface is the only mechanism by which Consumers directly interact with any of the Assembly resources, 
it represents a kind of contract. Best practice highly discourages breaking the contract by removing Services from the Interface
or changing how they are defined, once the Assembly is published. Consumers expect and rely on the Event Types and Procedures used to integrate
the Assembly into their Project. Removing or modifying existing connection points is almost guaranteed to break consumer Applications.
While authors may update Assemblies to change their internal implementations, it is highly encouraged to maintain the Interface
or only to add to the Interface between versions.

The Assembly pane allows authors and consumers to view the Interface as either a flat list of Events and Procedures or
by Service.

The pane displays the Interface by Events and Procedures by default. Users browse the inbound and outbound Event Types
as well as Service Procedures using the left-hand tree. The center of the pane displays information about the selected
Event Type or Procedure.

![Assembly Interface](assets/img/assemblies/AssemblyInterface.png "Assembly Interface")

Select *View By Services* in the upper right-hand corner to display the Interface by Service instead. 
The pane then shows the Service names on the left-hand side, while the center of the pane
shows each of the Event Types and Procedures defined by that Service.

![Assembly Interface By Service](assets/img/assemblies/AssemblyInterfaceByService.png "Assembly Interface By Service")

Services in the Assembly Interface are listed in the Assembly's *visibleResources* property by ResourceReference.  

For example, the screenshot above shows an Assembly that has two Services in the Interface: *WeatherService* and *apps.services.DetectDangerousWeather*.
These are added to the *visibleResources* property as:

```
 {
    "resourceReference": "/system.services/WeatherService"
 },
 {
    "resourceReference": "/system.services/apps.services.DetectWeatherEmergency"
 }
```

### Visible Resources

The Interface contains the exposed Services within the Assembly that represent the direct integration points.
Assembly authors may choose to expose other Assembly resources to the Consumer as
*Visible Resources*. Visible Resources are *read-only* from the Consumer's point of view. Any changes to visible Assembly 
resources are overwritten on Assembly update. 

The only resource types that can be exposed as Visible Resources are:

- App Components
- Clients
- Client Components
- Tests
- Test Suites
- Event Generators
- Documents
- Storage Managers
- GenAI Components
- LLMs
- Types

The consumer can run, execute, or reuse these resources without considering any of the implementation
details of the Assembly itself. 

**Note**: The best practice for Test, Test Suites, and Event Generators made visible to Assembly Consumers is to exclusively 
use Service Event Types as the Test inputs/outputs and Generator events. This mimics how the Consumers interact 
with the Assembly and maintains the correct abstractions.

![Visible Resources](assets/img/assemblies/VisibleResourceTree.png "Visible Resources")

The _visibleResources_ property of the Assembly instance contains both the Services in the Interface and any other resources that 
have been made visible. Given the two Services that were added to the Interface in the above section and the two resources
shown as visible in the screenshot above, the _visibleResources_ property of the Assembly instance is:

```
{
"resourceReference": "/system.services/WeatherService"
},
{
"resourceReference": "/system.services/apps.services.DetectWeatherEmergency"
},
{
"resourceReference": "/system.collaborationtypes/isDangerousWeather"
},
{
"resourceReference": "/system.clients/ResidentNotificationSystem"
}
```

### Configuration Properties
 
Configuration Properties define what is configurable by the Consumer of the Assembly. After a Consumer installs an
Assembly they customize the behavior of the Assembly to their requirements by supplying configuration values for each configuration property.

The author of an Assembly must carefully choose which aspects of the Project to make configurable by consumers. This is
always a balancing act; too much configuration makes the Assembly hard to use or understand for a consumer, but too
little configuration makes the Assembly too specific to be reusable.

Each Configuration Property contains the following properties:

- **type**: (*String, required*): The type of value that the Consumer must provide at configuration time to set this property. The type
  must be one of the following: *String, Integer, Decimal, Real, DateTime, Boolean, Object, User Defined Schema Type, App Component, Client Theme, Secret*.
- **description** (*String, optional*): A description of the configuration property
- **required** (*Boolean, optional*): A boolean representing whether the Consumer is required to provide a value for this property at configuration time
- **default** (*any, optional*): For configuration properties that are not required, the author may set a default value that is used if the consumer does not provide a configuration value
- **multi** (*boolean, optional*): A boolean representing whether the Consumer must provide a list of values for this property

Example: If the Assembly exposes a property called *sourceTopics* that is used to override the topics used by an
MQTT source, the *configurationProperties* property of the Assembly looks like:

```
{
    "sourceTopics": {
        "description": "topics used by the weather MQTT source to subscribe to",
        "multi": true,
        "required": false,
        "type": "String",
        "default": []
     }
}
```

![Source topics property](assets/img/assemblies/sourceTopicsProp.png "Source topics property")

### Using Configuration Properties to Customize Resources

The author of the Assembly also defines *how* each Configuration Property is applied to Assembly resources.

In the *Usage* section of the Configuration Tab, authors specify the resource, resourceId, and property to which
the Configuration Property is applied. A Configuration Property may be applied to zero, one, or many resources
or properties of a resource.

![Source topics property with usage](assets/img/assemblies/sourceTopicsPlusUsage.png "Source topics property with usage")

The *Usage* section is stored in the *configurationMappings* property of the Assembly definition.
The *configurationMappings* property of the Assembly definition is a map of the configuration property name to the list
of resource properties that it is applied to. 

For example the following is a configurationMappings that applies:

- **clientThemeName** to the *WeatherDisplay* and *EmergencyNotifications* Clients
- **sourceTopics** to the topics used by a Source called *weather*
- **detectionComponent** to the App Component used by the *isDangerousWeather* Task in the *DetectDangerousConditions* App.


``` 
{
    "clientThemeName": [
        {
            "resource":"clients",
            "resourceId": "WeatherDisplay",
            "property": "options.themeName"
        },
        {
             "resource": "clients",
             "resourceId": "EmergencyNotifications",
             "property": "options.themeName"
        }
    ],
    "sourceTopics": [
        {
             "resource": "sources",
             "resourceId": "weather",
             "property": "config.topics"
        }
    ],
    "detectionComponent": [
        {
             "resource": "collaborationtypes",
             "resourceId": "DetectDangerousConditions",
             "property": "assembly.isDangerousWeather.pattern"
        }
    ],
}
```

It is important to note that not all properties of all resources are configurable. In time, the configuration space for Assembly resources will grow.
The properties available for configuration are:

- **App Components**: The App Component used within an App may be swapped out for another App Component with the same interface
- **Client Theme**. The name of a theme to be applied to a particular client
- **Event Handler Properties**. Specific properties within an Event Handler. See the [Event Handler Configurations](#additional-event-handler-configurations) section for more details
- **Source Active Property**: Sources may be activated or deactivated via configuration
- **Source Configuration**: The full *config* object or any known sub-property of the config object for a given Source. See the [Source Configurations](#additional-source-configurations) section for 
more details.
- **Scheduled Procedure Interval**: The interval (in milliseconds) used by a Scheduled Procedure in a Service contained by the Assembly
- **VAIL Property**: A String property referenced in a Procedure or Rule fetched using the `ResourceConfig.get(<property>)` utility Procedure. See the [VAIL Configurations](#vail-configurations) section for
  more details.
- **Nested Assembly Property**: A Configuration Property defined in an Assembly that is a resource of the current Assembly

The configuration properties available for a resource instance may be queried using the following REST call:

```
Method: GET
URL: /api/v1/resources/<resource>/<resourceId>/_configProperties
```

This returns a list of properties. Below are a few examples:

- **App Components in an App**: *assembly.<taskName\>.pattern*
- **Source configuration**: *config.<configProperty\>*
- **Source activate flag**: *active*
- **Client Theme**: *options.themeName*
- **Scheduled Procedure Interval**: *scheduledProcedures.<procedureName\>.interval*
- **Nested Assembly Configuration**: *<nested configuration property name\>*

Assembly authors may view the configuration by resource by selecting *View by Resource* in the upper right-hand corner
of the Configuration Tab. This view shows each of the configurable Assembly resources in the left-hand tree. Selecting
any resource in the tree displays all of its configurable properties and whether that property currently has a Configuration
Property that overrides it.

![Configuration By Resource](assets/img/assemblies/ConfigurationByResource.png "Configuration by Resource")

#### VAIL Configurations

An Assembly Configuration Property may list Procedures and Rules under the Usage section so that the values for a Configuration
property may be accessed in those Procedures and Rules. The Assembly Author
specifies the name of the property used when calling
`ResourceConfig.get(<property\>)` from that Rule or Procedure. This may or may not be equal to the name of the Configuration Property. 
`ResourceConfig.getOrDefault(<property\>, <default value\>)` may also be used and will return the default value if the
configuration property is not set or is null.

In the example below, the *numberOfErrorsPerHour* defined in the Assembly can be accessed in the Procedure *ManageOrganization.checkErrors*
by calling `ResourceConfig.get("maxErrors")`

![VAIL Configuration Example](assets/img/assemblies/VailConfigExample.png "VAIL Configuration Example")

#### Additional Event Handler Configurations

By default, Vantiq only provides the list of App Components in an Event Handler. An Assembly Author may choose to also expose properties of individual tasks.

This is done in the UI by clicking the star next to a task property, or programmatically by adding `assembly.<task name>.configuration.<property name>` to the Event Handler's `ars_properties.additionalConfigProps` list. When setting up the configuration property in the Assembly it will appear as an option for the App.

Here's a Missing task with the *duration* property able to be configured and the *emitOnlyOnce* not available for configuration.

![App Task Configuration](assets/img/assemblies/AppTaskConfigPane.png)

This is the Assembly Configuration pane when targeting that property.

![App Task Config in Assembly Pane](assets/img/assemblies/AppTaskConfigAssemblyPane.png)

#### Additional Source Configurations

By default, Vantiq provides a short list of known configurable properties for a Source, given the Source's type.
For example, a *REMOTE* Source will contain configurable properties such as *requestDefaults* and *pollingInterval* whereas
an *MQTT* Source includes properties such as *serverURIs* and *topics*.

An Assembly Author may choose to expose additional configuration for a Source that Vantiq could not infer. For example,
the Author may want to expose the *key* property used by default when making a query to a *REMOTE* Source. In this case,
the Author exposes *requestDefaults.query.key* as a configurable property. This allows the Consumer to provide the API key
directly as the Configuration value instead of requiring the Consumer to provide the *requestDefault* Object in the correct format.

![AdditionalSourceConfigurations](assets/img/assemblies/AdditonalSourceConfigurations.png "Additional Source Configurations")

This feature is particularly useful in the case of Connector Sources where Vantiq cannot infer *any* configuration properties for the
Source type. Connector Implementations may now define a property called *baseConfigProperties*, listing 
each configurable property for that Source type. Each Source instance of that Connector's Type will automatically have
those configurable properties.

#### Custom Processing of Assembly Configurations

It can be useful to manage certain configuration properties programmatically. For example, activating an optional Source only if the relevant credentials have been provided, or making sure that a list of configured MQTT topics conform to certain restrictions. An Assembly Author may create a custom generation procedure and arbitrarily edit the configurations before the configuration occurs.

This is done from the Assembly pane. Navigate to the Configuration tab and click the "Click To Edit" button next to the "Custom Generation Procedure" text. This will open up a template for you to use. You should *only* add code in between the BEGIN and END CUSTOM ASSEMBLY GENERATION CODE sections. The comments in that section provide instructions on how to manipulate the configurations.

![CustomAssemblyGeneration](assets/img/assemblies/CustomAssemblyGeneration.png "Custom Assembly Generation Procedure Pane")

##### Creating a Custom Generation Procedure Without the UI

If using the UI is not feasible, it is ***strongly advised*** that you use the [template available here](/docs/system/assemblies/assemblyConfigurationGenerationProc.tmpl). The procedure *must* fully generate the relevant Resource Configurations, and this template takes care of that while providing a convenient section to insert custom code.

The template can also be filled out using VAIL, with the below code provided as an example.

```
var template = getDocument("assemblies/assemblyConfigurationGenerationProc.tmpl")
var config = {"packageName": <package name>, "serviceName": <service name>, "customCode": <custom VAIL code>}
var vailCode = generateResource(templateVar, config)
UPSERT system.procedures(ruleText: vailCode)
```

#### Including Data in the Assembly

There may be cases where the Assembly Project requires a small amount of data to be included in the Assembly definition such 
that when the Assembly is installed by a Consumer, the Consumer's Namespace contains the records required for the application
to run correctly. 

The *Assembly Data* section allows the Assembly Author to define which data Types should be included in the Assembly definition
when the Assembly is published to the Catalog.

![AssemblyData](assets/img/assemblies/ConfigureAssemblyData.png "Configure assembly data")

### Manually Testing the Assembly

Assembly authors test the Assembly locally by clicking **Configure as Consumer** and switching into *consumer mode*. 

![Configure as Consumer](assets/img/assemblies/ConfigureAsConsumerBtn.png "Configure as Consumer")

This places the author
in a *consumer* mode that simulates the experiences of an Assembly consumer. Now the author is _not_ able to edit or
change the definition of the Assembly Interface or Visible Resources--most of the pane becomes read-only.
However, in *consumer mode*, the author 
can supply configuration values to the Assembly in the *Configuration* tab. 

![Configure as Consumer](assets/img/assemblies/ConfigureAsConsumer.png "Configure as Consumer")

When the author provides configuration values as a consumer and clicks **save** in the Assembly pane, the configuration values
are saved and temporarily applied to the Assembly resources for testing purposes. 

When the author toggles back into *author mode* by clicking **Edit As Author**, the configuration is removed and the 
Assembly resources revert to their un-configured behavior.

### Assembly Integration Tests

Assembly Projects may be used as the Test Resource for an Integration Test. If the selected Project is an Assembly,
the test may define a configuration for the Assembly so that when the Assembly is deployed into the testing Namespace,
it runs using the provided configuration.

![AssemblyIntegrationTest](assets/img/assemblies/AssemblyIntegrationTest.png "AssemblyIntegrationTest")

![ConfigureAssemblyIntegrationTest](assets/img/assemblies/ConfigureAssemblyIntegrationTest.png "Configure AssemblyIntegrationTest")

### Dependent Assemblies
An Assembly may depend on other Assemblies to provide functionality. For example, an Assembly that provides weather monitoring functionality may depend on another Assembly that provides mapping functionality to display weatherdata on a map. A "dependent Assembly" is an assembly that the parent Assembly requires in order to function correctly.

To mark an Assembly as a dependent Assembly, the author navigates to the *Dependent Assemblies* button in the Interface tab of the Assembly pane. The resulting popup will show a list of published and subscribed Assemblies that have been added to the current Project. If an Assembly that you expect to see is not listed, ensure that you have installed the Assembly, or if it exists in the current namespace, ensure that it has been published to a Catalog. In either case, also add the Assembly to the current Project.

All dependent Assemblies are installed alongside the parent Assembly when a Consumer installs the parent Assembly, provided that the consumer has access to the Catalog where the dependent Assembly is published.

## Consuming Assemblies

When consumers install Assemblies, the Assemblies act as black boxes to provide high level, reusable tools.
Consumers can only interact with the Assembly through the Assembly Interface and only have access to the Assembly's 
Visible Resources. All other resources present in the Assembly are considered implementation details and are hidden from the 
consumer.

When an Assembly is added to a Project in the Consumer's namespace, all the Assembly resources are added to the Project
as well, though only the resources enumerated in the *Interface* and *Visible Resources* are visible in the Project Resource Graph and Tree.

### Integrating and Composing Assemblies

Consumers can easily and seamlessly integrate Assemblies with each other and into their own Projects using the Assembly Interface.

Inbound Event Types are used to send events to an Assembly to trigger any asynchronous processing or behaviors within the Assembly.
Outbound Event Types are the events the Assembly produces. Outbound events are used to trigger behaviors in Apps, Rules, or Collaboration Types
in the consumer Namespace.

Two Assemblies can be integrated or chained together by creating a simple Rule or App that is triggered by an Outbound
Event Type from one Assembly and publishes that event to an Inbound Event Type of another Assembly. Right-clicking on the 
Event Type in the Interface tab of the Assembly pane provides
a shortcut for creating transformation Apps to convert local events into Inbound or Outbound Assembly Events.

![Transforming Events](assets/img/assemblies/TransformingEvents.png "Transforming Events")

The Procedures exposed in the Assembly Interface are another integration point for the synchronous behavior encapsulated by
Assemblies. These Procedures may be executed from any App, Client, Collaboration Type, Procedure, Rule etc.

### Configuring the Assembly

Consumers may configure Assemblies either at installation time from the Catalog or by
navigating to the *Configuration* tab on the Assembly pane.

Any configurations provided at Assembly Installation time
are applied as the Assembly resources are created. This guarantees that the Assembly is always running in its 
configured state right from its creation. 

![Configure as Consumer](assets/img/assemblies/AssemblyInstallProperties.png "Configure as Consumer at install")

Consumers may change or update the configurations at any time in the *Configuration* tab on the Assembly pane. Updating
the configuration values and clicking **Save** in the Assembly pane applies the configuration values to all configured
resources in the Assembly. 

![Configure as Consumer](assets/img/assemblies/ConfiguredAssembly.png "Configure as Consumer")

Consumers must provide configuration values for all configuration properties marked as *required*. For any optional 
configuration property, if the consumer does not provide a configuration value, the default is applied.

To create an Assembly configuration via REST use the command:

```
Method: POST
URL: /api/v1/resources/assemblyconfigs
Body: {
    "name": <name of the assembly>,
    "assembly": <name of the assembly>,
    "configuration": <map from configuration property name to value>
}
```

For example, configure the assembly as shown in the screenshot above:

```
Method: POST
URL: /api/v1/resources/assemblyconfigs
Body: {
    "name": "WeatherEmergencyProject",
    "assembly": "WeatherEmergencyProject",
    "configuration": {
        "clientTheme": null,
        "useBuiltInSource": false,
        "detectDangerousWeather": "isDangerousAirQuality"
    }
}
```

#### Configuring App Components

One of the most powerful capabilities of Assemblies is allowing consumers to configure which App Component should be 
used by Apps within the Assembly.

When replacing one App Component with another through Assembly Configuration, the replacing Component must have the exact 
same configuration properties and downstream events as the original component. To guarantee that the replacing Component 
has the correct definition, you can use the shortcut provided in the Assembly Pane. The
**Create Component Stub** button (represented as a lightning icon) is present next to each Configuration Property of type *App Component*.

![Create Component Stub](assets/img/assemblies/CreateComponentStubBtn.png "Create Component Stub")

For example, in the WeatherEmergencyProject defined in the Assembly Tutorial, the default App Component the *DetectWeatherEmergency*
App uses contains two downstream events: *EvacuationRequired* and *WarnResidents*. If a consumer wanted to swap out the App
Component through Assembly configuration, the supplied App Component must also contain two downstream events called *EvacuationRequired* and *WarnResidents*.

Below is a screenshot showing the original App Component on the left-hand side and the Component stub generated by clicking
on the lightning icon on the right-hand side.

![Create New Component Stub](assets/img/assemblies/CreateNewComponent.png "Create New Component Stub")

Notice that the Component stub contains an empty Transformation Task by default as well as all the downstream events
defined on the original default App Component. The consumer then uses this as a starting place to add more tasks to the App
Component definition to accomplish the desired behavior.

In this case, the Consumer defines an App Component to detect whether the air quality is at dangerous levels.

![Air Quality Component](assets/img/assemblies/isDangerousAirQualityComponent.png "Air Quality Component")




