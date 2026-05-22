# Client Components User's Guide

## Introduction

Client Components are a feature of the Client Builder that allows you to build your own custom Widgets. All the Client Components which are saved into a Namespace will appear on the Client Builder's Widget palette alongside the builtin Widgets. Components can contain more than just Widgets; they can also carry other Client Builder objects inside them to support the Component's purpose:

* Pages
* Data Streams
* Localizations
* JavaScript Assets
* CSS Assets

This document explains Client Components from two different perspectives:

* The "Author" of a Component, who needs to know how Components are created, edited, configured and saved.
* The "Consumer" of a Component, who needs to know how a Component can be used inside a Client. This means both how they are configured when being edited within the Client Builder and how they can be controlled at runtime.

A common purpose for Components is to use them to build a "wrapper" around 3rd-party JavaScript libraries or plugins, allowing you to extend the builtin Widget set. Components can also be used to capture and generalize common UI patterns you use inside your Clients, and make them available to be reused and leverage in other Clients.

The [Client Component Tutorial](tutorials/clientcomponenttutorial.md) walks you through the process of creating a Component.


_A note on names:_ Keep in mind when reading this document that the name of a **Component** is not the same thing as the name of a **Widget** that embodies an **instance** of the Component inside a Client. For example, an Author might build a generic Component called "MyGauge". The Consumer of this  Component might drop 3 instances of "MyGauge" into their Client. Each instance of the Component is a separate Widget, and the Consumer can give each a separate name (e.g. "EngineTemp", "OilPressure" and "ExhaustTemp"). The name of the Component and the name of a Widget which instantiates it are not the same thing.


## Creating a Component

Components are saved into a special kind of Client that contains only the parts the Component needs to operate. All these special Clients in a Namespace will result in a palette entry when using the Client Builder, which allows you to drop them into a consumer's Client.

A Component author can create a Component Client in 2 different ways.

### Create an empty Component from scratch

The "Add / Clients" dialog contains a "New Component" button. You will be asked to supply a name for the Component and a special Component Client will be created. This Component will initially be empty, ready for the author to start adding Widgets.


<p><img style="border-style:solid;" width="700" alt="Add Client Dialog" src="../assets/img/ccug/addClient.png" title="Add Client Dialog"></p>


### Create a Component from an existing Layout Widget

An author can also create a Component by using an existing Layout Widget as a starting point. It will often happen that while developing a Client you will realize that some fragment of the Client would make a useful Component. Since a Component is just a single complex Widget, you simply select the Layout Widget which contains fragment you want to capture. (If the functionality you want is not already contained within a single Layout you must create one and move all the Widgets inside.)

Here's a simple example that contains a GridLayout with some Widgets and code to add two numbers and display the result.


<p><img style="border:none;" width="700" alt="Create Component Candidate" src="../assets/img/ccug/beginEdit.png" title="Create Component Candidate"></p>

After selecting a Layout Widget you will see a "Create Component" button appear in the toolbar at the top of the Client Builder pane. 


<p><img style="border:none;" width="700" alt="Create Component Button" src="../assets/img/ccug/createComponent.png" title="Create Component Button"></p>

Clicking that button will ask you for a name for the Component and create the special Client which will contain it.

<p><img style="border-style:solid;" width="400" alt="Prompt for Component Name" src="../assets/img/ccug/askForName.png" title="Prompt for Component Name"></p>


Clicking "OK" will save the new Component and open a Client Builder to edit it. (Notice that now the Client Builder just contains your "wrapper Widget" within a "Single" layout.)

<p><img style="border:none;" width="700" alt="Edit Component" src="../assets/img/ccug/editComponent.png" title="Edit Component"></p>


**_Important_** - Client Components often depend on other assets than just the Widgets inside them. When you create a Client Component in this way it is impossible to know **which** assets from the original Client are required by the new Component and which are not. Unfortunately this means that the Client Builder must copy **all** the assets into the new Client Component, and then it becomes the responsibility of the Author to clean up, deleting any of the assets which the Client Component does not actually require.

After the new Client Component is created you should review the assets which were added and delete any which you don't need. Here are the assets you should check:

* Pages
* DataStreams
* Global Localization Symbols
* CSS Assets
* JavaScript Assets
* Offline Assets
* Document Assets


## Editing a Component

The author edits a Component using the Client Builder, which runs in a special mode when editing a Component instead of a Client. There are variety of changes to the behavior that we will cover as we go.

A simple Component appears as if there is only a single "Start" page in the "Single" Layout Type. The outermost Widget is the "wrapper" that contains all the parts of the Component. If you created this Component from scratch this wrapper will be a VerticalLayout by default. If you prefer a different type of Layout you can use the context menu to convert it to a different type (GridLayout, HorizontalLayout, etc.) When the consumer drops your Component into a Client it is only this outer "wrapper" Widget which will be directly accessible when editing. (The "Start" Page itself is just a shell that is left behind when you drop the Component into a Client.)

A more complex Component may want to open or popup additional Pages; simply add them to the Component as needed and they will be carried along with the Component into the consumer's Client.

A Component is rather like a Class; it contains internal state and methods which allow the consumer to operate on it; it is up to the author to decide what to reveal. Unless the author exposes a more elaborate interface all the consumer would be able to do is to click on the Widgets inside the Component at runtime. The author creates a Component's interface by specifying a "Configuration".

When editing a Component you can open its "Component Properties Dialog"; this is similar to the "Client Properties Dialog" for a regular Client. 

<p><img style="border-style:solid;" width="700" alt="Component Properties Dialog" src="../assets/img/ccug/compPropDialog.png" title="Component Properties Dialog"></p>




The "Basic", "Events" and "Localization" tabs are similar to those found in the Client Properties Dialog (but with some irrelevant things removed). There is a new important tab called "Configuration".

### Component Configuration

As we noted above, a Component is a black box with no interface (except the visible Widgets) unless the author gives it one. This is done using the "Configuration" tab of the "Component Properties Dialog". In a sense you are simply defining an object whose properties represent the internal state and external interface of the Component. At runtime an instance of this object (also known as the "configuration") will be created for each instance of the Component. (The consumer can gain access to this object at runtime with the Component Widget's "configuration" property.) The author's job is to define all the properties and methods they want the configuration to contain.

<p><img style="border-style:solid;" width="700" alt="Component Configuration" src="../assets/img/ccug/emptyConfig.png" title="Component Configuration"></p>

There are five kinds of properties that can be defined within the configuration:

#### Widget Properties

When a consumer drops a Component into their Client while editing they will not be able to select or change the properties of any of the Widgets that live inside the Component. These are part of the internal implementation of the Component, and so the consumer can't change any of their properties directly, either while editing or at runtime. But the author may decide it makes sense to **expose** some of these properties so the consumer **can** affect them directly. Suppose for example the Component contains a button whose label says "Add". If they want the consumer of the Component to be able to override that label and change it to something else they can expose it by adding a "Widget Property" to the Configuration. Properties are being exposed by selecting the Widget and then clicking the little "+" sign that appears to the right of each property in the property sheet. That will add a Widget property to the configuration which will be bound to the selected Widget; it will be accessible to the consumer at both edit time and run time.

<p><img style="border:none;" width="700" alt="Adding a Widget Property" src="../assets/img/ccug/plusBtn.png" title="Adding a Widget Property"></p>


Now the Configuration for the Component will show the added property:

<p><img style="border-style:solid;" width="700" alt="Property Added" src="../assets/img/ccug/propAdded.png" title="Property Added"></p>

The author can edit the "Name" of the property and click the "pencil" icon to enter a description that will tell the consumer what this property does.

Since the property has been exposed in the Component's configuration the consumer can gain access to the property at runtime. If an instance of "MyComponent" has been given the name "MyComponentWidget1" they could do something like this:

```js
    var cmp = client.getWidget("MyComponentWidget1");
    cmp.configuration.buttonLabel  = "Sum the numbers";
```

This is the only way the consumer can get access to the Configuration, because the "component instance widget" that embodies it is the only thing they can touch. But when the **author** is writing the implementation of a Component they have access to all the actual widgets hidden inside, and any one of these can also be used to get access to the Component's configuration object that they all share.

#### Synthetic Properties

Synthetic properties are simply data values with one of these types:

* Boolean
* Color
* Integer
* Real
* String
* JSON

You add one by clicking the "Add Property" button then setting the Name, Type and Default values. These properties don't actually have any meaning unless the author uses them somehow in the operation of the Component. They can be used to convey information between the consumer and the Component. For example, the Component might set one of these values at runtime so the consumer can refer to it, or the consumer might set a value to tell the Component how to operate. The author decides how they are used.

For example, perhaps the Component allows the consumer to set some value the Component will use in some calculation:

```js
    var cmp = client.getWidget("MyComponentWidget1");
    cmp.configuration.temperatureThreshold  = 120;
```

These values can be bound to Widgets in a similar fashion to client.data.&ast; or page.data.&ast; values. For example, suppose your Component contains an InputInteger Widget. The author could set the Widget's _Data Binding_ property to "_configuration.temperatureThreshold_" so the Widget would always show the current value.

The consumer could do the same thing using a slightly different syntax. They could set the _Data Binding_ of one of their InputInteger Widgets outside the Component to "_MyComponentWidget1.configuration.temperatureThreshold_". 


#### Call-In JavaScript Functions

In the same way that a Class can expose methods that operate on the internal state of an Object, the Component Configuration allows an author to expose functions which can be called by the consumer. To expose a function, the author clicks the "Add Property" button and then defines it this way:

First set the Name of the function (e.g. '_add_') and set the Type to "_JavaScript Call-In Function_":

<p><img style="border-style:solid;" width="700" alt="Call-In Function Added" src="../assets/img/ccug/callinFcn.png" title="Call-In Function Added"></p>

Next declare the names of any function parameters. This is done by clicking the icon to the left of the pencil which pops up a dialog that lets you specify a comma-separated list of parameter names (e.g. '_a, b_'):

<p><img style="border-style:solid;" width="700" alt="Declare Function Parameters" src="../assets/img/ccug/fcnParms.png" title="Declare Function Parameters"></p>

Last click "_Click to Edit_" in the "Default" column to specify the body of the "add" function. (Note that the definition of the function will always contain a 'client' and 'configuration' parameter, followed by any parameters the author specified.)

<p><img style="border-style:solid;" width="700" alt="Edit Function Body" src="../assets/img/ccug/defineFcn.png" title="Edit Function Body"></p>


#### Callback JavaScript Functions

Sometimes it can be useful for the Component to call back into code provided by the consumer. This might be used like a primitive "event" notification, telling the consumer's Client about some change in state. Or it might be used to ask the consumer's Client to provide some information at runtime that the Component needs to operate.

To do this the author can declare a "Callback JavaScript Function" which the consumer can choose to override. (If the consumer does not override the callback then it appears to the consumer as if it simply returned "null".)

To declare a callback function the author clicks the "Add Property" button and then defines it this way:

1. Set the "Name" of the function (e.g. 'onHighTemperature')
2. Set the Type to "JavaScript Callback Function"
3. Declare the names of any function parameters. This is done by clicking the icon to the left of the pencil which pops up a dialog that lets you specify a comma-separated list of parameter names (e.g. '_a, b_')

At runtime the Author's component code could invoke the callback when appropriate like this:

```js
    var result = this.configuration.onHighTemperature(100);
```

Note that **all** Widgets inside the Component can always access the configuration using the "configuration" property. The only way to tell if the consumer overrode the callback or not is to check the "result" - if it's "null" then you can assume the consumer didn't provide an override.


#### Data Streams

By default when the definition of a Client Component includes a Data Stream it is only available internally to the Component itself. That is, consumers of the Component don't have access to it; it is part of the "black box" that is the Component's implementation. Remember that there is only one instance of this Data Stream that is shared by all instances of the Component; if you want each instance of a Component to have its own separate Data Stream you must allocate one dynamically at runtime. (See [Dynamic DataStreams](#dynamic-datastreams) below.)

There is another option to managing Data Streams - you can create a Data Stream configuration property. By default you can choose to bind this to one of the Client Component's statically defined Data Streams. But since it is exposed as a configuration property the consumer of the Client will have the option to override this to point to a DataStream of their own. In this way they could choose to have each instance of a Client Component to use a separate Data Stream of the consumer's choosing.

#### Hidden Properties

By default all the properties the author defines in the configuration are accessible to the consumer within the configuration and will appear in the property sheet for the Component. If some of those properties represent internal state, you might want them to **not** show in the properties, and you can do that by clicking "Hidden".

Note that this does not prevent the consumer from reading or modifying those values if they know they exist, it just hides them on the property sheet. 

#### The builtin "root" property

The configuration contains a special builtin property called "root" which will point to the topmost Widget of the Component. This means that in an event handler for Widgets inside the Component you can always reach the "topmost" Widget with

```js
    var theComponentWidget = this.configuration.root;
```



### Events

The outer Widget of a Component has several special events which the author can listen for and act on. These can be edited from the Events section of the wrapper Widget's property sheet or the "Events" tab of the Component Properties dialog. (These events are only for the author - they can't be seen or edited by a Component's consumer.)

#### On Component Start

A Component instance may require initialization, analogous to the way a Page can use the "On Page Start" event to initialize the state of Page. After the "On Page Start" for a Page is executed, the system will run all the "On Component Start" handlers for any Components on the Page. A common use for this event would be to do any last-minute initialization of the Component instances configuration object.

#### On Component End

A Component instance may require cleanup, analogous to the way a Page can use the "On Page End" event to finalize the state of Page. Before the "On Page End" handler for a Page is executed, the system will run all the "On Component End" handlers for any Components on the Page. 

#### On Component Assets Loaded

The Client may use the "On Assets Loaded" handler to defer certain initialization until all the JavaScript and CSS assets have completed loading. Some Components may require special processing as well, so after the "On Assets Loaded" handler for a Client is executed, the system will run all the "On Component Assets Loaded" handlers for all the Components within the Client. 

#### On Component Network Status Changed

The Client may use the "On Network Status Changed" handler to take action on a mobile device when the status of the network changes. Some Components my require special processing as well, so after the "On Network Status Changed" handler for a Client is executed, the system will run all the "On Component Network Status Changed" handlers for all the Components within the Client.



### Related parts

A simple Component (such as Calculator, for example) consists only of a collection of Widgets. More complicated Components might rely on other items as well. These other "parts" are packaged with the Component and are merged into the consumer's Client when the Component is added. In some cases these parts are hidden from the consumer and in some cases they are not. In the case of Pages, Data Streams and Localizations (described below) their names will be prefixed with "&lt;componentName>__" to avoid naming conflicts with the consumer's Client. (The author does not need to be concerned with this renaming - they should simply refer to the parts with their original name and the system will remap the names automatically.)


#### Pages

When editing a Component, the Client Builder shows it as if it is the sole occupant of the "Start" Page. But this "Start" Page is just a shell and will be left behind when the Component Widget and its contents are dropped into one of the consumer Client's existing Pages. However, a Component might require additional Pages of its own - for example the Component might want to open a Page as a Popup to prompt for additional information from the user. When the author builds and edits the Components, they simply add these extra Pages as needed and the Pages will be added to the consumers Client.

These Pages will be hidden from the consumer - they will not show up in the Client Builder and cannot be edited. If the consumer drops multiple instances of the Component into their Client, each instance will share the same hidden Pages. When the last instance of a Component is deleted from the user's Client, all the hidden Pages will be deleted as well.

#### Data Streams

A Component can include Data Streams which will be automatically added to the consumer's Client. These Data Streams are hidden inside the Component and the consumer cannot affect them. However, the author may decide to grant the consumer the ability to override such Data Streams with one of their own. 

For example, suppose the Component contains a GaugeWidget which is bound to a DataStream. The author could decide to expose the "DataStream" property of the Gauge Widget so it is visible in the Component's Configuration. In this case the consumer would be able to replace the DataStream by overriding it with one of their own, using the Component's property sheet.

These Component Data Streams will be hidden from the consumer - they will not show up in the Client Builder and cannot be edited. If the consumer drops multiple instances of the Component into their Client each instance will share the same hidden Data Streams. When the last instance of a Component is deleted from the user's Client all the hidden Data Streams will be deleted as well.

#### Dynamic DataStreams

As discussed above you may add a DataStream to a Component, but it is important to realize that all the instances of the Component will share the DataStream at runtime. This may be what you want, but if you need each Component instance to have its own separately configured DataStream then you may want to use "dynamic DataStreams" instead.

In this approach each Component instance will create and configure its own DataStream at runtime (probably in the "On Component Start" event handler). This is done using one of the appropriate Client methods, such as [client.createClientEventDataStream()](cbref.md#createclienteventdatastream). You can define your own "On Data Arrived" method using [addEventHandler()](cbref.md#addeventhandler). For appropriate [DataStreamWidgets](cbref.md#datastreamwidget) (such as the [NumberViewer](cbref.md#numberviewer)) you can bind to the DataStream by setting [dataStreamUUID](cbref.md#datastreamuuidstring) and the appropriate DataStream property name (such as "dataStreamProperty").

This would allow each Component instance to have its own unique DataStream rather than share a common one.


#### Localization

Just as with a normal Client, an author can supply "localizations" for all the text used by the Component. These localizations will be merged into the consumer's Client localizations (if any). The message keys will automatically be prefixed with "&commat;&lt;componentName>&lowbar;&lowbar;" or "$&lt;componentName>&lowbar;&lowbar;" as appropriated to avoid name conflicts.

These Component Localizations will **not** be hidden from the consumer - they will appear in the Localization tables alongside the consumers messages.
When the last instance of a Component is deleted from the user's Client all the Component localizations will be deleted as well. If the consumer "exports" the localization messages from their Client, the Component message keys and values will appear in the files also.

#### JavaScript and CSS Assets

When building a Component the author can include JavaScript and CSS "Custom Assets" just as with a regular Client. (If the purpose of a Component is to provide a "wrapper" for some 3rd-part Widget or plugin this would probably be required.)

These assets will **not** be hidden from the consumer; they will be merged into the consumers Client alongside any existing assets. Only a single copy of an asset (based on the name) can be included, so no matter how many Components attempt to request an asset it will only appear once. Because it is impossible to know whether code depends on an asset, assets will not be automatically removed with the last instance of a Component. It is up to the consumer to clean up the list of assets after a Component is removed and remove anything they no longer need.


## Consuming a Component

The consumer adds Components into their Client by dragging and dropping them from the "_Components_" section of the Widget palette in the Client Builder. You may add multiple instances of a Component to a Client if appropriate.

The Component will appear to the consumer as a single non-Layout Widget; they will not be able to select any of the "internal" Widgets it contains. When a Component is selected, a property sheet will appear in the usual way. The consumer can edit most of the usual properties for the "outer" Widget of the component ("name", "style", etc.) 


### Component Configuration ("Specific" Properties)

In addition, the "_Specific_" section of the property sheet will show any "_Configuration Properties_" exposed by the author. ("Hidden" items will not appear.)

The "_call in Functions_" are shown in a "read only_" state so the consumer can see what they do and how they are called, but they cannot be edited.

Any "_callback Functions_" **can** be filled in, following the directions supplied by the author in the comment section. If the callbacks are left empty, it will be as if the function simply returns "_null_".

The "_synthetic_" properties will have an "info tooltip" - this will contain text supplied by the author that describes what these properties are for and how they are used. In some cases it may be appropriate for the consumer to bind one of these values to a Widget elsewhere in the consumer's Client. 

For example, suppose the consumer drops in a Component whose Configuration has an integer property called "_temperatureThreshold_". If the consumer's Client had an InputInteger Widget they might want the user to be able to see and edit this value at runtime. If the Component's instance widget had been given a name "_MyComponentWidget1_" then the _Data Binding_ property of the InputInteger could be set to "_MyComponentWidget1.configuration.temperatureThreshold_". If the user changed this value in the Widget it would be changed in the Configuration as well.

#### Using the Component Configuration at runtime

The Configuration for a Component is also available at runtime. The consumer gets access to the Configuration object from the outer Component Widget itself:

```js
    var cmpWdg = client.getWidget("MyComponentWidget1");
    cmpWdg.configuration.temperatureThreshold = 100;
```

This is also the way the consumer could invoke "_call-in Functions_" on the Component:

```js
    var cmpWdg = client.getWidget("MyComponentWidget1");
    var sum = cmpWdg.configuration.add(100,200);
```

### Updating a Component

When the consumer drops a Component into their Client, all the parts (Widgets, code, Pages, etc.) are copied into the Client and saved along with it. This means that if the author makes changes to the Component those changes will **not** be automatically reflected in the consumer's Client. In order to get the latest version of the Component the consumer must explicitly update it.

If a Component has become outdated a _Replace_ menu item will appear on the Component's context menu like below:

<p><img style="border:none" width="700" alt="Update Component" src="../assets/img/ccug/update.png" title="Update Component"></p>


Selecting "_Replace all Components of this type with the latest version_" will cause all instances of the Component within the Client to be updated in place. (If a Component is up-to-date with the one available in the Namespace the "upgrade" menu item will not appear.)


### 'Exploding' a Component

A Component is a "black box" of features whose details can only be changed by the author. However, a Component can be "exploded" back into its constituent parts - at this point it is no longer a Component, simply a collection of Widgets, Pages and Data Streams which can be freely edited. This operation can be invoked from a Component's context menu (See the figure above.)


## Special handling of names within Client Components


This section is for advanced users of Components. Here we will discuss how the names of Widgets, DataStreams and Pages are automatically adjusted when a Component instance is added to a Client.

### Widget Names

When building HTML it is generally assumed that all the DOM elements will have a unique name (which is the "id" attribute of an element). This rule is not enforced by browsers but you can run into confusing situations if more than one DOM element has the same name. For example, suppose you use a JQuery selector of the form 

```js
$("#MyWidget")
```

If there are two widgets with this id only the first one found will be returned. 

Modelo Clients do their best to enforce this by making sure all your Widget names are unique. However this leads to problems when using Components, since you might have multiple instances of the same Component within a Client.

To avoid conflicts, all the widgets inside a Component are automatically renamed in a systematic way. For example, suppose you have a Component which contains a single button. When editing the Component the widgets (and their corresponding DOM elements) might  look something like this: (The details are actually different but this will serve to illustrate the point.)

```html
     <div id="MyComponent">
        <button id="MyButton">
            Click Me
        </button>
     </div>
```

Now suppose you drop **two instances** of this Component into your Client. In the consuming Client the HTML structure would look something like this:

```html
     <div id="MyComponent1">
        <button id="MyButton_38593">
            Click Me
        </button>
     </div>

     <div id="MyComponent2">
        <button id="MyButton_84712">
            Click Me
        </button>
     </div>

```


The outermost "div" of each Component is the only name that the user of the Component can see and change. The Client Builder will guarantee that these names are unique ("MyComponent1" and "MyComponent2" in this case.) But the DOM elements **inside** the Component ("button" elements in this example) will have their names automatically adjusted by adding a 5-digit random number to the end of the id. The number will be different for each Component instance (but the same for all elements inside each Component).

Normally the author's JavaScript code inside a Component won't care that the widget names have been changed. (The consumer of the Component certainly won't care because they don't know anything about the internals of the Component anyway.) But suppose that somewhere in the Component's code the author wanted to alter the Button's label at runtime. You might have written some code like this:

```js
     var btn = client.getWidget("MyButton");
     Btn.buttonLabel = "Some new label";
```

But at runtime there **is** no Button called "MyButton". So how does this work? In most cases the Client runtime system knows the "context" in which the Component's code is running. For example, if this code fragment was inside the "On Component Start" event handler for the Component, the runtime system would **know** that the code was running inside the context of a particular Component instance. That would allow it to **re-map** your request from "MyButton" to "MyButton_38593" or "MyButton_84712" as appropriate and return the Widget you expected. 

This all happens transparently - you normally never need to think about it. But in some situations where you need to look up a Widget inside a Component at runtime the code might be running in an asynchronous code block where the context is impossible to determine. This usually occurs when you are using some kind of asynchronous callback, such as setTimeout or a server request. Here's a simple example:

```js
    setTimeout(function()
    {
        var btn = client.getWidget("MyButton");
        ...
    }
```


Because of the way JavaScript works, when the callback function inside the setTimeout is executed the Client runtime can't determine the correct context it needs to re-map "MyButton" to the correct Widget, and the getWidget call will return "null".

There are several solutions to this problem - the simplest is just to establish the widget **before** you enter the asynchronous block. Like this:

```js
    var btn = client.getWidget("MyButton");

    setTimeout(function()
    {
        btn.buttonLabel = "Some new label";
        ...
    }
```


In more complicated situations you can use a different method that allows you to **provide** the missing context - instead of "getWidget" you can call this:

```js
    setTimeout(function()
    {
        var btn = client.getComponentWidget(context,"MyButton");
        ...
    }
```

where "context" can be several different things:

* Any other widget inside the Component instance 
* The "outermost" widget for the Component instance itself 
* The "configuration" object for the Component instance.

Note that when using the [client.setTimeout()](cbref.md#settimeout) or [client.setInterval()](cbref.md#settimeout) methods from within a Client Component you will **not** need to use the client.getComponentWidget version; the simpler client.getWidget() call will still work correctly.

### Page and DataStream Names

 Components can include Pages and DataStreams. When you drop more than one Component instance into a Client there is no need to create a separate Page or DataStream for each one. But to avoid possible naming conflicts with the enclosing Client these objects are automatically renamed as well - both are prefixed with the Component name followed by two underscores. For example,

 * "MyPage" becomes "MyComponent__MyPage"
 * "MyDataStream" becomes "MyComponent__MyDataStream"

 Just as with Widgets, the Client runtime knows how to remap the appropriate API calls to the correct objects at runtime. This means that calls like

```js
    client.popupPage("MyPage");
```
and
```js
    client.getDataStreamByName("MyDataStream");
```

will continue to work even though the actual Page and DataStream names have been altered.

If necessary there is also a special call for DataStreams like client.getComponentWidget which can be used inside blocks where the runtime can't determine a context:

```js
    client.getComponentDataStreamByName(context,"MyDataStream");

```
         