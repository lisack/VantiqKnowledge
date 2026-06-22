# Floor Plan Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningVis](../assets/img/imagemap/RunningClient.png "Running Client")
## Objective

To gain familiarity with the Client Builder and GeoJSON objects to build real-world location-tracking applications

## Purpose

* Create a Client with a Floorplan widget
* Define the dimensions of the area to be tracked
* Use geoJSON datatypes to deliver relevant location information, which will be shown graphically in the Client 

## Tutorial Overview
This tutorial guides a developer through creating a floor plan Client in the Vantiq system. It uses simulated data to display residents moving in a two-story building. The lessons include definition of a resident data type, generation of simulated motion data, and the definition of a floor plan client to display the data.

All sections assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the [Introductory Tutorial](tutorial.md) before starting this tutorial.

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item.  Just select _Tutorials_ for Import Type, then select _Floor Plan_ from the second drop-down, then click **Import**.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Creating a Floor Plan Project
The first task in learning about the Vantiq floor plan widget is to create a project in the Vantiq IDE to assemble all the client components.

Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project "FloorPlan":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![IMProject](../assets/img/intro/EMProject.png "Create Floor Plan Project")

The rest of this tutorial will take place inside this Project.

## 2: Creating a Data Type
The simulation data for this example needs to be stored in the Vantiq database so that it can be used to drive the floor plan client widget. You must create a data type to specify the data associated with each simulated building resident.

Use the **Add** button to select **Type...**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![B](../assets/img/intro/128_IntroTut_BlackTypeScreen.png "Add Resident Type")

Use the **New Type** button to create the Resident type. Give it the standard type.

The _Resident_ type contains three properties:

* floor: a String which identifies the floor on which the resident is standing
* location: a GeoJSON object which identifies the X and Y coordinates of the resident on the given floor
* name: a String which is the unique identifier of the resident


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateResident](../assets/img/imagemap/CreateResident.png "Create Resident Type")


While the _location_ property is defined as GeoJSON, the values of the property are not latitude and longitude values for floor plan purposes. Specifically, the coordinates property of the GeoJSON object will contain the X and Y coordinate offsets from the upper-left corner of the floor plan image you'll define in the next section. The longitude coordinate property is the X offset coordinate and the latitude coordinate is the Y offset coordinate.

Once these three user properties are defined, use the **Save** button to save the _Resident_ type and add it to the Project.

## 3: Simulating Resident Data
Now that you've created the resident data type, use the IDE to simulate residents changing location in a two-floor building. We will use the Event Generator tool to simulate resident data streams.

Use the **Test** button to select **Event Generators** and click **New Event Generator**. Name the Event Generator 
*ResidentGenerator*.

![DataGenTab](../assets/img/imagemap/CreateResidentGenerator.png "New Event Generators")

Click the *New* button in the Event Generator pane to add a new Event Descriptor. Select **Types** as the resource,
**Resident** as the resourceId, and **INSERT** as the operation. Set the *Repeat For* type to **Iterations** and set the value to **20**.
Set the *Interval* to **1 second**. This means that the Event Descriptor will generate 20 inserts on the *Resident* type at 
a rate of one per second.

![FirstEvtDesc](../assets/img/imagemap/ResidentEventDescriptor.png "Event descriptor")

Click on the *Properties* dropdown to configure the instance data.

![FirstEvtDesc](../assets/img/imagemap/EventDescriptorWithProps.png "Event descriptor")

Set the *floor* property variation type to *Set* and click the *Random* checkbox. Click *Edit Set of Strings* next to the 
*floor* property. Configure the list to contain two values: *one* and *two*. This is the set of possible floor
values. At runtime a value will be randomly selected from the set.
 
![FirstEvtDesc](../assets/img/imagemap/RandomFloorValues.png "Floor values")

Set the variation type for the *location* property to *Range* and check *Random*. Click *Origin* to set the Origin GeoJSON value.
Set the Location Type to *Point* and set the latitude and longitude to *5*.

![FirstEvtDesc](../assets/img/imagemap/ConfigureGeoJSONOrigin.png "Origin geojson values")

Click *Destination* to set the Destination GeoJSON value. Set the Location Type to *Point* and set the longitude to *25* and longitude to *20*.

![FirstEvtDesc](../assets/img/imagemap/ConfigureGeoJSONDest.png "Destination geojson values")

By setting the origin and destination values, you are having your user show up in a random location well within the confines of the floor plan. The X and Y coordinates of the GeoJSON object are the X and Y offsets from the upper-left corner of the floor plan image.

Set the *name* property variation type to *Set*. Click *Edit Set of Strings* next to the 
*name* property. Configure the list to contain three values: *alice*, *bob*, and *carol*. This is the set of names. 
At runtime, the name of the event will cycle through these three names.

![FirstEvtDesc](../assets/img/imagemap/NameValues.png "name values")

You now have an Event Generator ready to stream 20 Resident motion points to the Vantiq database. 
Use the Save button to save the generator and return to the Project.

![FirstEvtDesc](../assets/img/imagemap/ResidentGeneratorDefinition.png "name values")

## 4: Visualizing a Running System
Now we will use the IDE's Client Builder feature to create a visual representation of two floors of a building, as well as the movements of residents around those floors.

Use the **Add** button to select **Client...**, then use the **New Client** button to display the New Client dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![NewCB](../assets/img/imagemap/NewClient.png "New Client")

Enter "Resident" as the Client Name and use the default **Design for browser** radio button since we'll be running our client in a browser. Use the **OK** button to display the Client Builder.

Drag and drop two Plan widgets and two Label widgets from the **Data Display** list to the canvas area below the widget palette to create a Client Builder layout similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RawCB](../assets/img/imagemap/128_FPTut_RawCB.png "Client Builder")

We'll get to configuring each widget later so don't worry about the exact appearance of the widgets yet.

Now that the Client Builder widgets appear in the canvas, we need to create a Data Stream to feed live data for display in the widgets. A Data Stream defines from where a client widget receives its data. The Floor Plan widgets want to display location values, which are found in the _Resident_ records which are generated from the simulated data in Section 3.

Select the Edit tab to see the **Data Streams** menu item, then right click it to create a new 'On Data Changed' Data Stream. The Create New Data Stream dialog is displayed:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ResidentDS](../assets/img/imagemap/128_FPTut_ResidentDS.png "CreateDataModel")

Name the Data Stream "Resident", then select _Resident_ from the type menu and check the _Insert_ checkbox.  In addition, the Floor Plan widget makes use of the **Group By** feature to differentiate residents on each floor of the floor plan. The example uses the resident name (select _name (String)_ from the **Group By** pull-down) since it is used to uniquely differentiate residents on each floor of the floor plan. Use the **Save** button to save the new data stream.

There are two display widgets and two label widgets in the diagram above. What follows are the properties for each of those widgets. Any property not mentioned is the default value for that widget. To display the property sheet for any widget, click on the widget. For example, here is the property sheet for the First Floor floor plan:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![FPProperties](../assets/img/imagemap/FPProperties.png "Floor Plan Properties")

Floor Plan widgets rely on four properties to be set:

* URL: the location of an floor plan image. The example uses the default the IDE floor plan image but an image URL will work (e.g. [https://strandexecutivepark.com/wp-content/uploads/2024/11/5625floorplan.gif](https://strandexecutivepark.com/wp-content/uploads/2024/11/5625floorplan.gif)). 
* Width and Height: configure how wide and deep the floor plan represents in units (e.g. feet or meters) that match those used in the GeoJSON data. The actual units don't matter as long as the floor plan dimensions are expressed in the same units as the GeoJSON X and Y offsets in the _Resident_ record. The example uses the default dimensions of 30x25.
* Filter Properties: a JSON object that is used to associate a resident with a particular floor plan. The example uses the _floor_ property of the _Resident_ record to determine whether the resident should be located on floor "one" or "two". In a more complicated example, a client might want to locate a resident on one of several campus sites, on a specific floor in a specific building. In that case, a _Filter Properties_ JSON object could take the form _{"campus":"Downtown","building":"Psychology","floor":"one"}_.
	
For the First Floor Floor Plan widget (left):
```text
 Data Stream: Resident
 Filter Properties: {"floor":"one"}
 Data Stream Property: location
 Label Property: name (String)
```
	
For the Second Floor Floor Plan widget (right):
```text
 Data Stream: Resident
 Filter Properties: {"floor":"two"}
 Data Stream Property: location
 Label Property: name
```
	
For the label widgets (above each Floor Plan widget):
```text
 Text: First Floor/Second Floor
 Font Size: 20
```

When you have finished adding and configuring your client widgets, use the **Save** button to save the client and return to the IDE. The Floor Plan widgets are bound to a data stream and will automatically display data received from the defined data stream. Next, we will use the Event Generator created in section 3 to produce simulated resident data and run your client.

## 5: Running the Simulation
The last step of this tutorial is to start the event generator and observe the output from the Vantiq system in real-time.

From the Project Content side bar, open the **Client** list, then click the Click the _Resident_ listing.  This will bring up the Resident Client if it's not visible already. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Project Content](../assets/img/imagemap/128_FPTut_ProjectContent.png "Event Generators")

Use the **Run** icon button of the _Client: Resident_ pane (small triangle in a square at the top, right of the pane).
To begin the test, open the *ResidentGenerator* Pane and click the **Run Generator** button.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DataGenTab](../assets/img/imagemap/ResidentGeneratorDefinition.png "Event Generators")

As the generator inserts simulated resident motion data in the Vantiq database, colored markers will appear on the two image map images:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunningVis](../assets/img/imagemap/RunningClient.png "Running Client")

In this simple example, a resident be generated in a random location within the floor. In a real-world scenario, the coordinates might be provided by motion sensor or signal strength readings from wireless access points which move the resident markers in a more realistic manner.

The event generator will terminate after 20 seconds.

## 6: Customizing Markers
The Floor Plan widget (as well as the Map widgets) have two properties in the **Specific** set that allow the user to customize the markers used for data points: _Marker Array_ and _Marker Hash_. Use the **Marker Array** link in the Floor Plan widget's property sheet to display the Marker Array dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![MarkerArray](../assets/img/imagemap/MarkerArray.png "Marker Array")

In the example above, there are two uploaded PNG image documents in the Marker Array: star\_green.png and star\_blue.png. (To upload files, click on the cloud icon to the left of the entry.) When data points are displayed on this floor plan, those two images are used on a rotating basis, rather than the default markers as shown in section 5 above.

The **Marker Hash** link in the Floor Plan widget's property sheet can also be used to specify which custom images should be associated with your data points. There are two ways this lookup table can be used to associate a data point with a particular image.
 
### Single image for each data point
 
You may use this technique if you wish to assign a separate image for each unique data point. The unique "key" for each data point is used to look up an entry in the Marker Hash. 

For example, if you are showing a set of employees as they move through the map you might want each employee to show an icon of their face. (That is, there must be one image defined in the hash for each of the possible employees.)

This unique key comes from one of two places:

If the widget's associated Data Stream allows the use of a _Group By_ property, the key value comes from the _Group By_ property of the data point. 

If the widget's associated Data Stream is based on a Type the key value comes from the Type's Natural Key.

The value of the key for a data point object would be used as a key into the Marker Hash.

If no match is found for the key value in the Marker Hash, then a marker is chosen from the Marker Array if any is defined or from the default markers.

### Images for sets of data points

You should use this technique if your data points are divided into groups that shared some common characteristic and you want all the common points to show the same image.

For example, if you are showing a set of employees as they move through the map you might want all the managers to show one icon and all the regular employees to show a different one. (That is, there might be many data points but only two images.)

To indicate that you wish to use this technique you must set the "Marker Hash Key Property" in the widget property sheet. (If this property is left blank it is assumed you intend to use the "Single image for each data point" technique described above.) The value of this property in the data point object would be used as a key into the Marker Hash.

If no match is found for the key value in the Marker Hash, then a marker is chosen from the Marker Array if any is defined or from the default markers.

## Conclusion

Developers who have completed this tutorial should now feel comfortable building functionality in Vantiq in the following areas:

* Creating datatypes
* Creating clients
* Configuring Plan widgets
* Creating and linking Data Streams to Clients to simulate data from live sources
* GeoJSON point coordinates

 






