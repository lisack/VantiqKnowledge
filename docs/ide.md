# Vantiq IDE User's Guide
## Overview
The [Vantiq IDE](../../..) is Vantiq's web-based Integrated Development Environment (IDE). The IDE is made up of two web apps, Development and Operations, each of which can have multiple projects. A project allows the developer or operator to organize tasks, such as user management or App and Client building, as well as debugging, deployment and monitoring, in a graphical environment. This User's Guide describes the IDE features available in both the Development and Operations web apps and should be used in conjunction with the [Introductory Tutorial](tutorials/tutorial.md).

The Development web app is accessed using the following URL: [http(s)://(server host)](../../../) (e.g., https://dev.vantiq.com). The Operations web app is accessed using the following URL: [http(s)://(server host)/ui/ops/index.html](../../../ui/ops/index.html). The purpose and use of each web app is described later in this guide.

The Vantiq IDE is supported in current versions of the Chrome, Firefox, Safari, Edge and Opera browsers.

> Vantiq also supports the use of Agentic development tools such as Claude Code to construct Vantiq applications.  See the section on supporting [AI development tools](#via) for more details.

## The Navigation Bar
The Vantiq IDE Navigation bar appears at the top of the browser window:
&nbsp;&nbsp;&nbsp;![NavBar](assets/img/ide/NavBar.png "Navigation Bar")
In the left corner, the contents depend on the whether the user is using the Development or the Operations web app. However, three controls are the same in either app:

* **Project Name** contains the name of the current project. Use this text entry field to name new projects, change the name of the current project, or create a copy of the current project by renaming it.
* **Save** is enabled whenever there are unsaved changes to the current project.
* **Projects** allows the user to create a new project, manage all projects, and quickly switch between existing projects.

In the right corner are eight buttons and menus: **Search**, **Unseen Errors**, **Compilation Errors**, **Catalog Updates**, **Help**, **Namespace**, **User**, and **Project Settings**.
Unseen Errors, Compilation Errors and Catalog Updates only show up when those conditions are found in the Namespace. If none exist, those buttons will be hidden.

#### Search
The **Search** field allows the user to search all resources in a namespace for text matching the contents of those resources. For example, if you want to search all resources having to do with the word _engine_, type _engine_ then return into the **Search** field. This produces a dialog that might look like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Search](assets/img/ide/Search.png "Search Results")

This search found the word _engine_ in one App, two Clients, two Deployments, one Environment and one Event Generator. To add any of these resources to the current project, click the resource entry in the list.

#### Unseen Errors
Clicking the **Unseen Errors** button displays a pane with a list of any errors in the current namespace that have been recorded but are unseen.

#### Compilation Errors
Clicking the **Compilation Errors** button displays a pane with a list of any resources in the current namespace that have compilation errors.

#### Catalog Updates
Clicking the **Catalog Updates** button displays the Catalogs pane. Clicking the **Updates** tab in the pane displays a list of all subscribed Services and installed Assemblies in the Namespace that have updates available.

#### Help
The **Help** menu has four menu items:

* **What's New** displays a pane with the latest Vantiq system release notes.
* **Developer Guides** displays a new browser tab that contains the complete documentation set for the Vantiq system, including Reference Guides, Tutorials and details about the Vantiq REST API.
* **Developer Resources** displays a pane with links to Vantiq mailing lists, references to 3rd party connectors and adapters, and the Vantiq CLI and SDKs.
* **VAIL Documentation** displays a new browser tab that contains the VAIL Rule and Procedure Reference Guide. 

#### Current Namespace
The **Current Namespace** button opens a dialog that allows the currently authenticated Vantiq user to change namespace to any namespace in which they are authorized. 

#### User
The **User** menu shows the username of the currently authenticated Vantiq user. This menu also allows the user to log out, display detailed information about the version of the IDE, and change IDE settings used by the expert user who wants to speed up accomplishing certain tasks.

#### Project Settings
The **Project Settings** menu has the following menu items, which vary depending on which app is in use, Development or Operations.

* **Filter** (Development only) allows the user to select which project elements are displayed in the _Project Resource Graph_ and _Project Contents_ list. For example, by unchecking the **Types** filter item, a sample _Project Resource Graph_ might look like this, which shows that the four types in the project are dimmed in the graph:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![FilterPRG](assets/img/ide/FilterPRG.png "Filter Project Resource Graph")

* **Layout** allows the user to configure how the IDE canvas appears for each project. The Layout Options dialog has several options:

	* **Layout Style** allows the user to select either Custom or Tiled layout. See the [IDE Layout Styles](#ide-layout-styles) section for more details.
	* **Grid Size** selects how many rows and columns to use in Tiled layout. See the [IDE Layout Styles](#ide-layout-styles) section for more details.
	* **Toggle Grid** allows the user to select whether there is a grid pattern in the project canvas. (Only available when using the Custom layout style.)
	
* **Close All Panes** allows the user to close all open panes.
* **Close All Panes in the Current View** allows the user to close all open panes in the current project view (project views are described below).
* **Show All Resources** (Development only) displays a dialog that lists all resources found in the current Namespace and to which Project(s) each belongs.
* **Show Orphan Resources** (Development only) displays a dialog that lists all resources that are not contained in any Project in the current Namespace.
* **Manage Excluded Resources** (Development only) displays resources which have been explicitly removed from the project and placed in an "exclusion list" so they will never be indirectly re-added.

## Panes
Most tasks in the IDE can be accomplished by interacting with panes in the canvas area (the area under the Toolbar). For example, after completing the [Introductory Tutorial](tutorials/tutorial.md) your project might look like this:

&nbsp;&nbsp;&nbsp;![Panes](assets/img/ide/Panes.png "IDE Panes")

This canvas area contains four panes: _Project Resource Graph_, _Service: apps.services.EngineMonitor_, _Event Generator: EngineSimulation_, and _Client: EngineSimulation_. Each of these panes can be resized and their location on the canvas can be changed.

Each pane has a title bar at the upper, right which contains a set of icons. Each icon is a button that performs a specific action for the pane. Some of these icons will appear on every pane, like minimize, maximize, and close, while others are unique to the resource type displayed within the pane. Here are the common icons and their behaviors:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![PaneButtons](assets/img/ide/IconButtons.png "Pane Buttons")

From left to right, the buttons are:

* **Save Changes**: used to save changes made to the contents of the pane.
* **Help**: used to open a new browser tab that contains documentation pertinent to the contents of the pane.
* **Maximize/Normalize Display**: used to expand the contents of the pane to take over the entire browser window and, conversely, restore the pane to its original size. Maximizing a pane makes it easier to view and modify its contents.
* **Pin Pane to Canvas**: when in Tiled Layout mode, this pane will not be moved to the Inactive Panes dock when a pane needs to be replaced.
* **Send to Dock**: when in Tiled Layout mode, move this pane to the Inactive Panes dock.
* **Close**: used to close the pane, removing it from the canvas but not deleting the contents of the pane from the project.
As mentioned, panes may have additional buttons based on their content. Hover the mouse over any button to display a tooltip which contains a title for the button.

## Development App
A project contains a set of resources and related tools which provide an integrated environment for developing Services and Clients. Typical development tasks are:

* create [Types](resourceguide.md#types), [Sources](resourceguide.md#sources) and other Vantiq resources;
* build [Services](services.md) and [Clients](cbuser.md); and
* run, test and debug your [Applications](apps.md).

In the Development App, the IDE Navigation Bar contains five menus other than the three common controls: **Administer**, **Test**, **Deploy**, **Show**, and **Add**. Several of these menu controls have a sub-menu section titled **Advanced**. Menu items contained in the **Advanced** section are not commonly used and can safely be ignored by beginning users.

#### Administer
The **Administer** menu has 10 menu items:

* **Users** displays a list of the currently defined users for the namespace. To add a new user to the namespace, use the **Create New** icon button in the toolbar of the _Users_ pane.
* **Namespaces** displays a list of the currently defined [namespaces](resourceguide.md#namespaces) defined for a Vantiq organization. This list is only useful when authenticated as an organization administrator.
* **Audits** displays a list of the current [Vantiq Audits](resourceguide.md#audits).
* **Grafana** launches the Grafana UI enabling in-depth analysis of resource utilization and performance. (This menu item is only available for servers that have Grafana enabled (e.g. not on Edge servers).)
* **Advanced>Catalog** allows the user to host and manage a catalog. The Vantiq catalog system is described in the [Vantiq Catalog Reference Guide](broker.md).
* **Advanced>Profiles** displays a list of the currently defined Vantiq [profiles](resourceguide.md#profiles). A profile contains capabilities with which the user assigned the profile can access data and behaviors defined in the namespace.
* **Advanced>Access Tokens** displays a list of Vantiq [access tokens](resourceguide.md#tokens) used for authentication.
* **Advanced>Pending Invites** displays a list of outstanding invitations to the namespace.
* **Advanced>Secrets** displays a list of currently defined [secrets](resourceguide.md#secrets).
* **Advanced>Groups** displays a list of the currently defined groups for the current Vantiq namespace. From the [Groups documentation](resourceguide.md#groups), a group is a set of users with shared access to a collection of resources.


#### Test
The **Test** menu has 11 menu items:

* **Tests** displays a pane that lists any currently defined tests defined in the current namespace. The Vantiq test system is described in the [Vantiq Testing Reference Guide](tests.md).
* **Test Suites** displays a pane that lists any currently defined tests defined in the current namespace. The Vantiq test system is described in the [Vantiq Testing Reference Guide](tests.md).
* **Event Generators** is used to add [Event Generators](eventgenerators.md) to the current project.
* **Captures** displays a pane that lists currently defined [event captures](capture.md).
* **Autopsies** displays a pane that allows the user to retrieve Vantiq Rule and Procedure execution [autopsy records](tutorials/debugtutorial.md).
* **Errors** displays a pane that allows the user to retrieve historical Vantiq system errors.
* **Logs** displays a pane that allows the user to retrieve historical log messages.
* **Advanced>Collaborations** displays a pane that allows the user to retrieve lists of [collaborations](servicestatemgmt.md#collaborations), both active and closed. These lists can be used to determine the status of collaborations as well as deleting collaborations.
* **Advanced>Activity Patterns** displays a list of [App Activity Patterns](apps.md#activity-patterns) and [Collaboration Activity Patterns](apps.md#collaboration-management).
* **Advanced>Situations** displays a pane that allows the user to retrieve lists of situations.
* **Advanced>Debug Configurations** displays a list of [Debug Configurations](resourceguide.md#debug-configs).

#### Deploy
The **Deploy** menu has seven menu items:

* **Configurations** displays a list of [Deployment Configurations](config.md#configuration-and-deployment).
* **Network Graphs** displays a list of [Network Graphs](config.md#configuration-and-deployment). When creating a new Network Graph, the IDE does a network search for other Vantiq systems configured as connected to the current system.
* **Nodes** displays a list of other Vantiq systems about which the current system knows. Users can connect to other nodes by using the **Create New** icon button in the top, right of the _Nodes_ pane.
* **Node Configurations** displays a list of Vantiq [Node Configurations](config.md#node-configurations) used for bootstrapping a new Vantiq node.
* **Deployments** displays a list of Vantiq [Deployments](deploymentuser.md). Users can simplify deployment tasks with this graphical tool.
* **Environments** displays a list of Vantiq [Environments](deploymentuser.md#environment). An Environment contains a set of user selected Nodes. It is used by [Deployments](deploymentuser.md).
* **Clusters** displays a list of Vantiq [Clusters](extlifecycle.md). A Cluster is a managed environment such as [Kubernetes](extlifecycle.md#kubernetes-ref).

#### Show
The **Show** menu has seven menu items:

* **Find Records...** displays a pane that allows the user to retrieve a list of instances of a Vantiq [Type](resourceguide.md#types). Once the list has been retrieved, those instances can be edited or deleted.
* **Add Record...** displays a pane that allows the user to add a new instance of a Vantiq Type.
* **Catalogs** displays a list of any catalogs to which the current namespace is connected and allows the user to create new and delete existing catalog connections. The Vantiq catalog system is described in the [Vantiq Catalog Reference Guide](broker.md).
* **Compilation Errors** causes the _Compilation Errors_ pane to display, which contains all VAIL compilation errors in resources found in the Namespace.
* **Resource Graph** causes the _Project Resource Graph_ pane to display. The _Project Resource Graph_ is a graph that shows the relationship between all Vantiq resources that are present in the project. For example, if a Procedure references a Type, then the graph displays an edge linking the Procedure node to the Type node. Resources are added to a project by use of the **Add** menu, which is discussed in the next section.
* **Advanced>Documents** displays a list of documents stored for the current Vantiq namespace. Documents are typically uploaded from the Vantiq mobile apps or the Vantiq IDE.
* **Advanced>Quick Start** displays a Quick Start pane, which provides links and how to accomplish common Development web app tasks.

#### Add
The **Add** menu is used to add Vantiq resources to the current project. Each menu item references a resource. For example, selecting the **Service** item displays the following dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddService](assets/img/ide/AddService.png "Add Service")

Use this dialog to either add an existing resource (selecting it from the list) or creating a new resource (using the **New** button). Once the resource is either added or created, it is added to the _Project Resource Graph_ pane (if displayed) and the _Project Contents_ pane (if displayed).

## Operations App
An Operations project provides a set of tools for administering and monitoring a Vantiq namespace. Typical Operations app tasks are:

* create and edit current namespace [users](resourceguide.md#users),
* monitor the operation of tasks (e.g., Apps) by running Vantiq [Clients](cbuser.md),
* monitor errors and log messages produced by the namespace.

In the Operations App, the IDE Navigation Bar contains three menus other than the three common controls: **Administer**, **Deploy**, and **Monitor**. Several of these menus have a sub-menu section titled **Advanced**. Menu items contained in the **Advanced** section are not commonly used and can safely be ignored by beginning users.

#### Administer
The **Administer** menu has 10 menu items, which are discussed in the [Development App Administer Menu](ide.md#administer).

#### Deploy
The **Deploy** menu has seven menu items, which are discussed in the [Development App Deploy Menu](ide.md#deploy).

#### Monitor
The **Monitor** menu has five menu items:

* **Clients** displays a list of the currently defined [Clients](cbuser.md) which is used to launch and run Vantiq Clients. Clients allow the graphical input into and display of data from the Vantiq system. For example, here is the Client associated with the [Introductory Tutorial](tutorials/tutorial.md):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningClient](assets/img/intro/RunningClient.png "Running Client")
 
* **Errors** as described in the [Development App Debug menu](ide.md#debug).
* **Logs** as described in the [Development App Debug menu](ide.md#debug).
* **Advanced>Collaborations** as described in the [Development App Show menu](ide.md#show).
* **Advanced>Situations** as described in the [Development App Show menu](ide.md#show).



## Project Views

A Development project can be thought of as a container for resources and a set of tools that operate on them. The set of resources can grow quite large and it may be useful to divide the project up into smaller related subsets. This is done with a feature called "Views" which allows you to identify a related set of the Project's resources and group them together.

You don't have to use Views - you can ignore them and simply use the single "_Project Contents_" view which contains everything in one place. But Views can often be a way to organize the components of a big Project. Here are some basic facts about Views which help to understand how they work and what they are good for:

* There is always a default View called "**_Project Contents_**" which contains all the resources in the project.

* User-created "Custom" Views contain a subset of all the resources in the Project Contents View. A Resource can be in more than one View, but all Resources are always in the Project Contents View. If you save a Project with Custom Views, it will still be readable by older versions of Modelo but the Custom Views will be ignored.

* Custom Views show a subset of all Project resources in the Project Contents Dock and the Project Contents Graph. The Contents Dock can be displayed in four flavors: _tree_, _list_, _input_, and _output_. Each View saves its own layout within the Project Resource Graph. Each View can have its own layout style of "_Tiled_" or "_Custom_". Each View has its own set of panes open.

* The same pane can be open in multiple Views at the same time. In fact, there is only one copy of a specific running pane and all Views share it. This means the same pane will always have the same state no matter which View it appears in. This also means that closing a pane in one View doesn't really close it unless no other Views have it open.

* There is a gear/settings icon in the Contents Dock. When clicked, it allows you to pop up a "**_Manage Views_**" dialog that is used to create, delete and rename Custom Views. It also has a "**_New View_**" menu item to simply add a new one.

* When there is at least one Custom View, vertical tabs appear at the left edge of the Contents Dock and you can use them to easily switch between Views.

* In the IDE Toolbar Settings menu there is a "Close All Panes" menu item which closes **all** panes in **all** Views. There is also a menu item to just "Close all Panes in the current View".

* Removing a Resource from a Custom View doesn't remove it from the Project Contents View. However, removing a resource from the Project Contents View removes it from all Custom Views as well (and the Project). Adding a Resource to a Custom View adds it to the Project Contents View automatically (if it's not already there).

* The Contents Dock provides many context menus to operate on the resources there, as well as actions to copy Resources from the Project Contents View into a Custom View. In fact, you can select multiple resources in the Project Contents View and use a context menu to copy all of them to a Custom View at the same time.

* A context menu item in Custom Views allows you to add one level of **_folders_** and then move resources there via drag and drop. (The Project Contents View does not support folders.)


To get started using Views, click the Contents Dock's gear/settings icon and select **New View**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Tiled](assets/img/ide/NewView.png "New View menu item")

This displays a dialog that lets you give your View a name and, optionally, add an initial set of resources. When you click **OK**, the new View's tab appears in the Contents Dock and the new View will become the currently active one.



## IDE Layout Styles
In both the Development and Operations apps, each project may be configured to display the canvas panes in one of two styles: _Custom_ or _Tiled_. To choose a project's layout style, use the **Project Settings** menu to select **Layout...**.

Note that each [View](#project-views) can have its own Layout Style.

#### Flex Grid Layout Style
_Flex Grid Layout Style_ allows the user to split the canvas into multiple panes of various sizes.The user may split the canvas horizontally or vertically, and then split the resulting panes again. The resulting panes will always be rectangular and will fill the canvas. The user may resize Flex Grid groups by dragging and dropping the lines between groups. The user may also move panes between split groups by dragging and dropping, or by right-clicking and selecting the _Move into different pane_ menu item. Flex Grid Layout Style is the default layout style. The project below is shown using Flex Grid Layout Style:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![FlexGrid](assets/img/ide/Flexgrid.png "Flex Grid Layout Style")

#### Custom Layout Style
_Custom Layout Style_ allows the user to move and resize panes in the IDE canvas. The user may display a large number of panes in the canvas and then use the scroll bars to view panes outside the currently viewable canvas.

#### Tiled Layout Style
_Tiled Layout Style_ allows the user to display a fixed number of panes using a grid pattern sized to exactly fit in the viewable canvas. If the browser window is resized, the pane sizes will adjust to match the new size. The project below is shown using Tiled Layout Style with a 2x2 grid:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Tiled](assets/img/ide/Tiled.png "Tiled Layout Style")

If the user opens a new pane and the canvas grid is full, the canvas pane that was opened least recently is moved into the _Inactive Panes Dock_ at the top of the canvas. In the example above, there are three inactive panes: _/my/response/topic_ and two _SystemHUD_ entries. (The first _SystemHUD_ entry represents the SystemHUD type and the second _SystemHUD_ entry represents a subscription.) Each inactive pane associated with a Vantiq resource (e.g., type, topic, App, Client, etc.) has the same color coding as found in the _Project Resource Graph_. All other inactive panes have a default gray color.

To restore an inactive pane to the canvas, simply click on its entry in the Inactive Panes Dock. The inactive pane replaces the least-recently-used pane in the canvas. That least-recently-used pane is then added to the Inactive Panes Dock.

The Inactive Panes Dock is sorted using the sort menu in the dock. Inactive panes are sorted using one of four methods: _Category_, _Recently Used_, _Alphabetical_, or _Created Time_. If _Category_ is selected, the dock entries are sorted using one of seven general categories of panes (e.g., resource type, list, data), each represented by the icon in the dock entry.

Hovering the mouse over a Inactive Panes Dock entry will cause either one or two controls to display:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Hover](assets/img/ide/Hover.png "Hover over Hiden Pane")

* **Close** is represented by a small X icon. Use the **Close** icon to remove the entry from the Inactive Panes Dock.

* **Save** is represented by a small disk icon. Use the **Save** icon to save the resource, if that resource has unsaved changes.

When using Tiled Layout Style, panes in the canvas may have two additional icons in the toolbar at the upper, right of the pane:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DockIcons](assets/img/ide/DockIcons.png "Dock Icons")

* **Send to Dock** is used to move the visible pane to the Inactive Panes Dock. This will cause the canvas to have an open entry, which is filled by the next pane to be opened in the canvas.

* **Pin Pane to Canvas** is used to pin the visible pane to the canvas so that it may not be replaced by a newer pane. Use **Pin Pane to Canvas** to ensure that one or more panes are always visible in the canvas. After pinning, the **Pin Pane to Canvas** icon is replaced by the **Unpin Pane from Canvas** icon to reverse the pinning state.

The Inactive Panes Dock may be docked either to the top or the right of the IDE. Use the **Move Dock to Right** or **Move Dock to Top** buttons to switch the location of the dock.

## IDE Docks
In addition to the Inactive Panes Dock described above, there are two additional IDE Docks: _Project Contents_ and _Debug_.

#### Project Contents Dock
The Project Contents Dock is docked to the left of the IDE. It contains a list of all resources in the Project and is sorted using the **Change Resources View** button at the top of the dock. There are four sort methods: _Tree of Resources by Type_, _Tree of Resources with related Inputs_, _Tree of Resources with related Outputs_, and _List of Resources by Name_. The middle two sort methods display an additional tree level for resources to display how other resources relate to that resource. For example, if a publish to Topic "/patientChange" triggers Rule "ProcessChange", then the resource tree will show that relationship.

Use the **Collapse Dock Left** button to collapse the Project Contents Dock to save space in the IDE. Use the **Expand Dock Right** button to restore the Project Contents Dock to its full width. In expanded state, the horizontal size of the dock is changed by clicking and dragging on the gray dividing line at the far right of the dock.

If you have defined custom Views then a vertical set of tabs will appear on the left edge which allow easy navigation between Views.

#### Debug Dock
The Debug Dock is present for both Development and Operations Projects and is docked on the bottom of the IDE. It contains up to three debug panes:

* **Errors** lists any Vantiq system errors as they occur.
* **Log Messages** lists any log messages as they occur. Log messages are produced by [turning on debugging](tutorials/tutorial.md#5-testing-tasks) for Applications or Collaboration Types or by adding [explicit log calls](rules.md#logging) in Rules and Procedures.
* **Autopsies** lists any Autopsy records as they are created. Read more about Autopsy records in the [Autopsy Debugger Tutorial](tutorials/debugtutorial.md).

Select which of these three debug panes is visible by using the pull-down menu in the title bar of the dock.

Use the **Collapse Dock Down** button to collapse the Debug Dock to save space in the IDE. Use the **Expand Dock Up** button to restore the Debug Dock to its full height. In expanded state, the vertical size of the dock is changed by clicking and dragging on the gray dividing line at the top of the dock.

## Deleting Projects and Resources

Projects can be deleted from the **Projects > Manage Projects...** dialog by selecting one or more projects in the list and clicking **Delete Selected**, or by right-clicking a single project and choosing **Delete**. This will present a confirmation dialog with two choices:

* **Delete Project(s)**— removes only the project entries themselves. The resources inside those projects are left in the namespace and remain available to any other project that references them.
* **Delete Project(s) and Resources** — removes the selected projects *and* the resources they contain.

When you choose **Delete Project and Resources**, the IDE will only delete a resource if every project that currently references it is also being deleted in the same operation. In other words, a resource is preserved when at least one project that is *not* part of the current deletion still uses it. This protects shared resources from being unintentionally removed when a project that happens to reference them is deleted.

For example, if Project A and Project B both reference a Type `Sensor`:

* Deleting only Project A with **Delete Project and Resources** will leave `Sensor` in place because Project B still uses it.
* Selecting both Project A and Project B and choosing **Delete Projects and Resources** will remove `Sensor`, because no remaining project references it.

<a name="via"></a>
## Supporting AI Development Tools

The Vantiq Intelligent Assistant (VIA) is an MCP server which provides the resources and tools necessary for AI development tools to understand the Vantiq platform and construct Vantiq applications. We will use [Claude Code](https://claude.com/product/claude-code) as the exemplar, but the use of the [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) standard means that it should be possible to use other similar tools as well.

To connect to the VIA MCP server you will need to know 2 things, the MCP server URI and the value of an [access token](resourceguide.md#tokens). The MCP server URI is of the form `<vantiqBaseURI>/mcp/io.vantiq.via.mcpServer`.  The base URI will vary depending on the target Vantiq server. For the Vantiq Developer Cloud this is [https://dev.vantiq.com](https://dev.vantiq.com) and the MCP URI is `https://dev.vantiq.com/mcp/io.vantiq.via.mcpServer`. The access token should be a personal token associated with the current developer. It can be a single or multi-namespace token. To create the token you can either:

* Use the [New Project Wizard](tutorials/quickstart.md#newProjectWiz) to create an "AI Development" project. This will automatically create a VIA access token if one does not already exist.
* Use the [setupToken](cli.md#setup-token) command in the Vantiq CLI to create an appropriate token.
* Manually create a token using the [Administer...Advanced..Access Token](#administer) menu.

Once you have both the MCP server URI and the access token you can configure your AI development tool to connect to the server. Each tool supports a number of different approaches, but they mostly end up creating a JSON entry the looks like this:

```json
"via": {
  "type": "http",
  "url": "https://dev.vantiq.com/mcp/io.vantiq.via.mcpServer",
  "headers": {
    "Authorization": "Bearer <accessToken>"
  }
}
```

Once connected, Claude Code will use the VIA MCP server whenever it is tasked with creating a Vantiq application. It will also answer questions about how Vantiq applications work, how to address specific requirements, and assist in testing the application during construction. The [Quickstart Tutorial](tutorials/quickstart.md) is a good place for new users to start.

## Integration with Version Control Systems

Modelo allows you to "export" a Project and its contents into a zip file. Once this zip has been expanded into a directory tree it can be checked into a Version Control System (VCS) such as Git or TFS. 

We refer to this as the "VCS directory". (In "Git" terms, this means the VCS directory corresponds to a Git repository.) Normally there is one VCS directory that corresponds to a single namespace, and every Project in the namespace has its own subdirectory:

```
MyVCSDirectory/
   MyProject1/
      clients/
      types/
      ...
   MyProject2/
      clients/
      types/
      ...
   MyProject3/
      clients/
      types/
      ...
```

Using Modelo "export" you could sync a Project with this VCS directory in several steps:

1. Export the Project into a zip file (this requires using a dialog to select the target location)
2. Expand the zip file into a temporary directory (from outside Modelo)
3. Delete the contents of the Project's subdirectory 
4. Copy the contents of the temporary directory into the Project's subdirectory inside the VCS directory
 
This will work but requires some awkward manual steps. Modelo offers some mechanisms to make it much more convenient to sync your Project with its corresponding VCS directory. These operations are found in the **Projects** menu:

* **Sync Project to VCS** - export the current Project and overwrite its sub-directory inside the VCS directory
* **Sync Project from VCS** - import the current Project from its sub-directory inside the VCS directory, completely overwriting the current contents
* **Combine Project from VCS** - combine the contents in the selected Project with the current Project. Note that duplicate resources in the current Project will be overwritten.

Unfortunately browsers do not allow some of the filesystem operations needed to make this work. The Vantiq CLI command can be run in a special mode where it starts a small local server which Modelo can use to do these export and unzip steps for you without so much manual intervention. These operations all require the Vantiq CLI command to be running in its special mode; simply invoke it like this:

```
vantiq VCSSERVER
```

or this if you are running in Windows:

```
vantiq.bat VCSSERVER
```

This causes the Vantiq CLI to start a local server on localhost:4347 and then listen for requests from Modelo in the browser. (This port should **not** be exposed to the outside world since it would present a potential security exposure.) You can just leave the CLI running in this state until it's needed.

For example, if you select **Sync Project to VCS**, you will see a dialog like this:

&nbsp;&nbsp;&nbsp;&nbsp;![Sync To VCS](assets/img/ide/SyncToVCS.png "Sync To VCS")


You will need to enter the VCS directory name the first time you invoke one of these operations; after that it will remember your setting. Clicking the **Sync Project to Directory** button will then complete the sync operation for you.

Note that you will need to do all the actual VCS operations (such as "commit", "push", "pull", etc.) from outside Modelo.

Instructions for downloading and installing the Vantiq CLI can be found [here](cli.md#installation).


## IDE Shortcut Keys
Many IDE panes support common keyboard shortcuts which enhance developer productivity. A pane must be selected for keyboard short cuts to apply; a pane is selected when its title bar has a dark gray background and a blue border.

What follows is a list of keyboard shortcuts and the panes to which they apply. On Windows, the shortcut modifier is the Control (_Ctrl_) key; on Mac OS, the shortcut modifier is the Command (_Cmd_ or Apple) key although the Control key is also respected.

* _Ctrl-S_ & _Cmd-S_: save any changes in the pane
* _Shift-Ctrl-E_ & _Shift-Cmd-E_: display the [IDE search](ide.md#search) dialog

The following are used if the IDE Layout Style is set to the _Flex Grid_ layout:

* _Ctrl-]_: Switch focus to the next pane in the current split
* _Ctrl-[_: Switch focus to the previous pane in the current split
* _Ctrl-Shift-]_: Switch focus to the next split
* _Ctrl-Shift-[_: Switch focus to the previous split

See the [IDE Layout Styles](#ide-layout-styles) section for more details.

The following are used in the Client Builder, System Modeler, App Builder, and Collaboration Type Builder:

* _Ctrl-Z_ & _Cmd-Z_: undo changes
* _Shift-Ctrl-Z_ & _Shift-Cmd-Z_: redo changes
* _Delete_ & _Backspace_: delete selected object(s) in the pane

The following are used in the Client Builder and System Modeler and apply only to selected object(s) in the pane:

* _Ctrl-X_ & _Cmd-X_: cut
* _Ctrl-C_ & _Cmd-C_: copy
* _Ctrl-V_ & _Cmd-V_: paste

The following are used in the Client Builder and apply only to selected object(s) in the pane:

* _Right-arrow_: move object to the right
* _Left-arrow_: move object to the left

The following are used in the Rule/Procedure (VAIL) editor pane:

* _Ctrl-Click_ & _Cmd-Click_: on certain words in the editor will make the editor do the following:
    * If the word is a built-in Procedure or VAIL term the appropriate documentation will be opened in a new browser tab.
    * If the word is an existing Procedure, Source or Type in your namespace the resource will be opened in a new pane.
    * If the word is a Procedure, Source or Type that does not exist then a resource creation pane will be opened using the indicated name.
* _Shift-Ctrl-Space_ & _Shift-Cmd-Space_: display a menu of variables in scope
* _Shift-Ctrl-._ & _Shift-Cmd-._: Display available packages
* _Ctrl-Enter_ & _Cmd-Enter_: Import the selected resource
    
The following are used in any code (VAIL or JavaScript) editor pane:

* _Ctrl-/_ & _Cmd-/_: toggle comments on and off for the current line
* _Ctrl-A_ & _Cmd-A_: select all text
* _Ctrl-D_ & _Cmd-D_: delete the line under the cursor
* _Ctrl-Home_ & _Cmd-Up_: move cursor to the start of the document
* _Ctrl-End_ & _Cmd-Down_: move cursor to the end of the document
* _Ctrl-PageUp_ & _Shift-Ctrl-V_: move cursor up one screen
* _Ctrl-PageDown_ & _Ctrl-V_: move cursor down one screen
* _Ctrl-]_ & _Cmd-]_: indent current line or selection
* _Ctrl-[_ & _Cmd-[_: unindent/dedent current line or selection
* _Ctrl-F_ & _Cmd-F_: find text
* _Ctrl-G_ & _Cmd-G_: find next instance of text
* _Shift-Ctrl-G_ & _Shift-Cmd-G_: find previous instance of text
* _Shift-Ctrl-F_ & _Cmd-Option-F_: replace instance of text
* _Shift-Ctrl-R_ & _Shift-Cmd-Option-F_: replace all instances of text

The following is used in the Client Builder JavaScript editor pane:

* _Ctrl-Enter_ & _Cmd-Enter_: invoke the _AI Code Assistant_ after entering a single-line comment of the code you require. The Assistant will attempt to use Generative AI features to provide a code sample.

In addition, the _Return_ key can be used as a shortcut for the default (usually **OK**) button in most modal dialogs.

## Safe Mode

It is possible that some unusual conditions can prevent Modelo from starting up successfully. There are two scenarios that could lead to this condition:

* The last-saved Project could have been damaged in such a way that opening it causes Modelo to crash. Since by default Modelo always tries to re-open the last active Project on startup, this could prevent you from starting Modelo at all.

* If you are using custom CSS assets in a Client, it is possible that you could override Modelo's builtin CSS to such an extent that Modelo can no longer function. This would normally happen only when trying to test run the Client, but if you turned on the Client's "Apply Custom CSS Assets" option then your CSS would be loaded even when simply opening the Client to edit it.

Either of these unusual conditions could lead to Modelo either crashing on startup or being unusable. It is possible to start Modelo in "Safe Mode" so it will avoid these issues by not automatically opening the last Project and by forcing the "Apply Custom CSS Assets" option off when editing Clients.

Instead of the usual URL you use to launch Modelo, you can add '_safemode=true_' as a parameter. For example  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [https://dev.vantiq.com/ui/ide/index.html?safemode=true](https://dev.vantiq.com/ui/ide/index.html?safemode=true)


When starting Modelo in this way you will see a warning dialog that explains the changed behavior, something like this:

---
Running in "Safe Mode" - some features will be disabled:

* The last Project will not automatically be reloaded on startup.
* The 'Apply Custom CSS Assets' option will be automatically turned off when editing Clients.
---