# System Modeler Tutorial

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ModelPhase2](../assets/img/systemmod/128_SMTut_SM.png "Model Phase 2")

## Purpose

To introduce application developers to the low-code, no-code system modeling capabilities in Vantiq.

## Objectives

After completing this tutorial, developers will be able to:

* Create a System Model, either individually or as part of a group
* Ensure a System Model captures the requirements of a business process
* Generate a Design Model based on system modeling

## Tutorial Overview
This tutorial shows the user how to create an example System Modeler model using the [Vantiq IDE](../../../..). System Modeler uses [Event Storming](https://www.eventstorming.com/) as an inspiration for documenting (modeling) the events that represent business processes, then allowing automatic generation of Vantiq Design Model to further develop a working Vantiq system.

The tutorial lessons show the developer how to conduct a System Modeler modeling session that creates a city's pothole reporting and tracking system. The model will represent:

* a mobile app that allows city residents to report a pothole
* creation of new database records to document reported potholes
* notification of city services of new pothole reports
* allow workers to update the status of a pothole
* notification to the reporting resident when the status has changed

All lessons assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the lessons in the [Introductory Tutorial](tutorial.md) before starting the lessons in this tutorial.

>Note: if needed, you can import a finished version of this project and the generated project using the **Projects** button to select **Import**.  Select _Tutorials_ for Import Type, then select _System Modeler_ from the second drop-down, then click **Import**.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Creating a System Modeler Project
The first task in building our pothole reporting and tracking system is to create a project in the Vantiq IDE to begin the modeling session.

Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Requirements Model** as the Project type, and title the Project "Pothole":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![PotholeProject](../assets/img/intro/EMProject.png "Create Pothole Project")

If you choose _Requirements Model_ as the Project Type, with the _User Driven_ option, Vantiq will create a System Model workspace and place the first Command action in the project for you.

The next several lessons take place inside this Project.

## 2. Creating a System Model
Now that you've created the _Pothole_ Project from the New Project Wizard, a System Model named "Pothole" is created:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateAppModel](../assets/img/systemmod/CreateAppModel.png "Create System Model")

As outlined in [Event Storming](https://www.eventstorming.com/), a System Modeler session involves the use of five virtual sticky notes (notes) to represent:

* **Event**: something that happens in the business
* **Reaction**: responses to events
* **Command**: user-driven actions that produce events
* **External System**: systems that are external to the business 
* **Issue**: document potential problems or unknowns about events

and one container:

* **Story**: contain notes that share a common vocabulary (this is known as a Bounded Context in Event Storming)

System Modeler modeling sessions are collaborative in nature. It is anticipated that a Vantiq developer will create a new namespace, create a new System Model in that namespace, then invite other developers to share the modeling session within that namespace. (Please refer to the [User and Namespace Administration Tutorial](admin.md) for details on management of namespaces and users.) When multiple developers open the same System Model, changes made by any one developer will be reflected in all other developer sessions. In this case, the upper-right of System Modeler will contain a users icon with a red badge that contains the number of current editors. Click on the users icon to display a list of the current editors:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![MultiEditors](../assets/img/systemmod/MultiEditors.png "Multiple System Model Editors")

Drag and drop notes from the notes palette to the System Modeler canvas. To change the label within the note, double click the note.

## 3. Conducting a System Modeler Session
The developers creating a System Model are the business process experts who understand the events and related systems of the business at a high level. To develop a System Model, you will simply be dragging, dropping, and connecting notes within the System Modeler canvas to represent the pothole reporting and tracking system.

* To represent the mobile app that allows citizens to report potholes, a _Command_ note named _Pothole_ has already been added to the model. Double-click on that note and change its label to "PotholeReporter".

* To represent the pothole report event, drag and drop an _Event_ note, double-click on that note and change its label to "Report Received". To link the _PotholeReporter_ note to the _Report Received_ note, single click on the _PotholeReporter_ note, then click the small, green circle, dragging to the _Report Received_ note, then releasing the mouse, as shown below:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![LinkNotes](../assets/img/systemmod/LinkNotes.png "Linking Notes")

* To represent the creation of database records to document reported potholes, drag and drop a _Reaction_ note, double-click on that note and change its label to "Store Report". Link the _Report Received_ note to the _Store Report_ note.

* To represent the notification of city services of new pothole reports, drag and drop two notes: an _Event Note_ with label "Fix Order Issued" and a _Reaction_ note with label "Notify Team". Link the _Store Report_ note to the _Fix Order Issued_ note, then link the _Fix Order Issued_ note to the _Notify Team_ note. 

* To represent the ability for workers to update the status of the pothole, drag and drop a _Reaction_ note, double-click on that note and change its label to "Update Status". Link the _Notify Team_ note to the _Update Status_ note.

The System Model should now look something like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ModelPhase1](../assets/img/systemmod/ModelPhase1.png "Model Phase 1")

* To represent the notification of the reporting resident when the status has changed, drag and drop two notes: an _Event_ note with label "Status Updated" and a _Reaction_ note with label "Notify Reporter". Link the _Status Updated_ note to the _Notify Reporter_ note. These notes are unconnected to the previously created six notes.

The System Model should now look something like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ModelPhase2](../assets/img/systemmod/128_SMTut_SM.png "Model Phase 2")

Now that the business process experts have modeled their events and related systems, the model is complete. Use the **Save Changes** icon button (at the top, right of the _System Model: Pothole_ pane) to save the System Model.

## 4. Generating a Design Model
Once the system model is complete, the System Modeler can generate a [Design Model](tutorial.md#2-understanding-the-design-model) that implements the model. To generate a Design Model, use the **Generate Design Model** button in the System Modeler toolbar. This will cause the _New Design Model_ dialog to be displayed:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![NewDesignModel](../assets/img/systemmod/NewDesignModel.png "New Design Model")

Use the **Create** button to generate a new Design Model:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DesignModel](../assets/img/systemmod/DesignModel.png "Design Model")

Notice the Requirements List at bottom left of the Design Model. This is the list of all of the system model notes from this tutorial. As the Design Model is developed, check off each of the Requirements List items as they are developed in the Design Model. You can drag and drop list items to change the order of list items.

Use the Design Model to build a working pothole reporting system by adding new Clients and Services as defined by the requirements from the system model. Here's an example of what a completed Design Model might look like for the pothole reporting system:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Full DesignModel](../assets/img/systemmod/FullDesignModel.png "Complete Design Model")

The [Introductory Tutorial](tutorial.md) provides a good example of developing a working Vantiq system.

If the System Model contains one or more Stories, each containing at least one note, the **Generate** button will only be enabled when a Story is selected in the canvas. The generated Design Model will only contain those notes that are present in the selected Story.

## Conclusion

The powerful Vantiq Event Storming tools in the System Modeler allow the documentation of existing business processes and provide a starting point for developing Vantiq systems when used with the [Design Modeler](tutorial.md#2-understanding-the-design-model).
