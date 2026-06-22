# Client Builder User's Guide

This is a "User's Guide" for Client Builder. The Reference Guide for the Client Builder API may be found [here](cbref.md).

## Introduction
"Clients" are a component of Vantiq's application development system. They are the piece that embodies an interaction with the end user, and can be used to display and collect information. A Client is constructed by a Vantiq developer using the classic MVC design strategy, which means they will create three different types of parts:

* Models - Data (usually with a known schema) that can be read or streamed from the server or entered by the end user
* Views - Widgets and controls that are used to display data and collect user input (buttons, input fields, charts, images, etc.)
* Controllers - JavaScript code written by the Vantiq developer that expresses the behavior of the Client (e.g. "What happens when the user clicks that button?")

The "Client Builder" is the component of the Vantiq IDE that allows a Vantiq developer to create, edit and test a Client.

## Concepts
These are some basic concepts and terminology that you should be familiar with before reading the rest of this document.

### User vs. Developer
When this document uses the term "user" it is meant to refer to the **end user** of the Client. The term "developer" refers to the person who uses the Client Builder to create a Client. (That's probably **you**, the person reading this document.)

### Client 
This is the component you are building that contains Models, Views and Controllers to orchestrate an interaction with the end user. 

You should also note there is a single JavaScript object that is available at runtime and which provides an interface to the Client and the services it provides. (There is usually a JavaScript variable called "client" which points to it.)

### Page
The Client can contain multiple "Pages"; each page corresponds to a set of Widgets and the code that responds to events they generate. Your Client always contains at least one Page which is named "Start". The controller code you write can cause the Client to navigate between Pages. Many simple Clients will only need a single "Start" Page.

Each Page is represented at runtime by a single JavaScript object of type "Page" which provides an interface to the Page and the services it provides.

### Widget
Each Page can contain various types of "View" objects which are called "Widgets". Each type of Widget has a corresponding JavaScript class that implements it. (Some examples are "Button", "InputString", "DropList" and "BarChart"). Each Widget you create must have a unique name which can be used by your controller code to access the Widget at runtime.

Some Widgets may generate events when the user interacts with them, and you can write code which listens for these events and responds. (For example, Buttons have an "onClick" event.)

Some Widgets can be "bound" to data so that the Widget and data values will always be in sync. For example, if the user changes the contents of an InputString Widget, the bound data will change to match; if some of your controller code changes the data, any bound Widgets are automatically updated to reflect it.

### API
In order to build a running Client your code will often need to manipulate the Client, Pages and Widgets which comprise the Client. Taken as a whole all these objects and the services they provide are usually referred to as "the API".

## Creating a Client
To create a new Client, use the **Add** button to select **Client...**, then click the **New Client** button to display the New Client dialog:

![NewClientDialog](assets/img/cbuser/NewClientDialog.png)

Choose one of the built-in Client Templates (e.g., _BrowserEmpty_ or _MobileEmpty_) and provide a name for the Client, then click **OK** to display the Client Builder for the new Client.

After creating and editing a Client, you may want to use that Client to create other similar Clients. In that case, enable **Save as Client Template** in a Client's Advanced Properties. **Save as Client Template** means that whenever the Client is saved, it is also saved as a Custom Client Template and is displayed in the New Client dialog. In the figure above, the _Notifications_ Client Template is an example of a Custom Client Template. Custom Client Templates are saved as two files in the Vantiq document store in the _vantiq/clientTemplates_ hierarchy:

* the template itself has a file extension of _ctp_
* the image file (a small image of the Client itself) has a file extension of _png_

These two documents are also added to the Project so they can be easily exported and imported into new Projects.

## The Client Builder
The Client Builder is basically a WYSIWYG editor that allows the developer to manipulate the Client, Pages, Widgets, Data and Code which make up the Client.



![Client Builder Overview](assets/img/cbuser/cb_overview.png "Client Builder Overview")

The Client builder pane is made up of three sections. From left to right -


### Control Dock

On the left is the "Control Dock", which contains the widget palette and a tree view of the Client. The left section can either be resized by grabbing its right edge or collapsed completely using a control in its upper-right hand corner. This section is divided into two tabs:

#### "Add" Tab
The "Add" tab contains the widget palette, and is used to drag and drop new Widgets into a Page:

!["Add" Tab](assets/img/cbuser/cb_addtab.png '"Add" Tab')

#### "Edit" Tab
The "Edit" tab contains a "tree" visualization of the Client and its components:

!["Edit" Tab](assets/img/cbuser/cb_edittab.png '"Edit" Tab')

This tree contains 3 main nodes at the root:

The "Client" node contains a tree view of the Client, Pages and Widgets. Right-clicking on any of these nodes reveals a context popup menu.

Within the "Widget" portion of the tree you can drag and drop the Widgets to reparent them or re-order them within their parent.

#### Client Node

The Client context menu offers a way to edit the Client Properties (see the section [below](#client-properties)) , the "client.data" Data Object and all the events associated with the Client:

![Client Context Menu](assets/img/cbuser/cb_client_menu.png "Client Context Menu")



The "Add Page..." menu item allows you add a new Page to the Client (or you can use the more convenient "Add Page" button in the toolbar).  

Opening the Client node reveals a node for each of the Pages; inside the Page nodes are all the Widgets they contain.



#### Page Nodes

The Page context menu has an item to edit the Page Properties, the "page.data" Data Object and all the events associated with the Page:

![Page Context Menu](assets/img/cbuser/cb_page_menu.png "Page Context Menu")

Your Client must contain a least one Page which is always named "Start". (Of course, this is the Page that is displayed when the Client starts execution.) But your Client may contain more than one Page, and the "Edit" tree allows you to switch between them.

#### Widget Nodes

The context menu for a Widget will vary for each different type, showing the specific event handlers defined for each:

![Widget Context Menu](assets/img/cbuser/cb_widget_menu.png "Widget Context Menu")


#### Data Streams Node

The context menu for "Data Streams" provides a way to create a new Data Stream of all the various types:

![Data Stream Context Menu](assets/img/cbuser/cb_ds_menu.png "Data Stream Context Menu")

#### Data Objects Node

The "Data Objects" node does not have a context menu, but opening the node shows all the Data Objects, and clicking on each will open a Dialog to edit it (see the section [below](#data-objects)) :

![Data Objects](assets/img/cbuser/cb_data_obj_tree.png "Data Objects")

### Canvas Section

In the center is the "Canvas Section" which contains a WYSIWYG view of the Widgets on the current Page. You can select a Widget by clicking on it in the Canvas section or clicking on its corresponding item in the Edit tree. When a Widget is selected its property sheet appears in the Slideout Section on the right side of the Client Builder pane. If you right-click on a Widget in this section you will see a context menu which (among other things) allows you to edit the Widget's event handlers directly.

### Slideout Section

On the right is the "Slideout section" which appears only when a Widget is selected or when event code is being edited. This section can be resized by grabbing its left edge. 

When a Widget is selected the Slideout shows the Widget's property sheet:

![Slideout Property Sheet](assets/img/cbuser/cb_slideout_props.png "Slideout Property Sheet")


When you select an event the editor appears in the same space:


![Slideout Event Editor](assets/img/cbuser/cb_slideout_event.png "Slideout Event Editor")

You can reach these event editors in various ways for convenience:

* From the "Event" section in a Widget's property sheet.
* From a Widget's context menu in the Canvas section.
* From a Widget's context menu in the "Edit" tab tree. 
* You can also cause the events for the Client, Page and Widget to always be shown inside the tree by toggling them on from the toolbar at the top:


![Events in the Tree](assets/img/cbuser/cb_events.png "Events in the Tree")

<span style="color:red">(1)</span> This is the button that can be used to toggle showing events within the tree.

<span style="color:red">(2)</span> Click on this node to add content to the "Start" Page's "On Client Start" event (which is currently empty)

<span style="color:red">(3)</span> Click on this node to add content to the "Label" Widget's "On Context Menu" event (which currently has some content)

<span style="color:red">(4)</span> If you click on the little magnifying glass within the toolbar it will turn into a "search" input field. Typing into the field will cause the tree to show only the events which have text matching the search value.

Note that the event editor can be "maximized" (that is, expanded to take over all the space except for the Control Dock). There is a "maximize" icon in the upper-right-hand corner of the Slideout area.





#### Client Properties
From the Client's context menu in the tree you can open the Client Properties dialog.

![Overview](assets/img/cbuser/clientproperties.png "Client Properties")

From this popup you can change the name of the Client and edit its human-readable description. In addition, you can add a "Display Name", which is used in preference to the Client name when running the Client, either in a browser or in the Vantiq mobile apps.

The following properties are found under the **Advanced** tab:

* _Mark as Launchable_ is a checkbox that controls whether this Client will appear in the list of Clients shown by the "Client Launcher" and in the Start view of the Vantiq mobile apps. See the [Client Launcher](#the-client-launcher) section below for details.

* _Mark as Public_ is a checkbox that controls whether this Client can be run anonymously by un-authenticated users. Public clients are accessed through an alternate URL. Note that when a client is marked as public there are additional options that will appear under the Launch Menu for running the client in Public Mode. 

* _Restricted Users_ is a list of restricted users. If any Client contains a restricted user, then each user that needs access to any launchable Client must be added to the Restricted Users list. If a user is added to only one Client's Restricted Users List, that Client will automatically be launched by the Vantiq mobile apps. If a user is added to more than one Client's Restricted User list, then only those Clients are available in the mobile app's Start view.

* _Create Sidebar_ is a checkbox that controls whether a sidebar (vertical container on the left side of the Client) is placed on all Client pages. Widgets added to that sidebar appear on all Client pages.

* _Create Topbar_ is a checkbox that controls whether a topbar (horizontal container at the top of the Client) is placed on all Client pages. Widgets added to that topbar appear on all Client pages.

* _Show Edit Grid_ is a checkbox that controls whether a 10x10 pixel grid is shown in the canvas section to help with positioning Widgets. (When this grid is on Widgets will automatically "snap to the grid" when you move them.)

* _Show Outlines_ is a checkbox that controls whether outlines are shown around certain widgets which can be hard to see while editing.

* _Show Grid Cells_ is a checkbox that controls whether dotted cell outlines in Grids are shown when editing.

* _Apply Custom CSS Assets_ is a checkbox that controls whether Custom CSS Assets are applied to Client widgets as they are edited.

The **Theme** tab allows selection of colors that allow for basic styling of all widgets across the Client.

The **Localization** tab has properties associated with localizing Clients. See the [Localizing Clients](#localizing-clients) section below for details.

##### **Sidebar and Topbar**
Sometimes it is useful for a Client to have a "sidebar" or "topbar" which is visible on every page. Normally this will contain Menu Buttons. Clicking the **Sidebar** and/or the **Topbar** checkboxes will add these features to your Client.

Once the bar appears it can be manipulated like other containers; you can add children, move them, set their properties and change their order. (In general you will only add "Menu Button" widgets but other types of widgets can be added as well. "Menu Buttons" are just regular buttons which have been styled with a more appropriate look in a menubar.) Of course, you can add "On Click" handlers for these Menu Buttons to control what happens when the user clicks them.

##### **Custom Code**
Most of the JavaScript code you will enter is in the form of "event handlers" which is run when certain events occur. But it is sometimes useful to simply add your own set of JavaScript functions and global variables that is available for use by all the event-driven code. This **Custom Code** button pops up a modal editor which allows you to do that; the JavaScript you enter will always be inserted as the first thing in your generated runtime code. (And of course, it must be valid JavaScript.) The **Custom Code** button is found in the **Basic** tab, under the **Custom Properties** pull-down menu.

##### **On Start**
Here you may add JavaScript code that is run once when the Client first starts up; this is a good place to put any "initialization code" that will do any initial server queries or setup required by the rest of the Client. The code is wrapped in a function like this, where the "client" parameter contains a pointer to the Client object. The **On Start** button is found in the **Basic** tab, under the **Custom Properties** pull-down menu.

```js
//
//  This function is called when Client 'MyPageSet' first begins executing.
//
Client_onStart function (client)
{
    // Your code goes here
}
```

##### **On End**
Here you may add JavaScript code that is run when the Client stops running; this is a good place to put any "terminating code" that will do any cleanup of timers or widget contents used by the Client. The code is wrapped in a function, where the "client" parameter contains a pointer to the Client object. The **On End** button is found in the **Basic** tab, under the **Custom Properties** pull-down menu.

##### **Custom Assets**
In some cases you want to add 3rd party JavaScript libraries to your Client which is available at runtime. The _Custom Assets_ dialog is used to edit the list of CSS and JavaScript assets which should be available. All the requested assets are dynamically loaded into your Client at start time. The **Custom Assets** button is found in the **Basic** tab, under the **Custom Properties** pull-down menu.

The Assets can either be located externally to Modelo or stored within a Modelo Document. (See the [Accessing Documents](#accessing-documents) section for a discussion of how to reference a Document.)

##### **On Assets Loaded**
Because Custom Assets are dynamically loaded they may not be available immediately. The _On Assets Loaded_ event handler is driven when all assets have completed loading. You may need to delay making use of the 3rd party code until this event handler fires. The **On Assets Loaded** button is found in the **Basic** tab, under the **Custom Properties** pull-down menu.

```js
//
//  This function is called when the custom CSS and JavaScript assets have
//  finished loading and are available for use. (Note that both 'client' and
//  'this' point to the Client object.)
//
Client_onAssetsLoaded function (client)
{
    // Your code goes here
}
```

##### **Client Code Fragments** and **Namespace Code Fragments**
Developers often reuse portions ("fragments") of JavaScript code across Clients, Projects and Namespaces. When editing JavaScript within the Client Builder, developers may access that reusable code either on a Client-wide or Namespace-wide basis. Those fragments are defined and categorized in the **Client Code Fragments** or **Namespace Code Fragments** lists. Fragment lists are grouped by Category names, which are developer-defined groups of related fragments. Those fragments are then available in the Client JavaScript editor by using the pull-down menus at the top of the editor. The **Client Code Fragments** and **Namespace Code Fragments** buttons are found in the **Basic** tab, under the **Custom Properties** pull-down menu.

##### **Colors and Themes**
Client Widgets have many colors by default, broken up into two general categories: _General Colors_ and _Card Colors_. _General Colors_ control the colors of widget backgrounds, title bars, borders and other UI elements. _Card Colors_ control the colors of certain widgets related to mobile apps (for example, Camera and Audio).

Developers may also apply background images to Clients by using the properties found in the _Background_ section.

You may change the values for default colors using the color selectors. To get you started, there are several predefined "themes" that you may choose from that have a set of coordinated colors. In addition, developers may create their own named themes by modifying one of the predefined themes then using the **Save Theme** button. Those named themes are saved as a file in the Vantiq document store in the _vantiq/themes_ hierarchy and have a file extension of _thm_. Any defined named themes are then added to the **Theme** pull-down menu so can be easily applied to multiple Clients.

#### Data Objects
The Client and all the Page objects have a JavaScript Object property called "data" which you can populate with anything you like. This "data" property is a convenient place to define global variables which persist for the life of the Client and can be used to store the working data required by your Client. This is described in more detail in the [Data Objects](#data-objects_1) section below. To edit a Data Object open the **Data Objects** node in the "Edit" tree and click on one of them - this will pop up a dialog to let you create and edit Data Objects: 

![Overview](assets/img/cbuser/editdataobjects.png "Edit Data Objects")


#### Data Streams
"Streams" are a Vantiq mechanism which allows you to define a source of data that is associated with some kind of event. The stream listens for events which carry a "message" and which the Stream in turn passes along to all its "listeners". 

In the Client Builder a Stream can be bound to various kinds of Widgets (such as Line Charts, Gauges or Data Tables) which will incorporate the emitted data into their display.

![Overview](assets/img/cbuser/streams.png "Data Streams")

Most Data Streams provide a "time sequenced" source of data which might be either a single object or an array of objects. The bound Widget decides how the data is to be interpreted. For example, in the case of a Line Chart widget each new data item might be treated as a new point to be plotted, but a [DataTable](cbref.md#datatable) widget might completely replace the previous array of objects with the new set.

There are seven different types of Events which can be used to drive a Stream:

##### **"On Data Changed" Events**
These events are generated by the Vantiq server when some kind of operation (insert / update / delete) occurs on a Type. The Stream will emit the object instance which was inserted or modified.
##### **"Publish" Events**
This is an event associated with doing a PUBLISH on a particular "Topic", and is equivalent to a `WHEN PUBLISH OCCURS ON <topic> AS <message>` condition. The Stream will emit the associated message.
##### **"Source" Events**
This event is produced by a Vantiq Source and is equivalent to a `WHEN EVENT OCCURS ON "/sources/<source>" AS <message>` condition. The Stream will emit the associated message.
##### **"Timed Query" Events**
These are simply timer events used to run a pre-defined SELECT on a server Type at a regular interval. The Stream emits the results of the query.
##### **"Client" Events**
This allows JavaScript code within your client to use an arbitrary condition to write some data into the Stream which is emitted to the bound Widgets.
##### **"Resource" Events**
These are used internally by the Vantiq system and are currently not intended to be created by the user.
##### **"Service" Events**
This is an "outbound" event associated with a particular "Service".

There is also a special eighth **"Paged Query"** DataStream which can only be used with [DataTable](cbref.md#datatable) widgets; it is intended for use with Types which contain so many records that it would not be practical to load all the records into memory at one time. It is not driven by an Event; instead the [DataTable](cbref.md#datatable) only loads the records it needs to populate the currently displayed page.

Within the Edit tree the "Data Streams" node allows you to pops up a property sheet that allows you to edit the Data Streams defined in your Client. This process is described in more detail in the [Data Streams](#data-streams-detail) section below.



#### Page Properties

The context menu for a Page node within the "Edit" tree allows you to pop up the property sheet for a Page.

![Overview](assets/img/cbuser/pageproperties.png "Page Properties")

The **Layout Type** buttons allow you to select the kind of target on which you expect to run the Client. The different layout types are guides to the Client Builder to determine how to position widgets when running the Clients.

The **Name** field lets you set the name of the current Page. (The Page names must be unique, and the "Start" Page may not be renamed.)

The **Default Response Topic** allows you to set the default resource event associated the "response" generated by a Button with no onClick handler. More details can be found in the [Terminating with default Buttons](#terminating-with-default-buttons) section below.

The **Has Footer** checkbox indicates the page will always have a footer section which can hold any combination of widgets and is always pinned to the bottom of the Client.

The **On Client Start** button pops up a modal dialog that allows you to edit the JavaScript code that is run **once** for this Page when the Client first starts up; this is a good place to put any "initialization code" that will do any initial server queries or setup required by this Page. The code is wrapped in a function like this, where the "client" parameter contains a pointer to the Client object. "this" will reference the Page object itself.

(To clarify, the "On Client Start" callback for a Page gets called once when the Client starts; the "On Start" callback for a Page gets called right before a Page actually becomes visible no matter how many times the Page is started.)

```js
//
//  This function is called on page 'Start' once when the Client first begins
//  executing.
//
Client_Start_onClientStart function (client)
{
    // Your code goes here
}
```

The **On Start** button pops up a modal dialog that allows you to edit JavaScript code that is run **every time** a Page starts up; this is a good place to put any "initialization code" that must run more than once. The code is wrapped in a function like the one below, where the "client" parameter contains a pointer to the Client object. "this" will reference the Page object itself. "parameters" will contain any optional parameters that were sent by the caller (see the 'goToPage' and 'returnToCallingPage' methods in the [Client](#client) section below). 

(To clarify, the "On Client Start" callback for a Page gets called once when the Client starts; the "On Start" callback for a Page gets called right before a Page actually becomes visible no matter how many times the Page is started.)

The **On End** button pops up a modal dialog that allows you to edit JavaScript code that is run when the Page stops running; this is a good place to put any "terminating code" that will do any cleanup of timers or widget contents used by the Page. The code is wrapped in a function, where the "client" parameter contains a pointer to the Client object.

```js
//
//  This function is called when page 'Start' first begins executing.
//
Client_Start_onStart function (client,parameters)
{
    // Your code goes here
}
```

The **On Validation** button pops up a modal dialog that allows you to edit JavaScript code that is run after the contents of each widget have been validated (e.g., an Integer widget must contain only digits). The "On Validation" callback may be used to implement your own cross-widget value validation. See the [Field Validation](#field-validation) section for more details.

The **On Context Menu** button pops up a modal dialog that allows you to edit JavaScript code that is run whenever the user selects an item from a widget's optionally defined context menu. The code is wrapped up in a function, where the "client" parameter contains a pointer to the Client object and the "extra" parameter is an object containing the _key_ and _label_ of the selected menu item. Whenever a user selects a context menu item, whether it is associated with the Page-wide or a widget-specific context menu, the **On Context Menu** function is executed and the developer defines the Client interaction based on the _key_ of the "extra" parameter.

The **Context Menu** button pops up a modal dialog that allows you to create a context menu that appears in the upper-right of the Page and applies to the Page as a whole. Developers may use this context menu to provide context sensitive help and have corresponding JavaScript code executed by handling the _key_ value defined for each menu item.

The _Background Properties_ are defined by developers to apply background images to individual Pages. These properties override any _Background Properties_ defined for the Client as a whole.



### Palette Area

![Overview](assets/img/cbuser/palettearea.png "Palette Area")

#### Creating Widgets with the Palette
You can drag from the Palette in the "Add" tab to the Canvas Section to add Widgets to the current Page. The new Widget will always be assigned a unique name, but you may want to change it to something meaningful.

#### Editing Widgets 
Each Widget has its own set of properties which can be edited. All Widgets have some properties in common but each individual Widget class will generally have some properties that apply only to that particular kind of Widget. In order to edit a Widget's properties you must select it by clicking it with the mouse. (The selected Widget is highlighted with a checkerboard mask.) Only one Widget may be selected at a time, so clicking a Widget will cause any currently selected Widget to be de-selected.

#### Property Sheets
When a Widget is selected its property sheet pops up in the Slideout section. The properties are grouped into categories ("Specific", "Common", "Style", etc.) and each section is basically a two-column list with one row per property. To edit a property you simply click on the right hand column.

![Property Sheet](assets/img/cbuser/propsheet.png "Property Sheet")

#### Event Handlers
Many Widgets will offer Event Handlers within their list of properties. For example, in the Button property sheet shown above there is an "OnClick" event. Clicking on that property opens up an editor within the "Slideout" section (taking the place of the property sheet) that will allow you to edit the event handler. In the case of the Button:


![Event Editor](assets/img/cbuser/eventeditor.png "Event Editor")


```js
//
//  This function is called when the user clicks the 'myButton' button. (Note
//  that 'this' points to the button itself.)
//
Client_Start_myButton_onClick function (client,page,extra)
{
    // Your code goes here
}
```

The "client" and "page" parameters contain the Client and current Page objects. The "extra" parameter is usually null, but some Widgets will use it to pass extra context information about the event.

#### Undo, Redo, Delete
The Client Builder offers full Undo / Redo support for property changes made to Widgets. (This does not apply to changes made in the Client, Page, Data Object and Data Stream property sheets, just the Widgets themselves.)

A Widget which has been selected can be removed with the **Delete** button, and the **Undo** button will put it back.

## Views
The "Views" portion of your Client is made up of the Widgets which are placed on a Page. The widgets can be roughly grouped into three categories: Control Widgets, Data Stream Widgets and Layout Widgets.

### Control Widgets
These are in general the standard "controls" that most users is familiar with (buttons, input fields, droplists, etc.) as well as some special "viewer" controls. (When clicked the viewers usually open a separate window to display some resource.) Some of these have the ability to bind to a property of a Data Object. (For example, you would might bind an InputString widget to a String property in the Data Object of the current Page.)

### Data Stream Widgets
These widgets are typically for display only; they are connected to a Data Stream and will update themselves to response to new data arriving on the Stream. (For example, a line chart would draw new data points and shift the older data to the left.) More details on these widgets can be found below in the [Widgets and Streams](#widgets-and-streams) section.

### Layout Widgets
For simple Page layouts you can manually give each Widget a position on the Page. But sometimes it is useful to put the Widgets inside a "container" widget which assigns positions to its children using some algorithm. Generally if the size of the children changes for some reason the parent will automatically adjust the positions of its children to compensate.

For example, in the image below there are two VerticalLayout containers; both contain two children (a PieChart and some StaticText to act as a title). Note that in both cases the title has been automatically centered by the VerticalLayout even though the PieCharts are different sizes. Used this way containers can sometimes save time and effort in producing a pleasing layout. Layout containers can be nested and configured to produce many kinds of layout arrangements.

Note that in this example the borders are left in for clarity but can be turned off if you don't want to see them. 

(See [here](layout.md) for a more complete discussion of layout management.)

![Overview](assets/img/cbuser/vertlayout.png "VerticalLayout Example")

There are eight kinds of layout containers available:

#### AccordionLayout
This container is intended for use primarily in a "side bar"; it normally will only contain MenuButtons. You will usually add two or more AccordionLayouts to the side bar, each with a set of related MenuButtons. The container will stay closed until clicked at which point they will pop open and reveal the MenuButtons inside. Only 1 AccordionLayout is open at a time and their siblings will automatically close.

For example, here is a side bar that contains three AccordionLayouts as seen inside the Client Builder; for convenience all the AccordionLayouts are forced "open" when editing.


<p><img style="border:none;" alt="AccordionLayout Example" src="../assets/img/cbuser/accordion1.png" title="AccordionLayout Example"></p>

When the Client is running all three AccordionLayouts start closed:


<p><img style="border:none;" alt="AccordionLayout Example" src="../assets/img/cbuser/accordion2.png" title="AccordionLayout Example"></p>

If the user clicks on "Accordion Menu 1" it will pop open revealing the three MenuButtons inside:

<p><img style="border:none;" alt="AccordionLayout Example" src="../assets/img/cbuser/accordion3.png" title="AccordionLayout Example"></p>


If the user then clicks on "Accordion Menu 2" the lit will pop open (and "Accordion Menu 1" will close) revealing the two MenuButtons inside:

<p><img style="border:none;" alt="AccordionLayout Example" src="../assets/img/cbuser/accordion4.png" title="AccordionLayout Example"></p>


#### FixedLayout
This container allows you to set the position of its children explicitly (that is, there is no automatic layout). This container also duplicates the features of the FloorplanViewer.


#### FlowLayout
This container allows you to explicitly set the container's width and the children are arranged left-to-right and top-to-bottom in a "flow" layout (similar to the way a browser "div" lays out its children). The height of the FlowLayout is adjusted to fit the children but the width stays fixed.

#### GridLayout
In a GridLayout you set an explicit number or rows and columns which creates a fixed number of "cells". Each cell can be empty or accommodate a single child. This is often useful for creating a classic "form" layout.

![Overview](assets/img/cbuser/gridlayout.png "GridLayout Example")

#### HorizontalLayout
In a HorizontalLayout the children are laid out left-to-right in a horizontal row.

#### ScrolledLayout
A ScrolledLayout will provide scrollbars when needed to view the single child it contains.

#### TabbedLayout
In a TabbedLayout the children may be positioned with a multi-page "tabbed" container.


#### VerticalLayout
In a VerticalLayout the children are laid out top-to-bottom in a vertical column.

### Class Hierarchy
The Widgets are arranged in a class hierarchy which is shown below; note that only "leaf" classes can be instantiated.


* [Widget](cbref.md#widget)
    * [DataStreamWidget](cbref.md#datastreamwidget)
        * [BarChart](cbref.md#barchart)
        * [Calendar](cbref.md#calendar)
        * [ColumnChart](cbref.md#columnchart)
        * [DataTable](cbref.md#datatable)
        * [DynamicMapViewer](cbref.md#dynamicmapviewer)
        * [FloorplanViewer](cbref.md#floorplanviewer)
        * [Gauge](cbref.md#gauge)
        * [LineChart](cbref.md#linechart)
        * [ListViewer](cbref.md#listviewer)
        * [NumberViewer](cbref.md#numberviewer)
        * [PieChart](cbref.md#piechart)
    * [ControlWidget](cbref.md#controlwidget)
        * [AudioRecorder](cbref.md#audiorecorder)
        * [BarcodeReader](cbref.md#barcodereader)
        * [Button](cbref.md#button)
        * [Camera](cbref.md#camera)
        * [Chat](cbref.md#chat)
        * [Checkbox](cbref.md#checkbox)
        * [ComboBox](cbref.md#combobox)
        * [Conversation](cbref.md#conversation)
        * [Discussion](cbref.md#discussion)
        * [DocumentViewer](cbref.md#documentviewer)
        * [Droplist](cbref.md#droplist)
        * [ImageMarkup](cbref.md#imagemarkup)
        * [ImageViewer](cbref.md#imageviewer)
        * [InputDate](cbref.md#inputdate)
        * [InputDateTime](cbref.md#inputdatetime)
        * [InputNumeric](cbref.md#inputnumeric)
        * [InputInteger](cbref.md#inputinteger)
        * [InputReal](cbref.md#inputreal)
        * [InputObject](cbref.md#inputobject)
        * [InputString](cbref.md#inputstring)
        * [Label](cbref.md#label)
        * [MapViewer](cbref.md#mapviewer)
        * [MenuButton](cbref.md#menubutton)
        * [MultilineInput](cbref.md#multilineinput)
        * [RadioButtons](cbref.md#radiobuttons)
        * [SectionLabel](cbref.md#sectionlabel)
        * [Signature](cbref.md#signature)
        * [Tree](cbref.md#tree)
        * [VideoRecorder](cbref.md#videorecorder)
    * [Canvas](cbref.md#canvas)
    * [StaticHtml](cbref.md#statichtml)
    * [StaticIcon](cbref.md#staticicon)
    * [StaticImage](cbref.md#staticimage)
    * [StaticMarkdown](cbref.md#staticmarkdown)
    * [StaticText](cbref.md#statictext)
    * [WidgetContainer](cbref.md#widgetcontainer)
        * [AccordionLayout](cbref.md#accordionlayout)
        * [FixedLayout](cbref.md#fixedlayout)
        * [FlowLayout](cbref.md#flowlayout)
        * [FlowLayout](cbref.md#flowlayout)
        * [GridLayout](cbref.md#gridlayout)
        * [HorizontalLayout](cbref.md#horizontallayout)
        * [ScrolledLayout](cbref.md#scrolledlayout)
        * [TabbedLayout](cbref.md#tabbedlayout)
        * [VerticalLayout](cbref.md#verticallayout)


## Controllers
The "Controller" components of a Client are the JavaScript fragments provided by the developer to implement the actual behavior. Most of this is expressed as "Event Handlers"; that is, you define the body of a function that is called when certain conditions occur. This can be things like:

* The Client has started
* A Page has started
* A Button was clicked
* The value of an input field has changed

There is one exception to this; it is sometimes useful to simply supply your own set of JavaScript functions and global variables that is available for use by all the event-driven code. This is known as "Custom Code" and is added using the Client Property Dialog. For example, you might want to define various utility functions that could be called from an event handler. (Any function or data you define as "Custom Code" is available globally.)

Event handler functions will usually have a predefined set of parameters that is available when they are called. Usually there is a "client" and "page" parameter set since it is often useful to have them available.

In the case of handlers defined on Widgets (such as Button "On Click"), the "this" variable is pointing to the object (in this case, the Widget) to which the event applies.

### On Start Events
One important use for the event handlers is to initialize your Client and Pages in some way. At startup time, the runtime system will always call the Client "On Start" handler before anything else happens. It will then call the "On Client Start" handlers for every Page you have defined. Note that these startup events will only happen **once** no matter how many times you may enter or leave a Page.

Each Page may also have an "On Start" handler as well; these is called before the Page actually starts executing. The difference is that if you navigate away from the Page and then back again the Page's "On Start" handler **will** be called again.

### Navigation Between Pages
Your Client can be written so that everything happens on a single Page. But it is often useful to divide your Client into multiple Pages and then navigate between them when the situation requires it. There are two functions defined on the Client object that are used for this.
 
It is simpler to explain this with an example. Suppose your Client has two Pages: "Start" and "ShowDetails".
 
On the "Start" Page you add a button that has the label "Show Details" and whose "On Click" handler looks like this:
 
```js
//
//  This function is called when the user clicks the 'showDetailsButton' button.
//
Client_Start_showDetailsButton_onClick function (client,page,extra)
{
    //
    //  Navigate to the "ShowDetails" Page and pass some parameters. The parameters 
    //  is available in the "On Start" handler for the "ShowDetails" Page.
    //
    client.goToPage("ShowDetails",{x:1},"fade");
}
``` 

The second parameter of the "goToPage" method ("{x:1}") offers a way to pass a parameter to the target page; it will passed as "parameters" argument in the "ShowDetails" page's "onStart" callback. The optional third parameter of the "goToPage" method provides a way to customize the transition to the new page; in this example, the transition will fade from one page to the next. See the [goToPage section](cbref.md#gotopage) for more information about transition options.

The "ShowDetails" Page might have another button defined with the label "Done" and whose "On Click:" handler looks like this:

```js
//
//  This function is called when the user clicks the 'doneButton' button.
//
Client_ShowDetails_doneButton_onClick function (client,page,extra)
{
    //
    //  Navigate back to whichever Page called us and pass some parameters. The parameters 
    //  is available in the calling Page's "On Start" handler.
    //
    client.returnToCallingPage({someParms:1});
}
``` 

### Server Requests
Another common task for your Controller code is to interact with the Vantiq server via the REST API. Such requests are handled using a special class called Http. This example shows how you might do a sorted query for all the records of Type "MyType".

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "select" on our Type
    //
    http.setVantiqUrlForResource("MyType");
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Specify the (optional) query parameters
    //
    var queryParameters = {
        sort: {name:1}
    };
    
    //
    //  Execute the asynchronous server request. This expects three parameters:
    //
    //  queryParameters: "null" or an object containing the parameters for this request
    //  successCallback: A callback function that is driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that is driven when the request does not complete
    //                   successfully.
    //
    http.select(queryParameters,function(response)
    {
        console.log("SUCCESS: " + JSON.stringify(response));
    
        //
        //  At this point "response" is an array containing the objects returned for the "select"
        //
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a select on 'MyType'");
    });
```

More detailed information on crafting a REST API request can be found in the [API Reference Guide](api.md). In particular the "parameters" mentioned below are the standard "query object" which is described [here](api.md#detail-select).

There are variations of the "http.select" request for all the obvious server operations. Note that in all cases you must call http.setVantiqUrlForResource(&lt;resourceTypeName>) first to establish the Type or source you are targeting.


#### aggregate(pipeline:any[], successCallback:Function, failureCallback:Function):void;
Returns all the resources instances of the Type for an aggregation pipeline.

#### select(parameters:any, successCallback:Function, failureCallback:Function):void;
Returns all the matching resources instances of the Type.

#### selectOne(resourceId:string, parameters:any, successCallback:Function, failureCallback:Function):void;
Returns a single instance of the Type identified by &lt;resourceId>.

#### insert(data:any, parameters:any, successCallback:Function, failureCallback:Function):void;
Inserts a new instance of the Type (&lt;data>)

#### update(data:any, resourceId:string, successCallback:Function, failureCallback:Function):void;
Updates an existing instance of the Type (identified by the &lt;resourceId>) using the supplied &lt;data>

#### upsert(data:any, successCallback:Function, failureCallback:Function):void;
Upserts a new instance of the Type (&lt;data>)

#### deleteAll(parameters:any, successCallback:Function, failureCallback:Function):void;
Remove all instances of the Type which match the &lt;parameters>

#### deleteOne(resourceId:string, parameters:any, successCallback:Function, failureCallback:Function):void;
Deletes a single instance of the Type identified by &lt;resourceId>.

#### patch(resourceId:string, patchInstructions:any[], parameters:any, successCallback:Function, failureCallback:Function):void;
Patches a single instance of the Type identified by &lt;resourceId> and using &lt;patchInstructions>

#### publish(data:any, resourceId:string, successCallback:Function, failureCallback:Function):void
Publishes the JSON payload in &lt;data> using the topic, source name or "service/inboundEvent" in &lt;resourceId>.  You must have previously called http.setVantiqUrlForResource("sources"), http.setVantiqUrlForResource("services") or http.setVantiqUrlForResource("topics") for this to work.

#### execute(procedureArguments:any, procedureName:string, successCallback:Function, failureCallback:Function):void
Execute a procedure with the supplied name and arguments. You must have previously called http.setVantiqUrlForSystemResource("procedures") for this to work.

#### query(parameters:any, resourceId:string, successCallback:Function, failureCallback:Function):void
Perform a query against the Source named &lt;resourceId>.  You must have previously called http.setVantiqUrlForResource("sources") for this to work.


## Models
The "Model" portion of a Client refers to the data that it operates on. Of course you can always create JavaScript variables directly in your code, but the Vantiq Client "Model" also includes two other components called "Data Objects" and "Data Streams".

<a name="model-data-objects"></a>
### Data Objects 
As described in the [section above](#data-objects), each Page and the Client itself have a property called "data" which points to a Data Object. It is up to the developer to declare the properties that these objects contain. 

For example, if you click the "Data Objects" button in the Client Builder you will see a dialog like this:

![Overview](assets/img/cbuser/doblank.png "Data Objects Example")

The dropdown at the top of the dialog lets you select which Data Object you are editing. For a brand new Client with only a single Page you will see these two Data Objects:

* client.data
* page.data for page 'Start'

All of these Data Objects start off empty, containing no properties. It is up to the developer to populate them. Note that properties defined with the "client.data" Data Object are effectively "global variables" since the "client" object can be accessed from any page. In general a Page should not refer to a different Page's Data Object. 

Select the "page.data for page ‘Start’" item (if it is not already selected) and we will add some properties. 

Let's assume that you are trying to implement a Client that calculates the area of a rectangle; we will need properties for "height", "width" and "area". Click the "Add Property" button three times to add three new properties to this Data Object and fill them in like this:

![Overview](assets/img/cbuser/doarea.png "Data Objects Example")

Each row defines a property of the "Start" Page's data object. The first column is the property name; it must be a legal name for a JavaScript variable. The second column is a droplist that lets you set the property's type. (Note these are the same scalar datatypes used by the Vantiq server. There is one special exception called "Typed Object" which is discussed below.) The "Default Label" column is optional; it's a hint that the system can use to provide a more human-readable label in the UI. "Default Value" is also optional. When a Client starts up all the Data Objects you have defined is instantiated, and these are the values the property is assigned. Click the "Save and Exit" button to return to the main Client Builder.

Once these properties have been defined you can reference them from your code. For example, you might create a Button on the "Start" page with an "On Click" handler like this:

```js
//
//  This function is called when the user clicks the 'areaButton' button.
//
Client_Start_areaButton_onClick function (client,page,extra)
{
    page.data.area = page.data.width * page.data.height;
}
``` 

Most of the event handlers will pass the value for the "client" and the current "page" to you as arguments.

So far all we have done is compute the result and save it in a Data Object. The Data Objects are also useful if you want to edit or display the values as well.

From the Client Builder we can use the palette to create three "Real" number input widgets. For each one we can "bind" it to a value in a Data Object by setting the "Data Binding" property to "page.data.height", "page.data.width" and "page.data.area" respectively. When you run the Client and click the button the area is calculated and the resulting "page.data.area" value will appear in the bound widget. If you modify the values in the widgets which are bound to "height" and "width" the corresponding page.data values is updated automatically. Similarly if your code changes the value in a Data Object any "bound" widget will reflect the change.

Data Objects can contain any kind of scalar value ("Integer", "String, "GeoJSON", etc.). But they can also contain a special type called a "Typed Object". This is just like a regular JavaScript object **except** that it also maintains metadata on all the properties the Typed Object contains. It knows the property's name and datatype as well as a default value (which is assigned at start time) and a default label (which could be used when generating a UI for the property.)

These Typed Objects could be made manually of totally arbitrary properties or could correspond to the definition of a Type in the Vantiq server. The Client Builder can build these Types for you by using the Type's schema in the Vantiq server.

For example, suppose you have a Type defined in the server called "Employee" which has three properties:

<table style="width:auto;border-color:grey;border-width:2px;border-style:solid;">
    <tr>
        <th>Property</th>
        <th>Datatype</th>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
    </tr>
    <tr>
        <td>age</td>
        <td>Integer</td>
    </tr>
    <tr>
        <td>salary</td>
        <td>Integer</td>
    </tr>
    <tr>
    	<td>mgrName</td>
    	<td>String</td>
    </tr>
</table>


We could manually build a Data Object property of datatype "Typed Object" and populate it to match the definition in the server. But it is easier to let the Data Object dialog do it for you. First use the **Add a "Typed Object"** droplist to select the Type in the server ("Employee" in this case). A Typed Object property called Employee is added to the Data Object:

![Overview](assets/img/cbuser/doemp2.png "Typed Object Example")

Click the "pencil" (Edit) Action icon and we will "drill in" to see the details of this "Employee" property:

![Overview](assets/img/cbuser/doemp3.png "Typed Object Example")

You can see that a property was created to correspond to each of the properties defined in the "Employee" type. Of course you are free to update any of the property metadata items (such as to give the properties a better "Default Label"). Now click the **Cancel** button to pop back up to the previous display (**OK** if you made changes). From there we can click the "lightning bolt" (Generate Widgets) Action icon to cause a basic set of widgets to be created. Click **Save and Exit** to see what the generator did:

![Overview](assets/img/cbuser/doemp4.png "Typed Object Example")

This little form was built by creating a GridLayout with two columns and as many rows as needed to accommodate the properties in the Data Object. (You will probably want to move it to a suitable position on the Page.) Each Input widget was given an appropriate "Data Binding" property to connect it to its corresponding property in the page.data.Employee Data Object.

An obvious use for this group of generated Widgets would be to display the results of a query that returns a single instance of the "Employee" type. For example, you might put this code inside the "On Click" event of a Button marked "Run Query":

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "select" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Specify the (optional) query parameters
    //
    var queryParameters = {
        where: {name:"Michael"}
    };
    
    //
    //  Execute the asynchronous server request. This expects three parameters:
    //
    //  queryParameters: "null" or an object containing the parameters for this request
    //  successCallback: A callback function that is driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that is driven when the request does not complete
    //                   successfully.
    //
    http.select(queryParameters,function(response)
    {
        console.log("SUCCESS: " + JSON.stringify(response));
    
        //
        //  At this point "response" is an array containing the objects returned for the "select"; assign
        //  it to the page.data.Employee Data Object so that the bound widgets will show the results.
        //
        page.data.Employee = response[0];
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a select on 'Employee'");
    });
```

#### Summary
This may help visualize the way the Client, Pages and Data Objects are related in memory:

![Overview](assets/img/cbuser/dataobjectdiagram.png "Clients, Pages and Data Objects")


There is always a single "Client" object which is usually available to your code in as a "client" variable. The Client object has a property called "data" which points to the "global" data object. (i.e. "client.data"). The "getCurrentPage()" method on the Client will always point to the currently active Page. (But there is usually a "page" variable provided for you in the Event handlers that points to it as well.)

There is one "Page" object for each Page you have defined in your client (and there will always be a least one Page called "Start"). In general there is always a JavaScript variable called "page" provided which points to the current page. Each Page object has a property called "data" which points to that Page's Data Object (i.e "page.data"). 

A Data Object may contain zero or more properties. The properties may be scalars (Integer, Real, String. etc.) or a "Typed Object". Typed Objects can contain properties of their own; in this example "page.data.Employee" points to a Typed Object which contains the properties name, age, salary and mgrName.

<a name="data-streams-detail"></a>
### Data Streams
“Data Streams” are a mechanism which allow you to define a source of real-time data that is associated with some kind of event. 
(You should review the discussion of Data Streams in the [section above](#data-streams).)

Once a Data Stream has been defined and is producing data there are various kinds of widgets which can "listen" to the incoming stream and display it in some way. These are all the Widgets which inherit from the DataStreamWidget class:

* BarChart
* DynamicMapViewer
* FloorplanViewer
* ColumnChart
* DataTable
* Gauge
* LineChart
* ListViewer
* NumberViewer
* PieChart

You can visualize a Data Stream as a black box that periodically emits one or more objects. That stream of objects can be fed to a Widget which will extract data from the objects in some way and incorporate it into some kind of visual display.

#### Widgets and Streams

Different Widgets will interpret this flow of objects differently; there are four general categories: For some Widgets each burst of data is appended to a growing set of time-sequenced values. Others simply extract one or more values from the **last** object that arrived, and some take each burst as a complete replacement for any previous data. A special fourth category is intended only for use with the [DataTable](cbref.md#datatable) widget and just loads a page of records at a time as required.

##### Append Objects to an ever-growing set

The three most obvious examples of this category are the Line Chart:

![Overview](assets/img/cbuser/linechart.png "Line Chart")

the Bar Chart:

![Overview](assets/img/cbuser/barchart.png "Bar Chart")

and the Column Chart:

![Overview](assets/img/cbuser/columnchart.png "Column Chart")

Each time a new data object arrives the data is extracted and slides in from the right. (There is a limit and once points become old enough they disappear off the left edge.)

The ListWidget simply displays the last "n" values for a single property; old values roll off the bottom:

![Overview](assets/img/cbuser/listwidget.png "List Widget")


The PieChart does something slightly different; as each new value arrives it counts **how many** of each value has been seen and displays this histogram as a Pie Chart:

![Overview](assets/img/cbuser/piechart.png "Pie Chart")


The DynamicMapViewer extracts unique objects and their locations from the incoming data and display it against a map. As new points come in they update the positions of the objects and the markers move around the map:

![Overview](assets/img/cbuser/map.png "DynamicMapViewer")

The FloorplanViewer does the same thing but the points are plotted over a "floorplan image" saved with the widget:

![Overview](assets/img/cbuser/floorplan.png "FloorplanViewer")


##### Extract a value from the most recently arrived object

These widgets have no history, they just extract a value from the most recent object.

The NumberViewer is designed to act as an "infographic" that just displays a single important number:

![Overview](assets/img/cbuser/number.png "NumberViewer")

The Gauge is similar except the value is displayed like this:

![Overview](assets/img/cbuser/gauge.png "Gauge")


##### Complete Replacement using the latest update
This category takes each burst of data as a complete set of data which replaces whatever might have been there before. A common use for this would be to use a [DataTable](cbref.md#datatable) with a "Timed Query" Stream to show the complete set of results from some query:

![Overview](assets/img/cbuser/datatable1.png "Datatable")


##### Load records a page-at-a-time on demand
This is a special category that only applies to the [DataTable](cbref.md#datatable) widget and which is used to query for a "page" of records at a time as required by the widget as the user pages back and forth.

#### Defining Streams

To edit an existing Data Stream you can simply click on its item inside "**Data Streams**" in the "Edit" tree. To create a new Data Stream you must right-click on **Data Streams** to pop up a context menu which looks like this:

![Data Streams Context Menu](assets/img/cbuser/dsmenu.png "Data Streams Context Menu")

Selecting one of these items will open a dialog that allows you to configure a new Data Stream of the selected  type. In the sections below we will look at how you create a Stream for each of the types.

##### **"On Data Changed" Streams**
This Stream emits data whenever an insert, update or delete operation is done against the specified Type. The emitted data is the target record itself.

The "Group By" field is optional and is only required by certain types of Widgets such as the FloorplanViewer. It specifies which property of the target Type is used to divide the data into groups. (See the [Floor Plan Tutorial](tutorials/imagemaptutorial.md#group-by) for details.)

![Overview](assets/img/cbuser/ds-data-changed.png "On Data Changed")

##### **"On Publish Event" Streams**
This Stream listens for the event associated with doing a PUBLISH on a particular "Topic", and is equivalent to a `WHEN PUBLISH OCCURS ON <topic> AS <message>` condition in a Rule. (The Stream will emit the associated message.)

You must enter the topic that triggers the event. Note that there is no schema for the associated message (since it is not an instance of a server Type.)

The "Group By" field is optional and is only required by certain types of Widgets such as the FloorplanViewer. It specifies which property of the target Type is used to divide the data into groups. (See the [Floor Plan Tutorial](tutorials/imagemaptutorial.md#group-by) for details.)


![Overview](assets/img/cbuser/ds-publish.png "On Publish Event")

##### **"On Source Event" Streams**
This event is produced by a Vantiq Source and is equivalent to a `WHEN EVENT OCCURS ON "/sources/<source>" AS <message>` condition in a Rule. (The Stream will emit the associated message.)

You must select the Source that generates the messages. Note that there is no schema for the associated message (since it is not an instance of a server Type.)

The "Group By" field is optional and is only required by certain types of Widgets such as the FloorplanViewer. It specifies which property of the target Type is used to divide the data into groups. (See the [Floor Plan Tutorial](tutorials/imagemaptutorial.md#group-by) for details.)

![Overview](assets/img/cbuser/ds-source.png "On Source Event")

##### **"Timed Query" Streams**
These are simply timer events used to run a pre-defined SELECT at a regular interval. The Stream emits the results of the query.

You must select a server Type first. The "Update Interval" must be a non-negative number indicating the delay in seconds before the query is run again. (If this value is "0" the query is run once and never again.)

The "Group By" field is optional and is only required by certain types of Widgets such as the FloorplanViewer. It specifies which property of the target Type is used to divide the data into groups. (See the [Floor Plan Tutorial](tutorials/imagemaptutorial.md#group-by) for details.)

By default the entire query result is returned. If you click the "Limit maximum number of records to return" checkbox it will reveal some additional fields that will allow you set a limit and select the property to sort on (since setting a maximum isn't very useful without sorting the data first).


![Overview](assets/img/cbuser/ds-query1.png "Timed Query")

Once a Type has been selected you are allowed to set some simple constraints on the query (the "where" clause). These constraints are "and"ed together.

![Overview](assets/img/cbuser/ds-query2.png "Timed Query")

If the simple constraints are not sufficient you can click the "Use Advanced Query" checkbox, allowing you to specify the "where" clause as a JSON object. (For more details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

![Overview](assets/img/cbuser/ds-query3.png "Timed Query")



##### **"Paged Query" Streams**
**This Data Stream may only be used with the DataTable widget**; it is used as an alternative to the Timed Query DataStream when the Type to be displayed contains so many records that loading them all into memory at once would cause performance problems. It only loads enough records from the Type to populate a single page of results; each time you page forward or backward in the [DataTable](cbref.md#datatable) it only loads as many records as needed.

You must select a server Type first.


![Overview](assets/img/cbuser/ds-pquery1.png "Paged Query")

Once a Type has been selected you are allowed to set some simple constraints on the query (the "where" clause). These constraints are "and"ed together.

![Overview](assets/img/cbuser/ds-pquery2.png "Paged Query")

If the simple constraints are not sufficient you can click the "Use Advanced Query" checkbox, allowing you to specify the "where" clause as a JSON object. (For more details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

![Overview](assets/img/cbuser/ds-pquery3.png "Paged Query")



<a name="client-event-detail"></a>
##### **"On Client Event" Stream**

This allows JavaScript code within your client to use an arbitrary condition to decide when to write some data into the Stream which is emitted to the bound Widgets. In order for the data that is emitting from this Stream to have a Schema you must specify a server Type or a global Data Object (such as "client.data.Employee").

Your JavaScript code will use some criteria to determine when to cause the Stream to emit data and then call the "sendClientEvent" method. "theObject" must be an object that matches the schema you configured into the Data Stream.

```js
client.sendClientEvent("MyDataStream",theObject);
``` 

![Overview](assets/img/cbuser/ds-client.png "On Client Event")


##### **"On Resource Event" Stream**

This stream is currently used internally by the Vantiq system and is not intended to be used by developers. The functionality provided by this stream is duplicated by the "On Data Changed", "On Publish Event" and "On Source Event" stream types. For example, the "On Source Event" is duplicated by using the "On Resource Event" stream and entering '/sources/<source name\>' in the _Event Path_ property.

#### Binding Data Streams to Views

In order to bind a widget to a Data Stream you simply select it and set the relevant properties from the property sheet.

A simple example of this can be seen if you select a Gauge - there are properties to select the Data Stream the Gauge should be bound to ("Data Stream") and which property should be used to extract the relevant value ("Data Stream Property"). Note that if the Data Stream is of the "Publish" or "Source" variety then there is no schema available and you are asked to **type in** the name of the property which contains the value the Gauge should display. For the other Data Streams (which **do** have a schema) you will see a dropdown list that will allow you select from the list of appropriate properties.

![Overview](assets/img/cbuser/ds-ex-gauge.png "Gauge Example")

Other widgets such as the LineChart may be a little more complicated. In this case you must select the "Data Stream" but then you will need to select which properties should be used to extract values for the x-axis and y-axis data. ("X-Axis Property" and "Y-Axis Properties".) Since a LineChart can plot more than one value at a time you are allowed to specify more than one "y-axis" property value. (Again, schema-less Data Streams will require you to enter property names explicitly rather than select them off a list.)

![Overview](assets/img/cbuser/ds-ex-linechart.png "Line Chart Example")


## Terminating the Client
Clients are launched from inside some other environment. At present that means one of three things:

* The Client was run from inside the Client Builder as part of testing the Client being edited.
* The Client was run directly from the "Client List" inside the Vantiq IDE.
* The Client was run from the "Client Launcher" or the "MPI" ([see below](#launching-clients-from-a-browser))

This means there will probably be some sense in which the Client's work is "done" and you want to return to the environment which launched you. (When running from the Client Builder or Client list there is also a "Stop Client" button which can be used to abort the running Client.) In any case there needs to be a way for the Client to declare that it has "terminated" and the calling environment should take control again. 

### Explicit Termination

You can explicitly ask to terminate the client directly from your code with the Client "terminate" method like this:

```js
client.terminate();
``` 

### Terminating with Default Buttons

If you add a Button you may add your own "On Click" event handler which can do whatever it likes, including calling the "terminate" method. However Buttons which have **no** event handler but whose Page has a "resource event" defined have a special default behavior.

See the ["Default Submit" Behavior triggered by a Button](#default-submit-behavior-triggered-by-a-button) section below for more information.



## Uploading data to the Server

A common purpose for Clients is to collect input data from the user and then upload it to the server where it can be used to drive Rules, Procedures and Collaborations. This input data comes in two different flavors:

* Scalar data - These are simple data values that the user enters into various types of Widgets, such as Strings, Numbers, etc. These data values are added as properties to a "response Object" which is attached to a "publish" operation. (The name of the corresponding Widget is used as the property name; the value of the property comes from the user's input.)

* Media data - These are binary objects that are captured by special widgets that capture audio, images or video (i.e. the AudioRecorder, Camera and VideoRecorder). These are not appropriate to load into the "response Object"; instead they must be uploaded into a Vantiq Document which is automatically assigned a unique name. A property is added to the "response Object" but the value is the name of the corresponding Document rather than the media itself.

The URLs for document data are [explained here](cbref.md#getdocumenturl).

(Note that the techniques described here are all asynchronous; the requests are **queued** and may not actually reach the server until later. This is usually within a few seconds, but in "offline mode" the requests will be "pending" until contact is re-established with the netwwork.)

There are four different approaches to choose from when uploading data from the mobile app to the server; these are described below.

### "Default Submit" Behavior triggered by a Button

If your Client contains a Button widget with no "onClick" handler **and** its Page has a resource event defined it is assumed that you want the "default upload behavior" - this means that all the Scalar data from the current Page is automatically loaded into a "response Object". Any media widgets from the current Page will upload their data into Documents and save the generated names into the "response Object" as well. That Object is attached to a published "resource event" which is described from the values defined for the Page. The Client will automatically exit (and if there was a Notification it will be removed from the "inbox").

Note that if no Default Resource and Resource Id is defined for a Page then clicking a button with no "onClick" handler will do nothing at all.

### "Default Submit" Behavior triggered programmatically

At times the behavior described above is what you want but you would like to take some action **before** the process begins. In this case you can trigger the "Default Submit" behavior programmatically using this method on the Page object:

```js
    //
    //  Take some actions before the submit begins
    //
    // ...
    // ...
    // ...

    //
    //  Trigger the "default submit" behavior and the Client will exit. You must supply a "submit value" (100 in
    //  this case). This is the number the would normally come from the "submitValue" property of the 
    //  triggering button.
    //
    page.defaultSubmit(100);
``` 


### "Default Submit" Behavior using the Uploader

Sometimes you need to exercise more control over the submit process. A common requirement is to trigger the "default submit" behavior but **without** exiting the Client when done. This involves using an instance of the "Uploader" object which requires more code but offers a richer set of features. 

Here is a simple example that uses an Uploader instance to implement the "default submit" behavior but then takes control over what happens afterwards (e.g. exit the Client, **not** exit the Client, switch to another Page, etc.).

```js
    //
    //  Initialize an Uploader object
    //
    var uploader = new Uploader(client);

    //
    //  Create the response object and upload requests for everything on the current page
    //
    uploader.addRequestsForCurrentPage();
    
    //
    //   Set the response "resource event" (using the default for the current Page or a hardcoded value).
    //   (Usually "responseResource" is "topics" and "responseResourceId" is a topic string.)
    //
    uploader.setResponseObject(null, page.responseResource, page.responseResourceId);
    
    //
    //  Start the Uploader - this will upload the Media data into Documents and publish 
    //  the filled-in responseObject to the indicated resource event (usually a topic).
    //
    //  Note that if you do *not* supply a callback then the Client will automatically terminate
    //  after the upload has been queued.
    //
    uploader.start(function (theUploader) {
        //
        //  Upon completion the Uploader will contain the actual data that will be sent to the server 
        //  in theUploader.responseObject. It will contain the final document names assigned 
        //  to each uploaded media object.
        //
        //  At this point you could tell the user, terminate the Client, switch Pages, etc.
        //
    });
```


### Custom Behavior using the Uploader

In some cases the "default submit" behavior is not sufficient: perhaps your Client wants to add some custom data to the response object or specify that only **some** of the "media data" should be uploaded. Here is an example that shows how you can use the Uploader to take full control over what data gets uploaded and what happens after.


```js
    //
    //  Initialize an Uploader object
    //
    var uploader = new Uploader(client);
    
    //
    //  Schedule the upload of data from a specific Camera Widget to a Document
    //
    uploader.addRequestFor("Camera6");
    
    //
    //  Add the value of a specific InputString widget to the response object
    //
    uploader.addRequestFor("InputString1");

    //
    //  Add any extra custom values you like; these will be added to the responseObject values which 
    //  were defined above. (These should be included inside a "values" object as shown.)
    //
    var additionalResponseObjectValues = {
        "values": {
            "a":1,
            "b":2
        }
    };

    //
    //  Declare the response object and the topic which should be used with the publish
    //
    uploader.setResponseObject(additionalResponseObjectValues,"topics","/my/payload/topic");

    //
    //  Start the Uploader - this will upload the Media data into Documents and publish 
    //  the responseObject to the topic.
    //
    //  Note that if you do not supply a callback then the Client will automatically terminate
    //  after the upload has been queued.
    //
    uploader.start(function (theUploader) {
        //
        //  Upon completion the Uploader will contain the actual data that will be sent to the server 
        //  in theUploader.responseObject. It will contain the final document names assigned 
        //  to each uploaded media object.
        //
        //  At this point you could tell the user, terminate the Client, switch Pages, etc.
        //
    });

```

See the Reference Guide [here](cbref.md#uploader) for more details.


## Launching Clients from a browser

There are two different ways to launch a Client in a web browser from outside of the IDE:

### The Client Launcher
The Client Launcher is an app that allows you to launch Clients without using the IDE and the Client Builder environment. Normally you would launch the IDE with a URL like this:

```
https://dev.vantiq.com/ui/ide/index.html
```

The Client Launcher uses a slightly different URL:

```
https://dev.vantiq.com/ui/rtc/index.html
```

It has a very simple interface: it shows a list of all the Clients which have been marked as "Launchable" in the Client property sheet. (See the [Client Properties](#client-properties) section above.)

To appear in the Client Launcher list the Client must also have a "Target Device" setting of either "Browser Only" or "Browser and Mobile"; Clients marked "Mobile Only" will not appear.


![Overview](assets/img/cbuser/launcher.png "Client Launcher")

Simply click on the Client to launch it. When the client terminates it will return to this list.

You may also launch a Client directly with a URL like this:

```
https://dev.vantiq.com/ui/rtc/index.html?run=MyClient
```

To make sure it targets the correct namespace rather than the user's current namespace, you can add the `targetNS` parameter like this:

```
https://dev.vantiq.com/ui/rtc/index.html?run=MyClient&targetNS=ClientNamespace
```

#### Customizing the Client Launcher

By default the Client Launcher displays a "navbar" at the top of the browser window that uses the standard Vantiq style (icon, colors, fonts. etc.). When you launch a Client (either directly or from the list) the Clients show the same navbar and styling.

It is possible to customize the styling of this navbar for all the Clients within a given namespace. You need to create a single Document named "vantiq/navBar.json" that contains any properties to be overridden. For example:

```js
{
    "bgColor": "#00ffff",
    "fgColor": "#ff0000",
        
    "titleFontFamily": "cursive",
    "titleFontStyle": "italic",
    "titleFontSize": 30,
    "titleFontWeight": "bold",

    "icon": "../../docs/myIcon.png",
    "iconWidth": 100,
    "iconHeight":50
}
```

Only properties you specify is overridden; all others is remain set to their Vantiq defaults.


These values may also be overridden at runtime from inside the Client itself. These properties are defined on the Client object:

* [client.navBarBackgroundColor](cbref.md#navbarbackgroundcolor)
* [client.navBarForegroundColor](cbref.md#navbarforegroundcolor)
* [client.navBarTitleFontFamily](cbref.md#navbartitlefontfamily)
* [client.navBarTitleFontStyle](cbref.md#navbartitlefontstyle)
* [client.navBarTitleFontSize](cbref.md#navbartitlefontsize)
* [client.navBarTitleFontWeight](cbref.md#navbartitlefontweight)
* [client.navBarIcon](cbref.md#navbaricon)
* [client.navBarIconHeight](cbref.md#navbariconheight)
* [client.navBarIconWidth](cbref.md#navbariconwidth)
* [client.navBarTitle](cbref.md#navbartitle)
* [client.navBarShowControls](cbref.md#navbarshowcontrols)




Note that these settings **do not** effect Clients running in a mobile device (since no navbar is shown).

### The Mobile Platform Interface (MPI)

When running Clients on a mobile device your Client is actually running inside a "WebView" object - the Client runs within a special purpose web app called the MPI. You can also use the MPI to run specific Clients directly from a web browser by using a URL like this:

```
https://dev.vantiq.com/ui/mpi/index.html?run=MyClient
```

You can run any Client using the MPI, even if it has not been marked "Launchable" and even if it has been set to "Mobile Only". However, remember that some widgets (such as the Camera) would not work in this mode.

## Debugging

Before a Client starts execution all of your callback and custom code is assembled into a file called "ClientCallbackEvents.js" and injected into the HTML page so the functions can be called when needed. During development you can use your browser's built-in debugger to see this code at runtime and set breakpoints in the usual manner.

One of the drawbacks of JavaScript development is that often the runtime environment will "eat" any errors and exceptions, making failures very mysterious. The Vantiq Client execution environment will try to **catch** all exceptions in your code and display them in a popup dialog before terminating the client.

For example, suppose you create a Client which contains only a single InlineButton like this:

![Overview](assets/img/cbuser/crash1.png "Crash App")

The Button is given a name "crashButton" with a label of "Boom". The "On Click" event handlers is set to this:

```js
//
//  This function is called when the user clicks the 'crashButton' button.
//
Client_Start_crashButton_onClick function (client,page,extra)
{
    var a = null;
    a.boom();
}
```

Obviously this code will throw an exception if the "Boom" button is clicked. When that happens the exception is trapped and turned into a popup dialog showing the error like this: (note the details will vary between browsers; this example was done using Chrome.)

![Overview](assets/img/cbuser/crash2.png "Crash App")

After the user clicks the "OK" button the Client will terminate.

There are clues in the call stack that tell us what happened. First is the error message itself:

```
Cannot read property 'boom' of null
```

The top line of the error stack tells us where it happened:

```
at PIInlineButton.Client_Start_crashButton_onClick (ClientCallbackEvents.js:8:3)
```

The generated function name for a widget event handler will have a form like

```
Client_<page name>_<widget name>_<event name>
```

So we can assume that the problem happened on the "Start" page in the "OnClick" event of the "crashButton" widget.

You could also use your debugger to load "ClientCallbackEvents.js" and set a breakpoint inside the offending method and investigate the problem that way.

### Remote Debugging Clients on Android Devices

While it is always easiest to do most of your debugging inside a browser using the Client Builder there are
some features which make that impractical. (For example, any Client using a mobile-only widget like the Camera can't
be fully tested inside a browser.) 

It **is** possible to debug running Clients directly on Android using the "remote debugging" facility provided by the 
Chrome browser. Setting up this process is rather complicated and is described here. This requires attaching your Android
device to your computer using a USB cable and configuring your Android device to allow access.

#### Turn on "Developer Mode" on your Android device

The first step is to turn on "developer mode" on your Android device. Unfortunately this process is not always the
same on every Android model, so your best bet is to do an online search for the exact device you own. For example,
you might use Google to search for something like this:

```txt
Turning on developer mode Samsung Galaxy 7
```

This will usually reveal a page with the exact instructions for turning on "developer mode" on your Android device.
This process often varies from model to model, but most are a variation on something like this:

1. Launch the "Settings" app from your Home screen or the app drawer.
2. Tap on "About Device". 
3. Tap on "Software Info".
4. Tap on the "Build" number 7 times.

At this point the list of "Settings" will include a new item called something like "Developer Options".

The Developer Options page will contain a item called "USB debugging" which you must set to "on".

#### Attach your Android device to your personal computer with a USB cable

Your phone probably came with a cable used for charging; use this to connect your Android device to a USB port on your
personal computer.


#### Enable JavaScript debugging inside the Vantiq Android App

By default the Vantiq Android App does not allow remote JavaScript debugging. It must be turned on from inside the App;
you will find a "Settings" item inside the menu (which can be popped up using the "hamburger" button (three vertical dots) in the
upper-right-hand corner of the display).

Inside the Settings screen is an item labeled "Enable JavaScript debugging" which must be turned on. The next time you
launch a Client from the device it is enabled for remote debugging. This option will stay on unless you disable it.

#### Use a Chrome browser to access the "Remote Debugging" tool

The details of the process vary depending on the version of your Chrome browser, but here is a general description:

In the upper-right-hand corner of the Chrome browser you should find a "hamburger" button which can be clicked 
to pop up a menu; underneath the "More Tools" menu is an item called "Developer Tools". Select it.


 
![Launch Developer Tools](assets/img/cbuser/AndroidDebug1.png "Launch Developer Tools")


This will open another window titled "DevTools". In the upper-right-hand corner you will find another 
"hamburger" button which pops up another menu. It will again contain a menu item called "More tools", and inside 
of **that** you will find an item called "Remote Devices":

![Open Remote Devices Tab](assets/img/cbuser/AndroidDebug2.png "Open Remote Devices Tab")


Selecting "Remote Devices" will open a panel in the lower half of the DevTools window that will contain
a "Remote devices" tab:

![Remote Devices Tab](assets/img/cbuser/AndroidDebug3.png "Remote Devices Tab")

If your previous steps were done correctly the left-hand side of the display will contain a column labeled
"Devices" and you should see an item that describes your Android phone. In this example that means an item
called "SM-G93OU" which shows "Connected'.

If you now go to your Android phone and launch a Client the Vantiq App's internal WebView is relaunched with "remote debugging" enabled
and your "Remote Devices" pane will change to look like this: (Note that you may have to click on the text that says "Connected" in order to 
switch from the "Settings" display to the display that points to your device.)

![Open Debugger](assets/img/cbuser/AndroidDebug4.png "Open Debugger")

There should now be an item that indicates you can connect to a WebView; on the right side there is a button labeled
"Inspect". If you click that button a new window should open containing a Chrome debugger which is connected to 
your running Client.

![Debugger](assets/img/cbuser/AndroidDebug5.png "Debugger")

You should now be able to use the Debugger window against your Client as it runs in the Android
device.


## Field Validation

Many Clients will require some kind of validation to be done on the data which users enter into widgets. The Client runtime system contains a set of features to make this process easier.

The process of "validating input data" will automatically be triggered whenever the user does a "submit" for a page. (See [here](cbref.md#defaultsubmit) for a discussion of the different ways the Client can trigger a "submit".)

The Validation process evaluates all the input widgets on a Page and decides if they currently contain valid input values. If all widgets successfully pass validation then the "submit" will continue; if any widgets fail then the "submit" is aborted and the user is directed to the widgets which must be edited before the "submit" will succeed. 

Validation can also be triggered programmatically by invoking the current Page's "validate()" method; if the method returns "true' then the validation was successful. (This is useful if you want to validate the fields but don't want to do a "submit".)

The validation process consists of four steps - the first two are done automatically by the Client runtime system and don't require any work from the developer. The last two allow the developer to add Client-specific handlers that can make their own determination about whether the widgets are in a valid state or not.

There are ways in which widgets are evaluated -

#### Step 1 - Check for missing "non-optional" Widgets

Some widgets have an "Is Optional" property; if the developer has set a widget's "Is Optional " property to "false" then validation will fail if the user did not enter a value.

#### Step 2 - Check for legal numeric input

Make sure that all IntegerInput or RealInput widgets contain values which can be recognized as a valid number. Widgets with no input at all (the empty string) are interpreted as "null".

#### Step 3 - Execute "onValidation" handlers for any widgets which defined them

Certain widgets support an "onValidation" handler; if not specified then there is no additional validation done. But if the developer enters code for the handler you can write any test you like for the contents of the widget. If there is some Client-specific reason why the widget should be considered "not valid" then you simply return an error message using the supplied "vco" (Validation Control Object). For example, suppose you have an IntegerInput widget and specify an "onValidation" handler like this:

```js
//
//  This function is called when the widget is asked to validate its current
//  contents (Note that 'this' points to the widget itself and 'vco' is the
//  ValidationControlObject)
//
function Client_Start_InputInteger3_onValidation(client,page,vco)
{
    if (!vco.valueWasEntered)
    {
        vco.error = "No integer value was entered.";
    }
    else if (vco.valueAsNumber >= 10)
    {
        vco.error = "Value must be < 10 (" + vco.value + ")";
    }
}
```

If this handler is called you can assume that the widget passed the first two tests; that is, (1) it is not a non-optional widget without input and (2) if there was a value entered it is a valid integer (or null). If either of these conditions are true then the widget has already been flagged as "not valid" and the onValidation handler will **not** be called.

This widget is assumed to be valid unless your code sets an error message in the "vco.error" property. To make it easier to write your tests the VCO contains various useful values which tell you things about the input being validated:

```js
class ValidationControlObject
{
    //
    //  If "true" there was *something* entered in the field; if "false" it means the field was empty
    //
    valueWasEntered:boolean;
    
    //
    //  This is the value that was entered in its original form
    //
    value:any;
    
    //
    //  This is the entered value rendered as a String
    //
    valueAsString:string;
    
    //
    //  This is the entered value rendered as a Number (or "null" if the value was "not a number")
    //
    valueAsNumber:number;
    
    //
    //  This is the entered value rendered as a Date or null (this field is only used with the InputDate and InputDateTime widgets)
    //
    valueAsDate:Date;
   
    //
    //  After analyzing the input the handler may set this value to an error string that should be presented to the
    //  user; if left as "null" it means the input can be considered valid.
    //
    error:string;
}
```

In the example above the code tests two different conditions: (1) Has a value been entered? (2) Is the integer less than 10?

The first test could have been accomplished using the "is Optional" property, but for complicated validations you may want to do that test yourself, perhaps to provide a custom error message.

If one of the tests fails (causing the vco.error field to be set) then the widget is considered "invalid" and it is marked as such so the user knows it needs fixing.

Note that just marking one field as "invalid" does not abort the validation process - multiple widgets might be marked as invalid at the same time.

The onValidation handler can also be used with InputDate and InputDateTime - in the example below we check to make sure that the entered date is not in the future:

```js
//
//  This function is called when the widget is asked to validate its current
//  contents (Note that 'this' points to the widget itself and 'vco' is the
//  ValidationControlObject)
//
function Client_Start_InputDateTime1_onValidation(client,page,vco)
{
    if (vco.valueAsDate)
    {
        var now = new Date();
        
        if (vco.valueAsDate.getTime() > now.getTime())
        {
            vco.error = "Date is in the future";
        } 
    }
}
```

Developers may also use the features provided by [validate.js](https://validatejs.org/) for validating JavaScript objects inside a widget's "onValidation" handler. Since a widget usually has only a single value, developers should use the 'validate.single' method. For example, here is a validation to check for a legal email address using the 'email' validate.js built-in configuration:

```js
//
//  This function is called when the widget is asked to validate its current
//  contents (Note that 'this' points to the widget itself and 'vco' is the
//  ValidationControlObject)
//
function Client_Start_InputString1_onValidation(client,page,vco)
{
	var v = validate.single(vco.value, {email:true});
	if (v && (v.length > 0) {
		// return the first error
		vco.error = v[0];
	}
}
```
'validate.single' returns either _undefined_ or an array of error strings. In this example, we pass the value of the ValidationControlObject and _{email:true}_ as the configuration object specifying _email_ as the validator.

The developer may also write their own validators by customizing the _configuration_ parameter of 'validate.single'. For example, here is a custom validation to check for basic formatting of a US ZIP Code:

```js
//
//  This function is called when the widget is asked to validate its current
//  contents (Note that 'this' points to the widget itself and 'vco' is the
//  ValidationControlObject)
//
function Client_Start_InputString1_onValidation(client,page,vco)
{
	var v = validate.single(vco.value, {format:{pattern:/^\d{5}(-\d{4})?$/,message:"Not a valid ZIP Code"}});
	if (v && (v.length > 0) {
		// return the first error
		vco.error = v[0];
	}
}
```

#### Step 4 - Execute the Page's "onValidation" handler

If all the preceding validation steps were successful for all widgets, then the last step is to run the "onValidation" handler on the Page (if there is one). If this handler runs you know that all individual widgets have passed their tests. This Page "onValidation" handler allows you to do any kind of "cross-field" validations, such as "widget A must be less than widget B". For example, a Page's "onValidation" handler might do something like this:

```js
//
//  This function is called when the current page is being validated page.
//  It is only called if all the widgets on the page have been deemed valid.
//
function Client_Start_onValidation(client,vco)
{
    if (this.data.myField1 >= this.data.myField2)
    {
        vco.error = "Field 1 (" + this.data.myField1 + ") must be less than Field 2 (" + this.data.myField2 + ")";
    }   
}
```

#### What does the user see?

If any widgets fail the "Is Optional" validation test, a popup message is displayed and the widgets are a given a dotted red outline.

<SHOW SCREENSHOT>

If widgets fail validation for any other reason they are given a solid red outline and there is an additional error message that explains the problem with each widget. 

<SHOW SCREENSHOT>

When running the Client on a Browser the error message will appear nearby when the mouse pointer hovers above the widget.

When running the Client on a mobile device (where of course there is no mouse) the rules must be different. If the widget is one which requires the keyboard (such as IntegerInput or StringInput) the error message will appear when you touch the widget to give it the input focus. If the widget is one which does not require keyboard input (such as the DateTime widget) then the error message will always appear and will clear as soon as you touch it again.

## Loading Fonts
Widget text in a Client can be displayed using a font other than the standard fonts selectable in the widget or theme properties. Fonts, such as [Google Fonts](https://fonts.google.com/), are defined in terms of CSS so can be loaded using a Client's CSS Custom Assets. To add Custom Assets, open the **Client Properties** dialog, navigate to the **Basic** tab, then click the **Click to Edit** link under the _Custom Assets_ label:

![CustomAssets](assets/img/cbuser/CustomAssets.png)

In the example above, three Google Fonts, Sofia, Playwrite India, and Ubuntu, are loaded using their URLs from the Google Fonts site. Once the Client has been saved, whenever the Client is opened or loaded, any fonts specified as CSS assets are available in both the Client theme or individual widgets using the Font Face property:

![FontFace](assets/img/cbuser/FontFace.png)

It is important to note that each Client that uses a Custom Assets font needs to add the font in that Client's Custom Assets properties list. If during development a Client is opened that loads Custom Assets font(s), then those fonts may _appear_ to be available for any other open Client, even if the font has not been added to the other Client's Custom Assets. This is because those fonts are loaded in the Vantiq IDE browser instance so are available to all Clients until the browser is reloaded.

## Accessing Documents

_Note that while in this section we use a PNG image as an example of a Modelo Document, this discussion of URLs also applies to any kind of Document (JPEG, CSS, JS, text, etc.). You will find these Document references when specifying "Custom Assets" as well as various Widget property sheets._

Documents are accessible from within a running Client using a URL like this:

```
https://dev.vantiq.com/docs/myImage.png
```

But since a Client may run in different servers you don't really want to hardcode the server name.  When pointing at this document from within a Client (such as within the property sheet for a StaticImage Widget) you can type the document name using a "relative" path like this:

```
../../docs/myImage.png
```

This way the Client will know you mean to reference a Document within the current server. You can also use a shortened form and the Client will still know what you meant:

```
myImage.png
```

It is also possible to access this Document from **outside** the namespace by adding an argument containing a valid access token:

```
https://dev.vantiq.com/docs/myImage.png?token=yJqTaR7II96-6PkgQio7y1f7tOLWxMUNFGrHITn_A2g%3D
```

(The access token implies which Namespace the image will be found in.)

You can create a "public" document within a namespace by giving it a name with this special form:

```
public/myPublicImage.png
```

When a Document is "public" the image can be accessed from outside the namespace with a special URL like this:

```
https://dev.vantiq.com/ui/docs/NS/MyNamespace/myPublicImage.png
```

Since the image is "public" no access token is required, but you must use this form to specify the proper Namespace.

Document URLs are also discussed [here](cbref.md#getdocumenturl).

## Public Clients

Public clients may be run by users without first authenticating and do not require any Vantiq account to access. Public 
Clients can be accessed through a fixed URL similar to launching a Client directly though MPI or RTC with the addition 
of a namespace query parameter. For example, if `MyClient` is a Public Client in `MyNamespace`, it could be launched 
from the following URL:

```
https://dev.vantiq.com/ui/mpi/index.html?run=MyClient&namespace=MyNamespace
``` 

To get the RTC or MPI URL to launch a client in "Public Mode" use the Launch Menu and copy the url to the clipboard
using one of the options below the dividing line:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CopyPublicUrl](assets/img/cbuser/copyPublicClientUrl.png "Copy URL To Clipboard")

The addition of the `namespace` query parameter forces the Client into "Public Mode", which means all requests to the 
Vantiq Server will be made using the equivalent public API endpoint. There is no need to log out to test a client in 
"Public Mode". Authenticated users and developers may run and test their Clients in "Public Mode" by launching the 
Client through MPI or RTC with the extra `namespace` query parameter and the client will behave for them the same as it 
will for an un-authenticated user. 

### Public Client Restrictions

When running in "Public Mode", Clients will only be able to perform certain requests against the Vantiq server. When 
running in "Public Mode" the only interactions that can be made with the server are public interactions, which means you
can only invoke [Public Procedures](./rules.md#public-procedures) and query for 
[Public Resources](./api.md#public-resources). 

In addition, certain widgets that work in the Vantiq Mobile App cannot be used in Public Clients, for instance the 
Camera, Video, and Audio widgets all require access to device hardware that requires the Vantiq Mobile App.

Lastly, Public Clients are restricted to only use "Client Event" Data Streams. Without authenticating, the user running
the Public Client does not have sufficient authorizations to subscribe to events as they occur in the Vantiq server. 

In total, these restrictions mean Public Clients are forced to perform all of their Server interactions through Public 
Procedures which implement all of the underlying Server functionality. For an example, please import the `Public Client`
Contribution from the Import Projects Popup.

### When to use Public Clients

In some situations there is functionality that should be completely public, such as a sign-up form for an email newsletter,
or an app to check the weather. Both of these Clients are low-risk and don't need a Vantiq identity to function. These 
could be built as completely Public Clients.

It's also possible to build Public Clients that on-board users into a namespace that will host other Clients that require
authentication. The Public Client could simply be a form that collects a new user's information (name, email, etc) and 
passes that information in a call to a Public Procedure. The Procedure would then evaluate the input information, determine
whether or not the submitter should have an account created, and then can proceed to invite the submitter to create a 
Vantiq identity to access restricted features. 


### Enabling Public Access To Clients
Clients can be marked as "Public" under the "Advanced" Property Sheet.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![MarkPublic](assets/img/cbuser/markpublic.png "Mark Public")

Public Clients must also be launchable, as the only way to run non-launchable clients is through receiving a notification
in the Vantiq mobile app (which requires authentication).


## Localizing Clients

When you build a Client from Widgets and JavaScript code you will probably have initialized all user-visible fragments of text using your native language. If the target audience for Client does not share your language you may want to "localize" the text in your Client for various target locales. This section describes that process.

The process of localization usually involves identifying all of the bits of text that your Client contains which is visible to the end user. In general this text gets specified in two places:

* Widget Properties (e.g. Button labels, Text labels, etc)
* Text produced by your code at runtime (e.g. formatted error messages)

The typical approach to this problem requires you to produce a "message hash table" where you assign each fragment of text a unique name and then use that "message key" within your Client instead of the literal text. You create a series of files or tables that contains the actual value that should be used for the various locales required by your target audience. At runtime the message key is replaced by the proper literal value for the browser's locale.

Vantiq Clients use a similar approach with one slight change. We recognize that many of the text fragments are used only once within a Client, and it would be awkward to have to define them all one place and then use them somewhere else. To mitigate that problem we have two kinds of localized messages:

### Global Messages
There certainly *are* some messages which are used in multiple places such as Button labels. In such cases it certainly makes sense to define these fragments in one central place and then just reference them where needed. For example, it is possible that you would need the string "OK" to use with more than one button. In the Client Property sheet under the "Localization" section you can open a popup which will allow you to define such global symbols. During development you only need to define the value of these items using your default language, which means you might create an entry called "@btn.OK" and give it a default value of "OK".

Any appropriate Buttons should have their label set to "@btn.OK" (instead of the literal "OK"). As we will see later there is a way to provide alternate values for "@btn.OK" for other locales.

### Local Messages
The majority of localized messages only need to be defined "locally" (i.e. near the point they are used; Text labels are the most common example of this). You **could** use the centrally defined global messages but that's kind of awkward. Instead Clients allow you define the symbol and the value in the same place. 

For example, StaticText Widgets have a property called "Text" which is set to the literal text you want to display. Instead you can set the Text property like this:

$text.my.label = My Text Label

When editing in the Client Builder this StaticText widget will display as "My Text Label". When the Client is actually running the runtime system will look up the symbol "$text.my.label" and display the value for the current locale.

### Choosing Message Keys
Message keys must follow a standard format. They all must start with either "@" for global messages or "$" for local ones. The rest of the symbol should be made of alphanumeric characters and ".", "-" or "_". Traditionally these names are used to "group" the symbols in some meaningful way, such as where the message would be used or what it would be used for:

```
$text.page1.HelloWorld = Hello World!
$text.error.badValue = The entered value is invalid.
$droplist.value.red = Red
$droplist.value.green = Green
$droplist.value.blue = Blue

```

#### Local Messages in JavaScript code
These local messages can also be defined (and used) inside JavaScript code. There is a method defined on "Client" called "formatMsg" that allows you to look up the value of the message in the current locale and optionally substitute parameters within it. For example:

```js
//$my.text.msg = Hello, World!
//$my.error.msg = The {0} jumped over the {1}.

var cat = "Cat";
var dog = "Dog";
var msg1 = client.formatMsg("$my.text.msg");
var msg2 = client.formatMsg("$my.error.msg", cat, dog);

client.errorDialog(msg2);
```

Local messages are defined inside JavaScript by including them inside a comment; the example above defines two local messages called "$my.text.msg" and "$my.error.msg". The position of the comment does not matter; it can appear anywhere inside your code as long as it starts in column 1. Note that there must *not* be any spaces between the "//" and the leading "$" of the message name.

To use the localized message you must call the "formatMsg" method which is defined on "client". If you only supply a single argument then "formatMsg" just performs a lookup, returning the message value for the current locale. Additional arguments is substituted into the message where the special "{n}" expressions are found (where the first argument replaces {0} and so on).

In the example shown above the value of msg2 (in the default locale anyway) would be 

```txt
The Cat jumped over the Dog.
```

### Supporting additional Locales
Once your Client has been converted to use the global and local symbols instead of hardcoded literals you can start to think about supporting other locales at runtime. You do this by "exporting" all the symbols that have been defined along with their default values. You can export your symbols as either a JSON file (called "default.json") or using the traditional "Java properties file" format ("default.properties"). For every locale that you wish to support you will need to create a file which *overrides* the symbols which have been defined.

For example, let's say your default.json file looks like this:

```json
{
  "INFO": "Exported from Client 'DevLocalize' on 9/12/2018, 11:23:12 AM",
  "@btn.yes": "Yes",
  "@btn.no": "No",
  "$pet.cat": "Cat",
  "$pet.dog": "Dog",
  "$my.error.msg": "The {0} jumped over the {1}."
}
```

(The "INFO" property is added automatically during "export" and can be ignored.)

If you wanted to localize your Client for Spanish (locale "es") you would create a new file called "es.json" and initialize it like this:

```json
{
  "@btn.yes": "Sí",
  "@btn.no": "No",
  "$pet.cat": "Gato",
  "$pet.dog": "Perro",
  "$my.error.msg": "El {0} saltó sobre el {1}."
}
```

Note that you are not required to supply a new value for *every* message. Any message which you have not overridden will simply use the "default" value for the message. (For example, it so happens that the English and Spanish words for "No" are identical. If you omitted the definition of "@btn.no" from the "es.json" file it would actually have no effect, since the value from "default.json" would be used.)

Some Locales have a "country specific" variant where *some* words are different. For example, there is the "Mexican Spanish locale" known as "es-mx". Here you could override any messages which are different from the "Generic Spanish" values specified in "es".

There are several formats that are sometimes used to specify the name of the locale. For our purposes we separate the "language code" (es) from the "country code" (mx) with a hyphen (-) and the entire string is in lowercase.

All message files ("default.json" and any locale-specific files you have created) must be placed in the same directory or zip file which can then be imported into the Client.


#### Exporting message tables

You Export your Client's currently defined symbols using the "Localization" section of the Client Properties popup, where you may choose to export the files in either "JSON" or "Java Properties" format. The results is a zip file that define a single directory with all your locale files inside.

#### Importing message tables

After exporting your symbols and adding any translated "locale-specific" files to the directory you may import them back into the Client using the "Localization" section of the Client Properties popup. (You can import them from a zip file or simple directory).

The symbol files will *completely replace* the previously defined symbols in the Client. Once the Client is saved your symbols is saved with it. 

### Testing locales from the Client Builder

Once you have completed a Client and imported a set of localized symbols you may want to test your Client using various locales. You can always do this by changing your Browser's locale setting and then restarting Modelo but there is a quicker way.

Open the Client property sheet and select the "Localization" tab. You will find a dropdown list labeled "Force Locale when testing". There you may select one of the various locales which you have imported, and when you run the Client from within the Client Builder the runtime system will pretend that you are running under the selected locale.

This setting of this option will persist and be saved along with the Client.

Note that this setting **only** has meaning to the Client Builder - it has no effect when running the Client from a mobile device or within the Client Launcher or MPI.


### Changing locales at runtime

Normally a Client will simply run with whatever locale the end user has selected as the default in their browser or mobile device. But in some circumstances you may wish to force a particular locale at runtime, either by choosing one programmatically or allowing the end user to select one themselves.

There is a property of the Client object that allows you to override the current locale programmatically called overrideLocale which you can use like this:

```js
    client.overrideLocale = "es-mx";
```

Changing this property at runtime will force all the localized messages to be reset as if the environment's locale had changed.



## Client Startup 

When a Client starts there are a sequence of actions that take place and a related sequence of events that may be fired 
if they are defined:

1. If there are any JavaScript or CSS assets defined for the Client they are "injected" into the HTML page. This is an asynchronous 
operation, which means there is no way of knowing when all these loads will complete. When that happens the Client's 
'On Assets Loaded' event is fired.

2. The Client 'On Start' (if there is one) is fired; there is no guarantee as to whether the asset load has completed or not. 
You should not write any code in this handler that assumes the assets are loaded.

3. The Page 'On Client Start' events (if there are any) are called next. Again, you should not write any code in this 
handler that assumes the assets are loaded.

4. The Start Page's 'On Start event (if there is one) is fired last. Again, you should not write any code in this 
handler that assumes the assets are loaded.

At some unpredictable point after step (1) the Client 'On Assets Loaded' event **will** fire, at which time it is safe 
to assume that all the assets have been loaded. 
The actual timing will vary depending on network conditions and browser caching.

What if you have some actions that you want to take only after **both** the assets have completed loading and the 
Client 'On Start' event has been run? A simple technique to accomplish this is to create two global boolean variables, perhaps
something like "client.data.assetsLoaded" and "client.data.onStartComplete". Then you add code like this to the bottom
of each handler:

```js
    // At the bottom of the Client 'On Start' Event
    client.data.onStartComplete = true;
    finishInitialization(client);
```

```js
    // At the bottom of the Client 'On Assets Loaded' Event
    client.data.assetsLoaded = true;
    finishInitialization(client);
```

and then define a function in the "Common Code" area like this:


```js
    function finishInitialization(client)
{
     if (client.data.onStartComplete && client.data.assetsLoaded)
     {
         //
         // Do any final initialization that requires the assets to be loaded and the Client 'On Start'
         // event to be completed
         //
     }
}
```

## Client Resources
Clients are web apps designed to run in a browser-like environment, whether in a desktop browser or in the Vantiq mobile apps. The Client runtime platform allows the Client developer to specify JavaScript and CSS files that are loaded by using the previously described Custom Assets features. In addition, the Client runtime platform also automatically loads a number of JavaScript libraries that are available for use by the developer.

Here is a list of the UI-oriented JavaScript libraries automatically loaded and usable by Clients:

* [AngularJS](http://angularjs.org) -- Angular JavaScript runtime framework (v1.8.0)
* [Bootbox.js](http://bootboxjs.com/) -- Modal dialogs for bootstrap (5.4.0)
* [Bootstrap](http://getbootstrap.com/) ​-- HTML/CSS/JS framework (v3.4.1)
* [Bootstrap Datepicker](https://www.eyecon.ro/bootstrap-datepicker/#) -- Date picker plugin for bootstrap (2012)
* [Bootstrap Multiselect](https://github.com/davidstutz/bootstrap-multiselect) -- multi-select plugin for bootstrap (0.9)
* [bootstrap-slider](https://github.com/seiyria/bootstrap-slider) -- slider widget for bootstrap (9.9.0 )
* [CodeMirror](https://codemirror.net/) -- JS text editor (5.65.16)
* [D3](http://d3js.org/) -- JS data visualization (3.5.5)
* [DataTables](https://www.datatables.net/) -- Data Tables (1.10.11)
* [Fancytree](https://github.com/mar10/fancytree/) -- JS tree component (2.30.2)
* [FullCalendar](https://fullcalendar.io/) -- JS calendar UI (v4.0.2)
* [heatmap.js](https://www.patrick-wied.at/static/heatmapjs/) - JS dynamic heatmaps (v2.0.5)
* [JQuery](https://jquery.com) -- JQuery JavaScript Library (v3.5.1)
* [jQuery-contextMenu](https://swisnl.github.io/jQuery-contextMenu/) -- Context menus (v2.4.3-dev)
* [jQuery UI](http://jqueryui.com/) -- jQuery-based UI library (v1.11.4)
* [jQuery MiniColors](https://github.com/claviska/jquery-minicolors) -- jQuery-based color picker
* [ngPopup](http://markocen.github.io/ngPopup/ngPopupDemo.html) -- JS modeless dialog (v0.4.1)
* [ngToast](http://tameraydin.github.io/ngToast) -- Angular toast notifications (v1.5.4)
* [Moment](https://github.com/moment/moment) -- Date/Time utilities (2.29.4)
* [Numeral.js](http://numeraljs.com/) -- Number formatter (2.0.6)
* [TouchSwipe](https://github.com/mattbryson/TouchSwipe-Jquery-Plugin) -- Detect swipes for touch devices (1.6.18)
* [Validate.js](http://validatejs.org) - Validation tools (0.12.0)
* [ZingChart](http://www.zingchart.com/) -- Line/Bar Charts (2.9.9)


Please note that the loaded libraries listed above may *not* be the latest versions. If the Client requires versions different from the loaded libraries, please use the Custom Assets features to load those different versions.

## Offline Operation
Clients are often run in the Vantiq Android or iOS apps, for example, as part of a collaboration Notification task. (Please see the [Collaboration Tutorial](tutorials/introcollaboration.md) for an example of how Clients are used in a collaboration.) Clients run on a mobile device are usually run with the expectation that the device has an active network connection, either WiFi or cellular. However, it is sometimes the case that a device is run an environment that has limited or no network connectivity. The Vantiq mobile apps recognize when network connectivity is lost or is intermittent and operate in a degraded but still functional manner. This section describes running Clients and the mobile apps in general in an offline environment. (This does not apply when running a Client in a browser.)

When the Vantiq mobile apps detect that there is no network connectivity, an offline banner is displayed at the top of many of the views. For example, when running a Client in offline mode, the offline banner is displayed at the top of the Client:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![OfflineClient](assets/img/OfflineClient.png "Offline Client")

Not all Client widgets work without network connectivity. The Map widgets are a notable example since map updates need location-specific images to be downloaded in order to be accurate. Many of the Data Display widgets (e.g., Line and Pie Charts, Tables and Numbers) also require an active network connection in order to provide real-time data. When in offline mode, these data-fed widgets are displayed but their data isn't updated.

There are times when your mobile app is not technically offline but the network response is so poor or erratic that it interferes with normal operation. There is a setting in the Vantiq app called "Work Offline" which you can turn on to tell the app to act as if there is no network (which can actually lead to better behavior for some Clients.)

### Using StaticImages in Offline mode

The StaticImage Widget **can** work in offline mode if its configured resource has previously been retrieved and cached while online. This caching is done by the mobile app in one of two ways:

* Images are cached "implicitly" when the StaticImage Widget is displayed at least once while the mobile app is online. That is, if the user visits a Page that contains the StaticImage while the mobile app is online the image will be automatically cached and so will be available when the Client is later run in offline mode.

* Images may be cached "explicitly" by adding them to the Client's _Offline Assets_ list. This list causes images (whether Vantiq-hosted or externally hosted) to be automatically cached the first time the Client runs in online mode whether the StaticImage is visible or not. To specify these resources you use the Client **Properties** button to display the Client Properties dialog, click the _Basic_ tab then click the _Custom Assets_ link to display the Custom Assets dialog (see below). You may specify an external asset by typing in its URL, or a Vantiq-hosted asset by using the **Select or Upload Document** button (small cloud with up arrow). (See the [Accessing Documents](#accessing-documents) section for a discussion of how to reference a Document.)

### Using ImageViewers and DocumentViewers in Offline mode

The ImageViewer and DocumentViewer Widgets **can** operate in offline mode if their configured resources are retrieved and cached while online. This caching is done by the mobile app in one of two ways:

* Assets are cached "implicitly" when ImageViewer or DocumentViewer Widgets are displayed at least once while the mobile app is online. That is, if the user visits a Page that contain a ImageViewer or DocumentViewer and clicks it to display the resource while the mobile app is online the resource will be automatically cached and so will be available when the Client is later run in offline mode.

* Assets may be cached "explicitly" by adding them to the Client's _Document Assets_ list. This list causes resources (whether Vantiq-hosted or externally hosted) to be automatically cached the first time the Client runs in online mode whether the Widgets that use them are activated or not. To add resources you use the Client **Properties** button to display the Client Properties dialog, click the _Basic_ tab then click the _Custom Assets_ link to display the Custom Assets dialog (see below). You may specify an external asset by typing in its URL, or a Vantiq-hosted asset by using the **Select or Upload Document** button (small cloud with up arrow). (See the [Accessing Documents](#accessing-documents) section for a discussion of how to reference a Document.)


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![OfflineAssets](assets/img/OfflineAssets.png "Offline Assets")


### Submitting Data in Offline mode

If a Client submits data while in offline mode, that data is added to the _Pending Uploads_ list. When the device regains network connectivity, any items in the _Pending Uploads_ list are then transmitted to the server. If the Client attempts to transmit data to the server using JavaScript, that data is likewise added to the _Pending Uploads_ list. It is up to the Client user to realize that if the Client tries to update or add data to the Vantiq database when the Client is in offline mode that the data is not transmitted until the device can successfully transmit it from the _Pending Uploads_ list.

Please also note that other Vantiq mobile app features are degraded or unavailable when the mobile device is offline:

* notifications are not received;
* items in the _Pending Uploads_ list are not transmitted;
* chat messages already received may be viewed but new chat messages are not received nor may be transmitted and new chat topics may not be created;
* accounts in the _Accounts_ list may not be deleted (although the user may switch between accounts in Accounts list); and
* new accounts may not be added nor may the user explicitly log out;
* if a Client invokes a "select" (HTTP GET), it will fail with a special status code 555 ("Network Unavailable");
* if a Client invokes an "insert", "update", "upsert" or "execute" (HTTP POST, PUT and DELETE), the operation is deferred and added to the _Pending Uploads_ list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. The response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain your actual request. (Please note: this feature is not supported in the iOS app.)

The Client object contains a boolean property called "isNetworkActive" which is "true" when a network connection is available.

The Client also has an event called "On Network Status Changed" which will fire whenever the status of the network changes.

## Automatic Document Caching
When a Client containing a DocumentViewer widget is run in the Vantiq Android or iOS mobile app, the app maintains a special document cache for better performance and to minimize network utilization. This cache is known as the "Document Asset Cache". While it is similar to the Offline Mode Cache described in the previous section, it has a different purpose.

A Client's DocumentViewer widget is configured with a *URL* property. That URL may reference an external resource (e.g., https://www.vmware.com/pdf/ws6_manual.pdf) or a document stored in the Vantiq document database. When the Client is run and the user selects the DocumentViewer, the mobile app retrieves and displays the URL contents and also caches those contents locally in the Document Asset Cache. When the user subsequently selects that DocumentViewer, the cached copy of the contents is used rather than accessing the network to retrieve the contents. This caching results in much faster display of Client documents and is especially valuable if the mobile device is used in locations with poor network connectivity. Much like the implicit Offline Cache Mode described in the previous section, this implicit Document Asset caching occurs when a user selects the DocumentViewer for the first time.

The Document Asset Cache may also be filled explicitly by using the Client **Properties** button to display the Client Properties dialog, clicking the _Basic_ tab, then clicking the _Custom Assets_ link to display the Custom Assets dialog. Add URLs to be cached in the _Document Assets_ section. When the Client is started, those URLs are retrieved and cached automatically. When any DocumentViewer widget is selected that references a _Document Assets_ list item, the contents of that URL are immediately available for use.

Note that if the contents of the URL are modified (for example, a PDF document is updated) _after_ the document is cached, the cached copy will not match the updated contents. It is up to the mobile app user to clear the Document Asset Cache so that the updated contents are retrieved. Both the Vantiq Android and iOS apps have a button titled **Clear Document Cache** that allows the user to remove all cached documents so their contents are refreshed the next time the Client is run.

(_Advanced technical note: Why are there two separate caches? This has to do with the way Clients are executed on the Vantiq mobile apps. Most widgets (such as StaticImage) run inside a "WebView" on the mobile app, just as they run in a browser on the desktop. These rely on the "Offline Asset" cache which lives inside the WebView. However some widgets (such as ImageViewers and DocumentViewers) run natively in the mobile app and therefore do not have access to the WebView cache. These require a different cache on the mobile app itself, known as the "Document Asset Cache"._)
