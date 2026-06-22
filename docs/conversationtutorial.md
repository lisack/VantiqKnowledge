# Conversation Widget Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningVis](../assets/img/conversation/DemoWidget.png "Using the Conversation Widget")

## Objective
To gain familiarity with the Conversation widget to add chat-like generative AI features to Vantiq Clients.

## Purpose
* Create a Client with a Conversation Widget
* Configure a generative AI LLM to interact with one of many supported Large Language Models
* Build a Service that connects the Conversation widget running on the Android or iOS Vantiq app to the LLM

## Tutorial Overview

In a Vantiq Service you can create an Event Handler with a SubmitPrompt task that will send a "prompt" to an LLM and return a response. This can be done programmatically, but it is also useful to allow a user to do this directly through a Client running in a mobile device. The Conversation Widget (which is similar in appearance to the Chat Widget) is provided to facilitate this process. The steps below describe how to make this work.

In order to demonstrate this process, we first need to create a Service that will contain the SubmitPrompt task. You should be generally familiar with Vantiq Services and how they work before proceeding.

All sections assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the [Introductory Tutorial](tutorial.md) before starting this tutorial.

Large Language Models (LLMs) and how they are used in Vantiq are described in the [LLM Reference Guide](../llms.md). In Modelo you  will also find a "Contribution" called "PumpAITroubleshooting" which makes use of the Conversation Widget. Use the _Projects -> Import_ menu  with Import Type _Contributions_ and select _PumpAITroubleshooting_ to import it.

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item.  Just select _Tutorials_ for Import Type, then select _Conversation_ from the second drop-down, then click **Import**.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Create a Generative LLM

We first establish an LLM to respond to the prompts.

Use Modelo's **Add** button to select **LLM** and click the **New LLM** button. A pane will open where you can describe the LLM - here's an example:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateLLM](../assets/img/conversation/NewLLM.png "Create an LLM")

Note that if the LLM you choose requires an API Key you will need to create or point to a Secret that contains it.

## 2: Create an Empty Client

Use the **Add** button to select **Client** and click the **New Client** button. Create a Client called _MyClient_ using the _MobileEmpty_ template. You may leave it empty for now - we will come back later to add the Conversation Widget.

## 3. Create a Type

Use the **Add** button to select **Type** and click the **New Type** button. Call the Type _MyType_ and give it package name of `com.vantiq`. Click "Create" and add a single String property called "myEntityId" - this will contain the "entity ID" associated with a collaboration. Save the Type.

## 4. Create a Service

Use the **Add** button to select **Service** and click the **New Service** button. Call the Service _MyService_ and give it package name of `com.vantiq`.

## 5. Define the Entity Role

In _MyService_, select the **Implement** tab and select the _State_ section. Open the **Collaboration State Properties** section and click to edit the "Entity Roles". Add a reference to the myEntityId property of the "com.vantiq.MyType" you created earlier:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![EntityRoles](../assets/img/conversation/EntityRoles.png "Set Entity Role")

Click "OK" and save the Service.

## 6: Create an Event Handler to Launch a Client on a Mobile Device

In order to use a Client with a Service, we must run it within a mobile device and establish a "Collaboration". For the purposes of this example we will create an Event Handler to do that for us.

First create the Interface. In _MyService_, select the **Interface** tab. In the **Inbound** section, click the **plus** icon which should open a page that you must fill in to define the interface. Fill it in like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![LaunchInterface](../assets/img/conversation/LaunchInterface.png "Launch Interface")

Save the Service. 

In _MyService_, select the **Implement** tab. Open the **Unbound Interfaces** section and find the "Launch" interface, right-click it to reveal a context menu and select **Add Public Visual Event Handler**.  Use the visual editor to create an Event Handler like this:


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![LaunchEH](../assets/img/conversation/LaunchEH.png "Launch Event Handler")

Drag in a _LogStream_ task from the **Actions** palette section, an _EstablishCollaboration_ task from the **Collaboration** section and a _Notify_ task from the **Mobile** palette section. 

The _EstablishCollaboration_ task will create a separate Event Handler Collaboration for each separate entity which will be used later in the "Prompt" Event Handler to coordinate LLM prompts and responses. Configure it like this:

* _behavior_ - Establish existing collaboration or create new collaboration
* _entityId_ - event.myEntityId
* _roleName_ - myEntityId

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![LaunchEstCollab](../assets/img/conversation/LaunchEstCollab.png "Configure the Establish Collaboration Task")

The _Notify_ task sends a notification to the mobile app that will run the "MyClient" Client. You must configure the _Notify_ task like this:

* _title_ - "Test Conversation Widget"
* _body_ - "Support sending questions to an LLM"
* _users_ - [Context.username()] (The 'type' must be "Expression")
* _clientName_ - MyClient

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![NotifyTask](../assets/img/conversation/NotifyConfig.png "Configure the Notify Task")

Save the Service.


## 7: Create an Outbound Event

Select the **Interface tab**. Click the **plus** icon next to the **Outbound** section and create a new outbound event. This event will contain the responses from the LLM. Set the _Name_ field to "Response" and save the Service.


## 8: Create an Event Handler to Send a Prompt to the LLM

In _MyService_ select the **Implement** tab. In the **Event Handlers** section, click the **plus** icon next to **Public** - this should open a menu containing **Add Public Visual Event Handler**. Click the menu and create an Event Handler called "Prompt". Use the visual editor to create an Event Handler like this:


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![PromptEH](../assets/img/conversation/PromptEH.png "Prompt Event Handler")

Drag in an _EstablishCollaboration_ task from the **Collaboration** palette section, a _SubmitPrompt_ task from the **GenAI** section, a _Transformation_ task from the **Modifiers** section and a _PublishToService_ task from the **Actions** section.

This Event Handler will create a Collaboration, send the prompt to an LLM, add the collaborationId to the results and then publish them.

Configure the _EstablishCollaboration_ task like this:

* _behavior_ - Establish existing collaboration or create new collaboration
* _entityId_ - event.myEntityId
* _roleName_ - myEntityId

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![EstCollab](../assets/img/conversation/EstCollab.png "Configure the EstablishCollaboration Task")


Configure the _SubmitPrompt_ task like this:

* _llm_ - MyLLM
* _prompt_ - event.prompt
* _useConversation_ - checked

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SubmitPromptTask](../assets/img/conversation/SubmitPrompt.png "Configure the SubmitPrompt Task")

Configure the _Transformation_ task like this:

* _transformation_ - {"collaborationId":{"type":"expression","expression":"event.collaborationId"}}
* _transformInPlace_ - Checked

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Transform](../assets/img/conversation/Transform.png "Configure the Transformation Task")


Configure the _PublishToService_ task like this:

* _service_ - com.vantiq.MyService
* _eventTypeName_ - Response

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![PubToServ](../assets/img/conversation/PubToServ.png "Configure the PublishToService Task")

Save the Service.


## 9: Add a Data Stream for the Service to the Client

Now that the Service infrastructure is complete we can edit the _MyClient_ Client.

Select the **Edit** tab and right-click on the **Data Streams** section. Select **Add 'On Service Event'** and create a Data Stream like this:

* Data Stream Name - AIResponse
* Service and Event - com.vantiq.MyService and Response


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateDS](../assets/img/conversation/CreateDS.png "Create a DataStream")

Click **Save** to save the Data Stream.


## 10: Add the Conversation Widget

Click the **Add** tab. At the bottom of the **Data Display** section of the palette you will find the _Conversation_ Widget. Drag this palette item into the body of the Client. (Don't worry about position or size - we'll deal with that later.)

Select the widget so its property sheet pops up. In the **Specific** section set:


* Title - "Test Conversation Widget"
* Service - com.vantiq.MyService
* Inbound Event - Prompt

In the **Data** section, set the _Data Stream_ to "AIResponse".

> There are 2 ways in which the Conversation Widget can interact with an LLM. In this tutorial we do it by specifying a Service and Inbound Event as a way to make the request and a DataStream that listens for a Service Outbound Event to get the responses. There is a different approach that works as well;  instead you can specify a Public [GenAI Procedure](../services.md#genai-procedures) which will accept a request and return the response in a single step. If you use that approach no DataStream is required.

For this Client, we would like the Conversation Widget to fill the entire page; open the Property sheet for the "Start" Page and set the _Layout Type_ to _Single_.

Save the Client.

## 11: Testing

In the _MyService pane_, select the **Interface** tab. In the **Inbound** section, select _Launch_:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Launch](../assets/img/conversation/Launch.png "Publish an Event to start a Collaboration")

Open the **Publish** section and fill in some value (e.g. "AAA") for the "myEntityId" property which will uniquely identify the collaboration that will be created. (Using different values will simulate a real situation where each user has their own collaboration and the output responses are kept separate). Now click the **Publish** button. This will just trigger the Launch event to send a notification to the Inbox of your mobile device, telling it to launch the _MyClient_ Client.

Use the Vantiq mobile app to login to the same server, username and namespace where you built the Service and Client. You should find this notification in your Inbox:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Inbox](../assets/img/conversation/Inbox.png "Mobile Phone Inbox")

Tap the item in the Inbox to launch the Client. You can now use the Conversation Widget to send prompts to the LLM and see the response. Since we checked the _useConversation_ setting for the SubmitPrompt task, prompts can refer to earlier parts of the conversation.  For example, the first prompt below shows "_What is the capital of California?_" along with the answer.  If you send a second prompt of "_What about Nevada?_", the LLM should respond with the capital of Nevada.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DemoWidget](../assets/img/conversation/DemoWidget.png "Using the Conversation Widget")

## Conclusion
Developers who have completed this tutorial should now feel comfortable building functionality in Vantiq in the following areas:

* Creating a Client containing a Conversation Widget
* Creating a Service to add Event Handlers to interact with the Vantiq mobile apps running a Client
* Creating and linking Data Streams to send and receive data from a Service and its Event Handlers