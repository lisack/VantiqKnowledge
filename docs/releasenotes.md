# 1.44 Release Notes

> The Visual Analytics (VA) features of the Vanitq Platform have been removed.  This includes support for the *images*, *videos*, and *tensorflows* resources, for Vision Script, and for all features that were specific to these resources.

## Server Enhancements

## UI Enhancements

An Assembly may depend on other Assemblies to provide its functionality. An assembly that is dependent on other assemblies can mark those assemblies.  Then those dependent assemblies will be automatically subscribed to when the assembly is subscribed to. See [Dependent Assemblies](assemblies.md#dependent-assemblies).


# 1.43 Release Notes

## Server Enhancements

### GenAI Agents

* [Agents](agents.md) are now more formally defined and implement a standard framework based on the [A2A](https://a2a-protocol.org/latest/specification/) protocol.
* [Discovering and describing](agents.md#discovering-and-describing-agents) agents can now be done in a more structured manner.
* Support for building [Plan and Execute](agents.md#planning-agents) agents has been added.
* There are new built-in procedures related to both [Agents](rules.md#agent) and [A2A](rules.md#a2a).

### AI Support

* The GenAI Tool component now supports [MCP tools](./llms.md#mcp-tools) (Model Context Protocol tools) and allows overriding tool parameter values through the [`toolParameterOverride`](./llms.md#tool-parameter-override) runtime configuration.
* Semantic Indexes can now have their contents accessed remotely. This allows users to upload a Semantic Index's contents once, then use it across multiple namespaces. See [Remote Semantic Indexes](semanticsearch.md#remote-semantic-indexes) for more information.
* Semantic Indexes are now available in the catalog. They have the same functionality as Remote Semantic Indexes. [See here for more details](broker.md#semantic-index-catalog).

### GenAI Builder

* The GuardrailsAIServer GenAI Component has been removed due to issues with underlying library.

### VAIL

Added/updated the following built-in services:

* [`io.vantiq.text.Template`](rules.md#template) -- added support for "repeat" blocks in a template. This allows a section of a template to be applied multiple times when referencing a List input property.  

### Services

* The [Collaboration Management Procedure](servicestatemgmt.md#procedures) `ActiveCollabsGetCached` is now public so that it can be called by Modelo.

### Sources

* Added support for the [Open Inference Protocol](./openinference.md) via [REMOTE Sources](./sources/remote.md#open-inference-protocol). See the related [Open Inference Tutorial](./tutorials/openinference.md) for usage examples. 

### Semantic Indexes

* Added support for user-partitioned semantic indexes. With a partitioned index each user will have a separate view of the entries and underlying point data.

### Other

* Added the ability to generate [JSON Schema](https://json-schema.org/) for any Vantiq [Type](./resourceguide.md#types).
* Credentials stored in nodes are no longer included in selects. This is to avoid sharing those credentials with everyone who can use nodes.

## UI Enhancements

### GenAI Builder

* There is now a "multiple selection" mode in the GenAI Builder which allows you to select a subset of the current graph and then operate on it in various ways. Select items with Shift-Click to enter multiple selection mode. The supported operations are:
    * "Delete" all selected items
    * "Cut" or "Copy" all selected items to a local clipboard, and then "Paste" them back into the graph
    * "Enclose" all the selected items within a "Conversation", "Optional", "Loop", "Map" or "Repeat" task
    * "Create" a new GenAI Component from the selected items
* The Resources component [PromptFromMessages](genaibuilder.md#promptfrommessages) has been added.

### Client Builder

* You may now temporarily put your running Client into a "modal" state using the [client.blockInput()](cbref.md#blockinput) and [client.blockInputEx()](cbref.md#blockinputex) methods. You can control the messages the user sees and the "spinner" icon which will be displayed.

### Service Builder
* Semantic Indexes may now be published to and subscribed from Catalogs.
* GenAI Agent Services (Agents) may now be created from the New Service dialog or declared from the Service Builder's **Interface** tab. Agents may specify an optional version and tag(s) from the **General** section of the **Interface** tab. Public Procedures in Agents may be specified as Agent skills. Skills may specify an optional human-readable name, tag(s) and example(s). For more information, please see the [GenAI Agent Building Guide](agents.md).
* Service state accessor Procedures can now easily be managed using the **Generate State/Entity Procedures** section of the **Implement** tab. Use the tree structure to add or delete these Procedures for Global and Partitioned State Types and for Entity Roles.
* Minor changes such as zooming or moving nodes within the App or GenAI Builder will no longer cause the Service's **Save** button to enable.
* Embedded GenAI flow may be tested using the new Execute button similar to testing a service procedure or GenAI procedure

### LLM Playground
* An existing prompt can be edited using the template editor if the prompt was created from a template.
* Allow saving the Document template within the template editor.

### Modelo

* There are now shortcut keys to "close the current pane" and "close all panes" when using Flex Grid Layout

<table>
<tr>
<th> Windows Keys</th>
<th> Mac Keys</th>
<th>Action</th>
<th>Equivalent To</th>
</tr>

<tr>
<td> Ctrl-K</td>
<td> Cmd-K</td>
<td>Close the current pane/tab</td>
<td>Clicking the "X" in the toolbar</td>
</tr>

<tr>
<td> Ctrl-Shift-K</td>
<td> Cmd-Shift-K</td>
<td>Close all open panes/tabs</td>
<td>Selecting "Close all Panes" under the "gear" icon menu</td>
</tr>

</table>

* An advance filter is added to some tables with search capability. The complete list of affected panes are:
    * Compilation Errors
    * Deployments
    * Documents
    * Environments
    * Groups
    * Namespaces
    * Nodes
    * Choose Document Popup Dialog
    * Index entries table in Semantic Index Detail Pane.

  
# 1.42 Release Notes

## Server Enhancements

### VAIL

* Invocation of private procedures from procedures of differing state access modifiers is now supported.  This may require the use of an explicit [partition key](rules.md#partitioned-execution).
* The [Conversation Memory](rules.md#ConversationMemory) service emits events based on conversation state changes.  It also supports per-conversation properties.
* The default [execution time](workloadmanagement.md#executiontime-quota) quota value has been changed from *2 minutes* to *2 hours*.


### Services

* The [Collaboration Management Procedures](servicestatemgmt.md#procedures) have been updated/simplified.  If your service code invoked these directly, then you may need to update it based on these changes.  Please see the referenced documentation for details.
* The service builder now supports generation of [Entity Roles Procedures](servicestatemgmt.md#entity-role-procedures) for collaboration management services.
* [Agents](agents.md) have the ability to communicate with users either as part of an active [conversation](agents.md#direct-communication) or via [notifications](agents.md#notification).

### GenAI Builder

* The AI Guardrail components [GuardrailsAI](genaibuilder.md#guardrailsai), [GuardrailsAIServer](genaibuilder.md#guardrailsaiserver), and [NeMoGuardrails](genaibuilder.md#nemoguardrails) have been added.

### Assemblies

* Assembly configurations may now be customized using the *customGenerationProcedure* field. [See here for more details](assemblies.md#custom-processing-of-assembly-configurations).
* GenAI Procedures in visible Services are now also visible.
* GenAI Components may now be made visible in Assemblies.

### Other

* Semantic Indexes no longer return their entire entries list by default on SELECTs. You must now either explicitly include the "entries" property or do a SELECT on _ArsSemanticIndexEntry_ with the qual `{"indexName": <semantic index name>}`. [See here for more information on Semantic Index Entries](resourceguide.md#semantic-index-entries).
* Natural Language Processing support has been deprecated.  The functionality is now available as an assembly, `com.vantiq.nlp.NaturalLanguageProcessing` in the component public catalog.  Existing NLP collaborations and apps will continue to work.
* The Track Activity Pattern's *destination* and *waypoint* fields can now be specified using VAIL.
* You can now retrieve the contents of entries using [io.vantiq.ai.SemanticSearch.retrieveChunks()](rules.md#semanticsearch).

## UI Enhancements

### General
* Added a Public Catalog discovery UI to discover Client Components and themes, App Components, and GenAI Components.
    * Users may install Client Components and themes. See the Client Builder section below for more details.
    * Users may install publicly available App Components using the **Discover** button found next to the Visual Event Handler Components section title.
    * Users may install publicly available GenAI Components using the **Discover** button found next to the GenAI Builder's User Defined section title.
    * These **Discover** buttons will only appear if there are the corresponding resources available in any Public Catalog available to the user's current Namespace.
* Group resources by package in the resource explorer.
* Add search functionality to many resource pickers.
* Add deployment order support to Project partitions.  Partitions are deployed in ascending order. Partitions with the same deployOrder value are deployed simultaneously.
* Document uploads now show a floating progress dialog and don't suspend use of the IDE.
* During Namespace changes or browser refreshes, there is more text feedback in the IDE Navigation Bar.
* Assemblies may now be converted back into Projects using the **Projects>Convert to Project** menu item.
* The Threshold task in Visual Event Handlers now has AI Configuration Assistant support.
* When testing Procedures you now have the option of executing them in "Streaming" mode.
* The "Show Documents" list now highlights those Documents which belong to the current Project.
* There is now a spell checker running when editing text Documents.

### Client Builder
* Client theming capabilities have been expanded:
    * Client widgets have more consistent application of theming properties.
    * The number of theme properties has been greatly expanded.
    * There are two built-in themes, Light and Dark, with Light being the default. Users may add additional themes from Public Catalogs (see below) or save their own themes.
    * Previously created Clients will usually be assigned a Custom Theme unless their theme properties happen to match either the Light or Dark themes. Users may easily switch to the Light or Dark theme to update older Clients.
	* Previously created Clients may show some minor changes in appearance on load, both because of widget theme changes and changes to the meaning of "default" style.
	* There is a shortcut Theme button in the Client Builder toolbar to take the user directly to the Theme tab of the Client Properties dialog.
* Added a Public Catalog discovery UI to discover Client Components and themes.
	* Users may install publicly available Client Components using the **Discover** button found next to the Client Builder's Components section title. Currently, there is only one Component, Statistics. See below for details.
	* Users may install publicly available Client themes using the **Discover** button found next to the theme selection pull-down in the Client Properties dialog.
* There have been many enhancements to the Conversation Widget:
    * Support for both "Gen AI" and "Standard" Procedures
    * Support for "streaming" responses when using a Procedure
    * There are now read/write "conversationId" and "conversationName" properties that can be used programmatically at runtime to change which particular conversation will appear. There is also a new method _client.setCollaborationContext()_ which can be used to change which Collaboration is in use.
    * Support for the new "Callback" feature that allows followup questions to be added to the Conversation at runtime by external callers
    * Support for an "On Filter Conversation Message" event that is fired when each new message arrives into the Conversation. The event handler can modify the incoming message or hide it altogether.
    * Support for adding "Action Buttons" at the bottom of the conversation flow as well as buttons associated with each user or system message. The new "On Action Button" event is fired when the buttons are clicked. The user and system buttons can either appear when the mouse hovers over the message (the default) or "inline" with the message.
    * Support for control over which "message types" will be shown (By default "human", "ai" and "chat" types are shown and "system", "function" and "tool" types are hidden.)
    * More control over the styling of the widget.
* Added a Segmented widget in the Data Display section. It behaves much like the [iOS Segmented Control](https://developer.apple.com/design/human-interface-guidelines/segmented-controls).
* Added a Statistics Client Component which has title, value, and delta fields, all programmatically set. Users may install this Client Component using the **Discover** button found next to the Components section title.
* The Calendar widget now supports _On Select_ events.
* There have been significant enhancements to the "Context Menu"; you now have greater control over the icon, color and position.
* The InputString, InputInteger, InputReal and InputDecimal widgets now support an "onEnterKey" event.
* The widget context menu in the Client Builder now allows you to "enclose" the widget in various types of Layout widgets.


# 1.41 Release Notes

## Server Enhancements

### AI Support

* LLMs now support default system prompts. When provided, these will be placed before any other messages or conversations. [See here](resourceguide.md#llms) for more details.
* Semantic Index content ingestion now supports the ability to specify a GenAI Flow procedure to process the content as the default ingest mechanism. See [Content Ingestion Flows](genaibuilder.md#content-ingestion-flows) for more information. Further, note that complex content ingestion is no longer limited by procedure execution time-outs when performed via the Semantic Index Service.
* The [Chat Message](rules.md#chatmessage) builders now support `image_url` prompts containing `ResourceReference` values.  These are used by "multi-modal" LLMs.

### Sources

* Added VIDEO source type.  This source can fetch images from online cameras, returning them for processing in the Vantiq system.  See [Video Source Integration](sources/video.md) for details.

### Other

* Nodes now pay attention to the URI's path when targeting the local server. This may cause issues if you have nodes that have extraneous paths, e.g. `https://dev.vantiq.com/ui/ide/index.html` instead of `https://dev.vantiq.com`. Using the URI of the "self" node will fix any issues this causes.
* New Organizations can now be automatically provisioned with resources. This is only relevant on installations where you have system admin permissions. [See here](namespaces.md#creating-resources-for-new-organizations) for more details.
* The [`classOf()`](rules.md#miscellaneous-procedures) procedure is available for in-depth debugging of VAIL code.

## UI Enhancements

### General

* AI Client Assistant is a new feature added to Client Builder for generating client pages using an LLM. See the [Client Builder User’s Guide](cbuser.md#ai-client-assistant) for more information.

* LLM playground now supports exporting conversation to a JSON file and loading conversation from an exported file.

### GenAI Builder

* The GenAI Builder now enforces strict typing between connected tasks.  For each edge in the GenAI Flow, it must be possible to assign the output type of a parent task to the input type of the child(ren).  See [GenAI Task Typing](genaibuilder.md#task-typing) for more details.

* The AI Primitive components [Loop](genaibuilder.md#loop), [Map](genaibuilder.md#map), [Procedure](genaibuilder.md#procedure), and [Transform](genaibuilder.md#transform) have been added.

* The AI Pattern component [ReduceDocuments](genaibuilder.md#reducedocuments) was added.

* GenAI Flows may now access [per-flow memory](genaibuilder.md#memory-and-Conversations) as part of their implementation.

* The [LLM](genaibuilder.md#llm) component can now specify a schema type when expecting JSON output.

* Support for [retrieval with contextual compression](https://python.langchain.com/docs/how_to/contextual_compression/) (which includes "re-ranking") has been added via the new resource component [SemanticIndexWithCompression](genaibuilder.md#semanticindexwithcompression) and several [document compressors](genaibuilder.md#document-compressors).

# 1.40 Release Notes

## Server Enhancements

### VAIL

* The [return type](rules.md#return-type) of a procedure can now include the [sequence](rules.md#sequences) modifier.  Doing this allows callers to receive the procedure results as they are produced (a process known as "streaming"). 

### AI Support

* External Semantic Indexes are a new feature that allows you to create a Semantic Index that is backed by an external data source. This allows you to use the Vantiq Semantic Search capabilities with data that is not stored in Vantiq. See the [External Semantic Indexes](semanticsearch.md#external-semantic-indexes) documentation for more information.
* The [Chat Message](rules.md#chatmessage) builders have been expanded to support prompts used by "multi-modal" LLMs.
* [Semantic search](rules.md#semanticsearch) now handles Qdrant's filter language.

### Activity Patterns

* Added the [Branch](apps.md#branch) activity pattern.
* Added the *reset* event stream to the [Dwell](apps.md#dwell) activity pattern.
* Added the *reset* event stream to the [Threshold](apps.md#threshold) activity pattern.
* Added the *timeout* event stream to the [Join](apps.md#join) activity pattern.
* Added the *triggeringEvent* property to the event produced by all *onError* event streams.

## UI Enhancements

### General

* You can now dump and restore a Semantic Index from within Modelo from the list shown using "Administer / Advanced / Semantic Indexes"
* When editing a Semantic Index you can now create multiple index entries at the same time by selecting multiple files.
* Certain DataStreams in the Client Builder now support "Event Filtering". You may specify an object with one or more fields, and only those event with matching values will be delivered. (This only applies to these Data Stream types: "On Data Changed", "On Publish", "On Source", "On Resource Event" and "On Service Event").
* You can now execute Procedures which support "streamed output" directly from JavaScript, which allows you to process the output a chunk at a time rather than all at once. (This is useful when a VAIL Procedure returns a ["sequence"](rules.md#sequences).) There is a new method defined on the [Client](cbuser.md#client-builder-users-guide) called [client.executeStreamed()](cbref.md#executestreamed).
* The [Conversation](cbref.md#conversation) Widget can now operate using Service Events or a GenAI Procedure. Streaming output is supported, and the Widget will participate in the default Conversation if the Collaboration has one. The [Conversation Tutorial](tutorials/conversationtutorial.md) has been updated to reflect the changes.
* Most of the major resource editors  (such as Services, Clients, LLMs, Semantic Indexes, GenAI Builder, and Sources) will now show a "Discard" button which allows you to abandon your current changes and revert to the last saved version of the resource. (Look for "Discard" next to the "Save" button.)
* The "Select a Document" dialog (which is shown in many places in Modelo) now allows you to create or upload a new Document as well.
* The "Launch" menu in the Client Builder can now be used to launch a Client within the context of an active Collaboration. This can be useful during development since it allows you to test Clients in a browser which would normally be triggered with a Notify task and need to be run in a mobile app.


### GenAI Builder

* The [GenAI Builder](genaibuilder.md) now supports [tracing](genaibuilder.md#genai-flow-tracing) of GenAI Flows. This means that if the tool is open when data passes through the flow you will see a "count" badge appear and be incremented every time data is output from the task. There is a related viewer which shows the output from each task.
* Support for configuring [GenAI Flow Auditing](genaibuilder.md##genai-flow-task-auditing) has been added to the GenAI Builder.
* New [Gen AI Components](genaibuilder.md#vantiq-provided-genai-components) have been added to support [Content Ingestion](genaibuilder.md#content-ingestion-flows).
* It is now possible to generate an [Audit](resourceguide.md#audit) record for each execution of selected tasks in a GenAI Flow.
* There are now 2 new "shortcuts" that can be used to open the [GenAI Builder](genaibuilder.md) from inside a Service Event Handler. You can right-click on the "GenAIFlow" task and select the "Open GenAI Flow" item in the context menu or select the task and click the "GenAi Flow" / "Click to Edit" button in the slide-out pane.
* [Fallback](genaibuilder.md#fallback) and [Tool](genaibuilder.md#tool) GenAI Components added.
* GenAI Flows support [streaming](genaibuilder.md#streaming-results) when declared to return a [sequence](rules.md#sequences).

# 1.39 Release Notes

## Server Enhancements

### VAIL

* Added `Any` as a [VAIL Standard Type](rules.md#standard-types). `Any` can be used as part of the signature of a procedure, both as the type of a parameter and as the return type.
* You can now use built-ins like _toInteger()_ or _toString()_ directly on String, Integer, and Real constants.
* Added a new _io.vantiq.text.Strings.format(str, args)_ [utility procedure](rules.md#string-utility-procedures) that returns a formatted String like the existing built-in _format()_, but accepts an arbitrary number of substitution parameters (_format()_ is limited to 15).
* Added two `DateTime` [built-in procedures](rules.md#datetime-procedures): `addMonth()` and `addYear()`. These procedures return a date in the past or future on the same day as the current date.
* Added a `rethrow(exception)` [utility procedure](rules.md#general-utility-procedures) to handle rethrowing a caught exception, which avoids double formatting error messages.
* Added `Utils.deepMerge(target, source)` which recursively merges the source Object into the target. See [the Utils service](rules.md#utils).

### Large Language Model/AI Support

* Added _runtimeConfig_ argument to [SubmitPrompt](apps.md#submit-prompt) and [AnswerQuestion](apps.md#answer-question) ActivityPatterns, and [LLM](rules.md#llm) `submitPrompt` and [SemanticSearch](rules.md#semanticsearch) `answerQuestion` built-in services. This property allows specifying a runtime configuration that applies to the request only.
* Added _functionAuthorizer_ argument to [SubmitPrompt](apps.md#submit-prompt) ActivityPattern and [LLM](rules.md#llm) `submitPrompt` built-in services, providing control over automatic LLM functions execution.
* Added support for [Azure OpenAI](llms.md#azure) and [Nvidia NIM](llms.md#nvidia-nim).

### Sources

* Sources are no longer permanently deactivated when they fail to connect. Instead of setting _active_ to false, the new property _isUnavailable_ is set to `true`. Whenever the source is updated or has a resource configuration change, it will try connecting again and update _isUnavailable_ appropriately.

### Other

* Duplicating Documents over WebSocket sessions is now supported.
* The new [Org User profile](resourceguide.md#possible-system-permission-levels) will give user-level permissions in any namespace where the user has no explicit permissions.
* [Bootstrapping](config.md#bootstrapping) a node is now performed within an Organization.
* Deploying a K8sInstallation to the `self` cluster can only be performed by the organization admin.  See [Use of the `self` Cluster](extlifecycle.md#vantiq-self-cluster) for details.
* It is now possible to apply a "filter" to dynamic subscriptions established via [WebSockets](api.md#filtering-subscribed-events).

## UI Enhancements

* The [GenAI Builder](genaibuilder.md) is a major new tool that can be used to visually create a "GenAI Flow" based on [LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction/) and the [LangChain Expression Language (LCEL)](https://python.langchain.com/v0.1/docs/expression_language/). These flows can be invoked through Services and Event Handlers in various ways. For details refer to the [GenAI Builder Guide](genaibuilder.md) and the related [GenAI Builder tutorial](tutorials/genaibuilder.md).
* The [LLM Playground](llms.md#llm-playground) is a new tool for verifying LLM connections and experimenting with different large language models and their settings. It is also a useful tool for creating and refining prompts (a task often referred to as Prompt Engineering).
* Added a new Client widget, [Conversation](cbref.md#conversation), which provides a chat-like UI for interacting with LLMs. See the [Conversation Tutorial](tutorials/conversationtutorial.md) for an example of how to use the Conversation widget.
* The Visual Event Handler (AKA App Builder) UI has a new way to trigger the start of the Event Handler. By selecting any EventStream task, the resulting properties slideout shows a new section, **Trigger EventStream**. Expand that section to reveal a JSON editor and its **Trigger** button. Clicking the **Trigger** button will send the JSON object to the EventStream task to start the Event Handler.
* Configuration properties that reference a Type in the App Builder now show an 'eye' icon to open the Type definition and add that Type to the enclosing Project.
* Client DataTable, ListViewer, and chart (e.g., Line) widgets now respect their Data Stream's _Group By_ property.
* Client DynamicMapViewer widget now supports a new center type of "Bounds" which will center the map on the bounds of all markers.
* Standard Types may now be renamed and any data associated with the Type is moved to the new Type name. This feature is accessed by using the **Duplicate Type** context menu item for a standard Type in the Project Contents tree, then checking the **Rename Type** checkbox.
* Added a new Client function, [logout](cbref.md#logout), which allows Clients to force a relogin for mobile apps.
* Clients can now be added to a Group, which makes it possible to confine access to a specific list of Users.
* When multiple tasks are selected using the "Shift" key in the Visual Event Handler they will all move together if dragged.
* Deployment tool enhancements:
  * Provides new action button to terminate an unfinished deployment or un-deployment.
  * Provides new option while copying/moving resources between partitions to include/exclude related resources,
  * Partition constraints are now editable.
  * Partitions can be excluded from update partitions (to avoid deleted partitions from coming back during update).
  

### GenAI Enhancements

* To assist in the development of GenAI Applications, a new [GenAI Builder](genaibuilder.md) has been added.
* Services support GenAI Procedures, which are created and can be edited when the user drops a _GenAIFlow_ task in a Visual Event Handler graph.

# 1.38 Release Notes

## Server Enhancements

### REST API

* Updates, Inserts, and Patches now can limit what properties they return.

### Types

* Added a [rename](resourceguide.md#rename) operation to support changing the name of a type without the need to copy its contents.  Note that renaming a type will *not* automatically rename all references to that type (these must be updated manually).

### Services

* The collaboration state management properties (`writeFrequency`, `entityRoles`, `collaboratorRoles`, and `conversationNames`) are now defined once for a given service, instead of separately for each handler.  For existing services, the property values for each service will be "rolled up" from the existing handlers.  The same thing will occur when importing a service exported from 1.37 into a clean 1.38 namespace.  Once the conversion is complete, any subsequent updates via the event handler definitions will be ignored.
* The procedures used to manage collaboration state are now generated once for the service, instead of once per event handler. Existing services will have their procedures regenerated upon update. Note that this will change the procedure names (they no longer have their handler name appended) and may result in compilation errors that need to be resolved manually.
* Scheduled procedures can now have parameters as long as none are required. Single partition procedures still cannot be scheduled, as their partition key parameter is implicitly required. 

#### Event Handlers

* Individual task properties can now be configured in Assemblies. [See here](assemblies.md#additional-event-handler-configurations) for more detail.
* Generated procedures for event handlers with multiple inbound events are now consistently named. They would previously change depending on the order events were attached to the handler, leading to inconsistencies on import. Note that some generated procedures will be renamed when the handler is next regenerated.

#### Activity Patterns

* added _rejected_ event to [Filter AP](apps.md#filter) for events that do not match the filter
* added _restart_ event to [Missing AP](apps.md#missing) when incoming events restart
* Renamed the `Collaboration Status` activity pattern to be [Close Collaboration](apps.md#close-collaboration) to better reflect what the pattern actually does.

### User Invitations

* The expiration date of user invites may now be customized. [See here](resourceguide.md#authorize-user) for more details.

### User Documentation

* A [Semantic Search guide](semanticsearch.md) has been added.
* The [Deployment Tutorial](tutorials/deploymenttutorial.md) has been updated to use services.

### VAIL

* Procedure parameters may no longer be both required and have a default value. This will cause compilation errors when regenerating procedures with parameters marked as both.
* The `split()` procedure for strings now follows the usage of Java. This mostly affects instances where there are non-positive limits.
* The procedure [`Test.sendMockSourceEvent`](rules.md#test) has replaced `createSourceEvent`.  It has the same parameters and behavior as createSourceEvent() did.

Added the following built-in services:

* [`io.vantiq.StorageManager`](rules.md#storagemanager) -- start, commit and abort database transactions for Storage Managers that support them.

### Sources

### Storage Managers

Introduced support for database transactions in storage managers.  See [storage manager transaction support](storagemanagers.md#transaction-support).

#### REMOTE

* Support for dynamically determining whether to save a document, image, or video has been added.  See [REMOTE Source](sources/remote.md#processWith).

### LLMs

* Support for Gemini Pro model has been added.

## UI Enhancements

### Client Builder

* There is now a new MenuBar Widget which allows you to add a classic menubar to a Client.
* There is a new option in the "Editors" section of the IDE Settings dialog called "JS Editors in Panes". When turned on it will cause any JavaScript editor which would normally appear in the Client Builder's "popout" area to be opened in a Modelo pane of its own. By using the "Flex Grid" layout this makes it possible to edit and view multiple JavaScript handlers at the same time while editing a Client.

### Modelo

* The IDE Settings Dialog has been broken into collapsible sections.
* In dialogs where you may select a Secret the dropdown list will now contain an item that allows you to create a new Secret without leaving the dialog.

### User Invitations

* The expiration date of user invites may now be customized. This can be set when inviting users in Administer>Users>New User or Administer>Namespaces>(target namespace)>Manage Authorizations>Authorize User.

# 1.37 Release Notes

## Server Enhancements

### Large Language Model/AI Support

The Vantiq platform now supports interactions with Large Language Models (LLM) to develop AI powered applications.  It also offers a Semantic Search capability which combines the use of LLMs and a vector database to support asking questions about application specific content (this is used to implement the new AI Documentation Search feature outlined below).  This feature introduces two new system resources:

* [llms](resourceguide.md#llms) -- represents a specific LLM which can be used to perform actions based on its type:
    * **embedding** -- used to create vector embeddings for Semantic Search.
    * **generative** -- used to generate responses based on user input.
* [semanticindexes](resourceguide.md#semantic-indexes) -- represents a collection of user provided content over which Semantic Searches can be performed.

### Visual Service Event Handlers

* The [Notify Activity Pattern](apps.md#notify) has a new option called  "_firstResponseFilter_"  which is a WHERE clause for the firstResponse event. If specified, the firstResponse event will only be raised if the response passes the filter. It also has a new option "_disableTemplateSubstitution_" which, if set to true, will disable template substitution for the Client payload.
* All reservoirs for the Analytics pattern now accept Reals. Existing apps may need to cast the results to Integers.
* Escalations have been reintroduced with the [Escalate pattern](apps.md#escalate).
* The [Submit Prompt](apps.md#submit-prompt) and [Answer Question](apps.md#answer-question) activity patterns were added to support use of the new AI features.
* The [Assign](apps.md#assign) Activity Pattern has a new **roleType** called `result` which supports assigning a value to an arbitrary result property in the current collaboration.

### VAIL

Added the following built-in services:

* [`io.vantiq.text.Template`](rules.md#template) -- generates text from templates and substitution values.
* [`io.vantiq.ai.ChatMessage`](rules.md#chatmessage) -- builds/represents messages sent to an LLM.
* [`io.vantiq.ai.LLM`](rules.md#llm) -- facilitates LLM interactions.
* [`io.vantiq.ai.SemanticSearch`](rules.md#semanticsearch) -- perform semantic searches.
* [`io.vantiq.ai.ConversationMemory`](rules.md#conversationmemory) -- manage conversation state for LLMs and semantic indexes.

### Edge Nodes

* Nodes that are defined using the WebSocket scheme along with the `vqs` option for back-communication (typically from cloud to edge) now support the [`reconnect` property](resourceguide.md#named-websocket-connection).
* Catalogs can now support edge nodes and VQS connections. [See here](broker.md#enabling-edge-connections) for information on enabling this for catalogs. [See here](broker.md#connecting-from-an-edge-installation) for information on connecting as an edge node.
* The CLI can now be downloaded from the Edge edition, using the Help -> Developer Resources menu/link.
* Added [Edge Vision](vantiqedge.md#edge-vision-server) server setup documentation.

### Kubernetes Management and Deployment

* Configurations may now include items of type `hardAffinity`. The `annotation` and `label` items may now include the `targetResource` property. See [Deploying a K8s Installation](resourceguide.md#k8s-cluster-deploy) for details.
* The Vantiq system may enhance K8sInstallations deployed to the `self` cluster with `hardAffinity` and/or `label` specifications. See [Using the self Cluster](extlifecycle.md#vantiq-self-cluster) for details.
* [Service connectors](resourceguide.md#service-connectors) deployed via Kubernetes support additional properties (see link for details).

### Sources

#### REMOTE

* Support for sending multipart messages has been added.  See [REMOTE Source](sources/remote.md).
* Support for [`asFullExchange`](sources/remote.md#receiving-the-full-exchange) option in SELECT WITH clause to help troubleshoot HTTP request/response exchange.

#### AMQP

* The AMQP source now allows offset to be considered when reconnecting to Azure service bus via AMQP, using the selector AMQP configuration option.  See documentation at [Azure Event Hubs partition offset](sources/amqp.md#partition-offset).

### User Authorization

* Email invites can now specify the subject line. See [namespace invitations](resourceguide.md#authorize-user).

### CLI

* New command "_run_" and "_stop_" have been added for running tests and testsuites.  You can also run procedures using the _run_ command.  See [CLI Reference Guide](cli.md#run). 
>The "execute" command for invoking procedures is deprecated and may be removed in a future release.
* New commands to support loading content into a semantic index and support backup and restore of index content.  See [CLI Reference Guide](cli.md).

## UI Enhancements

### Modelo

* The Design Modeler can now use Vantiq's Generative AI features to generate a Design Model from a natural language description of the application to be built. See the [Quickstart Tutorial](tutorials/quickstart.md) for an example of how to use the Design Modeler's *AI Design Assistant*.
* AI Documentation Search, found under “Help”, provides a floating dialog in which you can ask questions about the Vantiq platform. It uses Vantiq’s Generative AI features to search Vantiq documentation to answer the questions. The results will also show links to the specific documents that were used to provide the answer.
* When setting the configuration properties for certain Tasks in an Event Handler you may now enter a natural language description of how the various properties within the Task should be set and Generative AI will be used to set the properties accordingly. Not all Tasks currently support this feature.
* The JavaScript editor used in the Client Builder can now use Vantiq's Generative AI features to provide code samples. The *AI Code Assistant* will generate code from your comments. Enter a single-line comment with a description of the code you require then use either Ctrl-Enter or Cmd-Enter to activate the *AI Code Assistant*. For example,

	```// change widget property```
	
	```// upload file```

* The JavaScript editor in the Client Builder is now the [Monaco Editor](https://microsoft.github.io/monaco-editor/).
* Project auto-save feature:  projects no longer need to be explicitly saved. Once a project has been given a name & saved, the Save button disappears and projects are automatically saved whenever they are changed.  The auto-save occurs after roughly 2 seconds.  The auto-save feature can be turned off in the _IDE Settings_ dialog, if desired. To rename a project, use the "Rename Current Project" menu item or the "Manage Projects" dialog.
* Catalogs may now use VQS (VantiQ Scheme protocol) to allow Vantiq Edge Nodes to subscribe to and install Catalog resources. When connecting to a Catalog, use the **Connect using VQS** checkbox to communicate using VQS. When creating a new Catalog in a Namespace, use the **Allow Edge** checkbox to allow connections to the Catalog to use VQS communications.
* Service Procedures generated by Vantiq may be shown or hidden by using the **Generated** checkbox in the *Procedures* section header in the Service Builder's *Implement* tab.
* Client Page Templates are another flavor of a Client resource that allow the reuse of Client pages. Page Templates are created using the **Save Page As Template** menu item associated with a Client page under the Client Builder's *Edit* tab. A new Client page from a Page Template is created using the **Add Page From Template** menu item associated with a Client under the *Edit* tab.
* The Client Builder contains two new Data Input widgets: Currency and Decimal.
* The Client Widgets that can accept data from a DataStream now support a new event called "On Data Consumed". This complements the existing DataStream event "On Data Arrived". This allows you to intercept and modify data as it flows into a specific Widget (rather than the DataStream itself).
* DataTable Widgets now support the declaration of a new type of "Derived" Column. This will show a column which is not bound to actual data in the DataStream. Instead you will need to use the DataStream's "On Data Arrived" event or the Widget's "On Data Consumed" event to compute the value and save it in the data object. This allows you to have the DataTable display values which are computed or derived from other values in the actual data.
* The "client" object now supports Text-to-Speech with the addition of the [client.speakText()](cbref.md#speaktext) and [client.cancelSpeaking()](cbref.md#cancelspeaking) methods.
* The Active Resource Control Center now lists Assemblies. The status of an Assembly can be active, inactive or partially active. Activate/deactivate of an Assembly unifies the active status of all resources within the Assembly.

# 1.36 Release Notes

## Server Enhancements

### Services

* Service procedures can be invoked via the `PUT` operation on the URI `resources/services/<serviceName>/<procedureName>`.  See [Operation to HTTP Method Mapping](api.md#operation-to-http-method-mapping) for details.
* Visual Event Handlers now fully participate in the Vantiq reliable messaging protocols.  See the [Reliable Apps](apps.md#reliable-apps) for more details.

### VAIL

* Added `getValueOrDefault` to `Concurrent.Value()` [procedures](rules.md#concurrent).
* Added built-in procedures `Utils.getHttpHeaders`, `Encode.formUrl`, `Decode.formUrl` and `Event.isRedelivered`.
* Tracing execution of VAIL [Function Expressions](rules.md##lambda-operator) is now supported.

### Security Administration

* Resource Ownership Transfer - when a user is deleted, resources like rules and services owned by that user can be orphaned & will no longer run.  To transfer ownership, new server operations exist to handle this case.  Resource ownership can be transferred at the same time the user is deleted from a namespace, or later, after the user has been deleted and the resources are orphaned.  [See here](resourceguide.md#revoke-authorization) for doing transfers on revocation, [see here](resourceguide.md#find-orphaned-resource-owners) for finding the owners of orphaned resources, and [see here](resourceguide.md#transfer-orphaned-resources) for claiming ownership of orphaned resources.

### Sources

* REMOTE sources and Enterprise Connectors have been extended to support the sending and receiving of Vantiq Document, Image, and Video objects.
* REMOTE sources:
    * acceptType property added to the request document.
    * automatic URL-encoding of the request body expressed as key-value pairs (`x-www-form-urlencoded`).
    * syntax `@secrets(secret-name)` support for headers and query parameters.
* MQTT Sources now acknowledge (ack) inbound events AFTER processing the event.

### Storage Managers

* Added support for native language implementations for storage manager services.  See [Storage Managers](storagemanagers.md#native-language-implementation) for more details.

## Natural Language Processing

* The Vantiq NLP processing now makes use of the [Azure Cognitive Services for Language](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/) (Conversational Language Understanding) capability.  LUIS support has been deprecated & will be removed in a future release.

### Grafana

* There are new dashboards in the list of Grafana dashboards for each namespace:  [Service Handler](grafana.md#service-handler-dashboard) and [Reliable Events](grafana.md#reliable-event-dashboard).  There is also additional documentation about the [Grafana Dashboards](grafana.md) and a [Workload Management guide](workloadmanagement.md).

### Deployment

* Deployment Partitions are now stored with the project as Project Partitions.  Export/import project includes project partitions.
* Users can use Vantiq IDE to migrate partitions defined in an existing deployment to its related project.

## UI Enhancements

### Modelo

* Popup dialogs have been reworked for consistency in styling and the way buttons are used. Validation errors now mostly appear "inline" so the error will be in red underneath the relevant field. The "OK" button will generally be disabled until all required fields contain an appropriate value.
* A new Layout Style called "Flex Grid" is now supported in Modelo, in addition to the existing "Tiled" and "Custom" styles. In the "Flex Grid" layout style all the open tools are inside a classically tabbed pane. Tabbed panes may be split horizontally and vertically so you can have as many panes visible at the same time as real-estate permits, and tabbed panes may be resized. You may make "Flex Grid" the default using the "IDE Settings" dialog.
* Resource Ownership Transfer - when a user is deleted, resources like rules and services owned by that user can be orphaned & will no longer run. To transfer ownership, new UI operations exist to transfer ownership for resources when a user is being removed from a namespace or organization or to transfer ownership for resources that are already orphaned. [See here](namespaces.md#removing-namespace-administrators) for handling it from an org namespace, [see here](namespaces.md#handling-administrators-leaving) for handling it from the namespace itself.
* Each item in the Find Records Results pane now has a **View as JSON** context menu item to view the record formatted as JSON.
* Collaboration-oriented tasks in the App Builder (e.g. Chat, Notify, Track) have a new color to distinguish them from other App tasks.
* Event Generators may be run from the Project Contents tree by using the **Run Event Generator** context menu item.
* Scheduled Events (from the Add>Advanced>Scheduled Event menu item) can now be created for Topics and Service Event Types using the **Resource Type** menu for selection.
* Captures (from the Test>Captures menu item) can now capture Service Events.
* The IDE Navigation Bar has been reorganized in several respects.
	* The Projects menu is no longer scrollable but instead keeps a list of 'recent' Projects.
		* The maximum number of recent Projects is set in the IDE Settings, **Maximum Recent Projects**.
		* If there are more Projects in the Namespace than recent Projects, a **Show All** menu item appears at the bottom of the menu.
	* The Deploy menu now appears as a hierarchical menu at the bottom of the Administer menu.
	* The Help menu has been relocated next to the Test menu.
	* The three VCS sync menu items have been moved to a Project hierarchical menu titled 'Sync'.
* The Client _MultilineInput_ and _InputString_ widgets' **defaultValue** property is now localizable.
* The horizontal ordering of a Type's properties may now be changed using the **Properties** tab of the Type definition. Use the **Move Up** and **Move Down** Action icons to change the order of display both in the **Properties** tab and when records of that Type are displayed in the Find Records Results pane.
* The context menu associated with the App Builder's task nodes now has a new menu item: **Delete Task and Reconnect Children** to make it easier to delete existing tasks without disconnecting the task's children.
* Each titlebar of the panes in the Debug Dock at the bottom of the IDE (Errors, Log Messages, and Autopsies) now have a **Open Associated Pane** icon. Clicking this icon opens the associated query pane so that targeted historical records may be displayed.
* The **Projects** menu now has a new **Show Partitions** menu item. It opens the Project Partitions pane to define partitions for a project. If there are existing deployments using the project, users must migrate partitions from one of the deployments before editing project partitions. Once migration is done and the project is saved, all existing deployments using the project will start using partitions from the saved project.



# 1.35 Release Notes

## Deprecated Features

Standalone Apps have been deprecated in this release and will be removed entirely in a future release. All existing standalone Apps should be converted to [Service Event Handlers](services.md#inbound-event-types) as soon as possible. No new standalone Apps should be created.

## Server Enhancements

### VAIL

* Added `toArray` to built-in [Array Procedures](rules.md#array-utility-procedures).

### Export (both CLI and UI)

* Export excludes "sub-artifacts" of a resource instance that have been generated.  The impacted resources are:

    * Types -- excludes any generated properties from exported definition.
    * Services -- excludes any generated procedures from the service interface.

> This change has been applied to 1.34.21. This version (or later) must be used when exporting code for import into 1.35.  Failing to do this may lead to compilation errors on import.

### Services

* The names used for various generated artifacts have changed in attempt to simplify them and make them easier to read/understand.  In most cases this change should be transparent; however, in cases where the generated name is referenced directly (e.g. when referencing a generated procedure), it may result in compilation errors when regenerating.  The impacted artifacts are:

    * Service State Types -- the new format is `<serviceName>.[Global|Partitioned]State` (unless the service is not in a package, then we use `<serviceName>_[Global|Partitioned]State`).
    * Event Type Schema Types -- the new format is `<serviceName>.<eventTypeName>` (unless the service is not in a package, then we use `<serviceName>_<eventTypeName>`).
    * Per-task Service Procedures -- the new format is `<taskName>State_<eventTypeName>`.
    * Service Visual Event Handlers -- the new format is `<serviceName>.<eventTypeName>`.
    * Service VAIL Event Handlers -- the new format is `<serviceName>.<eventTypeName>` (unless the service is not in a package, then we use `<serviceName>_<eventTypeName>`).
    
* [Inbound Service Event Handlers](services.md#inbound-event-types) must be triggered by the Inbound Event Type they implement.  This was previously flagged as a warning in 1.34.
* Services may now define [Internal Event Handlers](services.md#internal-event-handlers) which are triggered by *Type*, *Topic*, and *Source* events rather than Service Events. Internal Event Handlers are *not* part of the Service Interface.
* Services may define [Private Inbound Event Types](services.md#event-types) which can only be published to from within the Service. Private Event Types are not part of the Service Interface.
* The Design Modeler can be used to define [Service Routes](services.md#event-routing) which tell the system to automatically send the events emitted by Outbound Event Type to the event handler for an Inbound Event Type.
* Service Procedures allow a *[stateless](rules.md#procedure-modifiers)* access modifier. This is used to declare Procedures in a Stateful Service which *do not* interact with the Service's state in any way.

### Apps

> Standalone Apps are fully deprecated in release 1.35 and should be migrated to Services ASAP.  They will be removed completely in a future release.

* The names used for various generated artifacts have changed in attempt to simplify them and make them easier to read/understand.  In most cases this change should be transparent; however, in cases where the generated name is referenced directly (e.g. when referencing a generated procedure), it may result in compilation errors when regenerating.  The impacted artifacts are (note that the service name referenced here is that of the "App" Service):

    * Service State Types -- the new format is `<serviceName>.[Global|Partitioned]State` (unless the service is not in a package, then we use `<serviceName>_[Global|Partitioned]State`).
    * Event Type Schema Types -- the new format is `<serviceName>.<eventTypeName>` (unless the service is not in a package, then we use `<serviceName>_<eventTypeName>`).
    * Per-task Service Procedures -- the new format is `<taskName>State_<eventTypeName>`.
    * Service Visual Event Handlers -- the new format is `<serviceName>.<eventTypeName>`.
    * Service VAIL Event Handlers -- the new format is `<serviceName>.<eventTypeName>` (unless the service is not in a package, then we use `<serviceName>_<eventTypeName>`).

### Visual Service Event Handlers

* [Visual Event Handlers](apps.md) now display all the compilation errors for all tasks with errors rather than just the first caught error.
* The PublishToEventType Activity Pattern has been renamed [PublishToService](apps.md#publish-to-service) and now supports an optional Processed By clause.
* The [Join](apps.md#join) activity pattern includes a join order configuration property so that the Join order can be set dynamically.
* The [LoopWhile](apps.md#loop-while) activity pattern now correctly handles cases with a Filter under the *whileTrue* branch. If the filter results in a false condition, the loop will start the next iteration rather than terminating immediately.
* The [AccumulateState](apps.md#accumulate-state) activity pattern now defines a default accumulator: `state = event`. This will update the service state to hold the most recent event.
* The [ComputeStatistics](apps.md#compute-statistics) activity pattern has been enhanced to compute statistics on multiple event properties.
* A new [EstablishCollaboration](apps.md#establish-collaboration) activity pattern allows an App to either: continue processing in the context of a new or existing collaboration or prevent multiple active collaborations for a single entity.

There is a new suite of statistical and analytics based activity patterns. Each of these are built on top of the [Apache Commons Math Library](https://commons.apache.org/proper/commons-math/). Each of these activity patterns allow users to apply analytics to one or many properties of incoming events.

* [Analytics](apps.md#analytics): Computes the _mean, median, count, min, max, standard deviation, geometric mean, variance, skewness,_ and _kurtosis_. The Analytics activity pattern also supports dimensional analysis. 
* [DBScan](apps.md#dbscan): Applies a density-based clustering algorithm to determine if there are one or many clusters.
* [KMeansCluster](apps.md#k-means-cluster): Applies a K-Means Clustering algorithm to find the specified number of clusters in the data.
* [Linear Regression](apps.md#linear-regression) Applies linear regression to the data and generates a prediction procedure to predict future data points.
* [Polynomial Fitter](apps.md#polynomial-fitter) Applies a polynomial fit algorithm to the data and generates a prediction procedure to predict future data points. This pattern also generates procedures to calculate the derivative and integral at specific points.

### Assemblies

* Documents may now be visible resources within Assemblies.
* Installed resources are not editable by consumers.

### Sources

* Sources and Topics have a new _Unwind Arrays_ option.  If set to true, events that are arrays will be automatically unwound into separate events, one for each array entry.
* The examples for using [Azure Event Hubs](sources/kafka.md#azure-event-hubs-configuration-examples) with Kafka have been updated with additional recommended settings.

### Miscellaneous

* Application namespaces (also known as Namespace Admin namespaces) have a new UserAdmin profile available.  That profile can create users, but cannot change any development resources.
* User invitation emails can now be customized. See [here](namespaces.md#custom-user-invites) for more details.
* Catalogs can now repair connections. See [here](brokerapi.md#repair-catalog) for more details
* Org admins can now access namespaces in their organization without explicit permissions. See [here](namespaces.md#accessing-namespaces-in-the-organization) for more details.
* Org admins can now setup resources to be automatically installed into newly created namespaces. See [here](namespaces.md#creating-resources-for-new-namespaces) for more details.
* Users can create personal tokens that are limited to a single namespace. See [here](resourceguide.md#tokens) for more details.
* `SELECT` resource operation supports [REST POST binding](api.md#operation-to-http-method-mapping) via `/select` sub-URI.
* Added the ability to deploy connectors into the cloud (that is, to the same Kubernetes cluster as the Vantiq servers).

## UI Enhancements

### Modelo

* To make it easier to resolve VCS conflicts the set of "open folders" is no longer saved when you "Sync Project to VCS"
* In "Find Records", when querying for Boolean properties there is now a droplist that lets you specify that you want to see all the records with "true" or "false" as well as "Any" (which means 'don't care') and "None" (when the property was not specified and is neither true nor false).
* In "Add Records" when inserting a new record the droplist will let you specify "true" and "false" as well as "None" (which means 'don't set the property at all').
* When importing a Project you may now set "Select Import Type" to "Project from URL (zip)". This allows you to enter a URL which refers to the Project zip file.
* In Modelo's "IDE Settings" in the "Editors" section there is a checkbox called "Indent with Spaces" which controls whether JavaScript and VAIL editors will implement indents with an actual "tab" character (the default) or equivalent space characters.
* There are various places in Modelo where you can add a multiline "Description" field. These fields now support basic Markdown formatting:
     * Project Description
     * App and App Component Descriptions
     * Service Builder Descriptions
     * Assembly Descriptions
* Dialogs that allow you to enter a GeoJSON object now support the "Polygon" type.
* The [Storage Manager](storagemanagers.md) is used to access databases other than the default MongoDB.
	* To create a new Storage Manager, use **Administer>Advanced>Storage Managers** then click the **New** button.
	* Once a Storage Manager has been created, it can then be used when defining a new standard Type definition. Data stored in that Type will use the database defined by the selected Storage Manager.
* When Visual Event Handlers are used in the Service Builder, the **Save Changes** button will display a small, red circle to indicate that the Event Handler will be rebuilt when saved. If the red circle does not appear on the **Save Changes** button, this indicates only cosmetic changes have been made to the Event Handler.
* The icon selection dialog for the Icon widget in the Client Builder now has a Filter by Name feature.
* The ZingChart widgets in the Client Builder now have a **Chart Config Override** property under the **Specific** category. The value is a JSON object. If this property is configured, this JSON object is used to initialize ZingChart which will override all other default and widget properties defined by the widget. Refer to [ZingChart documentation](https://www.zingchart.com/docs) for legal properties.
* IDE Settings has a new property, **Show Namespace Org Filter**. Enabling this property displays a menu in the **Change Namespace** dialog which allows the Namespace list to be filtered to show only those in the current Organization.

### Design Modeler
* The [Design Modeler](designmodeler.md) is a new visual IDE tool for building Vantiq systems. It allows the user to easily connect Services and Clients, which are the building blocks of a Vantiq system.
* New Design Models are created using **Add>Design Model** and clicking the **New Design Model** button. The Design Modeler uses Design Templates to help the developer design Vantiq systems that are scalable and use best practices. The New Design Model dialog shows a diagrammatic representation and an explanation of each of the templates.

### System Modeler
* The [System Modeler](tutorials/systemmod.md) now generates Design Models (see above) rather than Vantiq Projects. It still uses [Event Storming](https://www.eventstorming.com/) concepts to document business requirements.
* Once the Event Storming session is complete, use the **Generate** button to produce a new Design Model. Design Models generated from System Models contain a Requirements checklist of all the Event Storming notes so the developer is reminded to implement all the business requirements within the Design Model.

### Service Builder

* Opening any Procedure, App, or Rule that is part of a Service will open the resource in the context of the Service rather than a standalone pane.
* EventStreams for Inbound Service Event Handlers are not editable. This is because they *must* be configured to trigger off the Inbound Event Type the Event Handler implements.
* Generate state managing procedures (Get, Update, Reset) for the property by clicking a new button next to the state property name in the State tab.
* Generate a Lookup only or Update and Lookup Cache Service by using a new option in the Add New Service popup.
* Task Contexts (blue bounded boxes) represent coarse-grained guidelines for Service Event Handlers generated by the Design Model. Clicking on each task context filters the activity pattern palette by only showing relevant patterns.

### Client Builder

* When editing JavaScript in the Client Builder there is a droplist called "Insert Code Fragment" which can be used to insert various helpful fragments of code. There are 3 new types of fragments which can now be inserted:
     * Data Streams - Insert code to access the Data Stream objects
     * Service Procedures - Insert code to invoke Procedures defined on a Service
     * Service Events - Insert code to publish to an inbound Service Event defined on a Service
* The Data Table 'On Format Cell Background' event has been deprecated in favor of the more comprehensive ['On Render Cell'](cbref.md#on-render-cell-event) event.
* For each column within a Data Table you can now set a CSS class which will be applied to each '&lt;td>' element inside the column.
* There is a new Widget called [StaticMarkdown](cbref.md#staticmarkdown) which can be used to format and display a fragment of Markdown text
* All Widgets now support the "minimumHeight" and "minimumWidth" properties. If set, they allow you to increase the minimum size that layout management would normally use.
* You may now open a Page inside a ScrolledLayout widget; this makes it act like a popup Page but it will be nested within another Page. See [openNestedPage](cbref.md#opennestedpage) and [closeNestedPage](cbref.md#closenestedpage).
* Client Components may now be instantiated at runtime and added to a WidgetContainer using the  [addComponentChild](cbref.md#addcomponentchild) method.
* Component names in the Client Builder palette no longer include full package names (although you can see the full name by hovering the mouse over it).
* Client Components now allow you to set a Data Stream as a "configuration property". This makes it possible to  override the Client Component's default DataStream with one of your own at runtime. (See ['Data Streams' in the Client Components User's Guide](ccug.md#data-streams).)
* When setting custom colors with the "color picker" you can now set the opacity as well as the color values. (There is an extra slider that lets you control the amount of translucency.) Colors which are "solid" (with an opacity of 1) are shown using the normal #RRGGBB coding - colors with any other opacity setting will use the "rgba(r,g,b,a)" format.
* The Drop Shadow Color is now settable in a Theme. For those widgets that support it can now be given one of 4 settings:
     * None (no drop shadow)
     * Theme (It has a drop shadow using the color from the Theme)
     * \#rrggbb (An explicit color, either set by the color picker or selected from a list)
     * &quot;Use Background Color&quot; (for backwards compatibility)
* In the Client Builder when a Page is in "Browser" layout mode you now "drag" the page around to scroll it rather than using the scrollbars.
* RadioButtons now have a new Boolean property "isHorizontal" which can be set to "true" to make the radio buttons layout left-to-right rather than top-to-bottom .
* When creating a "Timed Query" Data Stream in the Client Builder the "max records to return" will now be set to 100 by default.
* In Vantiq mobile apps there is now support for scanning for data from Bluetooth Low Energy (BLE) devices. See [client.startBLEScan()](cbref.md#startblescan) and [client.stopBLEScan()](cbref.md#stopblescan)
* You can now get the name of the current client with [client.getName()](cbref.md#getname)
* When running under the Client Launcher the [client.logout()](cbref.md#logout) method will logout the current user.
* ZingChart-based widgets ([BarChart](cbref.md#barchart), [ColumnChart](cbref.md#columnchart) and [LineChart](cbref.md#linechart)) now support a way to listen for ZingChart internal events by setting the "bindEvents" property.
* A Client can now force a location update from the Vantiq mobile apps with [client.sendLocation](cbref.md#sendlocation).

### Miscellaneous

* The Active Resource Control Center allows you to see all activatable resources in a namespace and easily change their activation status. When in an org namespace, you can do the same for all namespaces in that org. See [here](namespaces.md#active-resource-control-center) for more details.
* Organization Admins may use the Active Resource Control center to update the activation for any resource in any namespace within the Organization, regardless of whether the user is explicitly invited to each namespace.
* A placeholder root node has been added to App Components. This allows App Components to effectively have multiple root tasks.
* Users can create personal tokens, which act under the identity of the creator instead of a generated user. See [here](resourceguide.md#tokens) for more details.

# Vantiq Mobile Apps
Version 3.6.0 of the iOS Vantiq app is required to enable push notification functionality.

# 1.34 Release Notes

## Server Enhancements

### VAIL

* VAIL scalar types:
    * The system now correctly interprets these as case-sensitive.
    * To avoid the potential for collisions, it is illegal to create a user-defined Type with the same name as one of the Scalar types.
    * The Scalar types `Map` and `Value` have been added.
        * Can only be used when defining a "schema" type property.
        * Support data replication (see [Replicated Services](./services.md#service-replication)).
    * The built-in factory procedure [Concurrent.Cache()](rules.md#concurrent) has been added.  It creates an instance of the VAIL `Map` type which is implemented as an auto-evicting cache.
* New system procedures:
    * [Decode.base64Raw](rules.md#encoding-decoding-and-hashing)
    * [timezoneOffset](rules.md#timezone-procedures)
    * [getZoneIds](rules.md#timezone-procedures)
* Strict typing enforced for Stateful Service properties.
    * It is no longer legal to assign a value of the wrong type to stateful service property.  Doing so will result in a compile time error.  The most common example of this is assignment of `Concurrent.Map()` to a property of type `Object`.  In this case the property must be typed as `Map`.
* The `EXECUTE` statement has been augmented to support specification of a partitioning key.
* The `PUBLISH` statement has been augmented to support propagation of the "root" event id.

### Services

* Stateful Services may now be [replicated](./services.md#service-replication).
    * Prevents loss of data due to Vantiq server failures.
    * Only properties of type `Map` or `Value` will be replicated.
* Service state properties now have a default value based on their type.
* It is now illegal to directly invoke the service state initializers (`initializeGlobalState` and `initializePartitionedState`).
* Multi-partition procedures may now be invoked directly (based on their visibility).
* Service event handlers (whether implemented as `rules` or `collaborationtypes`) may now invoke private procedures of their service.
* Publishing directly to an Outbound Service Event Type from within the same Service is supported using the syntax:     
      `PUBLISH event TO SERVICE EVENT "<serviceName>/<outboundEventTypeName>"`

### Apps and Collaborations

* The App Builder now supports all the functionality of the Collaboration Builder. This adds the following activity patterns to the App Builder: *Assign*, *Chat*, *Notify*, *Track*, *Recommend*, *LoopWhile*, *GetCollaboration*, *CollaborationStatus*, *Interpret*, and *ProcessIntent*, The Collaboration Builder is now considered deprecated.
* Collaborations are primarily updated and managed as part of the Service State rather than database updates which provides significant performance improvements. 
* App Components may now include Collaboration functionality.
* The ComputeStatistics and AccumulateState activity patterns produce *reset* events which emit the value of the state right before it is reset
* The AccumulateState activity pattern allows users to configure which State property will be updated. This allows multiple AccumulateState tasks to update the same Service State property
* The EventStream activity pattern now supports Delete events, and the option BOTH was renamed to UPSERT.
* Any App tasks that are children of a SaveToType, PublishToSource, or PublishToTopic task will now only be triggered by their parent. If such an event is triggered outside the App, the App will not process the event at the intermediate task.

### Event Generators

* Event Generators now support ranges for GeoJSON events.
* Event Generators no longer require the "step" option for a Ranges. If no step is provided, a step will be calculated to spread the range over the number of iterations for the event.

### Sources

* [REMOTE sources](sources/remote.md) can be configured to obtain their access token from an OAuth authorization server.
* [PYTHONEXECUTION sources](https://github.com/Vantiq/vantiq-extension-sources/blob/master/pythonExecSource/docs/Usage.md) can be used to run Python code using the [Python execution connector](https://github.com/Vantiq/vantiq-extension-sources/tree/master/pythonExecSource).  There is also a [Vantiq Python SDK](https://github.com/Vantiq/vantiq-python-sdk).

### Catalogs

* [Public Catalogs](./broker.md#public-catalogs) are now available. Instead of providing credentials to every namespace that will connect to a given Catalog, those credentials may be provided to a system or organization administrator. They can create a Public Catalog in their system or organization namespace, which can then be used by any namespace inside their system or organization.
* Change logs may be provided when updating published resources. These will be shown to subscribers when they update, giving them a brief overview of the changes.
* Catalogs may be given custom names using the VAIL procedure `Broker.createCatalog(<custom name>)`.
* Assemblies can be created from a zipped export. This can be done by uploading the zip as a Document then using the [createEntry](brokerapi.md#create-entry) operation or the VAIL procedure `Broker.createAssembly(<catalog name>, <assembly name>, <document name>)`. Note that some publish validations cannot be performed in this case, so a successful creation does not mean that the Assembly and its resources can be successfully installed.
* Catalog nodes and tokens will try to repair themselves, and will clean themselves up when no longer needed. To repair connections you will need to either connect to the catalog again (for issues connecting to the catalog), or unsubscribe and resubscribe to the event or service that is having connection issues.

## UI Enhancements
  
### Modelo

* Overall styling of Modelo has changed with new fonts and colors. The Navigation Bar in particular reflects the new styling changes. See the [IDE User's Guide](ide.md) for details.
* The App Builder graphs have been improved to display links between tasks using Bezier curves and task category icons have been added to task nodes.
* The Catalogs pane has a new Updates tab which lists any updates available for installed Assemblies or subscribed Services. Each list item shows the description of the updates if the publisher provided them.
* Greatly reduced the number of 'toast' (temporary) notifications displayed at the upper-right of the IDE.
* Support for creating [Public Catalogs](./broker.md#public-catalogs) in system and organization Namespaces.
* The VAIL editor supports a new shortcut for displaying variables in scope. See the [IDE Shortcut Keys](ide.md#ide-shortcut-keys) section for a list of all shortcut keys used in Modelo.
* Expanded the use of the Resource Explorer UI across the IDE. The Resource Explorer dialog is usually accessed whenever the user is expected to select a resource (Procedure, Source, etc.) and is displayed by clicking a button with a magnifying glass icon. The Resource Explorer dialog also allows subscription or installation of Catalog-based resources, if Catalog connections have been created for the Namespace.
* When creating a new Type the default value for "Role" is now "Schema" instead of "Standard".
* Added the **Hide Toolbars** IDE Setting to hide the toolbars of some panes (e.g. App Builder, VAIL Editor) to save vertical space. If enabled, the pane's title-bar contains the **Show/Hide Toolbar** button to show and hide the toolbar dynamically.
* The Topics pane now supports the definition of the "Group" property.

### Service Builder

* The Service Builder now supports "bottom up" development. This includes:
    * Creating Inbound and Outbound Event Types from the Implement Tab
    * Automatically repairing the Procedure Interface when the Procedure implementation is changed either in the Service Builder or in a standalone Procedure pane
    * Executing Private Procedures from the browser in order to test them
* View the current value for each Global or Partitioned State property from the *State* tab of the Service Builder
* Visual Event Handlers now allow multiple EventStreams. This allows a single Event Handler to Merge/Join events from multiple Inbound Service Event Types

### Client Builder

* There is now a new layout widget to support scrolling:  [ScrolledLayout](cbref.md#scrolledlayout)
* You can now create DataStreams dynamically at runtime.
* The "Insert Code Fragments" droplist in the Client Builder's JavaScript editor has been enhanced to assist with creating references to Widgets, DataStreams and Global Functions.
* Scrolling is now supported inside the pages of a [TabbedLayout](cbref.md#tabbedlayout) through new properties on the [FixedLayout](cbref.md#fixedlayout) called "horizontalOverflow" and "verticalOverflow".
* The visibility of [TabbedLayout](cbref.md#tabbedlayout) pages can now be controlled at runtime using the getPageVisibility and setPageVisibility methods.
* The old "code fragment wizard" feature in the VAIL editors has been removed and replaced with the ability to create and save your own useful "VAIL Code Fragments". (This is analogous to the same feature in the JavaScript editors.)
* As a convenience, the parameters for  various dialogs (infoDialog, errorDialog, confirmCustom, confirmCustomEx, terminateWithDialog) now accept localization key strings directly in addition to literal strings.
* The [DynamicMapViewer](cbref.md#dynamicmapviewer) now supports an "On Click" event.
* Readonly properties have been added to the [FixedLayout](cbref.md#fixedlayout) widget to get "true" and "scaled" image sizes at runtime. (scaledImageHeight, scaledImageWidth, trueImageHeight, trueImageWidth)
* The new "dataValue" property now allows you to set the current value of a  [NumberViewer](cbref.md#numberviewer) directly.
* In previous releases a Page could be given a default "response topic" to which the "default submit" operation would publish the response object (See [here](cbuser.md#default-submit-behavior-triggered-by-a-button).) This has been enhanced so that in addition to topics you can now send resource events to a Service or Source instead; see the Page property sheet in the Client Builder.
* Previously the dataArray property of the [DataTable](cbref.md#datatable) was read-only - it is now writable and you can use it to completely replace the current contents of the table.

### Miscellaneous

* You now specify a namespace when running an [RTC client](../../../ui/rtc/index.html) by adding "_?targetNS=NS_Name_" parameter to the URL.  This also works when launching Modelo.

# 1.33 Release Notes

## Server Enhancements

### VAIL

* Loop iteration variables are now properly scoped.  Attempting to reference one outside the body of the loop will produce a compilation error (previously the result was a runtime error).

* Correctly reject invocation of a `private` procedure via `ResourceAPI.executeOp`.

* Added the [String Procedure](rules.md#string-procedures) `isReal`.

* Added the [DateTime Procedure](rules.md#date-utility-procedures) `truncateTo`.

* Improved debug tracing for `for` statements and `try/catch/finally` (especially in cases with empty blocks).

### Services

* Services may now have an explicitly defined interface.  When present the system will validate the definition of procedures declared as part of the service with the definitions found in the interface.  All services defined by the new [Service Builder](#service-builder) declare an explicit interface.

* Event Generators now support generating events on Inbound Service Event Types.

* Services can be named as a resource in a Debug Configuration.  This enables controlling logging levels and enabling debug tracing for the service as a whole.

* Services have an "activation state" and can be marked as "inactive".  Doing so prevents the handling of any inbound event types.  However, it does not prevent execution of the service's procedures.

* The `status` operation for stateful services now returns:

    * Whether or not the service state has been initialized.
    * The current status of the scheduled procedures.

### Assembly Enhancements

* Assemblies now allow you to include local Namespace data when publishing the Assembly to the Catalog
* Assembly configuration now supports swapping client components within Assembly Clients
* Configuration Properties may now be typed as Schema Types and Secrets in addition to the previous options
* Integration Tests for Assemblies allow the Author to specify a configuration for the Assembly which will be tested
* The following resources are now configurable:
    * Scheduled Procedure Interval
    * Client components within Assembly Clients
    * An Assembly may contain another Assembly and configure the child Assembly
    * Sources may define additional configuration properties besides those the server can infer
    * Procedures and Rules may access Assembly Configuration Properties in VAIL
  
### Sources


* [Secrets](resourceguide.md#secrets) can now be [used in source configurations](sources/source.md#using-secrets), using syntax `@secrets(secret-name)`.
* [Reliable messaging](reliability.md) is now supported for AMQP sources. 

### Deployment 

* Deploying a partition to an environment now handles larger deployments by doing the work in pieces called WorkItems.  This avoids timeouts when deploying large projects.

### Kubernetes Management and Deployment 

* Vantiq has added external lifecycle support for Kubernetes version 1.22. The Vantiq interface and API are unchanged for this support; the primary difference is that the Ingress resource type has changed for later versions of Kubernetes.
* Kubernetes Secrets can now be mounted as files in a K8s Installation.  See the [Resource Guide](resourceguide.md#k8s-clusters) for details.
* K8s Installations now support the *fetchLogs* operation. Please see the [Resource Guide](resourceguide.md#k8s-installations) for details.

### CLI

* added _-include \<typeName>_  flag to **export**
* added _-props_ flag to **select**

## UI Enhancements

**UI Update:**

* The Service Builder now supports "bottom up" development. This includes:
    * Creating Inbound and Outbound Event Types from the Implement Tab
    * Automatically repairing the Procedure Interface when the Procedure implementation is changed
    * Executing Private Procedures from the browser
  
### Modelo

* There are some new "resource specific" operations which have been added to the "context menus" in the Project Contents browser:
    * Procedures: Execute Procedure
    * Tests: Run Test
    * Test Suites: Run Test Suite
    * Types: Find Records, Add Records
    * Client: Run in Client Launcher
    
* When selecting topics, Services or Assemblies, allow the subscription or installation and use of Catalog-hosted resources.
* Added VAIL and JavaScript editor preferences to IDE Settings: Font Size and Family and background color.
* Added two IDE keyboard shortcuts:
	* _Shift-Ctrl-S_ & _Shift-Cmd-S_: save Project changes
	* _Shift-Ctrl-E_ & _Shift-Cmd-E_: display the [IDE search](ide.md#search) dialog
  

### Service Builder

The [Service Builder](services.md) is now the central server development tool in Vantiq.  The Service Builder allows users to:

- Define Inbound and Outbound Event Types and their schemas
- Publish Inbound Event Types and Subscribe to Outbound Event Types
- Define Service Procedure Signatures
- Implement Public and Private Service Procedures
- Implement Visual Event Handlers (Apps) and VAIL Event Handlers (Rules) for inbound Event Types
- Schedule Service Procedures
- Define and Run Service Integration Tests, Service Unit Tests, and Service Test Suites
- View all Compilation and Runtime errors for the Service and any of its implementing resources
- Since Apps, Rules, and Procedures can now be defined in the Service Builder, Add App, Rule, and Procedure have been moved to the Advanced sub-menu of the Add menu.

#### Package-Centric Trees

The Project Contents browser (at the left edge of the Modelo window) can now display the resource tree in a new "package-centric" flavor. Rather than dividing all the resource packages **inside** the resource type (Service, Client, App, etc.) you can now select "Tree of Resources by Package". In this flavor the packages come first and the resource types are inside. This is now the default for new Projects and Views, because this flavor better represents the new importance of packages in Modelo.

For example, suppose your Project resources looked like this (shown in the "list" flavor):

![TreeAsList](assets/img/releasenotes/treeAsList.png)

In previous releases you would usually show this as a "resource-centric" tree where all the resources are grouped by resource type with the packages shown inside:

![TreeByResources](assets/img/releasenotes/treeByResources.png)

In R1.33 you can now use the menu to display the resources as a "package-centric" tree. The new menu now looks like this:

![TreeMenu](assets/img/releasenotes/treeMenu.png)

Selecting "Tree of Resources by Package" makes the tree look like this:

![TreeByPackage](assets/img/releasenotes/treeByPackage.png)

If you prefer the old "Tree of Resources by Type" there is an IDE Setting to change the default.

### Client Builder

* You can now add an optional icon to each page title in a [TabbedLayout](cbref.md#tabbedlayout).

* There is a new flavor of DataStream which listens for an "outbound event" generated by a [Service](rules.md#services).

* In previous releases you could not open more than one "popup" Page a time. This restriction has been lifted so you can now call one popup Page from inside another. Note that these popups are still modal, so only the "topmost" popup page is active. The user must close a popup to reveal the older one beneath it.

* The standard for GeoJSON coordinates is to contain a 2-element array which contains [latitude, longitude]. This is the opposite order of how most humans think about positions, and some people would prefer that these coordinates be delivered as [longitude, latitude]. There is now a property on the  [FloorplanViewer](cbref.md#floorplanviewer) and  [FixedLayout](cbref.md#fixedlayout) widgets which will cause the coordinates to be swapped from the GeoJSON standard ([latitude, longitude]) to the "human standard" (longitude, latitude).

* The Client Builder has a "search" field in the "Add" Widget palette; in previous releases that would only allow you to filter out Widgets based the short name that was shown in the palette. In R1.33 this search is more forgiving, and will do a case-insensitive match against the actual Widget class name ("AccordionLayout"), the short visible label ("Accordion") and the longer tooltip ("Accordion Layout"). Note that Widget class name is always in English but the visible label and tooltip are always **localized** versions of the text.

* The  [NumberViewer](cbref.md#numberviewer) Widget now allows you to enter "color rules" for the background and foreground colors the Widget uses at runtime. The rules will be evaluated in order and the first one to match the current value will be applied. If no rules match the default colors will be used.

* The [DataTable](cbref.md#datatable) Widget now supports an optional icon in the header for each column.

* The [DataTable](cbref.md#datatable) Widget now allows you to optionally specify a "CSS width" for a column. (Any valid CSS width is accepted, such as "250px".) It's important to note that there are situations in which HTML won't allow this to work as you would expect. In  general the table must be wider than the minimum before these width settings will be respected, and if your specifications are conflicting or inconsistent they will not work. You will need to experiment to discover what HTML will allow in your situation.

* The [DropList](cbref.md#droplist) Widget now supports the "On Validation" event which you can use to force the user to pick some particular subset of the supported values. The 'On Validation' Event is fired as a part of the "Validation" process which is described [here](cbuser.md#field-validation).

### App and Collaboration Builders

> These changes also apply to the embedded version of the App Builder used to construct Service Event Handlers.

* The Filter Activity Pattern may be defined either as a VAIL condition or as a *Visual Filter*.

* It is now possible to save various "non-functional" changes to an App/Collaboration Type, such as:
    * Graph zoom level
    * Expand/contract Service group(s) in the palette.
    * Expand/contract Activity Pattern group(s) in the palette.
 
* Regeneration of the App/Collaboration Type resources only occurs when functional changes have been made to the App/CT definition.  Note that a simple "toggle" of the activation state (without an intervening save) will *no longer* trigger regeneration.

# 1.32 Release Notes

## Server Enhancements

### VAIL

* Services can declare [event types](rules.md#service-event-types) which are used to describe events that are either produced (aka "outbound") or consumed (aka "inbound") by the service.
* Added built-in procedures `Context.email()` and `Context.isEmailVerified()`.

### Assemblies

* Developers can now create, publish, and install Assemblies. Assemblies are reusable Vantiq Projects that are configurable
and customizable to each user's individual requirements. Assemblies may be published and installed via the Vantiq Catalog.
Please refer to the [Assembly Users Guide](assemblies.md) for a complete description of Assemblies and the [Assembly Tutorial](tutorials/assemblytutorial.md) for examples of how to use Assemblies.

### CollaborationType Builder

* **Incompatible change**: The InitiateCollaboration *initialTrigger* property has been deprecated and replaced with _inboundResource_, _inboundResourceId_, and _condition_, similar to App EventStreams.  Existing Collaboration Types will still run but, when updated or re-imported, the *initialTrigger* value will need to be replaced with the new properties.  
NOTE: Once that is done, any uses in VAIL code of _event.newValue_ will have to be changed to just _event_.  Other internal fields in the pre-1.32 _event_ object will no longer be visible in the collaboration.

### App Components

* **Incompatible change**: The signature of the generation procedure has changed.  The first parameter is now a collaborationType object (not a string Name).  Any existing generation procedures for App Components will have to be updated to the new signature.  Using the old signature will cause a generation error. 

### App Builder

* The deprecated **groupBy** property has been fully removed and is no longer allowed on any tasks.  SplitByGroup must be used instead.

* Each App now generates an associated [App Service](apps.md#app-service) which provides access to the App's state and related functionality.  The service declares event types representing the events that are consumed and/or produced by the App.  Use of any of the following Activity Patterns causes the service to be stateful: *AccumulateState*, *ComputeStatistics*, and *CachedEnrich*.

* The *Statistics* activity pattern has been deprecated and should be replaced by *ComputeStatistics*.

* A SplitByGroup task cannot be used beneath another SplitByGroup task.  This was not supported and now will get an explicit error during generation.  If a second SplitByGroup is needed, the app with the first SplitByGroup needs to publish an event to another app or stream that contains the second SplitByGroup.

* A Join task cannot be used beneath a SplitByGroup task.  This was not supported and now will get an explicit error during generation.

### Catalogs

* Assemblies can be published and installed through the catalog.

* Types in catalogs may now be updated. The new type's fields must have all the fields in the catalog type, and may have new, non-required fields. See [Catalog Reference Guide](broker.md#types-in-the-catalog)

* Permissions on each catalog operation can be set for each member. See [Catalog Reference Guide](broker.md#setting-permissions)

### CLI

* It is our general policy that the CLI is only guaranteed to work with servers of the same version. The export command for the 1.32 CLI is explicitly incompatible with previous versions.

### Resources

* Metadata for access tokens is now visible to all admins. The token string is only visible to the creator.

### Management and Deployment 

* Management of External Lifecyle (_e.g._ for Connectors) has been enhanced. New `Deploy` capabilities are provided for defining probes and fetching file contents from Vantiq resources. See the [Resource Guide](resourceguide.md#k8s-clusters) for details.

* A new `FetchLogs` operation has been defined on installations. See the [Resource Guide](resourceguide.md#k8s-clusters) for details.

## UI Enhancements

### Modelo
* Modelo supports creating, updating, publishing and installing of Assemblies, which are a special kind of Project that can be reused in other Projects. Assemblies allow developers to construct reusable solutions that can be integrated into Projects with a minimum of configurable properties to easily extend new Project functionality. Please refer to the [Assembly Users Guide](assemblies.md) for a complete description of Assemblies and the [Assembly Tutorial](tutorials/assemblytutorial.md) for examples of how to use Assemblies.

* The IDE Navigation Bar has a new icon to show the number of resources with compilation errors found in the current namespace. Clicking the icon opens the Compilation Errors Pane listing resources with compilation errors. This icon is hidden when no compilation errors exist.

* The Service pane supports Service Event Types from its Events tab. Service Event Types are used to trigger events on other resources (e.g. Sources, Topics, Types) to decouple the implementation of an event from its producer and consumer. For details about Service Event Types, please refer to the [Service Event Types](rules.md#service-event-types) section of the [VAIL Reference Guide](rules.md). In addition, the [App Services Tutorial](tutorials/statefulservices.md) provides examples on how to use Service Event Types.

* Catalog administrators can now specify custom permissions for various Catalog operations (e.g. publish, subscribe, install) for both the Catalog itself and any member Namespaces. More details are in the [Setting Permissions](broker.md#setting-permissions) of the [Vantiq Catalog Reference Guide](broker.md).

* The user interface used in the Management of External Lifecyle has been enhanced.
See the [External Lifecycle Management Guide](extlifecycle.md) for updates.
  
* Project Resource Graph arrows:
    * _Existing projects_ -- the relationship arrows for compiled resources will not show up in the graph for existing projects until they are recompiled with v1.32.  These resources include _Rules, Procedures, Clients, Apps, and CollaborationTypes_. To rediscover the relationships and restore the arrows in the graph, re-save each resource.  Then the relationships and arrows will be rediscovered.  (Note that Apps and CollaborationTypes will also be regenerated with package-names for their generated code.)  See also: [Resource Relationship Model](./resourceguide.md#resource-relationship-model) documentation.
    * _CLI Import_ -- the relationship arrows for _Clients_ that are imported from pre-1.32 export files will not show up in the graph after import using the Vantiq CLI.  To rediscover the relationships and restore the arrows in the graph, change the Client and re-save it.  You can then save and export the project or namespace to update the exported JSON files with the rediscovered relationships.  
NOTE: If you import such clients using Modelo, the clients will be automatically updated with the rediscovered relationships.

* In previous releases the Autopsy Debugger would "decompile" the source code of a Rule or Procedure in order to show the source text and derive the variables. This would often produce a result quite different from the actual source code. (For example, indentation, braces and comments would rarely match the actual source.) In this release the debugging data produced by the server has been enhanced to allow the debugger to use the _actual_ current source code and have more complete information about which variables are currently "in-scope". These changes result in a different look for the Autopsy Debugger which is more consistent with other standard tools (such as the Chrome DevTools debugger). The [Autopsy Debugger Tutorial](tutorials/debugtutorial.md) has been updated to reflect these changes.

* The IDE Navigation Bar has improved responsiveness to accommodate smaller browser windows. Likewise, the VAIL Editor (for editing Procedures and Rules) has been made more responsive and now has two toolbars: the main toolbar and the debugging toolbar. The debugging toolbar is shown and hidden by clicking the button at the far right of the main toolbar and contains features such as enabling tracing and log levels.

* The VAIL Editor has improved autocompletion features to support both [Stateful Services](rules.md#stateful-services) and for `WHEN EVENT OCCURS ON` clauses.

### Client Builder

* The new "Client Components" feature allows you to create your own Widgets which will be added to the Client Builder palette. For details see the [Client Components User's Guide](ccug.md) and the [Client Component Tutorial](tutorials/clientcomponenttutorial.md).

* The Client Builder now supports the ability to convert one type of Layout Widget to another; this feature is accessible through a Layout Widget's context menu.

* [DataTable](cbref.md#datatable) Widgets now support an option that allows the end user to download the data being shown in the table to a CSV or JSON file. This feature must be enabled using the "Show Download Button" option in the "Specific" section of the [DataTable](cbref.md#datatable) property sheet.

* In previous releases the client.getLocation() method was only implemented when running in a mobile device. For testing purposes this method now works in a browser as well (assuming the user has given permission to use "location services" in the browser). 

# 1.31 Release Notes

## Server Enhancements

### VAIL

* VAIL now supports [packages](./rules.md#packages) which can be used to organize an application's code.

* The builtin procedure `Utils.clone` is now deprecated.  Use `Object.clone` instead.

* **Incompatible change**: removed the following deprecated VAIL syntax:
    * Dedicated recommendation keywords `FILTER`, `MATCH`, and `RECOMMEND`.  Note that `FILTER` is still legal when used to process sequences.
    * SQL style block syntax using `DO`, `THEN` and `END` (all blocks must use the JavaScript style `{` and `}`).
    * SQL style variants of the DDL statements `CREATE`, `ALTER`, and `DELETE` (only the JSON style syntax is supported).
    * The `EVALUATE` keyword.
    * The `PUBLISH WITH` variant of `PUBLISH`.

### Catalogs

* Catalog and catalog member resource names are now distinct from the nodes they use. Most of the [catalog procedures](./brokerapi.md#catalog-procedures) have had their parameters changed to accept the catalog's name instead of the node's name.
    * To maintain compatibility with 1.30, catalogs, catalog members, and their nodes have the same names and use the same naming scheme as before. The names will continue to be generated to match until the 1.32 update.

* Catalog service updates now happen by re-registering as a publisher or subscriber.

* Publish To Catalog support was added, as optional parameters within the existing PublishToTopic activity pattern.

### App Components

Components are reusable and parameterizable sections of Apps that solve commonly found problems. Components may be dragged
from the Component section of the App palette and used as a
black box providing higher functionality than any out of the box Activity Patterns. This will significantly improve
developer efficiency for long-time users, reducing the redundant code written between Apps. Furthermore, this will
also lower the barrier to entry for new users.

Components may specify
configurable parameters that users of the Component will provide to tailor the Component to their needs.
Configurations for Components may be augmented using custom Component Generation Procedures.
Components may be created from scratch or by selecting a subsection of tasks within an existing App. Components may be
expanded within an App to visualize the tasks that constitute it or "exploded" to use the internal tasks directly 
(which severs the connection to the original Component).

For more information on Components, reference the [Component Documentation](apps.md#components)

### App Builder

* New [VAIL Activity Pattern](apps.md#vail) allows developers to write a block of custom code to 
  process events.
* The [Procedure Activity Pattern](apps.md#procedure) now supports returnBehavior options to change 
  the way the result of the procedure is used in the outbound event.
* The [Accumulate State Activity Pattern](apps.md#accumulate-state) now supports outboundBehavior 
  options to change the way the state object is attached to outbound events.
* Activity Patterns that support custom VAIL code now support optional 
  [imports](apps.md#dependencies-and-optional-imports), which list the resources referenced 
  in the custom code.  

Compatibility Note: If you use any of the following Activity Patterns and include custom code in the configuration, 
please check for the new imports property and configure it if necessary (e.g. if you save the App and it gets a compile error):
* AccumulateState (inline code variant only)
* Transformation (visual transformation variant only)
* Threshold (if the condition invokes a procedure)
* Filter (if the condition invokes a procedure)
* Dwell (if the condition invokes a procedure)
* Delay (if the interval expression references a procedure)
* Join (if the constraints invoke a procedure)
* Procedure (if a parameter invokes a procedure)
* SplitByGroup (if the groupBy expression invokes a procedure)
* StartCollaboration (if the entityConstraint references a procedure)

### Management and Deployment 

* Added an operation to [update all node URIs](./namespaces.md#updating-the-uri) on an installation, useful if the installation URI changes. Only usable by the system administrator.

* Management of External Lifecyle (_e.g._ for Connectors) has been added.
See the [External Lifecycle Management Guide](extlifecycle.md)
and [Resource Guide](resourceguide.md#k8s-clusters).

## UI Enhancements

### Modelo

* There have been various changes to Modelo in support of the new "package" feature:
    * When creating certain resources there is now a place to supply the "package" as well as the "name" of the resource.
    * The "Project Contents Browser" tree on the left side of a Project will now show packages as part of the hierarchy inside the appropriate resource type. 

* The "Show Documents" list pane can now be sorted by the "created" or "modified" date columns (but these only appear when the pane is maximized).

* The Inactive Panes Dock (when using Tiled Layout Style) is now configured to have a maximum number of ten inactive panes. This maximum may be changed or disabled using the Maximum Inactive Panes value in the IDE Settings dialog. When the maximum is reached, the oldest pane without unsaved changes is removed.

* The "Blacklist" feature has been renamed to the "Exclusion List".

### Client Builder

* **Incompatible change**: it is no longer legal for client names to contain the "dot" (`.`) character.  Any existing client which contains a "dot" in its name will need to be renamed before it can be updated/saved.

* There have been major changes to the structure of the Client Builder. These changes were in service of three goals:

    * Optimize the usage of real estate within the Client Builder and make it easier to temporarily reconfigure the tools to provide maximum working space for your task (e.g., editing Widgets, editing event handler code, etc.)
    * Provide a hierarchical "tree view" of the Widgets in a Page which is in sync with the current WYSIWYG view
    * Make the JavaScript "event handler" editors modeless with respect to the Client Builder and the rest of Modelo, making it easier to refer to other parts within the Project while editing.
    
    For a more detailed discussion of these changes you should refer to this section of the [Client Builder User's Guide](cbuser.md#the-client-builder).
    
* When creating a new Client, the developer now chooses from several built-in templates as a starting point. After creating and editing a Client, the developer may want to use that Client to create similar Clients. The new Client may be saved as a Client Template so that it will appear in the New Client dialog. For more details about using and creating Client Templates, please refer to the [Client Builder User's Guide](cbuser.md#creating-a-client).

* There is a new type of [DataStream](cbref.md#datastream) called "Paged Query" which is intended for use with the [DataTable](cbref.md#datatable) Widget when displaying Types with a large number of records in the result set. When bound to a "Paged Query" the [DataTable](cbref.md#datatable) will only query for the records it needs to display the current page. (This is in contrast to the "Timed Query" [DataStream](cbref.md#datastream) which will load the entire result set into memory.)

* There is now a new "Theme" color called "Title Bar Foreground Color" which applies to these Widgets:
    
    * [DataTable](cbref.md#datatable)
    * [AccordionLayout](cbref.md#accordionlayout)
    * [ListViewer](cbref.md#listviewer)
    * [Calendar](cbref.md#calendar)
    * [Chat](cbref.md#chat)
    * [Signature](cbref.md#signature)

### VAIL Editor

* When editing VAIL in Rules and Procedures, the VAIL editor now supports saving those resources even though they may contain compilation errors. If there are compilation errors, the word **Error** in red appears at the top of the editor and, if possible, the VAIL text causing the error is highlighted within the editor. Hovering the mouse over either **Error** or the highlighted text displays a tooltip with details about the error. If VAIL with highlighted errors is edited, all highlighted errors appearing after the edit point are cleared.

### Client Launcher

* When you run a Client within the Client Launcher, the text of browser's tab will be changed to match the title in the "nav bar". For example, if you change the title using "client.navBarTitle" the browser's tab text will now change as well.

### Deployment Tool

* The Deployment Tool adds a new tree view in the project tab for better visualization of large deployments.
* Deploy results now include details of each resource deployed, records copied, procedure executed, resource activated, and catalog setup status.  Users have the option to see errors only.

### Services

* Users can generate a JavaScript library for a service. Procedures of a service are exposed as JavaScript functions which can be included and used by Clients.
* Users can define Global or Partitioned State Types directly from the Service Pane. Users may reference and edit existing Types, or create a new Type.

### App and Collaboration Builder

* Search box in the Task palette allows users to quickly find the tasks they need
* Suggestions have been improved to include nested Type definitions
* Nodes within the Graph may be collapsed or expanded. Collapsing a node within the App or Collaboration graph hides all children
of that task.
* Publishing an App event to the Catalog now exists as part of the PublishToTopic task

### Test Tools

* Test Output Validation Procedures may either take one parameter, the received event, or two parameters, the received and expected
  event. This allows Validation Procedures to be more widely reusable between outputs.
* Users may delete individual Captures events
* A new REMOVE_KEY transformation value has been added for the specified property of a resource, which will remove the property from all events captured on that resource. 


# 1.30 Release Notes

## Server Enhancements

* [Services](./rules.md#services) -- support for services in VAIL has been substantially enhanced/altered.  Some of the more important changes are:
	* [Private procedures](./rules.md#visibility-modifiers) -- services may declare "private" procedures which can only be invoked from procedures that are part of the service definition.	
	* Interface definition -- the interface for a service consists of all non-private procedures in that service.  The only way to change a service's interface is to add or remove these procedures.  The notion of an "exposed interface" has been removed.  When subscribing to a service it is not possible to alter/augment the supplied interface.
	* State management -- services may declare in-memory state which they are responsible for managing via their interface.
	* [Scheduled procedures](./rules.md#scheduled-procedures) -- services may provide a schedule for the periodic execution of specified procedures.
<p></p>

* [VAIL typing changes](./rules.md#vail-types) -- there have been a number of changes relating to declaration and use of types in VAIL.  Please note that some of these may impact the semantics/behavior of your applications, please contact [Vantiq support](mailto:support@vantiq.com) if you need any assistance.
	* Expanded use of user defined types -- it is now legal to specify a user defined type (UDT) instead of `Object` as the type of a property and when declaring procedure parameters.
	* The VAIL type `Object` is now properly validated when used as the type of a property or parameter.  To be valid the value must be a JSON Object, not just a JSON literal (for example, `String` values are not valid as `Object`).
	* The VAIL type `String` is now properly validated and the appropriate conversions are performed when used as the type of a procedure parameter.
	* The `ARRAY` parameter modifier is now correctly validated when the procedure is untyped or declared with the type `Object` or `String` (it already worked correctly for all other types).
<p></p>

* Support for [required procedure parameters](./rules.md#parameter-modifiers) -- you can declare that a procedure parameter is `REQUIRED` which will verify that a value (including `null`) is provided for the parameter when the procedure is called.

* Support for [default parameter values](./rules.md#parameter-modifiers) -- you can define a `DEFAULT` value for any procedure parameter.  This value will be used whenever the procedure is called without specifying a value for the parameter.

* [VAIL concurrency control](./rules.md#concurrent) -- to support construction of stateful services VAIL now supports the creation of a concurrent map (`Concurrent.Map()`) and a lock (`Concurrent.Lock()`).

* ["Arrow Functions" (AKA lambdas)](./rules.md#lambda-operator) added to VAIL -- it is now legal to define an "arrow function" in VAIL.  These are primarily used by the newly introduced concurrent data structures.

* [Asynchronous procedure execution](./rules.md#asynchronous-execution) -- VAIL procedures can be invoked asynchronously by adding the `async` modifier to the `execute` statement.

* **Incompatible change**: we clarified and corrected some of the checking around [duplicate or overlapping declarations](./rules.md#variable-declarations) in VAIL. The main change is that it is only legal to have duplicate variable or event variable declarations. All other overlaps/variable redefinitions are illegal (e.g. you can't declare a variable with the same name as a parameter). This was always the intended semantics, but it wasn't properly enforced until now.
It is considered a best practice when creating a Vantiq application to use unique names as much as possible.

* **Incompatible change**: [Unicode escapes](./rules.md#escape-characters) were not being handled correctly in VAIL strings: they required an extra backslash before the "\u".
Now only one backslash is required, as intended, e.g. "\u20AC".

* When you do not require type rules for a particular type, you can specify `rulesSuppressed` in the type definition. With the rule processing suppressed, there is a significant improvement in the performance of insert, update, and delete operations against that type. See the [Resource Reference for Types](./resourceguide.md#types) for details.

* Catalogs are now a [resource](./resourceguide.md#catalogs) and, for member Namespaces, can be exported and 
imported to move their registrations between Namespaces (e.g., publishing to an event or subscribing to a service). The resource will be generated for existing catalog connections.
    * When importing projects or Namespaces that include Catalog connections, those connections must be reestablished by providing a current connection Access Token and URL. Use the **Show>Catalogs** menu item to reestablish Catalog connections.

* Vantiq now supports the LUIS version 3 API. The V2 API is still supported, but customers are strongly encouraged to move to V3.

* The BuildPath activityPattern has been deprecated and replaced with _BuildAndPredictPath_.

* Deployment Tool now allows bidirectional access through a firewall, using [named-websocket connections](./resourceguide.md#named-websocket-connection).  

### Testing Tools

* Data Generators have been replaced by _Event Generators_. Event Generators can produce events on Topics, Sources, and Types.
See the [Event Generator Documentation](./eventgenerators.md) for more details.
* Capture allows users to record events as they occur in the Namespace. Captures may be global or targetted for particular resources.
The Captured events may be transformed and exported into Tests or Event Generators to be replayed at will.
See the [Capture Documentation](./capture.md) for more details.

### App Builder
* **Incompatible change**: there is a new restriction to the names of tasks in the App and Collaboration Builders. 
These names now need to be legal Java resource identifiers. The most noticeable change is that the first character of 
a task name cannot be a number, it must be a letter.  Numbers are legal anywhere else in the task name, just not as 
the first character. Existing Apps with tasks that have a numeric leading character will continue to work as long as they are 
unchanged, however updating or importing an App on a 1.30+ system requires fixing the names of the tasks. Updating the 
names to be legal identifiers and saving will fix the error. 

* The Procedure activity pattern has new options to support the service enhancements made in 1.30:
    * You can now specify a list of parameters derived from the inbound event, rather than passing the entire event to the procedure.
    * You can now control the return behavior of the procedure call by choosing one of the three options: use the return value as the outbound event (1.29 behavior and new default), add the return value to a property of the inbound event and emit the combined object, or ignore the return value and emit the original inbound event.

## UI Enhancements

### Modelo

* Operations and Development mode have been merged in Modelo, so the Administer menu is always shown now.
* Menu items previously in the Debug menu are now in the Test menu.
* The Project Layout and Filter settings have been moved to the Project Settings menu. IDE Settings previously under the Preferences menu have been moved to User menu>IDE Settings.
* VCS (Version Control System) menu items have been moved to the Project menu.
* When maximizing a pane, it now resizes to cover only the work area leaving the outer dock areas visible. If you maximize a pane and then open a different one, the new pane will open maximized as well. If you prefer the old behavior (where the pane covers the entire window), there is an option in the IDE Settings dialog, which is located in the User menu found at the right of the Navigation Bar.
* Improved user interface for querying objects such as Records, Errors, Logs, etc.
* The creation and use of [Vantiq Catalogs](tutorials/eventbroker.md) has moved out of the Namespace pane.
	* To create a Catalog in a Namespace, use the **Administer>Advanced>Catalog** menu item.
	* To create new Catalog connections for a Namespace, use the **Show>Catalogs** menu item.
* Support for Stateful Services and new procedure modifiers.
* Services and Documents are now part of a development project. They can be exported, imported and deployed just like other project resources.
* Nested Type support. Type properties and procedure parameters can now use other user-defined type or schema as its type.
* The Document list pane now contains a context menu item that allows you to add a Document to an existing Group.
* When duplicating a Type from the context menu you are now offered the option to switch the role of the duplicate to "standard" or "schema".

### Operations
* For operations-only mode, there is a new Operations entry point that looks & behaves like the old Operations mode:
      [https://dev.vantiq.com/ui/ops/index.html](../../../ui/ops/index.html)

### Client Builder

* In the "Localization" tab of the Client properties dialog there is an option to automatically generate localization symbols for any text that does not already have them.

* In the "Theme" tab of the Client properties dialog there are now options to override the foreground and background colors of the "title bar" area when the Client runs in a mobile app.

* In the "Advanced" tab of the Client property dialog there is now an option to hide the "navbar" when the Client runs in the Client Launcher.

* The Clipboard has been enhanced to remember the last 5 items which were copied to the Clipboard. There is a control in the upper-right-hand corner of the Client Builder that when clicked will popup a pane that shows an image of each clipboard item. You may then drag an item onto the Page (in the same way you create new widgets by dragging from the palette area). This gives you full control of **where** the item will be placed.

* There are now eight new methods on the Client object which provide a streamlined version of some of the Http "server" methods: deleteOne, execute, select, selectOne, insert, publish, update and upsert.

* User-supplied JavaScript may now contain ECMAScript 6 (ES6) language features (e.g. "let", "const", etc.)

* Some of the builtin 3rd party libraries have been updated:
    * JQuery V3.5.1
    * Angular V1.8.0
    * Bootbox V5.4.0
    * moment V2.27.0
    * showdownjs V1.9.1
    * Papa Parse V5.3.0

### Widgets

* The [TabbedLayout](cbref.md#tabbedlayout) widget now supports an "On Page Changed" event.

* The [NumberViewer](cbref.md#numberviewer) widget now supports an "On Click" event.

* The [Checkbox](cbref.md#checkbox) widget now has an option to display in the "classic" style instead of the default sliding button.

* [DataTables](cbref.md#datatable) now support an optional "tooltip" for each of the defined columns.

* The [Checkbox](cbref.md#checkbox), [RadioButton](cbref.md#radiobuttons), [InputObject](cbref.md#inputobject), [Signature](cbref.md#signature) widgets now support an "isReadOnly" property.

* The [DataTable](cbref.md#datatable) widget supports two new event handlers ("On Format Cell" and "On Format Cell Background") which can be used to control the contents and styling of individual cells.

* The [AccordionLayout](cbref.md#accordionlayout) widget now supports a boolean property called "isExpanded" that controls whether the widget is open or closed.

* When the [VerticalLayout](cbref.md#verticallayout) widget is used as a container for [AccordionLayouts](cbref.md#accordionlayout) the boolean allowAllAccordionChildrenOpen property controls whether there can be only one (false) or more than one (true) [AccordionLayouts](cbref.md#accordionlayout) open at the same time.

* The [FixedLayout](cbref.md#fixedlayout) widget now supports "Natural" and "Size to Parent" Size Policies, which you can use to scale the Background image.

* The [StaticText](cbref.md#statictext) widget now can be
    * set to "Multiline" mode (which makes it respect '\n' characters)
    * bound to a [DataStream](cbref.md#datastream).

* The [FloorplanViewer](cbref.md#floorplanviewer) and [FixedLayout](cbref.md#fixedlayout) widgets have new properties to display heatmaps using GeoJSON data.


# 1.29 Release Notes

## Server Enhancements

* Vantiq supports a new type of Catalog: the [Service Catalog](./broker.md#service-catalog).
A service is a collection of Procedures. Each Procedure in a
Service may define a Procedure description, parameters, parameter types (including Schema Types), and parameter descriptions.
Services may be published to the Catalog, and other Namespaces may subscribe to them. Namespaces that subscribe to
Catalog Services have access to the Service Interface and may execute the Procedures as if they were defined in the current Namespace. See the [Catalog Tutorial](./tutorials/eventbroker.md) for more information.

* Added [motion tracking](imageprocessing.md#motion-tracking) support via activity patterns and service.
Find motion for entities output from YOLO activities.

* **Feature Removal** - it is no longer possible to enable logging for any of the Vantiq built-in services or procedures.

* `Processed By` now allows limits on the number of nodes selected, using the [EXACTLY ONE semantics](rules.md#limiting-number-of-remote-targets).

* Defaults for DateTime properties can be set to "now", which will set the field to the moment the instance was created.

* The `direction` property in sources has been deprecated.

* Users may now remove themselves from Namespaces regardless of their permissions there.

* `NOT` is now allowed in query constraints.

* Nodes are no longer exported as metadata in the CLI.

* Message count usage data now available to organizations via the `system.messagecounts` type.

## UI Enhancements

* Project Views - You may now organize your large Projects by creating custom "Views" to display a subset of the resources. More detail may be found in the [IDE Users Guide](ide.md#project-views).

* Enhanced UI and features for App and Collaboration Type Builders
    * Added a drag-and-drop palette of Activity Patterns and Services on the left side of the Builders. Developers may now add tasks to their App or Collaboration type by simply dragging palette items onto existing tasks or links between tasks.
    * Added Undo, Redo and Delete buttons and functionality for graph operations such as adding or deleting tasks.
    * The task property sidebar to the right of the graph now slides into view whenever a task is selected and slides out of view otherwise. The App or Collaboration Type properties, such as name and description, that used to appear in the property sidebar may now be set using the Properties button which is found above and to the right of the graph.

* Service definition and publishing tools available to describe Services to be published in the [Service Catalog](./broker.md#service-catalog).

* Provided collapsible [code folding](https://en.wikipedia.org/wiki/Code_folding) features in IDE editors for JSON objects, and JavaScript and VAIL code.

* There is now support for giving "Type" properties a default value.

* Deployment has a new option to include Tests and Test Suites.

* Standardized, expanded and documented keyboard shortcuts for operations throughout the IDE. See the [IDE Users Guide](ide.md#ide-shortcut-keys) for more details.

* Resources which have been explicitly removed from a Project will no longer be automatically added back in just because another Project resource points to them. Instead they will be added to a "blacklist" which prevents them from re-appearing in the future. Simply adding them back into the Project explicitly will remove them from the blacklist. (Or you can use the "Manage Blacklisted Resources" dialog in the "gear" settings menu found in the upper-right-hand corner of the Modelo window.)

* Improved Version Control System (VCS) integration by reducing the number of inconsequential merge changes.

* Automatically provide default parameters for some built-in service tasks in the Collaboration Builder.

* View Errors as a stack trace in single pane. This is for errors that occur in an inner procedure call and propagate up to the outermost rule or procedure call. All those errors will show up as a single error and the inner errors will be shown in a stacktrace list in that error pane. Note that inner errors from a stacktrace will no longer show up on Live Errors or the Error Query Results pane; only the outermost error will be shown in those panes.

# 1.28 Release Notes

## Server Enhancements

* Support for embedded [escape sequences](./rules.md#escape-characters) in VAIL strings

* Support for [Public Resources](./api.md#public-resources): can now create public Clients and Procedures

* Self-serve registration for consumer apps is possible using Public Clients

* Tools for testing applications are now available. Test Suites and Unit Tests can be created quickly and run interactively or automatically. This allows more of the Software Development Lifecycle to be used within the Vantiq system.

* Upgrade support for AMQP 1.0 (with ActiveMQ, not RabbitMQ plug-in).
This also supports Azure Service Bus and Event Hubs (but not Service Bus Sessions).

* TensorFlow module now supports Yolo V3 and Plain old TensorFlow models.

* CLI now supports Client Options and Namespace in profile settings and namespace & trustAll parameters.

* Statistics ActivityPattern: Starting with R1.28, the statistics event stream will NOT emit the first event that hits the stream. The correct behavior is to only output at the end of each interval. Since you will no longer see an output at the start of each interval, you may not see data as quickly as you did with R1.27.

* **Major Bug Fixes**
	* Values stored in properties declared as "String" will now be properly validated and converted. Currently if you store data in a property of type "String", that data is actually persisted in its original form. This means that if you set a "String" property to non-string value (such as an Integer) then the value of the property would retain its original type, both in the database and when subsequently retrieved from the database. Starting in 1.28 this has been corrected and the data will now be converted from its native type to String (assuming such a conversion exists). This may have an impact on existing applications which may need adjustment/correction. Possible impacts include (but are not limited to):
		* **Use of the property in numeric expressions** -- if the data stored was of a numeric type (Integer, Real, Decimal, Currency), then previously the property could be used in a numeric expression (because it was not converted). Now that the data is properly converted to String these expressions will fail, since String values cannot be used in that way.
		* **Storage of Object data** -- if the data being stored was of an object type (Object or GeoJSON), this will now fail when an attempt is made to insert/update such data, since there is no implicit conversion between Object and String.
	* VAIL Integer values will maintain their native type, even when serialized. In VAIL, Integer values are 64 bit integers represented in memory as the Java Long class (or its primitive form, long). There were times in the current system when these values might be implicitly converted to Integer/int values due to data being transmitted from one member of a Vantiq cluster to another. These conversions have been eliminated, so values should retain their initial format. This also applies to all integer values in parsed JSON data, whether that comes from a Vantiq Source or is parsed explicitly using the VAIL built-in procedure `parse`.

## UI Enhancements

* The Modelo interface has undergone a major upgrade to make it feel more like traditional IDEs. Among other changes:
    * There is now a collapsible _Project Contents Dock_ on the left side of the window that allows the display of the resources owned by the current Project. These can be shown as various types of trees and lists.
    * There is now a collapsible _Debug Dock_ at the bottom of the window that will show a live display of the newly arriving Errors, Autopsies and Log Messages.
    * The _Inactive Panes Dock_ (which is used to manage the currently open and inactive panes) can now be configured to appear at the top or right edge of the window.
    * Most lists and trees which used to have "Action" buttons in each row now show those buttons dynamically. As you hover over a row a "three dot" icon will appear at the right edge which can be "left-clicked" to bring up a context menu containing the actions. You can also "right-click" anywhere on the row to bring up the same menu. (If you prefer, this can be configured from the IDE Settings to simply display all action buttons when hovering ('Dynamic Action Buttons').)
    * Resources shown in the Project Resource Graph have new context menu items that allow you to highlight various kinds of "neighbor" nodes, making it easier to see relationships.

   
<p></p>
 
* Support for [Public Resources](./api.md#public-resources) and [Public Clients](./cbuser.md#public-clients). (Clients are marked Public in the "Advanced" tab of the Client Properties dialog.)

* The "client" object now offers a set of new API methods to allow you to programmatically execute actions that used to require a Widget. For example, instead of using a [Camera](cbref.md#camera) widget you could now call [client.takePhoto()](cbref.md#takephoto) to ask the user to take a picture. 

* The [HorizontalLayout](cbref.md#horizontallayout) and [VerticalLayout](cbref.md#verticallayout) containers now provide a way from their property sheet to make their "cell" sizes manually adjustable by the user.

* A new type of Widget called [TabbedLayout](cbref.md#tabbedlayout) lets you arrange children in a classic "tabbed page" container Widget.

* [StaticText](cbref.md#statictext), [StaticImage](cbref.md#staticimage) and [MenuButton](cbref.md#menubutton) Widgets have a new property to set their angle of rotation called 'rotationInDegrees'.

* The [StaticImage](cbref.md#staticimage) Widget now supports more "Size Policy" options (widthPolicies of Explicit, NaturalSize and SizeToParent and heightPolicies of Explicit and NaturalSize.) There is a new boolean property called 'preserveAspectRatio' which defaults to 'true' that controls whether the image will stretch out of shape when forced to a size that doesn't match the image's aspect ratio. (These new features make the "isScaleable" property obsolete so it no longer appears on the property sheet.) StaticImages should now reload more smoothly at runtime with less flicker.

* The WYSIWYG HTML editor for the [StaticHtml](cbref.md#statichtml) Widget is now using a different 3rd-party implementation. The property sheet also now provides a way to bypass the WYSIWYG editor and edit the raw HTML directly.

* The [DocumentViewer](cbref.md#documentviewer) Widget now automatically caches the contents of each resource on your mobile device the first time you access them. (This means they will be available in "offline mode" in the future.) You can also load such assets into the document cache proactively by specifying them in the Client Builder. Details may be found in the documentation on [Offline Operation](cbuser.md#offline-operation) and [Automatic Document Caching](cbuser.md#automatic-document-caching).

* [DataTables](cbref.md#datatable) now offer a way in their "onClick" events to access a JQuery selector for the row and column DOM elements that were clicked. (See the documentation for the various "click" events for [DataTables](cbref.md#datatable).)

* App Builder now supports Show Task Events in the main App Builder window (for the focused task).

* Deployment Tool New features
    * [Undeploy](deploymentuser.md#undeploy)
    * [Display historical Deploy and Undeploy status](deploymentuser.md#deploy-results-tab)
    * [Manual redeploy on failed nodes](deploymentuser.md#redeploy-on-a-failed-node)
    * [Reliable Deployment](deploymentuser.md#reliable-deployment)
    * [Create project on target node to hold deployed resources](deploymentuser.md#verify-application-after-deployment)
    

**Note for users of the "Sync project to VCS " feature**

If you have been using the "Sync project to VCS" directory feature in Modelo you may have noticed that the process of diff'ing and merging Projects is complicated by the presence of various timestamps in the Project JSON file.

In order to avoid the extra work caused by these timestamps when merging Projects they **will be removed** from the Project JSON file when using the "Sync project to VCS directory" feature. This should make the process of manually merging diff's less difficult.

The consequences of omitting these timestamps should be minor -- the Inactive Panes list might be resorted and Projects might load more slowly.

These timestamps are still preserved when doing a normal "save" within your Namespace or an "export" of the project -- only the "Sync project to VCS" directory feature is affected. You should note that the first time you use this feature it will still generate diffs, since an older version of the Project will still have the timestamps. But you can either accept or reject them all; eventually all "synced" projects will have been saved without the timestamps and the diffing process should become simpler.


## Vantiq Mobile Apps

* The Android v3.x mobile app supports Android 6.0 and later.
However, v3.x **does not** support Android 7.0 when using the Vantiq public cloud servers (e.g. api.vantiq.com). Android 7.1 and later are fully supported for all Vantiq server installations.
* The iOS v3.x mobile app supports iOS 11 and later

## Vantiq Testing Tools

Testing Tools are now available to build Event Driven Tests from within the Vantiq IDE. 
Tests are capable of simulating and validating every type of event that may occur within the system including
publishes to Topics, interactions with Sources, operations on Types, and executions of Procedures. 

The new Testing Tools support:

* Building [Unit Tests](./tests.md#unit-tests) for Rules and Procedures
* Building [Integration Tests](./tests.md#integration-tests) for Application wide Testing 
* Building [Test Suites](./tests.md#defining-a-test-suite) to run collections of Tests

The Testing Tools also support [Source Mocking](sources/source.md#source-mocking) to help drive Tests dependent
on Source events. Source Mocking allows you 
to Mock incoming Source messages as well as override the source's publish and query behavior with a Procedure.

# 1.27 Release Notes

## Server Enhancements

* There are new [App Builder](apps.md) Activity Patterns for interacting with Shared Memory:
    * [DeleteFromSharedMemory](apps.md#delete-from-shared-memory)
    * [GetFromSharedMemory](apps.md#get-from-shared-memory)
    * [SetInSharedMemory](apps.md#set-in-shared-memory)

	These patterns use the [Shared Memory procedures](rules.md#shmem).
	Note that the Shared Memory patterns only show up if the feature is enabled for your organization.
	<p></p>

* New properties have been added to Node Templates to support [Bootstrapping of edge nodes](config.md#bootstrapping) behind a fire wall. [Bootstrapping](config.md#bootstrapping) can create a user-defined Namespace and pull resources from Configurations and Deployments.

* (CLI) The loading of tensorflowmodels can now be resumed when interrupted. This is described in more detail [here](cli.md#load).


* (CLI) Export data feature now supports exporting larger datasets as well as specifying the new flags _until_ and _exclude_. More detail can be found [here](cli.md#export).

* (CLI) Select statements may now specify a qual file that will restrict the rows selected to those that pass the _qual_. More detail can be found [here](cli.md#select).

* Reliable messaging is now supported over web-socket subscriptions. Subscriptions may be flagged as persistent and re-established
if the connection breaks for any reason. [here](reliability.md###Reliability-in-Third-Party-Applications). 

* Performance enhancements for Pronto message forwarding from publishers to subscribers

* A new [Google Cloud Pub/Sub (GCPS) Source](https://cloud.google.com/pubsub/docs/). This source allows users to send and receive messages using Google Cloud Pub/Sub, and is described in more detail [here](sources/gcps.md).

* More detailed performance data can be gathered for rules, apps, and procedures by enabling *profiling* using profiling [Debug Configuration](resourceguide.md#debug-configs) type.

## UI Enhancements

* It is now possible to run a custom branded version of Modelo in a private cloud server. This capability (also known as "white-labeling") is described [here](idebranding.md). This primarily gives you the ability to change default styling and icons used in the "nav bar" at the top of Vantiq windows.

* Modelo now supports the Chinese (zh) and Japanese (ja) locales.

* Hitting Ctrl-Click (Windows) or Cmd-Click (Mac) on certain words in a VAIL editor will make the editor try to do something helpful:
    * If the word is a built-in Procedure or VAIL term the appropriate documentation will be opened in a new browser tab.
    * If the word is an existing Procedure, Source or Type in your Namespace the resource will be opened in a new pane.
    * If the word is a Procedure, Source or Type that does not exist then a resource creation pane will be opened using the indicated name.
<p></p>

* There is a new option called "Zoom to Fit" on Pages with a "Single" layout type. This will cause the Page and all the Widgets it contains to be automatically scaled to fit the available space. (This means the Page will be scaled to be as large as possible without requiring scrollbars and without changing the aspect ratio.) This is especially useful in conjunction with the new [FixedLayout](cbref.md#fixedlayout) container described below.

* There is a new container Widget called the [FixedLayout](cbref.md#fixedlayout) which does not change the position of its children; it leaves them at the location where you positioned them. It also has all the same capabilities as the [FloorplanViewer](cbref.md#floorplanviewer) in that you can show a background image and show "markers" based on data flowing in from a DataStream. This makes it suitable to use as a more fully-featured version of the [FloorplanViewer](cbref.md#floorplanviewer) since it can show regular Widgets as well as markers over its background "map". 

* A new Widget called a [StaticIcon](cbref.md#staticicon) can display a single "glyph" using the builtin set of "fontawesome" and "bootstrap" icons.

* A new Widget called a [Canvas](cbref.md#canvas) allows you to draw into an HTML5 "canvas" element to create your own custom graphics.

* DataStreams can now be "paused" and "resumed" at runtime using the boolean [isPaused](cbref.md#ispausedboolean) property.

* DataStreams can now be reconfigured at runtime using several new Client methods:
    * [modifyClientEvent()](cbref.md#modifyclientevent)
    * [modifyDataChanged()](cbref.md#modifydatachanged)
    * [modifyPublishEvent()](cbref.md#modifypublishevent)
    * [modifyResourceEvent()](cbref.md#modifyresourceevent)
    * [modifySourceEvent()](cbref.md#modifysourceevent)
<p></p>

* The "On Client Event" DataStreams now support the "Group By" property.

* The ['client.goToPage()'](cbref.md#gotopage) and ['client.returnToCallingPage()'](cbref.md#returntocallingpage) methods now support a new parameter 'transitionDuration' which controls the elapsed time in milliseconds of the transition effect (if there is one).

* There are no longer any Modelo tools that open as "full screen"; all tools are now standard panes (which can always be "maximized" if you want them to take over the whole screen). The "Type" and "Source" panes have been reorganized to allow editing of all properties.

* All Modelo "list panes" that display data from a server query (such as the "Find Record Results" pane) now include a "go to record" input field that allows you to jump directly to the page containing a specific record number.

* "Media" Widgets that upload data directly to a Vantiq Document (such as the Signature, Camera and VideoRecorder) now allow you to specify an associated [Group](resourceguide.md#groups) name. When a Document is created it will be added to the [Group](resourceguide.md#groups), which allows you to control which users will have access to the Document.

* Modelo now tries to remember which Project was last open in a Namespace so you will usually not have to reselect it if you switch between Namespaces. (This information is saved locally for a specific Browser.)

* The FloorplanViewer Widget now has two new method calls to remove markers from the display at runtime:
    * [removeLocationByKey()](cbref.md#removelocationbykey)
    * [removeLocationsByType()](cbref.md#removelocationsbytype)
<p></p>
  
* A helper method ['client.clone()'](cbref.md#clone) has been added to make copies of various kinds of objects and values.

* Enabling debug mode for apps and collaboration types now enables profiling as well as debug logging.

* You can now turn profiling on and off for all resources in a project from the 'Manage Projects' popup.

* A log level filter has been added to the "Live Log" pane; only logs at or above the selected level will be displayed.

* Connections between tasks in an App that are split by an upstream SplitByGroup task now show up as blue lines.

* In the Modelo Deployment Tool you can now specify "deploy" parameters on the "default" partition to support pulling a deployment from an "edge" node. There is also now an "update" button to make the deployment be in sync with the updated Project.

* The internal ZingChart libraries embedded in Modelo have been upgraded to version 2.8.7.

## Special Notes
* [Debug Configurations](resourceguide.md#debug-configs) now expire by default 2 hours after creation. Existing debug configurations created prior to the release of 1.27 will expire 1 week after a system is upgraded to 1.27.
